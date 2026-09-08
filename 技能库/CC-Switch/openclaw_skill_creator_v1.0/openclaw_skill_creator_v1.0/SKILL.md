---
name: "openclaw_skill_creator_v1.0"
description: "将工作流自动转为可复用技能脚手架（不落盘写入）。Invoke when you need to generate a new Hermes/Trae skill scaffold from a workflow."
---

# OpenClaw Skill Creator v1.0（Trae）

## 调用方式（统一走 Hermes 网关）

- URL：`http://127.0.0.1:18080/hermes/skill/openclaw_skill_creator`
- 方法：`POST`
- Body：`{ "spec": { ... } }`

## 量化参数建议（放在 spec.quant_defaults）

- symbols：标的列表（期货/股票/币）
- timeframe：周期（如 1m/5m/1h/1d）
- risk：风险约束（最大仓位、最大回撤、每日最大订单数）

