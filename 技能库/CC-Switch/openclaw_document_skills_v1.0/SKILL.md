---
name: "openclaw_document_skills_v1.0"
description: "提升技能/模块的文档质量并生成量化交易用法示例。Invoke when you need to document a skill, endpoint, or trading module."
---

# OpenClaw Document Skills v1.0

## 能力

- 读取指定技能的 `SKILL.md` 或代码片段，生成更清晰的文档结构与量化用法示例（不自动写回文件）。
- 输出面向“量化交易项目”的参数解释、调用示例、风险提示与验收清单。

## 统一入口

- 函数入口：`skill_openclaw_document_skills(target: dict) -> dict`

## 入参（target）

```json
{
  "skill_names": ["openclaw_rail_loop_v1.0"],
  "extra_context": "我的量化项目是…",
  "trading": {
    "symbols": ["IF9999"],
    "timeframe": "1m"
  }
}
```

