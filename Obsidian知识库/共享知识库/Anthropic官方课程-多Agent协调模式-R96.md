---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_10a50361688411f1a0095254002afed2
    ReservedCode1: ELnp/rghJigZHzUn9DEdquEpjx8L9yApTzhDUhIr5oNWwob8vWNNfRtPy2VtxfvMZTlCFzfsF4Zw3dHgatKote0LUfFeZV8snPzje3so/XsO7MQU6XMgT3LiFbtc/XUcegUMICFw9sSpEfvR57LuDkmWZdoKAk02GSgtgzqiLdjtbEbzY8L8+uJS2RQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_10a50361688411f1a0095254002afed2
    ReservedCode2: ELnp/rghJigZHzUn9DEdquEpjx8L9yApTzhDUhIr5oNWwob8vWNNfRtPy2VtxfvMZTlCFzfsF4Zw3dHgatKote0LUfFeZV8snPzje3so/XsO7MQU6XMgT3LiFbtc/XUcegUMICFw9sSpEfvR57LuDkmWZdoKAk02GSgtgzqiLdjtbEbzY8L8+uJS2RQ=
---

# Anthropic 官方课程 — 多Agent协调模式全集

> 来源：Anthropic 官方博客 (claude.com/blog) + 公开文档提炼
> 更新：2026-06-15 R96 第46轮学习循环 | 对标 Anthropic Academy 390节课程体系

---

## 一、前言：何时使用多Agent系统

多Agent系统的价值在于**上下文隔离**和**专业化分工**。当单Agent的上下文窗口不足以承载所有所需信息时，或当任务天然可分解为独立子域时，多Agent才有真正价值。

**核心原则**：从最简单可行的模式开始，观察它在哪里挣扎，然后演进。不要因为"听起来更高级"而选择复杂模式。

---

## 二、五种多Agent协调模式

### 模式 1: Generator-Verifier（生成器-验证器）

**结构**：Generator → Verifier → 通过/打回（循环至收敛）

**工作机制**：
1. Generator 接收任务并生成初始输出
2. Verifier 按明确标准评估输出
3. 通过 → 输出；未通过 → 带反馈打回 Generator
4. 重复至收敛或达最大迭代次数

**适用场景**：
- 客服邮件回复（准确度 + 品牌语调检查）
- 代码生成（一个写代码，一个写并运行测试）
- 事实核查、评分、合规验证
- 任何错误输出成本高于额外生成周期的领域

**关键约束**：
- 验证者仅如其标准——模糊的验证标准会沦为橡皮图章
- 生成与验证必须是可分离的技能
- 需要最大迭代次数 + 兜底策略（人工升级 / 带警告返回最佳尝试）

### 模式 2: Orchestrator-Subagent（编排器-子代理）

**结构**：Orchestrator 规划 → 分派 → 汇总 → 呈现

**工作机制**：
1. 编排器接收任务，确定分解方案
2. 编排器可直接处理部分子任务，其余分派给子代理
3. 子代理完成工作返回结果，编排器合成最终输出

**实际案例 — Claude Code**：主 Agent 自己编写代码、编辑文件、运行命令；同时在后台分派子代理搜索大型代码库或研究独立问题。每个子代理在自己的上下文窗口中运行并返回精炼发现，保持编排器上下文聚焦主要任务。

**适用场景**：
- 代码审查系统（安全检查/测试覆盖率/代码风格/架构一致性 → 4个子代理并行）
- 任何任务分解清晰、子任务相互依赖度低的场景

**局限性**：
- 编排器成为信息瓶颈——跨子代理的关键信息易在传递中丢失
- 串行执行限缩吞吐量（除非显式并行化）

### 模式 3: Agent Teams（Agent团队）

**结构**：Coordinator 派发 → Workers 自主多步执行 → 持久化上下文

**与 Orchestrator-Subagent 的关键区别**：
- Subagent 执行一个有限子任务后即终止
- Teammate 跨多次分配存活，积累上下文和领域专业化

**工作机制**：
1. Coordinator 生成多个 Worker Agent 作为独立进程
2. Teammates 从共享队列认领任务，自主多步执行
3. 完成后发信号，不重置

**适用场景**：
- 大规模代码迁移（每个服务独立迁移，积累依赖图谱/测试模式/部署配置）
- 子任务独立且受益于持续多步工作的场景

**局限性**：
- 独立性是关键要求——队友间无法轻易共享中间发现
- 完成检测困难（一个2分钟，另一个20分钟）
- 共享资源冲突（代码库/数据库/文件系统并发修改）

### 模式 4: Message Bus（消息总线）

**结构**：Agents 通过 Publish/Subscribe 通信，Router 投递

**工作机制**：
- Agents 通过两个原语交互：publish 和 subscribe
- Router 将匹配消息投递给订阅者
- 新 Agent 接入无需修改现有连接

**适用场景**：
- 安全运营自动化（告警流入 → 分类 → 路由 → 调查 → 响应协调）
- 事件驱动管道 + 工作流从事件中涌现
- Agent 生态系统预期增长

**局限性**：
- 事件驱动通信的灵活性使追踪困难（5个Agent级联事件→需要精细日志和关联）
- LLM路由器的语义灵活性带来自身的失败模式
- 路由失败时系统静默失效（不处理但也不崩溃）

### 模式 5: Shared State（共享状态）

**结构**：所有 Agent 直接读写共享持久存储，无中央协调器

**工作机制**：
- Agents 自主运行，从共享数据库/文件系统/文档读写
- 无中央协调器——Agent 自行检查存储中的相关信息
- 初始化步骤向存储写入问题/数据集，终止条件触发结束

**适用场景**：
- 研究综合系统（学术文献/行业报告/专利/新闻 → 多Agent各自调查不同侧面）
- 发现可直接写入存储，无需等待协调器路由
- 消除协调器作为单点故障

**局限性**：
- 无协调 → 可能重复工作或产生矛盾方向
- **反应式循环**是更难的失败模式：Agent A写→Agent B读+写跟进→Agent A看跟进+回应→系统燃烧token不收敛
- 需要一等终止条件（时间预算/收敛阈值/N轮无新发现/指定Agent判定）

---

## 三、模式选择决策树

### 结构性问题驱动选择

| 问题 | 答案 → 推荐模式 |
|------|----------------|
| 输出质量关键且有明确评估标准？ | 是 → Generator-Verifier |
| 任务分解清晰、子任务短且无依赖？ | 是 → Orchestrator-Subagent |
| 子任务需要持久化上下文、多步自主执行？ | 是 → Agent Teams |
| 工作流不可预测、Agent生态预期增长？ | 是 → Message Bus |
| 需要Agent相互发现并构建、消除单点故障？ | 是 → Shared State |

### 模式间对比

| 对比 | 选择指南 |
|------|---------|
| Orchestrator-Subagent vs Agent Teams | 子任务短且聚焦→Orchestrator；需持续多步+积累上下文→Teams |
| Orchestrator-Subagent vs Message Bus | 步骤序列可预知→Orchestrator；从事件涌现+不可预知→Message Bus |
| Agent Teams vs Shared State | 工作独立→Teams；需相互发现和构建→Shared State |
| Generator-Verifier vs 其他 | 仅在输出质量>速度时使用；是其他模式的附加层 |

---

## 四、六大破裂模式（引自 Anthropic 上下文工程）

| 破裂模式 | 症状 | 修复 |
|---------|------|------|
| Context Overflow | Agent 忽略早期指令 | Progressive Disclosure |
| Permission Creep | Agent 执行非预期操作 | 最小足迹 + 信任验证 |
| Tool Abuse | 不必要的工具调用链 | 工具使用审计 Hooks |
| Hallucination Cascade | 多 Agent 链式错误传播 | 先读后写 + Checkpoint |
| Infinite Loop | Agent 重复相同操作 | 停止条件 + 轮次上限 |
| Shadow Dependency | 隐性依赖外部服务 | MCP 健康检查 + 降级 |

---

## 五、Claude Code OS 四支柱

| 支柱 | 功能 | 龙虾映射 |
|------|------|---------|
| Skills | 长期记忆（领域指令注入） | 技能库 + 协议库 |
| Hooks | 条件反射（关键节点自动触发） | SafeGuard 安全钩子 |
| MCP | 实时感知（外部工具/数据源） | 工具网关 |
| Subagents | 并行执行（上下文隔离） | dispatch_task 多Agent |

---

## 六、上下文中心分解法

Anthropic 推荐按**上下文需求**而非任务类型分解工作。核心问题：每个 Agent 需要什么上下文才能完成工作？

- 同上下文 → 单Agent直接处理
- 不同上下文 → 考虑多Agent分解
- 上下文重叠 → 评估去重vs冗余成本

---

## 七、停止条件设计

每个多Agent系统必须有显式终止条件：

| 场景 | 终止条件示例 |
|------|------------|
| Generator-Verifier | 最大迭代次数 + 人工升级 |
| Orchestrator-Subagent | 所有子代理返回 + 编排器合成完成 |
| Agent Teams | 任务队列清空 + 所有队友完成信号 |
| Message Bus | 时间预算 / 收敛阈值 / 终端Agent判定 |
| Shared State | 时间预算 / N轮无新发现 / 指定关闭Agent |

---

> 设计哲学：选择模式的正确问题是"这个系统应该是什么样的"，而不是"我们应该用什么听起来高级的模式"。
> 来源：Anthropic Official Blog — Multi-agent coordination patterns: Five approaches and when to use them (2026-04-10)
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
