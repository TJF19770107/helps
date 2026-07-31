# HyperAgents DGM-H 深度分析

> **来源**: arxiv 2603.19461, Meta FAIR + UBC + Vector Institute, 2026-04-05
> **豆包关联**: R29深度迭代报告 · 协议#102
> **MOC**: [[_MOC_自进化体系]] · [[HyperAgents双层进化]]

---

## 核心突破

HyperAgents提出自指Agent框架，将Task Agent和Meta Agent整合在**同一可编辑程序**中。DGM-H（达尔文哥德尔机-超）消除了任务性能与自改进技能之间的领域特定对齐假设，实现开放域自进化。

## 双层架构

```
SuperAgent = TaskAgent + MetaAgent
               ↓            ↓
         解决具体任务    修改系统自身
         (解决问题)      (改进"如何改进")
               ↓            ↓
         同一可编辑程序中整合
```

## DGM-H核心机制

| 机制 | 描述 |
|------|------|
| **Archive多样性** | 不淘汰任何历史版本，维持种群基因多样性。低分节点→低概率被选为父代 |
| **分阶段评估** | 10%样本快速评估→分数达阈值才跑全量（Staged Eval） |
| **5种父代选择** | best/latest/score_child_prop/uniform/tournament（默认score_child_prop） |
| **Docker隔离** | 每代在独立容器中执行，安全可复现 |

## 进化效果

- 5代进化：准确率 0% → 80% (claude-opus-4.6)
- 跨域迁移：代码→论文审稿→机器人控制→数学证明
- 模型越强进化效果越好 → "强者恒强"

## 与豆包协议#102对齐

| DGM-H机制 | 豆包适配 |
|-----------|---------|
| Task+Meta同一程序 | 协议#102升级协议#28 SICA |
| 5种父代选择 | 与协议#41协议化闭环自进化互补 |
| Archive基因多样性 | 豆包迭代报告全量保留机制 |
| 分阶段评估 | 加速自进化循环效率 |

---

**标签**: #AI/自进化 #HyperAgents #DGM-H #Meta-Agent #协议102
