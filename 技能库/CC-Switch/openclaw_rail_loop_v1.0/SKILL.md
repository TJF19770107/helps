---
name: "openclaw_rail_loop_v1.0"
description: "实现任务自动循环执行（带步骤上限与量化回测/调参闭环）。Invoke when you need an automated loop: run→evaluate→adjust→repeat."
---

# OpenClaw Rail Loop v1.0

## 能力

- 以“轨道循环”的方式执行一组步骤：调用 VNPY 网关/调用其他技能/等待/记录。
- 支持两种模式：
  - 显式 steps：你给出步骤列表，按序执行并汇总结果。
  - 自主 planner：你给目标与上下文，由模型在 `max_steps` 内选择下一步动作（带白名单动作）。
- 量化场景：批量回测、参数扫描、风控阈值迭代、执行监控轮询。

## 统一入口

- 函数入口：`skill_openclaw_rail_loop(req: dict) -> dict`

## 入参

```json
{
  "objective": "对策略做 10 组参数回测，选最大夏普且回撤<10%",
  "mode": "steps",
  "max_steps": 10,
  "steps": [
    {"type": "vnpy", "cmd": "backtest_run", "params": {"strategy": "MyStrat", "start": "2024-01-01", "end": "2024-06-01"}},
    {"type": "sleep", "seconds": 2},
    {"type": "vnpy", "cmd": "backtest_status", "params": {}}
  ],
  "trading": {"symbols": ["IF9999"], "timeframe": "1m"}
}
```

