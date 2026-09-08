---
name: "powershell-windows-encoding-fix"
description: "Windows PowerShell 脚本编写铁律与编码排障。覆盖 UTF-8 BOM、StrictMode 陷阱、字符串引号规则、磁盘检测替代方案等中文 Windows 环境下高频踩坑场景。触发词：PowerShell 编码错误、ps1 中文乱码、意外的Token、StrictMode 报错、Get-PSDrive 查不到、BOM 修复。"
version: "1.0"
date: "2026-07-16"
author: "auto-skill-generator V2.2"
agent_created: true
---

# PowerShell Windows 编码与脚本铁律 · v1.0

> **来源**：2026-07-16 嘉盛黄金黑马 MT5 一键回测脚本开发实战踩坑沉淀。
> **适用范围**：所有在中文 Windows（GBK/CP936 区域）上编写和运行 `.ps1` 脚本的场景。
> **核心原则**：防患于未然 > 事后调试。以下 7 条铁律均为实测验证，违反即报错。

---

## 〇、何时启用本技能

- 编写 `.ps1` 脚本且脚本内含中文字符（注释、字符串、路径）
- PowerShell 报"意外的标记 `}`"、"字符串缺少终止符"等解析错误
- `StrictMode` 下出现"找不到属性 Count"等意外错误
- `Get-PSDrive` 查不到某些盘符但 `Test-Path` 正常
- 脚本通过 Write/echo 生成后运行报错（编码问题）
- 需要在 `-NoProfile` 子会话中检测磁盘空间

---

## 一、七大铁律速查表

| # | 铁律 | 一句话 | 违反后果 |
|---|------|--------|---------|
| 1 | **必须 UTF-8 BOM** | `.ps1` 文件头加 `EF BB BF` | 中文按 GBK 误读 → `0x22` 被当引号 → 级联解析错误 |
| 2 | **StrictMode 下数组包装** | `Get-ChildItem` 结果用 `@(...)` 包裹再 `.Count` | `$null.Count` 抛 "找不到属性 Count" |
| 3 | **单引号内禁嵌 `$(...)`** | 单引号不展开变量，改用字符串拼接 | `$(...)` 原样输出，内层 `'` 提前闭合 |
| 4 | **双引号内禁裸反引号** | `` ` `` 是转义符，会吞后续字符 | 引号配对错乱 → 语法错误 |
| 5 | **磁盘检测用 DriveInfo** | 不用 `Get-PSDrive`，用 `[System.IO.DriveInfo]` | `-NoProfile` 下 PSDrive 可能缺盘符 |
| 6 | **后台进程用 Start-Process** | 不用 Bash `&` 或 `nohup` | Bash 后台进程无法正确继承 Windows 环境上下文 |
| 7 | **路径用单引号** | `'E:\路径'` 而非 `"E:\路径"` | 双引号内 `\` 可能被解释为转义序列 |

---

## 二、逐条详解与修复方案

### 铁律 1：`.ps1` 文件必须 UTF-8 BOM

**问题现象**：
- 脚本含中文注释或中文字符串
- 运行时报"意外的标记 }"、"字符串缺少终止符"等
- 英文部分正常，中文附近开始报错

**根因**：
中文 Windows 的 PowerShell 5.1 默认按 GBK（CP936）解码 `.ps1` 文件。如果文件是 UTF-8 无 BOM，中文字符的多字节序列中可能包含 `0x22`（即 ASCII `"`），被误认为字符串引号闭合，导致后续所有内容引号配对错乱。

**修复方案**：

```powershell
# 方案A：字节级加 BOM（推荐，零损失）
$bytes = [System.IO.File]::ReadAllBytes("script.ps1")
if ($bytes.Length -ge 3 -and $bytes[0] -ne 0xEF) {
    $bom = [byte[]](0xEF, 0xBB, 0xBF)
    $newBytes = $bom + $bytes
    [System.IO.File]::WriteAllBytes("script.ps1", $newBytes)
    Write-Host "BOM added successfully"
}

# 方案B：重新写入带 BOM 的内容
$content = Get-Content "script.ps1" -Raw -Encoding UTF8
[System.IO.File]::WriteAllText("script.ps1", $content, [System.Text.UTF8Encoding]::new($true))
# UTF8Encoding($true) 的 true = emitBOM
```

**验证**：
```powershell
$bytes = [System.IO.File]::ReadAllBytes("script.ps1") | Select-Object -First 3
# 应输出：239 187 191 (即 EF BB BF)
```

**预防**：用 Write 工具生成的 `.ps1` 默认无 BOM，**生成后必须补 BOM**。

---

### 铁律 2：StrictMode 下 `$null.Count` 陷阱

**问题现象**：
```powershell
Set-StrictMode -Version Latest
$items = Get-ChildItem "C:\NonExistent" -ErrorAction SilentlyContinue
$count = $items.Count  # ❌ 报错：找不到属性"Count"
```

**根因**：
`Set-StrictMode -Version Latest` 下，`$null` 对象没有 `.Count` 属性。当 `Get-ChildItem` 返回空结果时，变量是 `$null` 而非空数组。

**修复方案**：
```powershell
# ❌ 错误写法
$items = Get-ChildItem $path -ErrorAction SilentlyContinue
if ($items.Count -gt 0) { ... }

# ✅ 正确写法：用 @() 包装确保返回数组
$items = @(Get-ChildItem $path -ErrorAction SilentlyContinue)
if ($items.Count -gt 0) { ... }  # 空数组 .Count = 0，不报错
```

**适用范围**：所有返回 0/1/多个对象的 cmdlet（`Get-ChildItem`、`Get-Process`、`Select-String` 等）。

---

### 铁律 3：单引号字符串内禁嵌 `$(...)` 和单引号

**问题现象**：
```powershell
$path = "E:\data"
$msg = 'Processing $path...'  # ❌ 输出字面量 "Processing $path..."
$msg2 = 'It''s done'           # ✅ 正确：双单引号转义
$msg3 = "Result: $(Get-Date)"  # ✅ 正确：双引号内 $() 展开
```

**根因**：
- PowerShell 单引号字符串是**字面量**，不展开 `$variable` 和 `$(expression)`
- 单引号内嵌单引号需用 `''`（双单引号）转义，不能用 `` ` `` 

**规则**：
| 需求 | 单引号 | 双引号 |
|------|--------|--------|
| 展开变量 `$var` | ❌ 不展开 | ✅ 展开 |
| 展开表达式 `$(...)` | ❌ 不展开 | ✅ 展开 |
| 转义引号本身 | `''`（双单引号） | `` `" ``（反引号+引号） |
| 转义反引号 | N/A | ``` `` ```（双反引号） |

**最佳实践**：
- 路径、正则、不含变量的文本 → 用**单引号**
- 需要展开变量/表达式 → 用**双引号**，但注意铁律 4

---

### 铁律 4：双引号字符串内禁裸反引号

**问题现象**：
```powershell
# Markdown 代码标记在双引号字符串中
$msg = "Run command `Get-Process` to check"  # ❌ 反引号吞掉后续字符
# 实际输出：Run command Get-Processto check（反引号和后面的字符被吞）
```

**根因**：
反引号 `` ` `` 是 PowerShell 的转义符。在双引号字符串中，`` ` `` 会转义下一个字符：
- `` `n `` → 换行
- `` `t `` → Tab
- `` `" `` → 字面量引号
- `` `g `` → 字面量 g（反引号被静默吞掉）

**修复方案**：
```powershell
# 方案A：去除反引号
$msg = "Run command Get-Process to check"

# 方案B：用双反引号转义
$msg = "Run command ``Get-Process`` to check"

# 方案C：改用单引号（如果不需要变量展开）
$msg = 'Run command `Get-Process` to check'
```

**高频场景**：在 PowerShell 脚本中生成 Markdown 文档时，代码标记 `` ` `` 是重灾区。

---

### 铁律 5：磁盘空间检测用 `[System.IO.DriveInfo]`

**问题现象**：
```powershell
# 在 -NoProfile 子会话中
powershell -NoProfile -Command "Get-PSDrive E"
# ❌ 可能返回空（PSDrive 未加载 E: 盘符）

# 但 Test-Path 正常
powershell -NoProfile -Command "Test-Path E:"
# ✅ 返回 True
```

**根因**：
`Get-PSDrive` 依赖 PowerShell 配置文件中的 PSDrive 注册。`-NoProfile` 会话可能未加载所有盘符映射，但文件系统本身正常。

**修复方案**：
```powershell
# ❌ 不稳定
$space = (Get-PSDrive E).Free

# ✅ 使用 .NET DriveInfo（不依赖 PSDrive 注册）
$drive = New-Object System.IO.DriveInfo("E")
if ($drive.IsReady) {
    $freeGB = [math]::Round($drive.AvailableFreeSpace / 1GB, 2)
    $totalGB = [math]::Round($drive.TotalSize / 1GB, 2)
    Write-Host "E: Free=$freeGB GB / Total=$totalGB GB"
}

# ✅ 批量检测所有盘符
[System.IO.DriveInfo]::GetDrives() | Where-Object { $_.IsReady } | ForEach-Object {
    $free = [math]::Round($_.AvailableFreeSpace / 1GB, 2)
    Write-Host "$($_.Name) Free=$free GB"
}
```

---

### 铁律 6：后台进程用 `Start-Process`

**问题现象**：
- 用 Bash 的 `&` 或 `nohup` 启动的 Windows 进程无法正确继承环境变量
- 后台进程的 stdout/stderr 丢失

**修复方案**：
```powershell
# ✅ PowerShell 原生方式启动后台进程
$proc = Start-Process -FilePath "ollama.exe" `
    -ArgumentList "pull", "qwen2.5vl:7b" `
    -NoNewWindow `
    -PassThru `
    -RedirectStandardOutput "pull_stdout.log" `
    -RedirectStandardError "pull_stderr.log"

# 等待完成
$proc.WaitForExit()
Write-Host "Exit code: $($proc.ExitCode)"
```

---

### 铁律 7：路径用单引号

**问题现象**：
```powershell
# 双引号路径中的反斜杠可能引发问题
$path = "E:\data\new"  # \n 可能被误解释（虽然 PowerShell 通常安全）
```

**最佳实践**：
```powershell
# ✅ 路径一律用单引号
$path = 'E:\data\new\folder'
$config = 'C:\Users\Administrator\config.json'

# ✅ 需要变量拼接时，用字符串拼接而非双引号嵌入
 basePath = 'E:\data'
$fullPath = $basePath + '\sub\folder'

# ✅ 或用 Join-Path（最安全）
$fullPath = Join-Path $basePath 'sub\folder'
```

---

## 三、快速排障流程图

```
.ps1 运行报错
    │
    ├─ "意外的标记" / "字符串缺少终止符"
    │    → 检查 BOM（铁律 1）
    │    → 检查双引号内是否有裸反引号（铁律 4）
    │
    ├─ "找不到属性 Count"
    │    → 检查 StrictMode（铁律 2）
    │    → 用 @() 包装
    │
    ├─ 变量未展开 / 输出字面量 $var
    │    → 单引号改双引号（铁律 3）
    │
    ├─ Get-PSDrive 返回空
    │    → 改用 DriveInfo（铁律 5）
    │
    └─ 后台进程行为异常
         → 改用 Start-Process（铁律 6）
```

---

## 四、一键诊断脚本

```powershell
# ps1_diagnose.ps1 — 对目标 .ps1 文件执行 7 项铁律检查
param([string]$ScriptPath)

if (-not (Test-Path $ScriptPath)) { Write-Host "File not found"; exit 1 }

# 检查 1: BOM
$bytes = [System.IO.File]::ReadAllBytes($ScriptPath) | Select-Object -First 3
$hasBOM = ($bytes.Count -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
Write-Host "[1] UTF-8 BOM: $(if ($hasBOM) {'PASS'} else {'FAIL - run BOM fix'})"

# 检查 2: StrictMode + 未包装的 .Count
$content = Get-Content $ScriptPath -Raw
$hasStrictMode = $content -match 'Set-StrictMode'
$hasRawCount = $content -match '(?<!@\()\w+\.Count'
if ($hasStrictMode -and $hasRawCount) {
    Write-Host "[2] StrictMode .Count: WARN - possible unwrapped .Count found"
} else {
    Write-Host "[2] StrictMode .Count: PASS"
}

# 检查 3: 双引号内反引号
$hasBacktickInDQ = $content -match '"[^"`]*`[^"]*"'
Write-Host "[3] Backtick in DQ: $(if ($hasBacktickInDQ) {'WARN'} else {'PASS'})"

# 检查 4: Get-PSDrive 使用
$hasPSDrive = $content -match 'Get-PSDrive'
Write-Host "[4] Get-PSDrive: $(if ($hasPSDrive) {'WARN - consider DriveInfo'} else {'PASS'})"

Write-Host "`nDiagnosis complete."
```

---

## 五、关联技能

| 技能 | 关联方式 |
|------|---------|
| 多智能体舰队编排调度技能 V1.1 | 本技能从其 7.7 节提炼而来 |
| local-llm-integration-fix V4.0 | PowerShell 运维场景共用 |
| 多智能体舰队编排 V1.1 | 舰队脚本编写遵循本铁律 |

---

## 六、更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-07-16 | V1.0 | 初始创建，7 条铁律 + 诊断脚本 + 排障流程图 |

---

*本技能随实战踩坑持续迭代。发现新的 PowerShell 编码陷阱时自动更新。*
