---
name: opc-intelligent-orchestrator
description: 智能化调度：当用户表达一人公司相关意图时，自动识别所处阶段并调用 OPC 庄家团对应专家/技能。
triggers:
  - 一人公司
  - 启动规划
  - 资源盘点
  - 利基定位
  - 商业模式
  - MVP
  - 转化闭环
  - 经营复盘
---

# OPC 智能化调度技能

## 触发识别表

| 用户表达 | 识别阶段 | 调度 |
|----------|----------|------|
| "从零开始" / "启动盘点" / "资源盘点" | 01 | opc-resource-audit |
| "找方向" / "利基" / "定位" | 02 | opc-niche-positioning |
| "价值主张" / "卖点" / "定价" | 03 | opc-value-proposition |
| "商业模式" / "怎么赚钱" / "画布" | 04 | opc-business-model-design |
| "MVP" / "验证" / "原型" | 06 | opc-mvp-designer |
| "获客" / "成交" / "转化" / "私域" | 07 | opc-conversion-loop |
| "资产" / "沉淀" / "复利" | 08 | opc-asset-ops |
| "复盘" / "瓶颈" / "优先级" | 09 | opc-dashboard-review |

## 执行逻辑
1. 读取 `opc-doc/state/current-stage.json`。
2. 匹配用户意图 → 阶段 → skill/expert。
3. 调用对应 skill，产出 Markdown 文件。
4. 更新 `current-stage.json`。
5. 给出下一步建议。

## 约束
- 优先 0 积分路径：复用已有上下文与本地文件。
- 不自动触发云端构建（CNB AI Credits 受控）。
