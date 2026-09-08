---
name: "openclaw_document_skills_v1.0"
description: "提升技能/模块文档并生成量化用法示例（不自动改文件）。Invoke when you need better docs for skills/endpoints/trading modules."
---

# OpenClaw Document Skills v1.0（Trae）

## 调用方式（统一走 Hermes 网关）

- URL：`http://127.0.0.1:18080/hermes/skill/openclaw_document_skills`
- 方法：`POST`
- Body：`{ "target": { "skill_names": ["..."], "extra_context": "...", "trading": {...} } }`

## 量化参数建议（target.trading）

- symbols/timeframe：用于生成更贴合的示例
- data.start/data.end：用于回测/复盘文档示例

