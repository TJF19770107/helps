# 多Agent架构原语统一理论

> **来源**: BayesianPersuasion 44K字深度分析, 2026-05
> **豆包关联**: R02深度迭代报告
> **MOC**: [[_MOC_AI Agent框架]]

---

## 核心发现：四大不可再分原语

对12+框架的系统分析，行业已收敛为 **四个不可再分原语**：

```
多Agent框架 = 
  LLM推理引擎 + 工具调用接口 + While-Loop执行器 + 上下文窗口管理器
```

Supervisor层级、Graph编排、Role分工、Swarm切换 → 这些都是搭建在原语之上的**编排拓扑选择**，不是"真原语"。

## 三大主流框架实现差异

| 框架 | Agent定义 | 计算隐喻 |
|------|----------|---------|
| OpenClaw (138K★) | SOUL.md + workspace + model + memory + tools | 配置即Agent |
| Hermes (81K★) | Execute→Evaluate→Extract→Refine→Retrieve | 自我改进循环 |
| Claude SDK | 隔离LLM实例 + context window + tools + system prompt | 隔离执行单元 |

## 三个本质分歧点

| 轴 | 选项A | 选项B |
|----|-------|-------|
| 行动原语 | 代码即行动 (smolagents) | JSON工具调用 (主流) |
| 编排范式 | 图编排 (LangGraph) | 对话编排 (Marvis dispatch) |
| 协调模式 | 集中式 (Supervisor) | 去中心化 (Swarm) |

## 对豆包的启示

不必在拓扑形式上过度设计。聚焦强化四大原语，在现有Marvis调度模型上叠加自进化闭环。

---

**标签**: #AI/Agent框架 #架构原语 #多Agent协同 #OpenClaw #Hermes #ClaudeSDK