---
name: "orca-agent-connection-fix"
description: "ORCA Agent (Codex/Claude Code/Hermes) 连接故障快速诊断与修复技能。覆盖 502 Bad Gateway、ConnectionRefused、command not found、协议不兼容等全部已知故障模式。含双配置文件同步原则、协议转换桥(v1.0.3)部署与一键恢复、MiMO连通性验证。触发词：Agent连接失败、502、ConnectionRefused、CloudCode不工作、Claude Code连不上、ORCA代理挂了、orca cmd报错、协议桥"
version: "1.2.0"
date: "2026-07-19"
merged_from: ["Codex_502排障实战", "Claude_Code_ConnectionRefused排障实战", "协议转换桥v1.0.3", "三Agent一键自愈V1.0"]
sync_mode: "bidirectional"
primary_path: "C:\\Users\\Administrator\\.workbuddy\\skills\\orca-agent-connection-fix\\SKILL.md"
---

# ORCA Agent 连接故障诊断与修复 v1.1

## 触发条件
当出现以下任一症状时激活本技能：
- ORCA 内 Agent 面板报 `502 Bad Gateway` / `ConnectionRefused` / `stream error`
- `orca cmd` 命令报错（`command not found` / `not supported on Windows`）
- Claude Code / Codex 独立模式也无法连接
- Agent 反复重试无法建立 API 连接
- 需要让 CloudCode/Claude Code 彻底脱离 ORCA 15721 原生代理独立运行

## 快速诊断三步法（30秒定位）

### Step 1: 确认症状类型
```
| 症状 | 可能根因 | 优先级 |
|------|---------|--------|
| 502 Bad Gateway | 代理端口死 + 配置指向代理 | P0 |
| ConnectionRefused | 代理端口未监听 | P0 |
| command not found | ORCA CLI 不支持该子命令/参数 | P1 |
| 模型不存在/无访问 | 模型名不匹配（Anthropic vs MiMO） | P1 |
| Auto-update failed | npm 缓存损坏或网络问题 | P2 |
```

### Step 2: 检查端口 + 上游
```bash
# 1. 桥接/代理端口
netstat -ano | grep 15721
# → LISTENING = 正常 | 无输出 = 桥接挂了

# 2. MiMO 上游健康 (OpenAI 格式)
curl -s -o /dev/null -w "HTTP %{http_code} %{time_total}s" \
  "https://token-plan-cn.xiaomimimo.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"model":"mimo-v2.5-pro","messages":[{"role":"user","content":"hi"}]}'
# → 200 = MiMO 健康 | 非200 = 上游问题

# 3. 舰队服务
netstat -ano | grep -E "878[789]"
```

### Step 3: 定位配置文件（关键！不同 Agent 配置位置不同）
```
┌───────────┬──────────────────────────────────────────────────────┐
│ Agent     │ 配置文件路径                                         │
├───────────┼──────────────────────────────────────────────────────┤
│ Codex     │ ① ~/.codex/config.toml (独立CLI)                   │
│           │ ② G:/Orca/data/appdata/Orca/codex-runtime-home/    │
│           │    home/config.toml (ORCA内嵌) ⚠️ 两份都要改！      │
├───────────┼──────────────────────────────────────────────────────┤
│ Claude    │ ~/.claude/settings.json (仅此一份，ORCA无独立目录)     │
│ Code      │ ⚠️ 协议是 Anthropic 格式，不是 OpenAI！              │
├───────────┼──────────────────────────────────────────────────────┤
│ Hermes    │ ORCA 内部管理，通常无需手动改配置                    │
└───────────┴──────────────────────────────────────────────────────┘
```

## 修复方案矩阵

### 方案 A：直连 MiMO（适用于 Codex，最简单）
**前提**：目标 Agent 使用 OpenAI 兼容格式

**Codex 操作**：
```toml
# 两份 config.toml 都要改！
[model_providers.custom]
base_url = "https://token-plan-cn.xiaomimimo.com/v1"  # ← 改这里
requires_openai_auth = false                          # ← 改这里
env_key = "OPENAI_API_KEY"
```

**验证**：`codex exec --full-auto "回复OK"` → 应返回 OK

### 方案 B：协议转换桥 v1.0.3（CloudCode/Claude Code **推荐**，彻底脱离 ORCA）⭐
**根因**：Claude Code 用 Anthropic Messages API 格式，MiMO 只接受 OpenAI `/chat/completions` → 必须做协议转换。
**旧方式**依赖 ORCA 15721 原生代理，但代理端口是 ORCA 临时动态分配的，易死、不可靠。
**本方案**：用独立常驻的「龙虾协议转换桥」做 Anthropic↔OpenAI 双向转换，固定监听 15721（对齐原端口，无需改客户端），彻底摆脱 ORCA 代理依赖。

**部署位置（G盘，全部）**：`G:\龙虾AI主控中心\AI分身技能库\ClaudeCode协议转换桥\`
```
lobster_protocol_bridge.py   # 桥接主体 (端口固定 15721)
.bridge_key                  # MiMO 真实密钥 (gitignore, 不入库)
.gitignore                   # 忽略 .bridge_key / *.log
recover_bridge.py            # 一键恢复脚本
bridge_watchdog.py           # 端口巡检 + 自动重启
```

**启动（手动）**：
```bash
PY="C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
"$PY" "G:\龙虾AI主控中心\AI分身技能库\ClaudeCode协议转换桥\lobster_protocol_bridge.py"
```

**Claude Code 配置**（`~/.claude/settings.json` env 块）：
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:15721",
    "ANTHROPIC_AUTH_TOKEN": "<MiMO真实密钥>",
    "DISABLE_AUTOUPDATE": "1",
    "CLAUDE_CODE_AUTOUPDATER_DISABLED": "1"
  }
}
```

**桥接核心能力（v1.0.3 已验证）**：
- ✅ 全局异常捕获：任何请求/解析/转发异常完整写入日志，不再静默 502
- ✅ 大载荷缓冲：`ThreadingHTTPServer` 并发 + 完整读取，实测 98KB+ 工程上下文正常
- ✅ 原生 SSE 流式：完全匹配 Claude Code 运行模式（message_start→delta→stop 全事件）
- ✅ 精细报文转换：自动剥离 Anthropic 独有字段、兼容 MiMO OpenAI 规范
- ✅ tools / tool_use 双向转换（请求侧 tool_use/tool_result→OpenAI；响应侧 tool_calls→tool_use）
- ✅ 模型强制映射 `mimo-v2.5-pro`，`system` 字段适配，思考链(reasoning)兜底为正文
- ✅ 固定端口 15721（对齐原 ORCA 代理），客户端零改动
- ✅ 全链路日志：`G:\AI日志\ClaudeBridgeLog\bridge_YYYYMMDD.log`（原始报文/转换后/上游码/耗时/堆栈）

**自启动 + 巡检（Windows 计划任务，已创建）**：
| 任务名 | 触发 | 动作 |
|--------|------|------|
| LobsterBridgeAutostart | 登录时 | `recover_bridge.py`（端口校验+启动+健康检查） |
| LobsterBridgeWatchdog | 每 5 分钟 | `bridge_watchdog.py`（端口/进程存活，异常自动重启+告警日志） |
| LobsterBridgeDailyCheck | 每日 09:00 | `recover_bridge.py`（每日连通性深度巡检） |

**验证结果**：
- 小体积非流式 / 98KB 大载荷压测 / 流式 SSE 三场景 **全部 PASS**
- 报文转换单元测试（请求 tools、多轮 tool_use/tool_result、响应 tool_calls、推理兜底）**ALL PASS**

### 方案 B+：三Agent一键自愈脚本 V1.0（**推荐首选操作**）⭐⭐
> 2026-07-19 新增。整合方案A+B+C全部逻辑，一条命令完成诊断+修复+验证。

**脚本位置**：`G:\龙虾AI主控中心\AI分身技能库\ORCA_Agent_Fleet\orca_agents_auto_recover.py`

```bash
PY="C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"

# 模式1: 自动诊断 + 按需修复（日常首选）
"$PY" "G:\龙虾AI主控中心\AI分身技能库\ORCA_Agent_Fleet\orca_agents_auto_recover.py"

# 模式2: 仅诊断不修复（巡检）
"$PY" "G:\...\orca_agents_auto_recover.py" --check

# 模式3: 强制修复（故障恢复后）
"$PY" "G:\...\orca_agents_auto_recover.py" --fix
```

**覆盖的三大模块**：
| 模块 | 检测项 | 自动修复 |
|------|--------|---------|
| Claude Code 协议桥 | 15721端口 / settings.json(3项) / HTTP健康检查 | 终止旧进程→重启桥→改配置→验连通 |
| Codex 代理链路 | 双config.toml(各3项) / MiMO POST对话测试 | 双文件重写→API验证 |
| ORCA 集群健康 | 4端口(15721/8787-9) / 3Agent进程 | 输出报告标记异常 |

**退出码**：`0`=全部正常, `2`=存在异常

**配套工具**：
- `task_validator.py` — 计划任务校验器（3任务/6文件/端口）
- `recover_bridge.py` — 桥接单组件恢复
- `bridge_watchdog.py` — 端口看门狗（计划任务调用）

### 方案 C：重启 ORCA 重建代理（兜底，仅当桥接不可用）
**原因**：ORCA 启动时自动重建 15721 代理端口，可临时恢复 CloudCode。
**操作**：
1. 关闭 ORCA 应用程序
2. 重新打开 ORCA（自动重建 15721）
3. 恢复 settings.json 为指向 15721 的桥接/代理配置
4. 在 ORCA 中打开 CloudCode 面板验证

> ⚠️ 此方案依赖 ORCA 进程，代理端口为临时动态分配，不适合长期依赖。优先用方案 B。

## 协议兼容性速查

| 发送方 | 原生格式 | 认证 Header | 模型名示例 | MiMO 支持 |
|--------|---------|------------|-----------|----------|
| **Codex** | OpenAI | `Authorization: Bearer` | `mimo-v2.5-pro` | ✅ 直接兼容 |
| **Claude Code** | Anthropic | `x-api-key` | `claude-opus-4-7[1M]` | ❌ **需要转换(方案B桥接)** |

## 防复发 Checklist（长效管控）

- [ ] 每次修改 Agent 配置前 **先备份**（settings.json → `G:\AI备份\ClaudeConfig\`）
- [ ] Codex 必须改 **两份** config.toml（独立 + ORCA 内嵌）
- [ ] Claude Code 固定走桥接 15721；**禁用 ORCA 内置 CloudCode `--teams`**（Windows 不支持），统一用独立 Claude Code 客户端 + 桥接
- [ ] Claude Code 版本锁定：settings.json 设 `DISABLE_AUTOUPDATE=1` + `CLAUDE_CODE_AUTOUPDATER_DISABLED=1`，杜绝 Auto-update failed
- [ ] 桥接进程由计划任务 `LobsterBridgeWatchdog` 每 5 分钟巡检自愈
- [ ] 密钥仅存 `.bridge_key`（gitignore），禁止提交到任何仓库
- [ ] 所有快照/脚本/配置 **统一存 G盘**，严禁写 C盘

## 回滚操作

```bash
# 1) 一键恢复桥接 (端口校验 + 启动 + 健康检查)
"$PY" "G:\龙虾AI主控中心\AI分身技能库\ClaudeCode协议转换桥\recover_bridge.py"

# 2) Claude Code 配置回滚
cp "G:\AI备份\ClaudeConfig\settings_backup_*.json" "$HOME/.claude/settings.json"

# 3) 桥接 Git 快照回滚 (仓库即 G盘归档目录)
cd "G:\龙虾AI主控中心\AI分身技能库\ClaudeCode协议转换桥"
git log --oneline -5            # 找到正常节点
git reset --hard <hash>

# 4) Codex 双配置回滚
cp ~/.codex/config.toml.bak ~/.codex/config.toml
cp "G:/Orca/.../config.toml.bak" "G:/Orca/.../config.toml"
```

---
*技能版本: v1.1.0 | 基于 Codex 502 / Claude Code ConnectionRefused / 协议桥 v1.0.3 三次实战沉淀 | 最后更新: 2026-07-19*
