---
name: "lobster_codex_dual_link_v1.0"
description: "龙虾Codex双链路架构技能——端口身份地图+主备链路隔离+一键切换+健康检测+自动故障切换。主链路4567(AI Code Switch)纯对话编码，备用链路15721(CC-Switch+Codex++)插件解锁。两条路并行不冲突。"
version: "1.0"
date: "2026-06-26"
primary_path: "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\lobster_codex_dual_link_v1.0\\SKILL.md"
sync_mode: "master-only"
hard_red_lines: ["15721总网关端口永久禁止修改", "tp-/sk-密钥类型绝不混用", "主链路不动=备用链路不受影响"]
---

# 龙虾Codex双链路架构技能 v1.0

技能名称：龙虾Codex双链路架构
技能标识：`lobster_codex_dual_link_v1.0`
适用范围：Codex本地AI开发环境的端口管理、链路切换、故障恢复
执行口径：**15721永久禁止修改**，密钥类型绝不混用，双链路隔离并行
生效时间：2026-06-26
生效范围：全域 / 永久 / Codex + CC-Switch + AI Code Switch + Codex++

---

## 0) 永恒铁律（硬性红线，违反即崩盘）

| # | 铁律 | 违反后果 |
|---|------|----------|
| 1 | **15721 永久禁止修改** — CC-Switch总网关端口，所有Agent(OpenCode/Hermes/Gemini/CloudCode)共用 | 全链路崩盘，所有Agent失联 |
| 2 | **tp-密钥 != api.xiaomimimo.com** — tp-套餐密钥必须走token-plan-cn端点 | 401全部拒绝 |
| 3 | **sk-密钥 != token-plan-cn.xiaomimimo.com** — sk-付费密钥必须走api端点 | 401全部拒绝 |
| 4 | **主链路不动 ≠ 备用链路受影响** — AICS(4567)与CC-Switch(15721)完全独立 | 隔离失效 |
| 5 | **57321不是API代理端口** — Codex++管理端口，不处理API请求 | 请求被拒绝 |
| 6 | **所有修改必须先备份** — 任何配置变更前先做全量备份 | 不可回滚 |

---

## 1) 端口身份地图（100%实测确认）

| 端口 | PID记录 | 进程 | 角色 | 能否改 | 依赖 |
|------|---------|------|------|--------|------|
| **15721** | 177228 | cc-switch.exe | CC-Switch 总网关 | ❌ 永久禁止 | 所有Agent |
| **4567** | 151436 | node.exe (AICS v6.0.1) | AI Code Switch 协议转换代理 | ✅ 独立不冲突 | AICS独享 |
| **57321** | 167048 | codex-plus-plus.exe | Codex++ 管理/控制端口 | ✅ 只改Codex++配置 | Codex++独享 |

### 57321 专项澄清
- 57321 **不是 API 代理端口**，所有API请求返回"未知后端路径"
- 职能：Codex客户端启动/停止管理 + auth注入 + 插件解锁 + 与管理器通信
- 之前 Codex++ 界面中 `base_url = 57321` 是**错误配置**（把管理端口当代理端口）
- **正确的 API 代理地址**：`http://127.0.0.1:15721/v1`

---

## 2) 双链路完整架构

### 数据流图
```
┌─────────────────────────────────────────────────────────┐
│                  Codex 桌面客户端                        │
│           (codex.exe, 由 Codex++ 启动/管理)              │
└───────────────┬─────────────────────┬───────────────────┘
                │                     │
        ┌───────▼───────┐    ┌───────▼───────┐
        │   主链路       │    │   备用链路     │
        │  (纯对话编码)   │    │ (插件解锁+对话) │
        └───────┬───────┘    └───────┬───────┘
                │                     │
        ┌───────▼───────┐    ┌───────▼───────────────────┐
        │ AICS :4567    │    │ CC-Switch :15721(总网关)   │
        │ config.toml:  │    │ MiMO provider→4567/codex  │
        │ base_url=4567 │    │ app_type=codex            │
        │ auth.json=KEY │    │ + Codex++ :57321(旁路管理) │
        └───────┬───────┘    │   - auth注入/插件解锁      │
                │            └───────┬───────────────────┘
                │                    │
        ┌───────▼────────────────────▼───────┐
        │     AI Code Switch :4567            │
        │  Responses → Chat Completions 转换   │
        │  token-plan-cn.xiaomimimo.com       │
        │  serviceId=9ddeae1b (tp-密钥)       │
        └────────────────┬───────────────────┘
                         │
        ┌────────────────▼───────────────────┐
        │     MiMO Token Plan API             │
        │  tp-cs3zbef... (Standard月度套餐)    │
        └────────────────────────────────────┘
```

### 链路选择规则
| 场景 | 使用链路 | Codex config.toml provider |
|------|----------|---------------------------|
| **纯对话编码** | 主链路(AICS直连) | `custom/xiaomi_mimo`, base_url=`http://127.0.0.1:4567/codex` |
| **需要插件解锁** | 备用链路(CC-Switch) | `custom/xiaomi_mimo`, base_url=`http://127.0.0.1:15721/v1` |
| **插件+对话** | 备用链路(CC-Switch) | `custom/xiaomi_mimo`, base_url=`http://127.0.0.1:15721/v1` |

---

## 3) 配置文件地图

### AI Code Switch (AICS) 核心配置
```
C:\Users\Administrator\.aicodeswitch\
├── fs-db\
│   ├── routes.json          # 路由规则: c1ae2367→9ddeae1b(token-plan)
│   ├── vendors.json         # 供应商+密钥: tp-cs3zbef...→MiMO
│   ├── access-keys.json     # 准入密钥注册
│   ├── api-path-bindings.json # 路径绑定: /codex/responses等9条
│   └── config.json          # 全局配置: failover/enableAgentTeams
├── server.log               # 运行日志
└── E:\aicodeswitch_v5\aicodeswitch.cmd  # 启动脚本
```

### Codex 客户端配置
```
C:\Users\Administrator\.codex\
├── config.toml              # 模型提供商: custom/xiaomi_mimo, base_url
├── auth.json                # OPENAI_API_KEY (主链路=真实密钥, 备用链路=PROXY_MANAGED)
├── cc-switch-model-catalog.json  # 模型目录
└── backups/                 # Codex++自动备份
```

### CC-Switch 配置
```
C:\Users\Administrator\.cc-switch\
├── cc-switch.db             # SQLite数据库
│   ├── providers → settings_config(JSON内嵌TOML)→base_url
│   ├── provider_health → is_healthy/failures
│   └── proxy_config → 代理规则
└── skills/                  # CC-Switch技能库
```

### 启动命令
```
AI Code Switch:  E:\aicodeswitch_v5\aicodeswitch.cmd start    (端口4567)
CC-Switch:       E:\龙虾AI主控中心\CC-Switch\cc-switch.exe      (端口15721)
Codex++:         E:\龙虾AI主控中心\tools\Codex++\codex-plus-plus.exe (端口57321)
```

---

## 4) 密钥类型法则（绝对不可混淆）

| 密钥前缀 | 类型 | 目标端点 | serviceId | 混用后果 |
|----------|------|----------|-----------|----------|
| `tp-` | 套餐密钥 | `https://token-plan-cn.xiaomimimo.com/v1/chat/completions` | `9ddeae1b` | 401 |
| `sk-` | 按量付费 | `https://api.xiaomimimo.com/v1/chat/completions` | `a7b9cc33` | 404 |

**当前生效密钥**: `tp-cs3zbef7vhc75lcpsw9x7pau27mjftwhqnovn5zrq2d0puft` (Standard月度套餐)

---

## 5) 故障模式与修复

### 故障1: 黑名单级联
**症状**: AI Code Switch 日志出现 "blacklisted"，所有请求503
**原因**: 某次405→自动重试→再失败→进黑名单→后续请求全跳过
**修复**: 等待failoverRecoverySeconds(默认60s)自动恢复，或重启AICS

### 故障2: access-keys.json为空
**症状**: 所有请求500，fallback到15721
**原因**: 准入密钥未注册，认证失败后走fallback
**修复**: 确保access-keys.json包含当前tp-密钥

### 故障3: CC-Switch数据库被锁
**症状**: CC-Switch无法启动，日志显示database locked
**原因**: 前次异常退出导致SQLite锁残留
**修复**: 停止CC-Switch → 删除`.cc-switch/cc-switch.db-journal`和`.cc-switch/cc-switch.db-wal` → 重启

### 故障4: 57321端口被误认为代理
**症状**: Codex++配置base_url=57321，对话失败
**原因**: 将Codex++管理端口当API代理端口
**修复**: 修改Codex config.toml的base_url为`http://127.0.0.1:15721/v1`

### 故障5: tp-密钥走了api.xiaomimimo.com
**症状**: 401 Unauthorized
**原因**: routes.json的targetServiceId配成了a7b9cc33(付费API)而非9ddeae1b(token-plan)
**修复**: 确认routes.json中targetServiceId=`9ddeae1b-949b-4099-a9db-81b466379c9c`

---

## 6) 健康检查清单

运行 `DualLink_HealthCheck.bat` 自动检测：
1. [ ] 端口15721 → cc-switch.exe → HTTP 200
2. [ ] 端口4567 → node.exe → HTTP 200
3. [ ] 端口57321 → codex-plus-plus.exe → 存活
4. [ ] 主链路穿透: POST :4567/codex/responses → 200
5. [ ] 备用链路穿透: POST :15721/v1/chat/completions → 200
6. [ ] MiMO直连: POST token-plan-cn → 200
7. [ ] AICS日志无异常
8. [ ] CC-Switch数据库provider健康

---

## 7) 关联技能

- `lobster_task_standard_workflow_full_v2.1` — 龙虾标准五步法
- `lobster_codex_aicodeswitch_fix` — AICS专项修复技能
- `cc-switch-ollama-fix` — CC-Switch Ollama诊断
- `cc-switch-mcp-auto-import` — CC-Switch MCP自动导入

---

## 8) 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-26 | 初始版本，固化双链路架构+端口地图+一键脚本 |
