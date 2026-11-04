---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_6e7b401c605411f1aa435254002afed2
    ReservedCode1: wN8C5DR/f+cQGh7v/TxpAPV711BxmdP5l8ObIxl2ZhHOmJ0uTQXrZrFf8dEul5ZDdPez7mKukVqhlp6CzgVFsjt39Knw+pF3LpP0o8QR2/FIs7gYFp+oNuTnrGjjXXNSwKwUqs8RlrTqo0nSbdy7ltNHLLs0z9EvGkmkNHZuvKEQ9WNK06KE1Y9roj4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_6e7b401c605411f1aa435254002afed2
    ReservedCode2: wN8C5DR/f+cQGh7v/TxpAPV711BxmdP5l8ObIxl2ZhHOmJ0uTQXrZrFf8dEul5ZDdPez7mKukVqhlp6CzgVFsjt39Knw+pF3LpP0o8QR2/FIs7gYFp+oNuTnrGjjXXNSwKwUqs8RlrTqo0nSbdy7ltNHLLs0z9EvGkmkNHZuvKEQ9WNK06KE1Y9roj4=
---

# Anthropic 官方课程学习笔记 · 公开源替代方案

> **更新日期**: 2026-06-05
> **执行轮次**: R58 全域迭代
> **来源**: Anthropic 官方文档公开部分 + 社区深度解读 + Code with Claude 2026 大会内容
> **说明**: anthropic.skilljar.com 需注册登录认证，本文档基于公开等效来源整合

---

## 一、Claude Managed Agents 核心架构

### 1.1 核心概念

| 概念 | 定义 |
|------|------|
| Agent | 模型 + system prompt + 工具 + MCP servers + Skills 的组合体 |
| Environment | 配置好的容器模板（依赖包、网络访问等） |
| Session | 在环境中运行的 Agent 实例，执行特定任务并生成输出 |
| Events | 应用与 Agent 之间交换的消息（用户回合、工具结果、状态更新） |

### 1.2 脑-手分离三层架构

```
Session（会话层）
   ↕
Harness（编排层：工具集成 + 上下文工程 + 状态调度 + 子Agent编排 + 安全防护 + 可观测审计）
   ↕
Sandbox（执行层：独立容器 / 进程隔离 / 审计日志）
```

---

## 二、Multiagent Orchestration（多智能体编排）

### 2.1 架构设计

- **Lead Agent（主智能体）**：复杂任务分解 → 委派给专家子智能体
- **Specialist Sub-agents（专家子智能体）**：各自拥有独立的 model / prompt / tools
- **共享文件系统**：子智能体并行工作，结果贡献回主智能体上下文
- **持久事件记忆**：整个 agent fleet 上保留完整追踪记录
- **Console 追踪**：展示哪个智能体在何时做了什么以及为什么

### 2.2 模型异构性策略

```
Haiku（主Agent） → 廉价分流和请求路由
Opus（子Agent） → 起草、深度分析等复杂任务
```

**设计原则**：模型异构性是重点，而非单模型蜂群。

### 2.3 与开源框架对比

| 特性 | Claude Managed Agents | LangGraph / CrewAI / AutoGen |
|------|----------------------|------------------------------|
| 持久事件记忆 | ✅ 内置 | ❌ 需自行实现 |
| Console 追踪 | ✅ 内置 | ❌ 需第三方 |
| 共享文件系统 | ✅ 原生 | ⚠️ 需配置 |
| First-party 模型访问 | ✅ 原生 | ⚠️ API 调用 |
| 编排粘合代码 | ❌ 不需维护 | ⚠️ 需维护 Python 胶水代码 |

---

## 三、Outcomes 评分器（Rubric-Graded Iteration）

### 3.1 架构特征

- **独立评分实例**：Claude 实例作为独立 Grader，在自己的上下文窗口中评估输出
- **隔离推理轨迹**：评分器与 Agent 的推理轨迹隔离
- **迭代循环**：评分器指出问题 → Agent 迭代改进

### 3.2 性能收益

| 任务类型 | 提升幅度 |
|----------|----------|
| 最难任务（综合） | +10 个百分点 |
| DOCX 生成 | +8.4% |
| PPTX 生成 | +10.1% |

### 3.3 关键创新

**Grader-in-isolated-context 架构**：将成功指标与产出工作的同一模型隔离，更接近 LLM-as-judge 领域，而非 chain-of-thought 自我批评。

---

## 四、Claude Code Harness 七层扩展体系

### 4.1 构建顺序

```
CLAUDE.md → Hooks → Skills → Plugins → LSP → MCP Servers → Subagents
```

### 4.2 逐层解析

| # | 层次 | 核心作用 | 关键实践 |
|---|------|----------|----------|
| 1 | **CLAUDE.md** | 每次会话自动加载的上下文文件 | 根目录精简放全局概况，子目录放局部约定 |
| 2 | **Hooks** | 事件触发的自动化脚本 | Stop hook → 会话结束后自动反思并建议更新 CLAUDE.md；Start hook → 按模块动态加载上下文 |
| 3 | **Skills** | 按需加载专业知识，不膨胀会话 | 绑定到特定路径（如支付团队 skill 只在支付目录激活） |
| 4 | **Plugins** | 打包 skills+hooks+MCP 配置为可安装组件 | 新工程师第一天装上即拥有和老员工相同的能力 |
| 5 | **LSP** | 让 AI 按符号搜索而非字符串匹配 | 部署前先铺 LSP，过滤在读文件之前完成 |
| 6 | **MCP Servers** | 连接外部工具（文档、工单、分析平台） | Claude 连接内部世界的桥梁 |
| 7 | **Subagents** | 独立上下文的子助理 | 只读子Agent先摸清子系统 → 主Agent带完整信息编辑 |

### 4.3 Subagents 最佳实践

```
探索-编辑分离模式：
  只读子Agent → 摸清子系统结构 → 发现写文件
  主Agent → 带完整信息 → 编辑修改
```

**优势**：避免一个实例既探索又修改时的上下文混乱。

---

## 五、三大验证配置模式

### 模式一：让代码库可导航

- CLAUDE.md 精简分层（根目录只放指针和关键坑点）
- 在子目录初始化而非仓库根目录
- 按子目录范围跑测试和 lint
- .ignore 排除生成文件和构建产物
- 目录结构不清晰时建"代码地图"

### 模式二：配置必须随模型进化维护

- 旧模型指令可能在新模型上变成约束
- 建议每 3~6 个月做配置审查
- 重大模型发布后立即检查

### 模式三：指定专人负责

- 先有专人或小团队把基础设施搭好
- 再广泛开放访问
- 首次体验是"好用"而非"折腾"

---

## 六、核心原则总结

1. **Agent = Model + Harness**：决定成败的不是模型本身，而是围绕模型的工具链
2. **Harness 投入收益确定**：比换一个更强模型带来的收益更确定
3. **配置需要持续维护**：这不是一次性投入，而是类似 CI/CD 的基础设施
4. **分层扩展优于一次性配置**：从 CLAUDE.md 到 Subagents 逐层构建
5. **模型异构性**：Haiku 路由 + Opus 执行，不同模型各司其职
6. **独立评分器**：Grader 在独立上下文评估，避免自我一致性伪装质量控制

---

## 七、与龙虾AI体系对标

| Anthropic 最佳实践 | 龙虾AI已有对齐 | 差距分析 |
|---------------------|----------------|----------|
| Lead-Specialist 多Agent架构 | 协议#25 Lead-Specialist多Agent推理分发 | ✅ 完全对齐 |
| Outcomes Rubric 评分器 | 协议#60 反思自纠正循环 | ⚠️ 独立Grader上下文架构待优化 |
| Claude Code 七层扩展 | 协议#135 Claude Code四件套扩展体系 | ⚠️ LSP集成待补充 |
| Harness 工程化 | 协议#173 Agent Harness六层运行时架构 | ✅ 完全对齐 |
| Subagents 探索-编辑分离 | 协议#135 Subagent上下文分流 | ✅ 已覆盖 |
| CLAUDE.md 分层配置 | 协议#124 ACE上下文工程 | ✅ 已覆盖 |
| Dreaming 跨会话记忆 | 协议#29 Dreaming记忆策展 | ✅ 已覆盖 |
| Managed Agents 容器部署 | 协议#75 Managed Agent沙箱部署 | ✅ 已覆盖 |

---

> **归档状态**: ✅ 已存入共享知识库
> **下次更新**: 2026-06-05 下一轮定时任务触发
*（内容由AI生成，仅供参考）*
