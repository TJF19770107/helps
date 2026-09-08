---
name: "openclaw_gateway_quick_fix_v1.0"
description: "Quickly fixes OpenClaw gateway port conflicts and 1006 connection failures. Invoke when you need to force port 18791, align service/cli/dashboard, and verify via status/logs."
---

# OpenClaw 网关端口快速修复（v1.0）

## 目标

- 强制将 OpenClaw 网关统一到 `18791`。
- 保证 `service 端口 == cli 端口 == 仪表盘填写端口`。
- 解决常见连接失败：`1006`、`EADDRINUSE`、`/client/id connect params`。

## Step 0：先读结论（避免走弯路）

- 端口冲突的根因通常是 **ClawX 自带网关**抢占端口（ClawX 进程监听），导致 openclaw-cn 网关无法启动或探测失败。
- `/client/id must be equal to constant` 大概率是 **UI 页面端口与 WS 端口不一致**（用 A 网关 UI 连 B 网关 WS）。

## Step 1：强制查清真实端口（service vs cli vs dashboard）

```powershell
openclaw gateway status
```

必须确认输出里：
- `Gateway: ... port=18791`
- `Listening: 127.0.0.1:18791`
- `RPC 探测: 正常`

## Step 2：关闭冲突端口（18789/18791）

```powershell
$ports=18789,18791; foreach($p in $ports){ $con=Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue; if($con){ Stop-Process -Id $con[0].OwningProcess -Force -ErrorAction SilentlyContinue; \"killed listener on $p\" } else { \"free $p\" } }
```

若你需要确保 ClawX 不抢回端口（强制）：

```powershell
taskkill /F /IM ClawX.exe /T
```

## Step 3：强制统一端口为 18791（干净不冲突）

```powershell
openclaw doctor --fix
openclaw config set gateway.port 18791 --json
openclaw config set gateway.mode local
openclaw config set gateway.bind loopback
openclaw config set gateway.controlUi.enabled true --json
```

## Step 4：彻底重启网关服务

```powershell
openclaw gateway stop
openclaw gateway start
```

## Step 5：仪表盘只填一个地址（同源原则）

- 仪表盘页面：`http://127.0.0.1:18791/`
- WebSocket：`ws://127.0.0.1:18791`

注意：不要用 `18789` 页面去连 `18791` 的 WS（会触发 `/client/id` 之类错误）。

## Step 6：查日志确认（必须看到 listening）

```powershell
openclaw logs --limit 30 --plain
```

必须出现类似：
- `listening on ws://127.0.0.1:18791`
- 无 `EADDRINUSE`

## 安全提醒

- 网关 token 不要写入共享文档/日志；只在本机 UI 内粘贴或通过官方命令自动注入。

