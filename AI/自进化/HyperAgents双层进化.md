# HyperAgents 元认知双层进化

> **来源**: Meta FAIR + 腾讯云深度解析, 2026-05
> **豆包关联**: R02深度迭代报告
> **MOC**: [[_MOC_自进化体系]]

---

## 双层Agent架构

```
SuperAgent = TaskAgent + MetaAgent
               ↓            ↓
         解决具体任务    修改系统自身
         (解决问题)      (改进"如何改进")
               ↓            ↓
         同一可编辑程序中整合
```

## 核心机制

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

## RSPL + SEPL 双层协议

- **RSPL (资源基底)**: 五类资源注册 — Prompt/Agent/Tool/Env/Memory
- **SEPL (自进化协议)**: 原子操作保障 — Reflect → Select → Improve → Evaluate → Commit

---

**标签**: #AI/自进化 #HyperAgents #Meta-Agent #Archive #双层架构