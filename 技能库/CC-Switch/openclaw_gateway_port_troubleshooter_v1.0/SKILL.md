---
name: "openclaw_gateway_port_troubleshooter_v1.0"
description: "Diagnoses OpenClaw/ClawX multi-gateway port mismatches and fixes dashboard connection issues. Invoke when gateway port shows wrong value, 1006 close, or /client/id connect-param errors."
---

# OpenClaw 网关端口识别与连接故障排查（v1.0）

## 适用场景

- ClawX 显示的网关端口与预期不一致（例如显示 18789，但你配置了 18791）。
- 仪表盘/网页连接失败：WebSocket `1006`、`unauthorized`、或报 `invalid connect params: /client/id must be equal to constant`。
- 本机同时存在两类网关：
  - ClawX 自带网关（由 ClawX 进程托管，端口由 ClawX 自己的 settings 控制）
  - 独立 OpenClaw（openclaw-cn）网关（由 openclaw 服务/计划任务/手动命令托管，端口由 openclaw.json + 服务参数控制）

## 核心结论（先定性）

- “网页/仪表盘 UI”和“网关实现”必须匹配；不要用 A 网关的 UI 去连 B 网关的 WebSocket。
- 你看到的端口“错位”通常不是网关没改，而是：
  - 你改了 openclaw.json，但 ClawX 仍按自己的 settings 运行；
  - 或者服务参数（--port）覆盖了 openclaw.json；
  - 或者网关 token/连接参数不匹配导致 1006/401/unauthorized。

## 一键定位（端口→进程）

在 PowerShell 执行（按需改端口列表）：

```powershell
$ports=18789,18790,18791,18792,18793; foreach($p in $ports){ $con=Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue; if(-not $con){ "PORT ${p}: FREE"; continue }; $ownerPid=$con[0].OwningProcess; $proc=Get-Process -Id $ownerPid -ErrorAction SilentlyContinue; $name=if($proc){$proc.ProcessName}else{"<unknown>"}; "PORT ${p}: PID ${ownerPid} (${name})" }
```

判读：
- PID/进程名是 `ClawX`：端口由 ClawX 控制（改 openclaw.json 不会改变 ClawX 显示的端口）。
- PID/进程名是 `node`：多半是 openclaw-cn 网关或其派生服务（浏览器控制/画布等）。

## 配置源对照（ClawX vs openclaw）

### 1) ClawX 的网关配置源

文件（Windows）：
- `%APPDATA%\\clawx\\settings.json`

关键字段：
- `gatewayPort`
- `gatewayAutoStart`
- `gatewayToken`（不要在日志/文档中打印明文）

快速读取（不输出 token）：

```powershell
$p="$env:APPDATA\\clawx\\settings.json"; $j=Get-Content $p -Raw|ConvertFrom-Json; "gatewayPort=$($j.gatewayPort)"; "gatewayAutoStart=$($j.gatewayAutoStart)"
```

### 2) openclaw-cn 的网关配置源

配置文件：
- `~\\.openclaw\\openclaw.json`

服务状态（会显示服务参数与探测信息）：

```powershell
openclaw gateway status
```

关键判读点：
- `Service env: OPENCLAW_GATEWAY_PORT=...` / `Command: ... --port ...`：服务参数可能覆盖配置文件。
- `Config (cli)` vs `Config (service)`：CLI 读取与服务读取可能不一致（例如 token 依赖环境变量时）。

## 典型故障与修复路径

### A. UI 端口与 WS 端口不一致（最常见）

症状：
- 你在浏览器打开的是 `http://127.0.0.1:18789/...`，但 WS 填 `ws://127.0.0.1:18791`，随后出现 `/client/id` 或 1006。

修复：
- 让 UI 和网关同源：
  - 如果目标网关是 18789：UI 也打开 18789，并用 `ws://127.0.0.1:18789`
  - 如果目标网关是 18791：UI 打开 18791，并用 `ws://127.0.0.1:18791`

### B. 1006 / unauthorized（token 不匹配）

症状：
- 网关监听正常，但连接被拒绝：`unauthorized` / `token mismatch` / `1006`。

修复要点：
- 确保“客户端使用的 token”和“网关要求的 token”一致。
- 不要在文档/日志里记录 token 明文；只做“是否已设置/是否一致”的检查。

### C. openclaw.json 使用了 ${OPENCLAW_GATEWAY_TOKEN} 导致 CLI/服务读取失败

症状：
- `MissingEnvVarError: OPENCLAW_GATEWAY_TOKEN`，导致 CLI 不能读配置、状态判断混乱。

修复：
- 方案 1：在启动服务/命令前设置环境变量 `OPENCLAW_GATEWAY_TOKEN`（仅在当前会话生效）。
- 方案 2：把 token 写入 openclaw.json（不推荐在多人/共享环境明文保存）。

## 端口段隔离建议（避免冲突）

推荐将不同系统服务分配到不同“连续端口段”，并为 OpenClaw 预留派生端口：

- Hermes：18080
- Doubao：18000
- WeChat：8092
- Ollama：11434
- OpenClaw 网关主端口：18791
- OpenClaw 可能派生端口：18792-18795（例如 browser control、canvas 等）

当你调整 OpenClaw 主端口时，务必同时检查其派生端口是否被占用。

