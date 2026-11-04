---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_adabb7aa684011f1a0095254002afed2
    ReservedCode1: zctBExwHzFH46QrgnbsVzqmM+LkbdgVhlqLPDz+G/M/mnIHeFxzvYa9Kcme88duFSTSQDrDAZS1I82P78Oi/vl0ivW6NQ2pkIYGKQuC9uxZXpigGw6QxY0HHIM/XQFJT13fm5herGjuoup3OqpKdHY7e19kxC4QuSuT6MAAk7HZQp2Y5NTY0f4JGm7I=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_adabb7aa684011f1a0095254002afed2
    ReservedCode2: zctBExwHzFH46QrgnbsVzqmM+LkbdgVhlqLPDz+G/M/mnIHeFxzvYa9Kcme88duFSTSQDrDAZS1I82P78Oi/vl0ivW6NQ2pkIYGKQuC9uxZXpigGw6QxY0HHIM/XQFJT13fm5herGjuoup3OqpKdHY7e19kxC4QuSuT6MAAk7HZQp2Y5NTY0f4JGm7I=
---

# SOUL.md — AI Agent 设计原则

> 来源：Anthropic 官方课程 + 六大 Agentic 模式 + Context Engineering + 生产级实践
> 版本：v1.0 | 创建日期：2026-06-15

---

## 一、核心哲学：从简单开始

### 1.1 复杂度阶梯原则

Anthropic 的现场数据表明：**最成功的生产部署使用简单、可组合的模式，仅在单 Agent 明显达到极限时才使用多 Agent 编排。**

```
Augmented LLM → Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer
  (基础)          (顺序)          (分类)      (并行)            (编排-工人)            (评估-优化)
```

**每次升级前问自己**：当前模式的瓶颈是否已**不可忽视**？如果没有，不要增加复杂度。

### 1.2 Workflow vs Agent 根本区分

| | Workflow | Agent |
|---|---|---|
| **本质** | LLM + 工具遵循预定义代码路径 | LLM 动态自主指导自身过程 |
| **价值** | 可预测性 | 适应性 |
| **生产建议** | 大多数系统受益于 Workflow | 仅在需要真正动态决策时使用 |

> "一分钟的计划，能省下十分钟的构建时间。" — Claude Code Plan Mode 设计哲学

---

## 二、六大 Agentic 模式详解

### 2.1 Augmented LLM（增强 LLM）

**层级**：最基础。**覆盖场景**：摘要、分类、结构化提取。

核心组件：单个 LLM + 检索增强 + 工具访问 + 记忆系统。这个模式已能覆盖大多数生产用例。

### 2.2 Prompt Chaining（提示链）

**层级**：顺序调用。**覆盖场景**：生成→审查→格式化。

每步处理上一步输出，步骤间设可选验证门。每个步骤可独立测试和调试。

### 2.3 Routing（路由）

**层级**：分类分发。**覆盖场景**：客服系统。

分类器将输入根据类型/意图路由到专用处理器。路由器通常为轻量 LLM 调用或传统分类器。

### 2.4 Parallelization（并行化）

**层级**：并行处理。**覆盖场景**：多文档分析、候选生成、并行评估投票。

两种形式：
- **Sectioning**：不同输入切片并行处理
- **Voting**：生成独立输出后聚合

### 2.5 Orchestrator-Workers（编排-工人）

**层级**：第一个真正 Agentic 的模式。**覆盖场景**：多文件重构、跨源研究合成。

中央 LLM 动态分解任务并委派给 Worker LLM。这是**第一个运行时做出任务分解决策的模式**。

### 2.6 Evaluator-Optimizer（评估-优化）

**层级**：反馈循环。**覆盖场景**：代码生成+测试验证、翻译+质量评分。

一个 LLM 生成输出，另一个根据定义标准评估，迭代至质量阈值。当存在清晰评估标准和迭代改进可产生可测量提升时最有效。

---

## 三、上下文工程：从提示到系统

### 3.1 范式转变

**上下文工程 = 构建动态系统，在正确的时间以正确的格式向模型提供正确的信息。**

Agent 输出质量不再取决于提示的巧妙程度，而取决于上下文窗口中有多少有效信息被正确组织。

### 3.2 工具设计四项原则

| 原则 | 实施 |
|------|------|
| **格式匹配** | 工具描述应与模型调用方式一致（参数类型、返回形状、失败模式） |
| **错误结构化** | 内置验证，返回模型可推理的结构化错误 |
| **最小表面积** | 每个工具只做一件事 |
| **模型犯错预案** | 经验验证不同输入下模型的选择和参数化 |

### 3.3 上下文窗口管理

| 策略 | 触发条件 |
|------|---------|
| 早期频繁摘要 | 冗长中间结果产生后 |
| 选择性检索 | 仅拉取最相关文档 |
| 滑动窗口 | 长期任务中固定近期历史 |
| 硬 Token 预算 | 为每段上下文定义最大分配 |

### 3.4 多 Agent 上下文隔离

**每个 Agent 操作自己的上下文窗口**，仅接收与其任务相关的信息。编排器管理 Agent 间信息流，过滤并摘要输出再传递。此模式降低幻觉风险，使单个 Agent 行为更可预测和可测试。

---

## 四、设计韧性：破裂模式与防御

### 4.1 可靠性衰减法则

**每步 99% 成功率的 10 步流水线，端到端可靠性仅 90.4%。每步 95% 时，降至 59.9%。**

### 4.2 六大破裂模式

| 模式 | 防御 |
|------|------|
| 无限循环 | 迭代上限 + 超时门 + 成本断路器 |
| 上下文溢出 | 早期摘要 + 滑动窗口 + Token 预算 |
| 工具调用级联 | 工具输出验证 + 回滚 + 死信队列 |
| 幻觉工具名 | 调用前验证 Schema + 结构化错误返回 |
| 歧义放大 | 流水线早期设澄清门 |
| 状态漂移 | 定期重新锚定原始目标 |

### 4.3 代理记忆隔离

Subagent 持久记忆物理隔离：
- `memory: user` → `~/.claude/agent-memory/<name>/`
- `memory: project` → `.claude/agent-memory/<name>/`
- 防止跨项目信息泄露

---

## 五、Subagent 设计规范

### 5.1 定义结构（YAML Frontmatter）

```yaml
---
name: security-reviewer
description: 审查代码安全漏洞，专注认证、注入、权限三类风险
tools: Read, Grep, Glob
model: sonnet
memory: project
permissionMode: acceptEdits
maxTurns: 25
---
```

### 5.2 关键设计约束

- **有限嵌套（v2.1.172 更新）**：Subagent 可派生子 Subagent，实际最多 2 层。Plan Mode 下仍禁止嵌套以防无限循环。需 Agent 工具权限才可委派。嵌套增加 Token 消耗，仅在单层无法满足时才使用。
- **工具级隔离**：白名单 `tools` 或黑名单 `disallowedTools` 精确限制
- **权限分层**：六档权限（plan 至 bypassPermissions），企业默认 acceptEdits
- **Hooks 前置拦截**：PreToolUse Hook 执行前校验脚本

### 5.3 成本管控

| 手段 | 效果 |
|------|------|
| 轻量任务指定 `model: haiku` | 降低单价 |
| 工具白名单缩小操作范围 | 减少工具定义 Token |
| 合理设置 `maxTurns` | 防止失控循环 |

---

## 六、Agent Teams 实验性架构

### 6.1 核心机制

- 多个 Claude Code 实例并行工作
- 各自独立上下文
- 通过共享任务列表自我协调
- **Mailbox 系统**：Peer 间直接 P2P 通信，无需 Lead 中转

### 6.2 当前状态

**实验性功能**（需手动 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 开启），不推荐生产环境。已知限制：任务状态滞后、无法恢复会话。稳定性关键路径继续使用 Subagent。

### 6.3 Git Worktrees 必备

```bash
git worktree add ../project-agent-a feature/agent-a
git worktree add ../project-agent-b feature/agent-b
git merge feature/agent-b  # 完成后合并最佳版本
```

---

## 七、Dynamic Workflows 编排引擎

### 7.1 何时使用

当任务需要的 Agent 超过一个会话能协调的数量，或希望编排被编写为可阅读和重运行的脚本时。

### 7.2 核心能力

- 最多 16 并发 Agent，单次运行最多 1000 Agent
- 脚本持有循环、分支、中间结果
- Claude 上下文仅接收最终答案
- 可保存为 `/command` 复用

---

## 八、插件体系六组件

```
my-plugin/
├── .claude-plugin/plugin.json
├── commands/       → 斜杠命令
├── agents/         → 专用子代理
├── skills/         → 技能
├── hooks/          → 事件处理器
├── .mcp.json       → MCP 配置
└── README.md
```

### 8.1 Hooks 四事件

| 事件 | 触发时机 |
|------|---------|
| PreToolUse | 工具调用前（可阻止） |
| PostToolUse | 工具执行后 |
| SessionStart | 会话开始时 |
| SessionEnd | 会话结束时 |

### 8.2 Skills vs Hooks

| 维度 | Skills | Hooks |
|------|--------|-------|
| 本质 | 程序性知识（应该遵循） | 确定性动作（必须执行） |
| Token 成本 | 30-50 tokens/技能 | 极低 |
| 触发 | 上下匹配自动加载 | 事件无条件触发 |

---

## 九、Agent 可观测性五维支柱

1. **推理追踪**：每步思维链+动作+观察 → Agent 版 Stack Trace
2. **工具分析**：每个工具成功率/延迟/错误分布
3. **Token 消费**：每任务/步/Agent Token 用量 + 异常告警
4. **任务完成**：完成率 + 步数 + 人工干预次数
5. **漂移检测**：跨运行质量/推理/工具使用变化

### 核心指标

| 指标 | 目标 |
|------|------|
| 任务完成率 | 追踪趋势防回归 |
| 步效率 | 实际步数÷最小步数 |
| 工具成功率 | 识别工具设计问题 |
| 完成时间 | 追踪百分位而非均值 |

---

> **SOUL.md v1.0 完成** | 基于 Anthropic 官方课程 + 六大 Agentic 模式 + Context Engineering + 生产级最佳实践
> 下次更新将补充 CodeSignal 认证路线和 Partner Network Learning Path 相关内容
*（内容由AI生成，仅供参考）*

---

## Anthropic 官方课程·R86 更新 (2026-06-15)

### 新增：CCA 认证级别AI Agent设计原则

#### 1. 子代理架构五项铁律
1. **单一职责** — 每个 sub-agent 仅处理一类任务，description 决定 Claude 何时委托
2. **最小权限** — 仅授予子代理完成工作所必需的工具（通过 tools/disallowedTools 字段）
3. **分层模型策略** — 探索任务用 Haiku（低成本），复杂推理用 Sonnet/Opus
4. **隔离性设计** — 需修改代码的子代理使用 isolation: worktree 获得独立工作副本
5. **上下文预算管理** — 搜索结果/日志等探索数据留在子代理上下文，仅摘要返回主对话

#### 2. Agentic 架构的 24 个生命周期钩子
Claude Code 现已支持 24 个 Hook 事件（较 v1.0 的 18 个新增 6 个）：
- 新增：PermissionDenied（审计日志）、FileChanged（文件监控）、ConfigChange（配置变更检测）
- 新增：WorktreeCreate/Remove（隔离环境管理）、PreCompact/PostCompact（压缩控制）
- 新增：Elicitation/ElicitationResult（MCP 交互式请求-响应）
- 五种执行类型：command / http / mcp_tool / prompt / agent

#### 3. 四位一体扩展哲学
`
Skills（会什么）→ Hooks（何时做）→ MCP（连什么）→ Plugins（如何分享）
`
- 每层独立演化，但组合产生协同效应
- Skills 是知识编码，Hooks 是自动化触发，MCP 是能力扩展，Plugins 是生态分发
- 设计原则：先编码知识（Skills）→ 再自动化规则（Hooks）→ 然后连接工具（MCP）→ 最后打包分发（Plugins）

#### 4. CCA 五域能力矩阵更新
| 域 | 权重 | 本次课程新补充 |
|----|------|---------------|
| D1 Agentic Architecture & Orchestration | 27% | Agent Teams 动态生成 + 共享任务列表 + 队友间通信 |
| D2 Tool Design & MCP Integration | 18% | Elicitation 协议 + MCP server scoping to sub-agents |
| D3 Claude Code Configuration & Workflows | 20% | managed-settings.d/ 分层策略 + --bare 模式 |
| D4 Prompt Engineering & Structured Output | 20% | Skills 系统提示设计 + paths 限定 + compaction 行为 |
| D5 Context Management & Reliability | 15% | 1M-token Opus + 努力级别 + Auto Mode 分类器 |

#### 5. 2026 三项突破性能力
- **Plugins 插件市场**：技能可发现、可安装、可共享的生态化分发
- **Agent SDK**：Python/TypeScript 程序化 API，将 Claude Code 嵌入 CI/CD 管道
- **Computer Use**：桌面 GUI 直接控制，按应用审批的安全模型

---

## Anthropic 官方 Agent 设计原则

> 来源：Anthropic Engineering Blog (2026.06)
> 更新：2026-06-15

### 复杂度阶梯
单次LLM调用 → 增强型LLM → Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer → 自主Agent
**核心原则：仅在简单方案不足时才增加复杂度。**

### 六大Agentic模式
| 模式 | 场景 |
|------|------|
| Prompt Chaining | 固定步骤分解 |
| Routing | 多类型分类 |
| Parallelization | 无依赖并行 |
| Orchestrator-Workers | 动态分解 |
| Evaluator-Optimizer | 迭代评估 |
| Autonomous Agent | 开放问题 |

### 上下文工程五大维度
选择 → 结构化 → 排序 → 压缩 → 时机

### Skills三层设计
L1(描述) → L2(SKILL.md) → L3+(引用文件) — 渐进式信息披露

### 韧性五原则
错误隔离 · 状态恢复 · 护栏优先 · 可观测性 · 渐进授权


---

## Anthropic 2026 Agent 设计原则（R89轮 · 2026-06-17）

> **来源**：Anthropic 官方最佳实践指南（code.claude.com/docs/en/best-practices）+ "A harness for every task"官方博客 + therouter.ai 上下文管理权威解读
> **新增原则**：上下文窗口首要资源 / Explore-Plan-Code三阶段 / 验证与执行分离 / 动态工作流优于静态流水线 / 五层栈组合 / Hooks护栏

---

### 原则一：上下文窗口是首要资源

**这是 Anthropic 官方指南明确的首要约束**：上下文窗口填满速度快，LLM 性能随窗口填充而下降。编码 Agent 的 Token 消耗量是对话的 3-10 倍。

- 每次文件读取、每条命令输出都消耗上下文
- 持续追踪上下文使用量（建议自定义状态栏实时显示）
- 设计 **Context Budget 机制**：为每类操作定义最大 Token 分配
- 压缩策略：早期频繁摘要 + 选择性检索 + 滑动窗口 + 硬 Token 预算
- 核心公式：决定团队 AI 成本模型的不是模型选择，而是单次 Agent 会话实际燃烧的 Token 数

### 原则二：Explore-Plan-Code 三阶段

1. **Explore**：先用 Explore agent（Haiku，低 Token 成本）探索代码库，将搜索结果留在子代理上下文，仅摘要返回主对话
2. **Plan**：基于探索结果制定方案，在 Plan Mode 下运行（只读，防止无限嵌套）
3. **Code**：用 general-purpose agent（Sonnet）执行实现

**设计依据**：避免分析过程污染主会话上下文。探索阶段的高噪声结果（文件路径、grep 输出等）不进入主对话窗，仅结构化摘要返回。

### 原则三：验证与执行分离

**对抗验证（Adversarial Verification）**是实现此原则的结构性手段：
- 产出 Agent 和验证 Agent **必须不同**——不能自己检查自己
- 每个子代理的产出交由另一个独立子代理按标准做对抗性验证
- 这从架构层面消除了自偏好偏差（Self-preferential bias）——模型给自己打分时天然偏向自己的产出

**核心洞见**：修复不是靠更好的提示词，而是靠架构——让产出和验证在两个独立的、互不知晓对方产出的上下文中进行。

### 原则四：动态工作流优于静态流水线

- 静态流水线必须预先处理所有边界条件 → 泛用但不够精准
- 动态工作流为当前任务专门编写 → 精确但需模型够智能（Opus 4.8+）
- **类比**：通用框架 vs 为此任务专门写的脚本
- 何时使用动态工作流：任务需要的 Agent 超过一个会话能协调的数量，或希望编排被编写为可阅读、可重运行、可共享的脚本

### 原则五：五层栈组合原则

```
MCP（连接外部） → Skills（知识编码） → Agent（执行者） → Subagents（并行分解） → Agent Teams（协作通信）
```

逐层叠加而非混用。每层独立演化，但组合产生协同效应。典型决策序列：
1. 先编码知识（Skills）
2. 再自动化规则（Hooks）
3. 然后连接工具（MCP）
4. 需要并行时引入 Subagents
5. 需要通信时引入 Agent Teams

### 原则六：Hooks 护栏机制

在 17 种生命周期事件中，两个最关键的应用：

| Hook 事件 | 用途 | 机制 |
|----------|------|------|
| **PreToolUse** | 安全护栏 | 在工具调用执行前阻止危险操作（如拦截 rm -rf、阻止生产数据库写操作） |
| **PostToolUse** | 质量检查 | 文件写入后自动 lint、格式化、运行类型检查 |

**设计原则**：
- PreToolUse 做阻断（安全第一）
- PostToolUse 做验证（质量保障）
- 非关键任务（日志、通知）使用异步模式 `"async": true`
- Hook 错误可能中断工作流，确保脚本健壮
- 将 `.claude/hooks/` 纳入 Git，团队共享安全策略

---

> **R89 轮新增** | 基于 Anthropic 2026 年 6 月最新公开文档提炼的六项核心设计原则
> *（内容由AI生成，仅供参考）*
