---
name: "ccgui-orca-bridge"
description: "CCGUI v0.7.11 与 ORCA 舰队协同作战完整指南。包含双系统架构定位、快捷使用方法、截图桥接、MIMO链路共享、技能同步、故障排查。"
version: "1.0"
date: "2026-07-30"
agent_created: true
---

# CCGUI × ORCA 协同作战指南

## 系统定位

| 系统 | 角色 | 安装路径 | 进程 | 端口 |
|------|------|---------|------|------|
| **ORCA** | 舰队调度中枢 | E:/龙虾AI主控中心/我的AI分身 | Orca.exe(7进程) + hermes.exe + claude.exe | 15721(cc-switch) + 63767(hooks) |
| **CCGUI** | GUI操作台+插件系统 | C:/Users/Administrator/AppData/Local/ccgui | cc-gui.exe(PID 244380) + cc_gui_daemon | 62273(daemon API) |
| **CC-Switch** | MIMO V2.5代理网关 | E:/龙虾AI主控中心/CC-Switch | cc-switch.exe(PID 2240) | 15721 |
| **AI Code Switch** | 模型协议转换 | G盘Junction | 进程内嵌 | 4567(/v1) |

## 架构关系图

```
┌─────────────────────────────────────────────────────┐
│                    用户桌面                          │
│   ┌──────────┐        ┌───────────────────┐         │
│   │ CCGUI    │ ←桌面→ │ ORCA IDE          │         │
│   │ 快捷方式 │        │ (多标签+worktree)  │         │
│   └──────────┘        └───────────────────┘         │
│        ↓                      ↓                      │
│   ┌──────────┐        ┌───────────────────┐         │
│   │cc-gui    │        │ hermes(调度)       │         │
│   │daemon    │        │ claude(核查)       │         │
│   │:62273    │        │ codex(执行)        │         │
│   └──────────┘        └───────────────────┘         │
│        ↓                      ↓                      │
│   ┌──────────────────────────────────────┐          │
│   │        CC-Switch :15721              │          │
│   │   → AI Code Switch :4567/v1         │          │
│   │   → MIMO V2.5 Pro 后端              │          │
│   └──────────────────────────────────────┘          │
└─────────────────────────────────────────────────────┘
```

## 使用方法

### 1. 启动CCGUI

双击桌面 `ccgui.lnk` 快捷方式，或在命令行运行：
```
C:/Users/Administrator/AppData/Local/ccgui/cc-gui.exe
```

CCGUI会自动启动守护进程 `cc_gui_daemon`（端口62273）。

### 2. 在CCGUI中切换引擎

CCGUI支持4种引擎，在CCGUI界面顶部下拉选择：
- **Claude Code** — Anthropic官方CLI
- **Codex CLI** — OpenAI Codex
- **Gemini CLI** — Google Gemini
- **OpenCode** — 开源替代

### 3. 截图功能（补齐ORCA可莉缺失）

CCGUI内置截图能力。通过守护进程API调用：
```bash
# 检查CCGUI daemon状态
curl http://127.0.0.1:62273/status

# CCGUI界面内直接截图（Ctrl+Shift+S 或界面截图按钮）
# 截图保存至 C:/Users/Administrator/.ccgui/ 或 CCGUI workspace目录
```

ORCA可莉CLI无法截图，但CCGUI截图后可通过共享目录让ORCA读取。

### 4. 技能共享

CCGUI `curated-skills/` 目录结构与ORCA `skills/` 同源（metadata.json + SKILL.md）：
```
CCGUI: C:/Users/Administrator/AppData/Local/ccgui/curated-skills/
  ├── caveman/         (metadata.json + SKILL.md)
  └── lazy-senior-dev/ (metadata.json + SKILL.md)

ORCA WorkBuddy: C:/Users/Administrator/.workbuddy/skills/
  ├── ccgui-orca-bridge/
  ├── github-release-verify-download/
  ├── orca-fleet-dual-control/
  └── ... (30+ skills)
```

双向同步方式：将WorkBuddy技能的SKILL.md复制到CCGUI curated-skills目录即可。

### 5. MIMO V2.5 链路共享

两个系统共享同一MIMO链路，通过CC-Switch代理：
```
CCGUI → cc-switch :15721 → AI Code Switch :4567/v1 → MIMO V2.5 Pro
ORCA  → cc-switch :15721 → AI Code Switch :4567/v1 → MIMO V2.5 Pro
```

**关键约束**：CC-Switch baseURL必须带 `/v1` 前缀（`http://127.0.0.1:4567/v1`），否则404。

### 6. 项目互通

ORCA打开的项目worktree路径与CCGUI可共享：
```
ORCA worktree → E:/龙虾AI主控中心/我的AI分身/企业微信群定制接单项目/worktrees/hermes
CCGUI workspace → 可在CCGUI界面中打开同一路径
```

## 故障排查

| 症状 | 原因 | 修复 |
|------|------|------|
| CCGUI白屏/闪退 | WebView2渲染问题 | 重启cc-gui.exe，检查WebView2运行时 |
| daemon端口62273无响应 | daemon未启动 | 手动启动cc_gui_daemon.exe |
| MIMO 404 | CC-Switch baseURL缺/v1 | SQL修复：UPDATE providers SET settings_config... |
| ORCA面板空白 | 会话清空(正常) | 输入"查看历史会话"从state.db检索 |
| Codex EPERM | 进程卡死 | taskkill /F /IM codex.exe → 重启 |
| Marvis闪退 | CEF GPU加速冲突 | 启动参数加 --disable-gpu --no-sandbox |

## 基线快照与回滚

快照路径：`G:/龙虾AI主控中心/system_snapshot/2026-07-30_1712_stable_baseline/`
- `process_snapshot.txt` — 进程PID+端口清单
- `e_project_files.txt` — E盘2705个关键文件路径
- `git_log.txt` — Git提交记录
- `cc_switch_config.json` — CC-Switch配置备份
- `ccgui_status.txt` — CCGUI安装状态

回滚方式：参照快照中的文件清单和配置，逐一恢复。

## 触发词

CCGUI、ORCA协同、截图桥接、MIMO链路、ccgui使用、双系统、GUI操作台、可莉截图、daemon端口、舰队协同
