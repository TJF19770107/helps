---
name: "openclaw_find_skill_v1.0"
description: "精准匹配需求并在本仓库的技能库中检索可用技能。Invoke when you want to find the best skill for a task or trading workflow."
---

# OpenClaw Find Skill v1.0

## 能力

- 在 `.hermes/skills` 与 `.trae/skills` 中按关键词检索 `SKILL.md`（名称/描述/正文）。
- 返回匹配技能列表与最短调用方式（Hermes 端点/入口函数）。

## 统一入口

- 函数入口：`skill_openclaw_find_skill(query: dict) -> dict`

## 入参

```json
{
  "q": "回测 循环 参数调优",
  "limit": 10
}
```

