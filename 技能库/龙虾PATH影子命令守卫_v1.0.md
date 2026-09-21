---
name: lobster-path-shadow-guard
description: >
  龙虾 PATH 影子命令守卫 v1.0。诊断「假成功/假失败」第 32 形态 —— 同一命令名在
  bash / cmd / PowerShell 三个宿主视角下解析到不同可执行文件（Windows 系统命令抢注、
  多版本并存、陈旧废弃版抢占、跨 shell 语义相反）。零积分纯 stdlib 只读。
  触发词：命令被抢、timeout 参数错、find 不对、裸 python 版本不对、pip 装错环境、
  PATH 冲突、which 找不到、bash 和 cmd 结果不一样、命令莫名其妙报错、PATH影子命令。
agent_created: true
version: 1.0
created: 2026-09-22
author: 汤小龙（汤哥 AI 分身）
cost: 0（纯 Python 标准库，不调用任何付费模型/接口）
---

# 龙虾 PATH 影子命令守卫 v1.0

> 防「假成功 / 假失败」**第 32 形态：PATH 影子命令 + 跨宿主 shell 同名异义**

## 1. 一句话定位

**命令名相同，落点不同，语义不同；命令不报错，但结果完全错。**

- bash 里 `timeout 5 cmd` = GNU 限时运行
- cmd 里 `timeout 5 cmd` = Windows `timeout /T` 语法错误（或直接把 `5` 当参数吃进交互）
- bash 里 `find . -name '*.py'` = 遍历目录
- cmd 里 `find` = **在文件内容里搜字符串**（类 grep），语义几乎相反

这类故障的恶毒之处在于：**它属于「假成功」家族** —— 命令跑完了、退出码也可能是 0，
但干的事完全不是你想的那件事；或者报出一个与真因毫无关系的错，把排查带偏。

## 2. 为什么必须工具化（本机 2026-09-22 实测，非推演）

| 命令 | bash 视角落点 | cmd/PowerShell 视角落点 | 危害 |
|---|---|---|---|
| `python` | `…\3.13.12.old.2224\python.exe`（**废弃版**） | `E:\VNPY\python.exe` | VNPY Python **缺 `_ssl` 模块**，`import ssl` 即崩 → 代理端口空转 |
| `pip` | `E:\VNPY\Scripts\pip.exe` | 同左 | 包装进错误解释器；且 VNPY 环境缺 ssl，联网安装直接失败 |
| `timeout` | Git `/usr/bin/timeout` | `C:\Windows\system32\timeout.exe` | 参数体系完全不同 |
| `find` | Git `/usr/bin/find` | `C:\Windows\system32\find.exe` | 语义相反（遍历文件 ↔ 搜索文本） |
| `bash` | Git `/usr/bin/bash` | `C:\Windows\system32\bash.exe`（**WSL 桩**） | cmd 里敲 `bash` 会拉起 WSL，不是 Git Bash |
| `tar` / `sort` | GNU 版 | Windows `bsdtar` / `sort.exe` | 参数部分不兼容 |
| `node` / `npm` | managed 22.22.2 | `C:\Program Files\nodejs`（4 个版本并存） | 装包装到系统盘，违反隔离铁律 |
| `git` | PortableGit mingw64 | `C:\Program Files\Git\cmd` | 两版 git 行为/凭据助手不一致 |

**7 个 Python 版本并存、4 个 node 版本并存** —— 裸调用落到谁，完全由 PATH 顺序决定。

## 3. 快速使用

```bash
PY="C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe"
G="E:/龙虾AI主控中心/我的AI分身/企业微信群定制接单项目/scripts/path_shadow_guard.py"

# ① 全量扫描（只看有问题的）
"$PY" "$G" scan --only-risky

# ② 只扫关心的几个命令
"$PY" "$G" scan python pip find timeout

# ③ 给一条待执行的命令行做风险评级（**执行前先过一遍**）
"$PY" "$G" risk "timeout 5 find . -name *.py | head -20"

# ④ 查单个命令的跨宿主语义差异
"$PY" "$G" explain find

# ⑤ 自检（离线，不依赖本机 PATH）
"$PY" "$G" selftest

# 机器可读
"$PY" "$G" scan --json
```

退出码：`0` = 正常；`selftest` 未全过 = `1`；参数缺失 = `2`。

## 4. 四个子命令

| 子命令 | 作用 | 输出重点 |
|---|---|---|
| `scan` | 对比**三宿主视角**解析落点 | DIFF（跨宿主异义）/ 多版本数 / STALE（陈旧版） |
| `risk` | 对一条命令行评级 | 逐 token 命中 CRIT/HIGH/MID/LOW + 替代写法 |
| `explain` | 单命令语义对照 | Win 原生语义 vs GNU 语义 vs 规避建议 |
| `selftest` | 8 条内建用例 | 离线校验判定逻辑与知识库完整性 |

## 5. 三条设计铁律（都是踩坑换来的）

### 铁律 A：绝不用 `where` / `which` 定位命令
它们**本身就是被抢注的头号受害者**（`which` 在 cmd 下不存在、`where` 在 bash 下不存在）。
本工具改为纯 Python 遍历 `PATH × PATHEXT`，零外部依赖。

### 铁律 B：cmd/PowerShell 视角的 PATH 从注册表读，不启动子进程
用 `winreg` 只读打开：
- `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment\Path`
- `HKCU\Environment\Path`

再前置 `System32` / `Windows` / `System32\Wbem`（cmd 的隐式优先目录）。

> 符合项目铁律 4：**禁 `reg`/`wmic`/`sc`/`schtasks` 命令，但 `winreg` 模块可用。**

### 铁律 C：陈旧版本看**目录名特征**，不做版本号比较
命中 `.old / _old / .bak / _bak / backup / deprecated / obsolete / _disabled` 即告警。

理由：版本号字符串比较在 Python/Node 上极易误判（`3.13.12.old.2224` 比 `3.13.12` "大"），
会制造**守卫误报**（形态 #11）—— 守卫一误报，可信度就崩了，比不守卫更糟。

## 6. 判读手册

### 输出字段
```
命令  风险等级  bash落点类型  cmd落点类型  差异标记  版本数
```
- 落点类型：`WIN-SYS` / `GIT-BASH` / `MANAGED` / `VNPY(危险:缺_ssl)` / `NONE`
- 差异标记：`DIFF`（两边不是同一个文件，**高危**）/ `ONE-SIDE`（一边根本没有）/ `same`
- `[STALE]` 行：命中废弃目录特征，裸调用会用到废弃版

### 风险等级
| 等级 | 含义 | 处理 |
|---|---|---|
| **CRIT** | 语义完全不同，必炸或必假 | 立刻改全路径 / 换 Python 等价物 |
| **HIGH** | 参数体系不同或落到已知危险环境 | 显式指定路径 |
| MID | 行为有差异 | 尽量用标准库替代 |
| LOW | 仅来源不同 | 知悉即可 |

### 决策规则
1. 出现 `DIFF` + `CRIT` → **禁止裸调用**，必须写全路径。
2. 出现 `[STALE]` → 该命令的裸调用**已在用废弃版**，先查 PATH 里有没有干净的、把它前置。
3. `VNPY(危险:缺_ssl)` → 涉及网络/`import ssl` 的任务**一律换 P0 Python**。
4. 写给别人执行的脚本 → 命令全部写全路径，或干脆用 Python 等价物。

## 7. 与其他形态的关系

| 形态 | 关联 |
|---|---|
| **#32（本形态）** | PATH 影子命令 / 跨宿主同名异义 / 陈旧版抢占 |
| #11 守卫误报 | 本工具用「目录名特征」而非版本号比较，正是为了不重蹈覆辙 |
| #20 bash 反引号被吞 | `risk` 子命令顺带检测反引号与双引号内 `$()` |
| #25 陈旧环境变量遮蔽注册表 | 同一家族：陈旧项排在前面，遮蔽了修好的那一个 |
| #24 同 host 多凭据顺序决定命运 | 同一家族：**PATH 顺序决定命运** |

> 家族共性：**「谁排在前面，谁就决定命运」**。凭据如此，PATH 亦如此。

## 8. 落地建议

1. **每日自进化首步**跑一次 `scan --only-risky`，把 DIFF/STALE 记进日志。
2. **写脚本前**对命令行跑一次 `risk`，CRIT 项改掉再执行。
3. 项目级硬编码：Python 一律 P0 全路径（项目铁律 #2），Node 一律 managed 全路径。
4. 长期根治：清理 PATH 里的废弃项（`3.13.12.old.2224`、`E:\VNPY\Scripts`）——
   **需汤哥确认后动手**（涉及环境变量，属破坏性操作，先备份再改）。

## 9. 变更记录

- **v1.0**（2026-09-22 汤小龙 第 13 期自进化）
  - 初版：scan / risk / explain / selftest 四子命令，30 条命令语义知识库
  - selftest **8/8 通过**
  - 本机实测命中：跨宿主异义 9 项、多版本并存 10 项、陈旧版抢占 1 项（python）
  - 关键实证：`E:\VNPY\python.exe` 实测 `ModuleNotFoundError: No module named '_ssl'`，
    而它在 **cmd 视角是裸 `python` 的第一落点**
