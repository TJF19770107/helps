---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_1157fd23736911f1897e5254002afed2
    ReservedCode1: yGVWQVgE7F+dHO0kKt/vSQITbShOVWal5Bi2PzSv5KrvvGwiQ3gIAUpWIm1rTV5u8f3qwJfM4MbjUB/lPL2Lq+gsMN1TOfYQTLi/jgRXHrGsLlL1XZxrtaDQMMBPpORvpzlmdZ6T0CssSAIL8D5Suie9fqDba0iTcRPSf0QTh1A5uy5LqbZqAr9muiw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_1157fd23736911f1897e5254002afed2
    ReservedCode2: yGVWQVgE7F+dHO0kKt/vSQITbShOVWal5Bi2PzSv5KrvvGwiQ3gIAUpWIm1rTV5u8f3qwJfM4MbjUB/lPL2Lq+gsMN1TOfYQTLi/jgRXHrGsLlL1XZxrtaDQMMBPpORvpzlmdZ6T0CssSAIL8D5Suie9fqDba0iTcRPSf0QTh1A5uy5LqbZqAr9muiw=
---

﻿# MT5 MCP 双链路配置同步报告

**生成时间**: 2026-06-29  
**任务**: 补充 Codex 侧 MT5 MCP 配置，完成 Claude Code + Codex 双链路统一 MCP 配置  
**状态**: ✅ 已完成

---

## 一、Codex MCP 配置更新

| 项目 | 详情 |
|------|------|
| 配置文件 | `C:\Users\Administrator\.codex\mcp.json` |
| 备份文件 | `C:\Users\Administrator\.codex\mcp.json.backup_20260629` |
| 操作 | 追加 `metatrader-real` 条目 |
| JSON 有效性 | ✅ 已验证通过 |

### 当前 mcpServers 条目（4个）

| # | 条目名 | 类型 | 描述 |
|:---:|------|------|------|
| 1 | `lobster-cluster-collaboration` | stdio | 龙虾群体协作集群 - Codex端入口 |
| 2 | `lobster-codex-to-claude` | sse | 龙虾双向互注册 - Claude Code MCP服务端 |
| 3 | `lobster-codex-to-hermes` | sse | 龙虾双向互注册 - Hermes MCP服务端 |
| 4 | **`metatrader-real`** | **streamable-http** | **MT5实盘 MCP Server - 仅行情查询/回测，已屏蔽下单接口** |

### 新增 metatrader-real 配置

```json
{
  "type": "streamable-http",
  "url": "http://127.0.0.1:8000/api/v1/mcp",
  "description": "MT5实盘 MCP Server - 仅行情查询/回测，已屏蔽下单接口"
}
```

---

## 二、CC-Switch 中 MT5 相关配置

| 检查范围 | 结果 |
|------|------|
| `C:\Users\Administrator\.cc-switch\` 下 .json / .toml 文件 | ❌ 未发现 "metatrader" 或 "mt5" 关键字 |
| skills 子目录 | 已排除（非配置目录） |

**结论**: CC-Switch 当前未涉及 MT5 MCP 配置，无需额外操作。

---

## 三、sim/real 双环境配置文件检查

### 文件存在性

| 文件 | 存在 |
|------|:---:|
| `E:\龙虾AI主控中心\MT5-MCP-Server\sim\.env` | ✅ |
| `E:\龙虾AI主控中心\MT5-MCP-Server\sim\mcp_sim.json` | ✅ |
| `E:\龙虾AI主控中心\MT5-MCP-Server\real\.env` | ✅ |
| `E:\龙虾AI主控中心\MT5-MCP-Server\real\mcp_real.json` | ✅ |

### sim 模拟盘 (Claude Code STDIO)

| 配置项 | 当前值 | 状态 |
|------|------|:---:|
| `LOGIN` | `SIM_LOGIN_PLACEHOLDER` | ⚠️ 待填入 |
| `PASSWORD` | `SIM_PASSWORD_PLACEHOLDER` | ⚠️ 待填入 |
| `SERVER` | `SIM_SERVER_PLACEHOLDER` | ⚠️ 待填入 |
| `MT5_PATH` | `C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe` | ✅ |
| mcp_sim.json `metatrader-sim` 条目 | 已存在（STDIO模式） | ✅ |

### real 实盘 (Codex HTTP API)

| 配置项 | 当前值 | 状态 |
|------|------|:---:|
| `LOGIN` | `REAL_LOGIN_PLACEHOLDER` | ⚠️ 待填入 |
| `PASSWORD` | `REAL_PASSWORD_PLACEHOLDER` | ⚠️ 待填入 |
| `SERVER` | `REAL_SERVER_PLACEHOLDER` | ⚠️ 待填入 |
| `MT5_PATH` | `C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe` | ✅ |
| `API_HOST` | `0.0.0.0` | ✅ |
| `API_PORT` | `8000` | ✅ |
| mcp_real.json `metatrader-real` 条目 | 已存在（STDIO + `MT5_TRADE_MODE=readonly`） | ✅ |

---

## 四、需填入真实凭证的字段汇总

### sim/.env（模拟盘—3个字段）

| 字段 | 占位符 | 说明 |
|------|------|------|
| `LOGIN` | `SIM_LOGIN_PLACEHOLDER` | MT5模拟账户登录号 |
| `PASSWORD` | `SIM_PASSWORD_PLACEHOLDER` | MT5模拟账户密码 |
| `SERVER` | `SIM_SERVER_PLACEHOLDER` | MT5模拟账户服务器名（如 FOREX.com-Demo） |

### real/.env（实盘—3个字段）

| 字段 | 占位符 | 说明 |
|------|------|------|
| `LOGIN` | `REAL_LOGIN_PLACEHOLDER` | MT5实盘账户登录号 |
| `PASSWORD` | `REAL_PASSWORD_PLACEHOLDER` | MT5实盘账户密码 |
| `SERVER` | `REAL_SERVER_PLACEHOLDER` | MT5实盘服务器名（如 FOREX.com-Real） |

### mcp_sim.json（模拟盘—3个字段）

| 字段 | 占位符 |
|------|------|
| `--login` | `SIM_LOGIN_PLACEHOLDER` |
| `--password` | `SIM_PASSWORD_PLACEHOLDER` |
| `--server` | `SIM_SERVER_PLACEHOLDER` |

### mcp_real.json（实盘—3个字段）

| 字段 | 占位符 |
|------|------|
| `--login` | `REAL_LOGIN_PLACEHOLDER` |
| `--password` | `REAL_PASSWORD_PLACEHOLDER` |
| `--server` | `REAL_SERVER_PLACEHOLDER` |

---

## 五、双链路 MCP 配置一致性总览

| 链路 | MCP 配置文件 | metatrader 条目 | 类型 | 状态 |
|------|------|:---:|------|:---:|
| **Claude Code** | `C:\Users\Administrator\.claude\mcp.json` | `metatrader` (STDIO) | stdio | ✅ (已于前置任务配置) |
| **Claude Code SIM** | `sim\mcp_sim.json` | `metatrader-sim` | stdio | ✅ |
| **Codex** | `C:\Users\Administrator\.codex\mcp.json` | `metatrader-real` | streamable-http | ✅ (本次新增) |
| **Codex REAL** | `real\mcp_real.json` | `metatrader-real` | stdio | ✅ |

---

## 六、结论

✅ **Codex MCP 配置已完成补充**，`metatrader-real` 条目已成功追加至 `C:\Users\Administrator\.codex\mcp.json`。  
⚠️ **所有 .env 凭证仍为 PLACEHOLDER**，sim 和 real 共 6 个凭证字段待填入真实值后方可启动 MT5 MCP 服务。  
📋 CC-Switch 无需额外操作，双链路 MCP 配置层面已统一。
*（内容由AI生成，仅供参考）*
