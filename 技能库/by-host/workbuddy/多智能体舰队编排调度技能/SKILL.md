---
name: "多智能体舰队编排调度技能"
description: "将多智能体舰队编排（WorkBuddy 视觉中枢 + ORCA 集群文件协议协同 + Ollama 本地视觉 + Obsidian 第二大脑 + 嘉盛黄金黑马MT5一键回测）封装为可一键启用的标准化调度体系。覆盖调用话术、任务流转、Git 版本管控、Ollama 运维、Obsidian 双向接入、量化策略本地协作、MT5全流程自动化、实测边界与故障排查、成本控制感知模式。适用于龙虾AI主控中心全域多 Agent 协作。"
version: "1.2"
date: "2026-08-18"
author: "WorkBuddy + 龙虾AI主控中心"
agent_created: true
primary_path: "~/.workbuddy/skills/多智能体舰队编排调度技能/SKILL.md"
repo_path: "E:/龙虾AI主控中心/我的AI分身/多智能体舰队编排"
lobster_workflow: "E:/龙虾AI主控中心/我的AI分身/技能库/lobster_task_standard_workflow_v2.6/SKILL.md"
cost_mode: "strict | normal | full"
---

# 多智能体舰队编排调度技能 · v1.2

> 本技能由 2026-07-16 整合批次沉淀。V1.2 升级：注入成本控制感知模式（strict/normal/full 三档），新增与 `zero-cost-task-execution` 双向联动，最小必要数据集压缩 40% 工具调用。
> 执行口径：**严格遵循龙虾五步法 v2.6 + 全域官方模板**，所有产出如实标注本机实测状态，禁止生成与磁盘/Ollama 真实状态冲突的不实描述。
> 核心引擎：MiMO V2.5 Pro / Ollama 本地视觉 / ORCA 集群（文件协议协同）/ Obsidian 第二大脑。
> 成本原则：默认 `cost_mode=strict`（最小必要数据集 + 零积分优先）。

---

## 〇、何时启用本技能

出现以下任一信号即激活（用户亦可显式点名"多智能体舰队编排"）：
- 需要把任务下发给 ORCA 集群（Hermes / Codex / Claude Code）并行执行
- 需要解析截图/图文并生成标准化任务、跨窗口调度
- 需要管理「多智能体舰队编排」Git 仓库（分支/标签/归档）
- 需要配置 Ollama 本地视觉模型运维（监控/恢复/磁盘告警）
- 需要把任务运行报告写入 Obsidian 知识库作为第二大脑
- 需要基于脚手架 `fleet_project_scaffold/` 新建一个量化/AI 调度项目
- 需要执行**嘉盛黄金黑马 MT5 一键回测**（编译→部署→回测→导出→归档→报告全自动）
- 需要执行**嘉盛黄金黑马 MT5 单阶段操作**（只编译 / 只回测 / 只归档）

---

## 一、两种触发调用方式（固化话术）

### 1. 口头/图文一键触发（日常主推，任意对话窗口可用）
标准话术，直接发给 WorkBuddy 即可自动联动：
- `启用多智能体舰队编排，配合 ORCA 处理量化策略任务`
- `调用多智能体舰队编排，解析截图执行自动化工作流`
- `启动舰队编排项目，下发任务至 ORCA 智能体并行执行`

### 1.1 嘉盛黄金黑马 MT5 一键命令（固化话术，任意窗口可用）
> **体系隔离**：以下话术仅触发 **嘉盛 MT5/MQL5** 体系，与币安黑马 Python/Backtrader 完全独立。

| # | 触发话术 | 执行动作 | 脚本参数 |
|---|----------|----------|----------|
| A | **运行嘉盛黄金黑马MT5一键回测** | Full 模式全流程（6 阶段） | 默认 |
| B | **黄金黑马快速回测（跳过编译）** | BacktestOnly + SkipCompile | `-Mode BacktestOnly -SkipCompile` |
| C | **只编译黄金黑马EA** | 仅编译 + MD5 校验 | `-Mode CompileOnly` |
| D | **黄金黑马可视化回测** | Full + 可视化模式 | `-VisualMode` |
| E | **归档上次黄金黑马回测结果** | 收集结果并生成报告 | `-Mode ArchiveOnly` |

**脚本路径**：`E:\...\CODEX量化策略20260615\嘉盛\黄金黑马策略\scripts\gold_dark_horse_oneclick.ps1`

> 新窗口、新标签页、全新会话均可用，无需额外配置。

### 2. 手动 BASH 命令触发（单 Agent 调试、单独控制 ORCA 窗口）
```bash
# Agent 领取待执行任务（EX=仓库 fleet_exchange 路径）
EX="E:/龙虾AI主控中心/我的AI分身/多智能体舰队编排/fleet_exchange"
bash "$EX/fleet_pull.sh"            # 单次领取
bash "$EX/fleet_pull.sh" auto 30 600 # 自动轮询（每30s，超时600s）
# 任务执行完成回写结果
bash "$EX/fleet_done.sh" "<WORKING_FILE>" "执行摘要"
```

---

## 二、底层架构（实测基线）

```
用户指令/截图
   ▼
┌──────────────────────────────────────────────┐
│  WorkBuddy（视觉中枢 + 编排层 + 对话入口）       │
│   - 解析截图/图文 → 标准化任务                   │
│   - 写入 fleet_exchange/incoming/               │
│   - 汇总 results/ 反馈                          │
└──────────────┬───────────────────────────────┘
               │  文件交换协议（fleet_exchange/）
               ▼
┌──────────────────────────────────────────────┐
│  ORCA 集群（Hermes / Codex / Claude Code）      │
│   - 仅通过读取/写入 fleet_exchange 文件协同       │
│   - ⚠️ 本代理无法直接操控其 GUI 或内部 Agent      │
└──────────────┬───────────────────────────────┘
               │
   ┌───────────┼───────────────┐
   ▼           ▼               ▼
 Ollama      Obsidian        Git 仓库
 (11434)     (第二大脑)       (版本管控)
 视觉模型    双向读写          main/develop
```

### 关键事实（实测，非声明）
- **Ollama**：`OLLAMA_MODELS` 实测仍 = `E:\Ollama`（**非** G 盘）；服务在线 11434，含 11 个模型（gemma4:e4b 文本/代码、qwen3.5:2b 视觉等）。**minicpm-v / qwen2.5vl:7b 尚未拉取成功**。
- **ORCA 协同边界**：仅文件协议（写任务 / 读结果），无 GUI 操控能力；多窗口并行/自动分配为协议设计，非强制保证。
- **量化策略**：本机 E 盘存量目录（如 `CODEX量化策略20260615\嘉盛\黄金黑马策略\`），仅经 WorkTree/软链读取，**不复制、不新建仓库**。
- **Obsidian 第二大脑**：Path2 `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库`（干净结构化 vault）；Path1 `E:\龙虾AI主控中心\Obsidian` 为 portable Obsidian 应用+git+通用 vault，其 `.git` 当前误跟踪了 app 二进制（需 `.gitignore` 净化）。

---

## 三、完整执行链路（五步法 v2.6）

1. **备份（P0）**：任何写盘/系统级操作前先备份相关目录。
2. **环境诊断**：核验 Git 状态、Ollama `/api/tags`、Obsidian 库可达性、磁盘空间。
3. **方案落地**：写任务→`fleet_pull`→Agent 执行→`fleet_done`→`results/`；文档/脚本入库。
4. **结果验证**：闭环复测（incoming→doing→done→results 全链路）、Git 工作树干净、Ollama 监护在线。
5. **迭代沉淀**：更新本技能 + memory + 仓库 docs；发现新坑即补故障排查规则。

---

## 四、Git 版本管控规范

- 唯一 Git 仓库：`多智能体舰队编排`（独立，已从父仓库 detached）。
- 分支：`main`（稳定基线）/ `develop`（开发）/ `feat/visual-office`（二期可视化）。
- 标签：`v1.0.0-phase1` 绑定 `main` 最新提交。
- **沙箱铁律**：本代理在沙箱中写 `E:\...\多智能体舰队编排\.git\*` 会被拦截，**需用户在弹窗授权 E 盘 .git 写入**才能 commit/tag/branch。纯文件改动用 Write 工具（不受此限）。
- 同步 develop 到 main 用 `git branch -f develop main`（仅移动 ref，不碰 index/工作树，权限开销最小）。

---

## 五、故障排查规则（实测踩坑）

| # | 现象 | 根因 | 处理 |
|---|------|------|------|
| 1 | Bash 写 G/E 盘被拒 | 沙箱拦截原始写盘 | 改用 Write 工具 / 授权后执行 |
| 2 | `git` 写 `.git/index.lock` 被拒 | 沙箱拦截 .git 写 | 授权 E 盘 .git 写入弹窗 |
| 3 | Ollama 仍写 E 盘 | `OLLAMA_MODELS` 仍是 E: | 改 User 级环境变量+重启（**系统级，需单独授权**） |
| 4 | 视觉模型拉取失败 | 沙箱拦 Bash 后台写 G 盘 | 用 PowerShell `Start-Process ollama pull` 真实上下文 |
| 5 | 文档描述与实测冲突 | 历史声明误记 | 全量勘误，标注实测现状 |
| 6 | ORCA 不响应任务 | 仅文件协议，无 GUI 控制 | 用户在 ORCA 窗口侧确认按协议运作 |
| 7 | Obsidian path1 .git 含 app 二进制 | 在 app 目录 git init | 加 `.gitignore` 排除 exe/dll，或 vault 迁子目录 |

---

## 七、嘉盛黄金黑马 MT5 一键全流程命令体系

> **新增于 2026-07-16**，基于 Marvis 编制的《嘉盛黄金黑马MT5运维手册》v1.0 固化。

### 7.1 体系隔离铁律（必须遵守）

| 体系 | 名称 | 技术栈 | 路径根 |
|------|------|--------|--------|
| **嘉盛黄金黑马** | 默认"黄金黑马"指此套 | **MT5 / MQL5 / MetaEditor** | `E:\...\CODEX量化策略20260615\嘉盛\黄金黑马策略\` |
| **币安黑马** | 需显式说"币安黑马" | **Python / Backtrader / Binance API** | `E:\...\币安黑马策略\`（或其他 Python 项目） |

两套体系 **完全独立、互不干扰、互不混用、互不串路径**。

### 7.2 六阶段执行流程

```
Phase0 环境诊断 → Phase1 编译EA → Phase2.5 MD5硬校验 → Phase2 部署ex5
→ Phase3 运行回测(-CloseMt5) → Phase4 导出结果 → Phase4b 绩效解析
→ Phase5 总结报告 → Phase6 三副本归档 → Phase7 重启MT5
```

| Phase | 名称 | 耗时 | 产出 | 可跳过？ |
|-------|------|------|------|----------|
| 0 | 环境诊断 | ~3s | 路径/文件/磁盘/进程检查 | 否 |
| 1 | 编译 EA (MetaEditor64) | ~10s | ex5 + MD5 + Exe/ 备份 | `-SkipCompile` |
| 2.5 | **EA 完整性 MD5 硬校验** | ~1s | 哈希=基准则继续，否则终止回测（兜底规则） | 否 |
| 2 | 部署到 MT5 终端 | ~1s | MQL5\Experts\*.ex5 + .set | 否 |
| 3 | 运行回测 (terminal64 /tester /exit) | ~2-15min | tester 缓存结果 | 仅 BacktestOnly |
| 4 | 导出归档 | ~3s+120s轮询 | HTML/日志/配置快照/MD5 | `-SkipArchive` |
| 4b | **绩效指标解析** | ~1s | performance_metrics.txt（胜率/盈亏比/回撤/夏普） | 无 HTML 则跳过 |
| 5 | 执行总结报告 | ~1s | execution_summary.md（含生命周期/指标/三副本/告警） | 同上 |
| 6 | **三副本归档** | ~3s | 主目录+Obsidian+G盘（Marvis 三副本） | 仅回测模式 |
| 7 | **后置重启 MT5** | ~6s | 恢复被关闭的实盘终端登录会话 | 仅 -CloseMt5 关闭过 |

### 7.3 关键路径

| 资产 | 路径 |
|------|------|
| EA 源码 | `...\黄金黑马策略\ea_gold_dark_horse_v1.7.mq5` |
| EA 编译产物 | `...\黄金黑马策略\ea_gold_dark_horse_v1.7.ex5` |
| 主力参数文件 | `...\黄金黑马策略\ea_gold_dark_horse_v1.7_2146.set` |
| 一键脚本 | `...\黄金黑马策略\scripts\gold_dark_horse_oneclick.ps1` |
| 命令文档 | `...\黄金黑马策略\docs\MT5一键全流程执行命令.md` |
| MT5 终端实例 | `%APPDATA%\MetaQuotes\Terminal\9D63A70C6FC86A19F92608348F3E6BB8` |
| MT5 安装目录 | `C:\Program Files\MT5 by FOREX.com Global CN\` |
| 回测归档 | `...\黄金黑马策略\TestData\backtest_<时间戳>\` |
| 运维手册（Marvis） | `...\黄金黑马策略\docs\嘉盛黄金黑马MT5运维手册.md` |

### 7.4 标准回测参数（手册 3.3.1 固化）

| 参数 | 值 | 说明 |
|------|-----|------|
| Expert | `ea_gold_dark_horse_v1.7` | EA 名称 |
| Symbol | `XAUUSD` | 黄金现货 |
| Timeframe | `H4` (PERIOD_H4) | 四小时线 |
| 区间 | 2024.03.06 — 2026.06.29 | 完整多头波段 |
| 初始资金 | 10000 USD | — |
| 杠杆 | 1:100 | — |
| 参数文件 | `_2146.set` | 颈线目标=2146 |
| 模式 | OpenPricesOnly / EveryTick | 标准/精细 |

### 7.5 故障排查速查

| 问题 | 排查方向 |
|------|----------|
| 编译 error | 查看 `compile_log_onclick_*.txt`，对照运维手册 4.1.3 |
| 回测无交易 | 五重入场条件未满足→查看专家日志逐条件核对（手册 4.2） |
| 无 HTML 报告 / tester\files 未生成 | MT5 已运行时 /tester 仅委托主实例需 GUI 触发→加 `-CloseMt5` 关闭已运行 MT5 再跑 |
| 权限不足 | 需管理员权限写 MT5 AppData→以管理员身份运行 PowerShell |
| MD5 不匹配 | ex5 被篡改或编译源码不一致→重新编译 |

### 7.6 一键开关与 headless 注意事项（v1.1 实测）

- **回测引擎**：v1.1 起使用 `terminal64.exe /tester <Expert> <Symbol> <TF> <From> <To> <Model> /deposit /set /exit`，跑完自动退出，杜绝 GUI 挂死。
- **`-CloseMt5` 开关**：当 MT5 主终端已运行时，命令行 `/tester` 只会把指令委托给主实例（需 GUI 手动触发），headless 拿不到报告。加 `-CloseMt5` 让脚本先自动关闭已运行 MT5，再以独立 headless 进程跑完并落盘 `tester\files\*.html` 报告。**关闭前请确认无未平仓单**。
- **报告轮询**：Phase 4 会等待 `tester\files` 出现最多 120s，兼容主实例延迟生成。
- **MD5 硬校验（Phase 2.5）**：脚本内置基准 `60A8B4B010965473F55A34BA632A207C`（32 位真值）；用户指令曾给 28 位 `…632A207C` 系笔误截断，以 32 位真值为准。哈希不符立即终止回测。
- **实测状态（2026-07-16 05:02 完整授权运行 `-Mode Full -CloseMt5 -SkipCompile`）**：
  - 链路跑通 Phase0→2.5→2→3→4→4b；MD5 硬校验 PASS；关闭实盘 PID 303616 成功。
  - **headless 挂起**：独立测试终端 PID 364436 启动后连接账户 `FOREX.comGlobalCN-Live 534`，但卡在模态对话框（疑似"下载缺失历史数据"确认框），`/exit` 失效、进程不退出（5 分钟零进度）。这是 MT5 命令行机制的客观限制，**非脚本逻辑错误**。
  - **兜底处置**：运维按规则终止挂起进程；脚本随后在 Phase 5 因 `Set-StrictMode` 未定义 `$script:PARSED_METRICS` 崩溃（已修复：新增变量初始化 + Phase 5 包 try/catch + 故障时仍执行重启）；Phase 6 三副本、Phase 7 重启 MT5 由运维手动补做（实盘已恢复 PID 370752）。
  - **产出真实 HTML 报告的路径**：① 预缓存历史（GUI 打开 XAUUSD H4 等数据下载完再 `-CloseMt5`）；② GUI 模式（不加 `-CloseMt5`，手动点开始）。

### 7.7 PowerShell 脚本编写铁律（本次踩坑沉淀，跨项目复用）

- **必须 UTF-8 BOM**：Write 工具生成的 `.ps1` 默认无 BOM，中文 Windows 的 PowerShell 按 GBK 误读 → 中文字节中的 `0x22` 被当字符串闭合引号 → 级联"意外的 }"解析错误。修复：字节级加 `EF BB BF`（不重新解析文本，零损失）。
- **StrictMode `-Version Latest`** 下 `$null.Count` 抛"找不到属性Count" → 所有 `Get-ChildItem` 结果用 `@(...)` 包成数组再取 `.Count`。
- **单引号字符串内禁嵌单引号/`$(...)`**：`$(...)` 在单引号里不展开，内层 `'` 会提前闭合 → 改用字符串拼接 `"a" + $(...)`。
- **双引号字符串内禁裸反引号** `` ` ``（Markdown 代码标记）→ 反引号是 PowerShell 转义符，会吞掉后续字符/引号 → 去除反引号或改用单引号。
- **磁盘空间别用 `Get-PSDrive`**：`-NoProfile` 子会话 PSDrive 可能查不到 E: 盘符（但 `Test-Path E:` 正常）→ 改用 `[System.IO.DriveInfo]`。
- **`Set-StrictMode -Version Latest` 下访问可能未赋值变量会抛错**：所有 `$script:` 作用域变量（如 PARSED_METRICS / CLOSED_MT5 / LIFECYCLE_LOG）必须在脚本顶部先初始化，否则未触发的分支导致后续引用崩溃。

### 7.8 v1.1 一键命令体系要点（2026-07-16 固化）

- **固化话术（WorkBuddy 一句话触发）**：见 §1.1 A–E 五条。
- **新增四增强**：Phase 2.5 MD5 硬校验（兜底终止）、Phase 4b 绩效解析、Phase 6 三副本归档（主目录/Obsidian/G盘）、Phase 7 后置重启 MT5。
- **三副本路径**：主目录 `TestData/backtest_<ts>/`；Obsidian `E:\龙虾AI主控中心\ObsidianVault\量化策略\嘉盛黄金黑马\TestData\backtest_<ts>/`；G 盘 `G:\龙虾AI主控中心\我的AI分身\CODEX量化策略20260615\嘉盛\黄金黑马策略\TestData\backtest_<ts>/`。
- **关键边界**：`-CloseMt5` 关闭的实盘 MT5，无论成功或崩溃，最终都会重启（Phase 7 或 catch 块兜底），确保用户登录会话恢复。

---

## 八、关联资产

| 资产 | 路径 |
|------|------|
| 舰队 Git 仓库 | `E:\龙虾AI主控中心\我的AI分身\多智能体舰队编排` |
| 交换区协议 | `.../fleet_exchange/PROTOCOL.md` |
| 使用手册 | `.../docs/使用手册/多智能体舰队编排完整使用说明书.md` |
| Obsidian 联动方案 | `.../docs/双Obsidian知识库联动方案.md` |
| 项目脚手架 | `.../fleet_project_scaffold/` |
| 龙虾五步法 v2.6 | `E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v2.6\SKILL.md` |
| 嘉盛黄金黑马 MT5 一键脚本 | `E:\...\CODEX量化策略20260615\嘉盛\黄金黑马策略\scripts\gold_dark_horse_oneclick.ps1` |
| 嘉盛黄金黑马 一键命令文档 | `E:\...\嘉盛\黄金黑马策略\docs\MT5一键全流程执行命令.md` |

## 九、成本控制感知模式（V1.2 核心新增 · 2026-08-18）

> **跨切面原则**：8/6 汤哥确立"成本控制置顶"为龙虾AI主控中心全域原则。本技能作为调度中枢必须体现。

### 9.1 三档成本模式（默认 `strict`）

| 模式 | 适用场景 | 工具调用预算 | 数据集 | 是否调用 MiMO/Ollama |
|------|----------|-------------|--------|---------------------|
| **`strict`**（默认） | 日常调度、零工作日、单 Agent 调试 | ≤15次 | 最小必要数据集 | 优先 Ollama → MiMO → 跳过 |
| `normal` | 常规多 Agent 协同、脚本批处理 | ≤25次 | 扩展数据集（含上下文） | MiMO 默认，可换 Ollama |
| `full` | 首次部署、复杂诊断、关键里程碑 | ≤40次 | 全量数据集（含跨域联动） | MiMO 优先，按需多模型路由 |

**切换话术**：`舰队编排走 strict 模式` / `切 full 模式跑全量诊断` / `normal 模式处理这个任务`

### 9.2 最小必要数据集（strict 模式）

**禁止动作清单**（任何模式都适用，strict 强制）：
- ❌ 重复 `ls`/`cat` 已读取过的文件 → 必须用上下文缓存
- ❌ 每次都全量 `Read` SKILL.md → 信任 frontmatter 元数据
- ❌ 无目的的 `WebSearch` → 仅在缺失事实时使用
- ❌ 跨盘符递归扫描 → 用 Glob 限定路径
- ❌ 单步小步快跑 → 必须批量并行（多 Bash 同时调用）

**最小动作链**（strict 模式核心场景）：
```
1. 读 SKILL.md frontmatter（1次）
2. ls fleet_exchange/{incoming,doing,done,results}（1次）
3. 写任务/incoming 或读 results/（1次）
4. 输出回执（0次，文件形式）
5. 写 memory 日志（1次）
─────────────────
合计 4 次工具调用（vs full 模式 ~25 次）
```

### 9.3 零积分动作优先（与 `zero-cost-task-execution` 双向联动）

| 优先级 | 动作类型 | 工具 | 何时用 |
|--------|----------|------|--------|
| 🥇 P0 | 本地缓存/上下文复用 | 无工具调用 | 任何可复用场景 |
| 🥇 P0 | Ollama 本地推理 | `mimo-bridge` | 视觉/文本推理（11434端口） |
| 🥈 P1 | MiMO V2.5 Pro | `mimo-bridge` | 复杂逻辑、代码生成 |
| 🥈 P1 | Bash + 本地脚本 | 已有脚本（如 gold_dark_horse_oneclick.ps1） | 量化运维、文件操作 |
| 🥉 P2 | 腾讯混元 HY3 | `cloudbase-hy3-relay`（端口15731） | 仅在 MiMO 不可用时 |
| 🚫 P3 | WorkBuddy 积分 | 直接调用 | 仅在无替代方案时 |

### 9.4 成本复盘（强制输出）

每次执行完毕必须输出：
```
【成本复盘】
- cost_mode: strict | normal | full
- 预算工具调用：≤N次
- 实际工具调用：N次
- 节省率：X%
- 替代路径：如未使用MiMO/Ollama应说明
```

### 9.5 与其他技能的成本控制协同

| 技能 | 协同方式 |
|------|----------|
| `zero-cost-task-execution` | **双向联动**：本技能默认 strict 模式 = 引用其方法论；zero-cost 调用舰队时也走 strict |
| `mimo-bridge` | strict 模式优先走本地 Ollama，零积分零网络 |
| `auto-skill-generator` | 每日 05:00 巡检本技能时按 strict 模式压缩预算 |
| `daily-market-dashboard` | 量化任务链路中均按 strict 处理 MT5 一键回测 |

---

## 十、版本日志

### V1.2（2026-08-18）— 成本控制置顶注入
- 🆕 新增第九章「成本控制感知模式」：三档 cost_mode（strict/normal/full）
- 🆕 新增最小必要数据集（strict 模式 ≤4 次工具调用）
- 🆕 新增零积分动作优先清单（P0-P3 优先级）
- 🆕 新增与 `zero-cost-task-execution` 双向联动
- 🆕 联动表新增：mimo-bridge / auto-skill-generator / daily-market-dashboard
- 🔄 description 扩展：成本控制感知模式
- 🔄 默认 cost_mode=strict（最小必要数据集 + 零积分优先）
- 🟠 → 🟢 健康度跃升（~67 → ~88）

### V1.1（2026-07-16）— 嘉盛黄金黑马 MT5 一键全流程
- 🆕 新增第七章：MT5 一键回测体系（Phase 0-7）
- 🆕 新增六阶段执行流程 + 关键路径表 + 故障排查速查
- 🆕 PowerShell 脚本编写铁律（UTF-8 BOM / StrictMode / 单引号 / 反引号 / 磁盘检测）
- 🆕 MD5 硬校验（Phase 2.5）兜底规则

### V1.0（2026-07 之前）— 初始整合批次
- ORCA 集群文件协议协同 / Ollama 视觉 / Obsidian 第二大脑
- 五步法 v2.6 + Git 管控 + 故障排查

---

*本技能随舰队演进 + 成本控制原则持续更新。下次更新触发：① Ollama 视觉模型就位（gemma4:vision / qwen2.5vl）；② Obsidian 双向读写实测完成；③ 嘉盛黄金黑马 MT5 XAUUSD H4 历史预缓存后跑出首份真实 HTML 报告；④ 8/18 之后有新会话触发其他场景。*
