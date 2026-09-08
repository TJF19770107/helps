---
name: orca-fleet-dual-control
description: ORCA舰队双实例统一控制。双实例CLI↔GUI一键切换+六窗口全互联(OMF v1.0)+Workbody外部调度(orca_dispatch)+脚手架A/B/C交互弹窗+全量验证自愈(T1-T7)。触发词：双实例切换、六窗口互联、舰队调度、orca dispatch、switch gui、脚手架弹窗、全量舰队模式、OMF消息、ORCA双实例、六窗口
agent_created: true
version: 1.1
updated: 2026-07-30
---

# ORCA 舰队双实例统一控制 v1.1

> 中央运行时（唯一真源）：`E:\龙虾AI主控中心\我的AI分身\项目脚手架\orca_multi_agent_fleet_v1.0\dual_core\`
> 手册：workspace `ORCA双实例舰队调度操作手册.md` ｜ 全域模板协议#294 ｜ 五步法Type-H实装章节

## 一、何时激活本技能

- 用户说"双实例""六窗口""ORCA切换GUI""舰队调度"
- 需要从 CLI 实例切换到 GUI 实例（或反向）
- 需要通过 WorkBuddy/orca_dispatch 外部向某个 Agent 发送任务
- 新建项目时需要选择 A(单实例)/B(双实例)/C(全量舰队) 模式
- 全量验证 T1-T7 未通过，需要排查
- OMF 消息总线消息丢失或未送达

## 二、架构速记

- 3 Agent (hermes/codex/claude) × 2 实例 (cli/gui) = **6窗口全互联**
- 消息：OMF v1.0（text/json/file_ref），总线 `<项目>/msgbus/inbox/<窗口>/`，防重台账 `msgbus/ledger/seen.txt`
- 程序E盘 / 数据G盘 `G:/龙虾AI主控中心/ORCA数据/`（logs/reports/edge_profiles/fleet_projects.json）
- GUI = gui_server.py + Edge --app（Hermes/Claude **无官方GUI exe**，Web面板为标准实现）
- 环境变量覆盖：`ORCA_G_DATA`（数据根）、`ORCA_FLEET_REG`（舰队注册表）——沙箱测试必用

### 双实例端口分配原则

| 端口段 | 用途 | 说明 |
|--------|------|------|
| 4567 | MiMO V2.5（共享） | 所有 Agent 共用 AI Code Switch |
| 57321 | Codex++ 本地控制 | 非代理端口 |
| 57330 | Claude serve | Claude Code 独立端口 |
| 57345-57347 | netdisk GUI | 网盘项目专用 |
| 57355-57357 | sports GUI | 赛事预测项目专用 |
| 57365-57367 | wecom GUI | 企微接单项目专用 |
| 15800-15802 | 原生桌面 GUI | Hermes/Claude/Codex 原生 exe（<49152 规避 WinError 10013） |

## 三、常用命令（PY=managed python 3.13.12）

```bat
set PY=C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe
set CORE=E:\龙虾AI主控中心\我的AI分身\项目脚手架\orca_multi_agent_fleet_v1.0\dual_core

REM 新建/升级项目（A单实例/B双实例/C全量舰队；缺省交互弹窗）
%CORE%\..\init_orca_dual_interactive.cmd <项目根> C 57370

REM 外部调度（从 WorkBuddy/orca_dispatch 向 Agent 发任务）
%PY% %CORE%\orca_dispatch.py send -p <项目/别名> -a codex_cli -m "任务" [--chain standard_loop --level full]

REM 切换实例（CLI ↔ GUI）
<项目>\scripts\switch.cmd --agent hermes --to gui
<项目>\scripts\switch.cmd --agent codex --to cli

REM 消息路由监控
%PY% %CORE%\orca_msgbus_router.py --project <根> --watch

REM 全量验证（必须 7/7 通过）
%PY% %CORE%\orca_full_validation.py --project <根> --report r.md
```

## 四、全量验证 T1-T7 检查清单

| 检查项 | 验证内容 | 常见失败原因 |
|--------|---------|-------------|
| T1 | 目录结构完整性 | scripts/ msgbus/ 缺失 → 重新 init |
| T2 | Agent 配置文件 | config.yaml 端口冲突 → 检查端口矩阵 |
| T3 | 消息总线连通 | inbox 目录权限 → 沙箱拒绝 mkdir |
| T4 | CLI 实例可启动 | python 路径错误 → 用 managed 3.13.12 |
| T5 | GUI 实例可启动 | Edge --app 路径 → 检查 Edge 安装位置 |
| T6 | OMF 消息投递 | seen.txt 防重台账 → 清空后重试 |
| T7 | switch.cmd 切换 | PID 文件残留 → 手动删除后重试 |

## 五、常见故障与排查

### 5.1 消息丢失（发送方显示成功，接收方未收到）

```
排查步骤：
1. 检查 msgbus/inbox/<目标窗口>/ 目录是否存在
2. 检查 msgbus/ledger/seen.txt 是否已记录该消息ID（防重误判）
3. 清空 seen.txt → 重新发送
4. 如仍丢失 → 检查 orca_msgbus_router.py 是否在 --watch 状态
```

### 5.2 switch.cmd 切换失败

```
排查步骤：
1. 检查目标实例 PID 文件是否存在残留（<项目>/run/<agent>_<mode>.pid）
2. 手动删除残留 PID 文件
3. 确认端口未被占用：netstat -ano | findstr :<端口>
4. 重新执行 switch.cmd
```

### 5.3 GUI 面板白屏/无法打开

```
排查步骤：
1. 确认 gui_server.py 进程存活
2. 确认 Edge --app 模式可用（检查 Edge 安装路径）
3. Hermes/Claude 无官方 GUI exe → Web 面板是唯一选项
4. 尝试改用 CLI 实例作为降级方案
```

### 5.4 沙箱环境限制

```
已知限制：
- bash/python mkdir 被沙箱拒绝 → 用 Write 工具创建文件
- .git/index.lock 被拒绝 → git 命令交用户本机粘贴执行
- cscript 被LOLBin策略硬拦 → 快捷方式vbs只能本机执行
- PowerShell 因 __PSScriptPolicyTest 被拒 → 改用 Bash/Python
```

## 六、沙箱经验（本机 WorkBuddy 环境）

1. E盘项目目录：Write/Edit工具可写；bash/python `mkdir`、`.git/index.lock` 被沙箱拒绝 → 文件用Write工具，git命令交用户本机粘贴
2. `cscript` 被LOLBin策略硬拦 → 快捷方式vbs只能本机执行（热键Ctrl+Alt+H/K/L）
3. PowerShell工具会因 `E:\tmp\__PSScriptPolicyTest` 被拒 → 改用 Bash/Python
4. 运行时集中放脚手架 dual_core、项目仅引用中央路径 → 避免三份拷贝版本漂移（最佳实践）
5. 全量验证在 workspace 建临时项目跑（ORCA_G_DATA/ORCA_FLEET_REG 指向workspace），E盘项目做只读结构终验

## 七、关联技能

| 联动技能 | 联动方向 | 联动内容 |
|---------|---------|---------|
| orca_scaffold_silent | 单向→本技能 | 脚手架静默初始化创建项目结构，本技能管理双实例运行 |
| fleet-devops-orchestrator | 双向 | DevOps编排层调用本技能进行舰队调度，本技能故障时上报编排层 |
| orca-agent-connection-fix | 单向→本技能 | Agent连接故障修复后，本技能接管实例切换 |
| 多智能体舰队编排 | 双向 | 总架构层定义舰队拓扑，本技能执行双实例具体控制 |
| codex-mimo-link-repair | 间接 | Codex实例的MiMO链路修复后，本技能管理Codex CLI/GUI切换 |
| windows-lnk-sandbox-safe | 间接 | 生成舰队快捷方式时调用，确保沙箱安全 |

## 八、版本日志

- V1.0 (2026-07-2x)：首次创建，基础架构+命令+端口矩阵+沙箱经验
- V1.1 (2026-07-30)：auto-skill-generator 巡检迭代
  - 新增「何时激活本技能」触发条件
  - 新增「全量验证 T1-T7 检查清单」
  - 新增「常见故障与排查」4类故障+排查步骤
  - 新增「关联技能」6个联动关系
  - 新增「版本日志」
  - 扩展端口分配原则为表格
  - 预估健康度：55🟠 → 80🟡（+25分跃升）

---

> 本技能是 ORCA 舰队双实例运行时控制层，与 orca_scaffold_silent（初始化）、fleet-devops-orchestrator（DevOps编排）、orca-agent-connection-fix（连接修复）形成完整运维链路。
