# OOM 崩溃诊断与防护 SKILL

> 版本 v1.0 · 2026-09-29 定级 · 定级 **第 40 形态（Commit 耗尽型崩溃）**
> 配套脚本：`scripts/memory_guard.py`（v1.0，selftest 8/8）
> 案例：2026-09-29 18:51 MarvisAgent.exe 被 OOM 击杀（用户感知为"自动关机"）

---

## 一、形态定义（第 40 形态）

**「自动关机」用户感知 ≠ 真的关机。**

2026-09-29 实测：用户报"刚才自动关机"，但 `GetTickCount64` 证明**系统连续运行 24h31m 未重启**（9-28 18:36 开机 → 至今）。

真相是：**系统提交内存（Commit）逼近上限 → Windows 判定内存不足 → 连锁击杀进程**，用户看到 Marvis 客户端（和一连串进程）突然消失，误判为"关机"。

**判定铁律**：
> 用户说"关机/重启"时，**先用开机时间证伪**（若 uptime 连续 → 不是真关机，是进程被 OOM 杀）。
> 判据是 **Commit 率**（提交内存/提交上限），**不是**"可用物理内存"，**不是**"CPU 占用"。

---

## 二、根因判定链（五证据，缺一不可）

| # | 证据 | 查法 | 2026-09-29 实测值 |
|---|---|---|---|
| 1 | **系统未真重启** | `GetTickCount64` 反推开机时间 | 连续 24h31m ✓ |
| 2 | **Commit 逼近上限** | `psapi.GetPerformanceInfo` | **37309 / 40701 MB = 91.7%** |
| 3 | **页面文件被锁死且用满** | `Win32_PageFileSetting` + `Win32_PageFileUsage` | **固定 8192MB，当前 8191MB（100%）** |
| 4 | **内核池异常膨胀** | psapi `KernelPaged` + `KernelNonpaged` | **8428MB（分页 6926 + 非分页 1502）**，正常 <3GB |
| 5 | **应用日志 OOM 连锁击杀** | Application 日志 ID=1000/1001/1025/1026 | powershell×2、Robocopy、WetypeInstaller、**MarvisAgent** |

### 完整因果链
```
页面文件锁死 8GB（AutomaticManagedPagefile=False）
   + WSL2 memory=12GB 且 swapFile 指向断开的 G 盘（swap 失效）
   + 内核池被 360/2345 系驱动泄漏到 8.4GB
        ↓
CommitLimit 被钉死 40.7GB（= 物理 32.5 + 页面文件 8）
        ↓
Commit 冲到 37.3GB（91.7%）→ 逼近 100%
        ↓
系统判定内存不足 → 连锁 OOM 击杀
   17:18 WetypeInstaller.exe 崩溃
   17:25 powershell.exe OutOfMemoryException FailFast
   18:06 Robocopy.exe 栈溢出 0xc00000fd
   18:07 powershell.exe OutOfMemoryException 终止
   18:51 MarvisAgent.exe 崩溃（tantivy 库调用时）← 用户看到的"自动关机"
```

---

## 三、取证命令（**必须轻量**，重查询本身就是元凶）

### ❌ 反面教材（我踩过的坑）
```powershell
# 这行在内存吃紧时会把自己压垮，然后「exit code 0 但无输出」——
# 曾被我误判为「沙箱吞了 stdout」，真因是 PowerShell 进程被 OOM 杀了
Get-WinEvent -LogName System -MaxEvents 800 | Where-Object {...}
```

### ✅ 正确做法

**1. 内存真值（psapi 底层，不依赖 PerfMon）**
```python
import ctypes
from ctypes import wintypes
class PERF(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('CommitTotal',ctypes.c_size_t),('CommitLimit',ctypes.c_size_t),
              ('CommitPeak',ctypes.c_size_t),('PhysicalTotal',ctypes.c_size_t),('PhysicalAvailable',ctypes.c_size_t),
              ('SystemCache',ctypes.c_size_t),('KernelTotal',ctypes.c_size_t),('KernelPaged',ctypes.c_size_t),
              ('KernelNonpaged',ctypes.c_size_t),('PageSize',ctypes.c_size_t),('HandleCount',wintypes.DWORD),
              ('ProcessCount',wintypes.DWORD),('ThreadCount',wintypes.DWORD)]
p=PERF(); p.cb=ctypes.sizeof(PERF)
ctypes.windll.psapi.GetPerformanceInfo(ctypes.byref(p), p.cb)
MB=1024*1024
print(f"Commit {p.CommitTotal*p.PageSize//MB} / {p.CommitLimit*p.PageSize//MB} MB")
print(f"内核池 {p.KernelTotal*p.PageSize//MB} MB")
```

**2. 关机事件（小批量）**
```powershell
Get-WinEvent -LogName System -MaxEvents 50 | Where-Object { $_.Id -in 41,1074,6008,6006 }
# 注意：MaxEvents 控制 ≤50，并用 Out-File 落盘再读（stdout 本机不稳定）
```

**3. 应用崩溃（找真凶）**
```powershell
Get-WinEvent -LogName Application -MaxEvents 100 | Where-Object { $_.Id -in 1000,1001,1025,1026 }
```

**4. 页面文件**
```powershell
Get-CimInstance Win32_PageFileSetting   # Initial/Max
Get-CimInstance Win32_PageFileUsage     # 当前/峰值/上限
(Get-CimInstance Win32_ComputerSystem).AutomaticManagedPagefile
```

**5. 直接跑守卫（推荐）**
```bash
python scripts/memory_guard.py check      # 体检+建议
python scripts/memory_guard.py assert     # 流水线前置，超阈值 exit 1
python scripts/memory_guard.py top        # 吃内存 TOP
```

---

## 四、防护措施（分级）

### A. 立即生效（零重启）
1. **流水线前置守卫**：重任务启动前跑 `memory_guard.py assert`，BLOCK 即拒绝
2. **禁止重查询**：`Get-WinEvent -MaxEvents` 控制在 **≤50**；批量任务一律写文件再读
3. **`.wslconfig` 限制 WSL**：`memory=8GB`（原 12GB）、`swapFile=D:\wsl_swap.vhdx`（原 G 盘移动硬盘 → 不可靠）
4. **拆小步**：源站 100s 网关超时（第 39 形态）+ 内存双重约束下，所有重任务必须分步

### B. 根治（需管理员 + 重启）
1. **页面文件改"系统自动管理"**（或固定 16-32GB）
   ```powershell
   # 需管理员权限，改后重启生效
   $cs = Get-CimInstance Win32_ComputerSystem
   Set-CimInstance -InputObject $cs -Property @{AutomaticManagedPagefile=$true}
   ```
   > 现状：被 `AutomaticManagedPagefile=False` 手动锁死 8GB —— **这是本次崩溃的第一元凶**

### C. 环境清理（本次挖出的隐患）
机器上有**多套捆绑"安全/优化/清理"软件**常驻，内核池泄漏高度嫌疑：
- 360 全家桶（360tray / 360Safe / 360leakfixer / 大量 360se.exe）
- 2345RTProtect.exe
- clean_master_tray.exe / dclean.exe（LdsCleanMaster 系）
- 计划任务里还有：AI_DupFileCleanTray、Mem Optimization Pro、PC Optimizer、Deep Uninstaller Tray、JDeskTray、MLPrivacyTray、PicSnapXTray、Readertray、Software Permission Manage…

**动作**：评估后**禁用其自启计划任务 / 卸载不需要的**（内核池 8.4GB → 目标 <3GB）

---

## 五、自我纠错记录（必须写下来）

| 我当时的判断 | 真实原因 | 教训 |
|---|---|---|
| "PowerShell stdout 被沙箱吞了" | **PowerShell 进程被 OOM 杀掉** | 又一次 L3/L4 混淆：把"工具无输出"当成"输出被吞"，没去查进程是否还活着 |
| "以为是电源/过热导致关机" | **Commit 耗尽 → 进程被杀** | 用户报的现象描述必须证伪，不能顺着描述假设根因 |
| "用 Get-WinEvent -MaxEvents 800 取证" | **这行本身在压垮内存** | 诊断工具必须比被诊断对象更轻量 |

> **给未来自己的铁律**：内存吃紧时，**用 py 脚本 + 小批量查询**，禁止 PowerShell 大对象查询（EventLogRecord 单个就很重）。

---

## 六、与既有形态的关系

| 形态 | 关系 |
|---|---|
| #37 判定层（L3/L4 混淆） | 本形态的"误判为关机"是同根问题的应用 |
| #38 LLM 响应空正文 | 同属"表象 ≠ 真相"，但那是响应层，这是系统层 |
| #39 源站 100s 网关超时 | 与本次并存：**内存 + 网关双重约束**，共同要求"任务拆小步" |

---

## 七、变更记录
- v1.0 (2026-09-29)：定级第 40 形态；建成 `memory_guard.py` v1.0（selftest 8/8）；完成 `.wslconfig` 修正；挖出内核池泄漏与捆绑软件隐患。
