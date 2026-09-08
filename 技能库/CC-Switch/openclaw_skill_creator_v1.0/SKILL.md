---
name: "openclaw_skill_creator_v1.0"
description: "将一次性工作流规范化为可复用技能（输出技能脚手架与端点契约）。Invoke when you want to turn a workflow into a reusable Hermes/Trae skill."
---

# OpenClaw Skill Creator v1.0

## 能力

- 将你的“工作流/流程步骤/输入输出契约”整理成可复用技能的脚手架（不落盘写入，只返回文件内容草案）。
- 输出：Hermes 技能（`.hermes/skills/...`）与 Trae 技能（`.trae/skills/...`）两份 `SKILL.md` 草案，以及 `skill_entry.py` 草案。
- 量化场景：默认带 `trading` 参数约定（标的/周期/风险/数据源/回测范围）。

## 统一入口

- 函数入口：`skill_openclaw_skill_creator(spec: dict) -> dict`

## 入参（spec）

```json
{
  "skill_name": "my_skill_v1.0",
  "description": "一句话描述（包含何时调用）",
  "inputs": [{"name": "param1", "type": "string", "required": true, "desc": "..." }],
  "outputs": [{"name": "result", "type": "object", "desc": "..."}],
  "quant_defaults": {
    "symbols": ["IF9999"],
    "timeframe": "1m",
    "risk": {"max_position_pct": 0.2, "max_drawdown_pct": 0.1}
  }
}
```

## 出参

- `files`: `{path: content}` 的字典，包含 3 个文件草案
- `contract`: 端点与请求体/返回体契约

