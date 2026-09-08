---
name: "lobster_tripartite_frontend_chat_v1.0"
description: "三方前台群聊窗口与消息互通验收（豆包↔Bridge↔Trae↔Hermes）。Invoke when 需要肉眼可见地验证三方消息收发闭环或排查断片/不回传。"
---

# 三方前台群聊窗口（v1.0）

## 能力范围

- 启动 Trae 前台可见“群聊窗口”（HTTP + 页面），用于肉眼验证消息收发。
- 让 doubao_bridge 在收到 webhook 后把消息推送到群聊窗口并获取 Trae 自动回复，再把回复回填给豆包（通过 webhook response）。
- Hermes 作为执行/可视化节点：Bridge 会异步触发 Hermes `/v1/runs`，保证 Hermes WebUI 可见链路事件。

## 固定端口

- 群聊窗口：`http://127.0.0.1:18092/`
- Bridge 监控：`http://127.0.0.1:18091/monitor`
- Hermes WebUI：`http://127.0.0.1:6060/`

## 必要配置（docker-compose.lobster.yml）

- `TRAE_INBOX_ENABLE=1`
- `TRAE_INBOX_URL=http://host.docker.internal:18092/inbox`
- `TRAE_INBOX_TIMEOUT_S=3`

## 启动

```powershell
python .\scripts\trae_groupchat_server.py
```

## 一键验收（本地模拟 webhook，避免泄露 trigger token）

```powershell
python -u .\scripts\test_frontend_chain.py
```

验收通过标准：
- `test_frontend_chain.py` 输出 `OK: reply_from_trae_inbox=YES`
- 群聊窗口页面出现两行：`doubao:` 入站 + `Trae:` 自动回复
- Bridge 监控页出现 `bridge.webhook.recv` 与 `bridge.webhook.trae_reply`

