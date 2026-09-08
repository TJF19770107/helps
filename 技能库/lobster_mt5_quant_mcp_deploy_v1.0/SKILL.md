---
name: "lobster_mt5_quant_mcp_deploy_v1.0"
description: "龙虾MT5双AI量化MCP对接运维：覆盖MT5 MCP Server（ariadng/metatrader-mcp-server）的本地部署、双AI链路配置（方案A Claude Code+MT5 / 方案B Codex+MT5）、全服务巡检与故障排查四大环节"
version: "1.0"
source: "基于 ariadng/metatrader-mcp-server v0.5.1 本地部署实践经验提炼"
merged_from: ["MT5终端环境诊断实战", "metatrader-mcp-server 源码部署实战", "Ollama+Codex+Claude Code三引擎启动实战", "MT5 MCP STDIO/HTTP双模式配置实战", "4567 HTTP代理中继层部署实战", "全服务端口巡检实战"]
date: "2026-06-29"
sync_mode: "bidirectional"
primary_path: "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_mt5_quant_mcp_deploy_v1.0\SKILL.md"
backup_path: "G:\龙虾AI主控中心\我的AI分身\技能库\backup\"
---

# 龙虾MT5双AI量化MCP对接运维 v1.0

技能名称：龙虾MT5双AI量化MCP对接运维
技能标识：lobster_mt5_quant_mcp_deploy_v1.0
适用场景：MT5双AI量化链路的搭建、诊断、部署、巡检与故障排查
来源：基于 [ariadng/metatrader-mcp-server](https://github.com/ariadng/metatrader-mcp-server) v0.5.1 的本地部署实践经验
版本号：v1.0
更新时间：2026-06-29

---

## 一、技能概述

本技能封装了 MT5 双AI量化链路（Claude Code + Codex）从零部署到全服务巡检的完整工作流，分四大环节：

```
环境诊断 → 组件部署 → 链路配置 → 服务巡检
```

### 双方案拓扑图

```
                    ┌──────────────────────────────┐
                    │      CC Switch (:15721)       │
                    │    AI推理调度/模型路由中心     │
                    └──────────┬───────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
     ┌────▼────┐         ┌────▼────┐         ┌─────▼─────┐
     │ Ollama  │         │ 4567代理│         │Claude Code │
     │ :11434  │         │  中继层  │         │  (内置路由) │
     │ 本地LLM │         └────┬────┘         └─────┬─────┘
     └─────────┘              │                    │
                              │                    │
                         ┌────▼────┐         方案A:  │
                         │ Codex++ │         STDIO   │
                         │ :57321  │         MCP─────┤
                         └────┬────┘                 │
                              │                      │
              方案B: HTTP API │                      │
               localhost:8000 │                      │
                              │                      │
                    ┌─────────▼──────────┐           │
                    │  MT5 MCP Server    │◄──────────┘
                    │  (metatrader-mcp-  │
                    │   server v0.5.1)   │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  MetaTrader 5      │
                    │  terminal64.exe    │
                    │  FOREX.com CN      │
                    └────────────────────┘
```

### 关键端口映射表

| 端口 | 服务 | 用途 | 方案归属 |
|:---:|------|------|:---:|
| 11434 | Ollama | 本地LLM推理引擎 | 双方案共用 |
| 15721 | CC Switch | AI推理调度中心 | 双方案共用 |
| 57319 | Codex++ Manager | Codex管理后台 | 方案B |
| 57320 | Codex++ | Codex推理服务 | 方案B |
| 57321 | Codex++ | Codex推理服务 | 方案B |
| 4567 | HTTP代理中继 | /codex→57321转发 + /statistics监控 | 方案B |
| 8000 | MT5 HTTP API | metatrader-http-server REST API | 方案B |
| 8080 | MT5 MCP SSE | MCP远程SSE模式（默认） | 方案A远端 |

---

## 二、环节一：环境诊断

### 2.1 MT5 终端检查

| 检查项 | 预期路径 | 检查命令 |
|--------|----------|----------|
| MT5安装目录 | `C:\Program Files\MT5 by FOREX.com Global CN\` | `Test-Path <路径>` |
| terminal64.exe | `C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe` | `Get-Item <路径>` |
| MQL5目录 | 同上 `MQL5\` | `Get-ChildItem` |

### 2.2 Python 环境检查

```powershell
python --version  # 必须 >= 3.10
```

Python 3.10+ 是 metatrader-mcp-server 的硬性要求。

### 2.3 MT5 MCP Server 源码检查

搜索关键词：`metatrader-mcp-server`、`ariadng`

预期路径：`E:\龙虾AI主控中心\MT5-MCP-Server\`

若缺失 → 进入环节二部署。

### 2.4 已有技能库检查

检查 `E:\龙虾AI主控中心\我的AI分身\技能库\` 下已有技能列表，避免重复部署。

---

## 三、环节二：组件部署

### 3.1 获取 MT5 MCP Server 源码

```powershell
# 方案一：Git clone（需Git已安装）
git clone https://github.com/ariadng/metatrader-mcp-server.git E:\龙虾AI主控中心\MT5-MCP-Server\

# 方案二：下载 ZIP 解压（Git不可用时）
Invoke-WebRequest -Uri "https://github.com/ariadng/metatrader-mcp-server/archive/refs/heads/main.zip" -OutFile "$env:TEMP\mt5-mcp.zip"
Expand-Archive -Path "$env:TEMP\mt5-mcp.zip" -DestinationPath "E:\龙虾AI主控中心\MT5-MCP-Server\" -Force
```

### 3.2 安装 Python 包

```powershell
pip install metatrader-mcp-server   # PyPI 发布版 v0.5.1
cd E:\龙虾AI主控中心\MT5-MCP-Server
pip install -e .                     # 可编辑模式安装
pip install pytest python-dotenv    # 开发依赖
```

> metatrader-mcp-server 自动安装依赖：MetaTrader5、numpy、pandas、tabulate、pytest、httpx、python-dotenv

### 3.3 验证部署完整性

```powershell
Get-ChildItem E:\龙虾AI主控中心\MT5-MCP-Server\src\ -Recurse -Directory | Select-Object FullName
```

核心子模块检查清单：

| 模块 | 路径 | 职责 |
|------|------|------|
| metatrader_client | `src/metatrader_client/` | 核心 MT5 客户端库 (6子模块/66+ .py) |
| metatrader_mcp | `src/metatrader_mcp/` | MCP 服务端实现 |
| metatrader_openapi | `src/metatrader_openapi/` | HTTP/REST API 服务 (5路由模块) |
| metatrader_quote | `src/metatrader_quote/` | WebSocket 报价流 |
| claude-skill | `claude-skill/trading/` | Claude 交易助手技能 (32工具) |

---

## 四、环节三：链路配置

### 4.1 创建 .env 环境变量文件

路径：`E:\龙虾AI主控中心\MT5-MCP-Server\.env`

```ini
# MT5 账户凭证（请取消注释并填入实际值）
# LOGIN=YOUR_MT5_LOGIN
# PASSWORD=YOUR_MT5_PASSWORD
# SERVER=YOUR_MT5_SERVER_NAME

# MT5 终端路径（非标准安装时指定）
# MT5_PATH=C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe

# MCP 传输配置（可选，默认 SSE）
# MCP_TRANSPORT=stdio
# MCP_HOST=127.0.0.1
# MCP_PORT=8080
```

### 4.2 方案A：Claude Code + MT5 MCP（STDIO 模式）

在 Claude Code 的 `mcp.json` 中追加 metatrader 条目：

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader-mcp-server",
      "args": [
        "--login",     "LOGIN_PLACEHOLDER",
        "--password",  "PASSWORD_PLACEHOLDER",
        "--server",    "SERVER_PLACEHOLDER",
        "--transport", "stdio",
        "--path",      "C:\\Program Files\\MT5 by FOREX.com Global CN\\terminal64.exe"
      ]
    }
  }
}
```

### 4.3 部署 Trading Assistant Skill

将 `E:\龙虾AI主控中心\MT5-MCP-Server\claude-skill\trading\SKILL.md` 复制到 Claude Code skills 目录：

```powershell
Copy-Item -Path "E:\龙虾AI主控中心\MT5-MCP-Server\claude-skill\trading\SKILL.md" -Destination "C:\Users\Administrator\.claude\skills\trading\SKILL.md" -Force
```

该 Skill 提供 32 个交易工具的结构化知识，包括：账户信息、市场数据、订单执行、仓位管理、挂单管理、历史查询。

### 4.4 方案B：Codex + MT5（HTTP API 模式）

#### 4.4.1 启动 metatrader-http-server

```powershell
metatrader-http-server --login LOGIN_PLACEHOLDER --password PASSWORD_PLACEHOLDER --server SERVER_PLACEHOLDER --host 127.0.0.1 --port 8000
```

#### 4.4.2 确保 4567 HTTP 代理中继层就绪

代理脚本功能：
- `GET /codex/*` → 转发到 `http://127.0.0.1:57321/*`
- `GET /statistics` → 返回监控面板（JSON）

验证命令：`curl http://127.0.0.1:4567/statistics`

---

## 五、环节四：服务巡检

### 5.1 全端口巡检命令

```powershell
# 一次性检查所有关键端口
@(11434, 15721, 57319, 57320, 57321, 4567, 8000, 8080) | ForEach-Object {
    $conn = Get-NetTCPConnection -LocalPort $_ -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($conn) { "$_ : LISTENING (PID $($conn.OwningProcess))" }
    else { "$_ : NOT LISTENING" }
}
```

### 5.2 服务验证命令

| 服务 | 验证端点 | 预期响应 |
|------|----------|----------|
| Ollama | `curl http://127.0.0.1:11434/api/tags` | JSON 模型列表 |
| CC Switch | `curl http://127.0.0.1:15721/v1/models` | 模型列表 |
| Codex++ | `curl http://127.0.0.1:57321/v1/models` | 模型列表 |
| 4567代理 | `curl http://127.0.0.1:4567/statistics` | 监控面板 JSON |
| MT5 HTTP API | `curl http://127.0.0.1:8000/api/v1/account/info` | 账户信息 JSON |

### 5.3 巡检汇总清单模板

| 序号 | 服务 | PID | 端口 | 状态 | 验证端点 |
|:---:|------|:---:|:---:|:---:|------|
| 1 | Ollama 推理引擎 | — | 11434 | — | `/api/tags` |
| 2 | CC Switch | — | 15721 | — | `/v1/models` |
| 3 | Codex++ | — | 57320/57321 | — | `/v1/models` |
| 4 | Codex++ Manager | — | 57319 | — | TCP LISTENING |
| 5 | 4567 HTTP代理中继 | — | 4567 | — | `/statistics` |
| 6 | MT5 HTTP API | — | 8000 | — | `/api/v1/account/info` |

---

## 六、常见故障排查指南

### 6.1 端口冲突

| 症状 | 根因 | 解决方案 |
|------|------|----------|
| 端口 LISTENING 但进程非预期 | 端口被其他进程占用 | `Get-NetTCPConnection -LocalPort <端口>` 定位占用进程，按需终止 |
| 4567 代理无法启动 | 端口被残留进程占用 | `Stop-Process -Id <PID> -Force` 后重试 |

### 6.2 连接失败

| 症状 | 根因 | 解决方案 |
|------|------|----------|
| MT5 MCP 连接超时 | MT5 终端未运行 | 手动启动 MT5 terminal64.exe |
| "Connection failed" | 算法交易未启用 | MT5 → 工具 → 选项 → EA交易 → 勾选"允许算法交易" |
| "Module not found" | Python 版本 < 3.10 | 升级 Python 到 3.10+ |
| "Order execution failed" | 品种不存在/市场关闭/保证金不足 | 逐一检查：品种可用性、交易时段、账户资金 |

### 6.3 凭证问题

| 症状 | 根因 | 解决方案 |
|------|------|----------|
| 认证失败 | .env 或 CLI 参数凭证错误 | 核对 MT5 账户号、密码、服务器名三要素 |
| .env 未生效 | 文件路径不正确 | 确认 `.env` 在 MT5-MCP-Server 根目录下 |

### 6.4 代理/网络问题

| 症状 | 根因 | 解决方案 |
|------|------|----------|
| 4567 代理无响应 | 中继进程崩溃 | `Get-Process python` 检查，重启 `mt5_proxy_relay.py` |
| Codex 端口不通 | Codex++ 未启动 | 启动 `codex-plus-plus.exe` 和 `codex-plus-plus-manager.exe` |
| ECONNRESET | 系统代理残留 | 执行代理清理 + 网络栈重置（参见 direct-network-recovery-rollback skill） |

### 6.5 MT5 终端路径问题

| 症状 | 根因 | 解决方案 |
|------|------|----------|
| "MT5 terminal not found" | 路径配置错误或非标准安装 | 在 `.env` 中设置 `MT5_PATH` 或 CLI 加 `--path` 参数 |
| terminal64.exe 无法启动 | 文件损坏或权限不足 | 以管理员身份重试，检查文件完整性 |

---

## 七、关联技能

- lobster_task_standard_workflow_v2.3_locked：龙虾五步法核心框架（环境诊断/方案落地/迭代沉淀）
- direct-network-recovery-rollback v1.0：网络栈重置与代理清理（端口问题修复）
- CC-Switch：AI推理调度中心配置管理
- lobster_codex_dual_link_v1.0：Codex 双链路配置

---

## 八、安全注意事项

- 本技能所有示例中的凭证（LOGIN/PASSWORD/SERVER）均为 `PLACEHOLDER`，实际部署时从 `.env` 文件或用户提供获取
- MT5 MCP Server 的 SSE 模式默认无内置认证，暴露到公网时须使用防火墙 IP 白名单或 SSH 隧道
- 交易操作具有风险，所有订单执行由用户自行负责
- 禁止在日志/代码/配置文件中明文落盘真实凭证

---

## 九、版本历史

| 版本 | 日期 | 变更 |
|:---:|------|------|
| v1.0 | 2026-06-29 | 初始版本，基于 ariadng/metatrader-mcp-server v0.5.1 本地部署全流程实践经验提炼 |
*（内容由AI生成，仅供参考）*
