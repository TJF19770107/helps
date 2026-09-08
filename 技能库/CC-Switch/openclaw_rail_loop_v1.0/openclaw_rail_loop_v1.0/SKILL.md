---
name: "openclaw_rail_loop_v1.0"
description: "任务自动循环执行（回测/调参/监控），带步骤上限与白名单动作。Invoke when you need an automated trading loop."
---

# OpenClaw Rail Loop v1.0（Trae）

## 调用方式（统一走 Hermes 网关）

- URL：`http://127.0.0.1:18080/hermes/skill/openclaw_rail_loop`
- 方法：`POST`
- Body：`{ "req": { "objective": "...", "mode": "steps|planner", "max_steps": 10, "steps": [...], "trading": {...} } }`

