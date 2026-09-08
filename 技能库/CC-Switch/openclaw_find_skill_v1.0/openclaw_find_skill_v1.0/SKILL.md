---
name: "openclaw_find_skill_v1.0"
description: "精准检索本地技能库并返回匹配项。Invoke when you want to find which skill to use for a trading task."
---

# OpenClaw Find Skill v1.0（Trae）

## 调用方式（统一走 Hermes 网关）

- URL：`http://127.0.0.1:18080/hermes/skill/openclaw_find_skill`
- 方法：`POST`
- Body：`{ "query": { "q": "...", "limit": 10 } }`

