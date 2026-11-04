# Anthropic 官方课程全集 — 知识库

> 来源：Anthropic Skilljar 学习平台（https://anthropic.skilljar.com/）
> 检索日期：2026-06-14
> 课程总数：18 门（覆盖 7 大领域）
> 学习方法：全部免费，部分课程提供认证证书考试（$99）

---

## 一、课程全景地图

### 1.1 课程分级体系

| 阶段 | 课程名称 | 难度 | 时长 | 证书 | 核心价值 |
|------|---------|------|------|------|---------|
| 入门 | Claude 101 | 初级 | ~2h | — | 建立Claude完整认知，全场景使用模式 |
| 入门 | AI Fluency: Framework & Foundations | 初级 | ~3h | √ | AI协作四大原则：委托/描述/辨别/勤奋 |
| 入门 | AI Capabilities and Limitations | 初级 | ~1.5h | — | AI能力边界与局限性的诚实认知 |
| 流利度 | AI Fluency for educators | 初级 | ~2h | √ | 教育场景AI流利度实践 |
| 流利度 | AI Fluency for students | 初级 | ~2h | √ | 学生AI学习与职业规划 |
| 流利度 | Teaching AI Fluency | 中级 | ~2h | √ | 教授AI流利度的方法论 |
| 流利度 | AI Fluency for nonprofits | 初级 | ~2h | √ | 非营利组织AI效率提升 |
| 流利度 | AI Fluency for Small Businesses | 初级 | ~2h | √ | 小企业AI应用落地 |
| 开发者 | Building with the Claude API | 中级-高级 | ~8.1h | √ | 旗舰课程：API全栈开发+RAG+Agent架构 |
| 开发者 | Claude Code 101 | 中级 | ~2h | √ | Claude Code开发工作流入门 |
| 开发者 | Claude Code in Action | 中级-高级 | ~2h | √ | Claude Code开发流程深度集成 |
| 开发者 | Introduction to Claude Cowork | 中级 | ~2h | — | Cowork桌面协作环境的任务循环与多步操作 |
| 协议 | Introduction to Model Context Protocol | 中级-高级 | ~3h | √ | MCP三大原语：工具/资源/提示 |
| 协议 | Model Context Protocol: Advanced Topics | 高级 | ~3h | √ | MCP进阶：采样/通知/文件系统/生产部署 |
| **Agent** | **Introduction to Agent Skills** | **中级-高级** | **~3h** | **√** | **SKILL.md编写、配置、team共享、子代理集成** |
| **Agent** | **Introduction to Subagents** | **中级-高级** | **~2h** | **√** | **子代理创建、上下文隔离、多Agent系统构建** |
| 云平台 | Claude with Amazon Bedrock | 高级 | ~3h | √ | AWS平台Claude部署集成 |
| 云平台 | Claude with Google Cloud's Vertex AI | 高级 | ~3h | √ | GCP平台Claude部署集成 |

---

## 二、Agent 核心课程深度提炼

### 2.1 Introduction to Agent Skills（Agent技能入门）

#### 课程大纲
1. **What are Skills?** — Skill定义、与CLAUDE.md/Hooks/Subagents的区别
2. **Creating Your First Skill** — SKILL.md编写、Frontmatter字段、触发描述撰写
3. **Configuration and Multi-File Skills** — 进阶配置、多文件组织、渐进式披露
4. **Skills vs. Other Claude Code Features** — 何时用Skill、何时用CLAUDE.md/Hooks
5. **Sharing Skills** — 团队仓库共享、插件分发、企业管理员部署
6. **Troubleshooting Skills** — 诊断不触发、优先级冲突、运行时错误

#### 核心最佳实践

**SKILL.md Frontmatter 关键字段：**
```yaml
---
name: skill-name
description: 触发匹配的描述（决定何时自动调用）
user-invocable: true/false    # 是否允许用户手动调用
disable-model-invocation: false  # 是否禁止模型自动触发
allowed-tools: [tool1, tool2]   # 限制工具权限的白名单
context: fork                   # 在独立子代理上下文中运行
---
```

**Skill 类型分辨：**
| 特征 | Skills | CLAUDE.md | Hooks | Subagents |
|------|--------|-----------|-------|-----------|
| 作用 | 可复用的专业知识包 | 项目级行为规范 | 事件驱动的自动化 | 独立AI分身 |
| 触发 | 根据任务意图自动匹配 | 会话启动时加载 | 特定事件后执行 | 任务委派时创建 |
| 运行位置 | 当前/独立上下文 | 当前上下文 | 后台 | 独立上下文 |
| 适用场景 | "怎么做"的知识 | "应该遵守什么"的规则 | "何时做什么"的触发器 | "谁来做"的委派 |

**团队共享策略：**
- 提交到Git仓库的 `.claude/skills/` 目录
- 通过Claude Code插件系统分发
- 企业管理员通过managed settings全局部署

---

### 2.2 Introduction to Subagents（子代理入门）

#### 课程大纲
1. Subagent概念与架构 — 独立上下文、独立系统提示、独立工具权限
2. 内置Subagents — Explore/Plan/General-purpose 三种内置子代理
3. 创建自定义Subagents — 通过 `/agents` 命令管理
4. 上下文管理与任务委派 — 如何避免主对话污染
5. Subagents与Skills的结合 — 将Skills注入自定义子代理
6. 构建专业化工作流 — 多Agent系统实战

#### 核心最佳实践

**三种内置子代理模型对比：**

| 子代理 | 模型 | 工具权限 | 用途 |
|--------|------|---------|------|
| **Explore** | Haiku（快速低延迟） | 只读 | 代码搜索、文件发现、代码库探索 |
| **Plan** | 继承自主对话 | 只读 | 计划模式下的代码库研究 |
| **General-purpose** | 继承自主对话 | 全部工具 | 复杂研究、多步骤操作、代码修改 |

**自定义子代理创建流程：**
1. 使用 `/agents` 命令打开管理界面
2. 选择 "Create new agent"
3. 配置：名称、描述、系统提示、工具权限白名单
4. 可注入 Skills 让子代理获得专项能力
5. 通过 Frontmatter 的 `skills:` 字段绑定

**上下文隔离黄金法则：**
- Explore 子代理的搜索结果不污染主对话上下文
- 每个子代理在自己的上下文窗口中运行
- 子代理完成后只返回结果摘要，不返回冗长的中间推理
- 避免超过上下文窗口导致性能下降

---

### 2.3 多Agent编排模式

#### 三种核心编排模式

**1. Supervisor/Orchestrator（主管/编排者模式）**
```
Main Agent（全局指挥官）
  ├── Subagent A → 专项任务1
  ├── Subagent B → 专项任务2
  ├── Subagent C → 专项任务3
  └── 合并结果 → 最终输出
```
- 单个协调Agent分解目标为子任务
- 分发给工作Agent并合并结果
- 适合：结构化项目、确定性子任务

**2. Peer-to-Peer/Swarm（对等/群集模式）**
```
Agent A ←→ Agent B ←→ Agent C
   ↕         ↕         ↕
共享消息总线 / 共享记忆
```
- Agent之间通过共享消息系统直接通信
- 无单一协调者
- 适合：探索性研究、开放式问题

**3. Hierarchical（层级模式）**
```
Top Orchestrator
  ├── Mid Coordinator 1
  │     ├── Expert Pool A
  │     └── Expert Pool B
  └── Mid Coordinator 2
        ├── Expert Pool C
        └── Expert Pool D
```
- 多层协调者和工作者
- 顶层编排者 → 中层协调者 → 专家池
- 适合：大型企业级系统

#### 编排关键原则
- **并行调度**：零依赖子任务并行运行，消除时间瓶颈
- **评估循环**：每次Agent执行包裹自动验证步骤（Execute and Judge Loop）
- **上下文隔离**：避免子代理间上下文污染
- **模型选择**：根据任务复杂度为不同子代理分配合适模型（Haiku/Opus/Sonnet）

---

## 三、Claude Code 完整功能栈

### 3.1 五层架构模型

```
┌──────────────────────────────────────────┐
│  集成层 (Integration Layer)               │
│  MCP协议 → 连接外部工具、API、数据库       │
├──────────────────────────────────────────┤
│  自动化层 (Automation Layer)              │
│  Hooks → 事件驱动的自动化触发              │
├──────────────────────────────────────────┤
│  委派层 (Delegation Layer)                │
│  Subagents → 独立AI分身处理专项任务        │
├──────────────────────────────────────────┤
│  能力层 (Capabilities Layer)              │
│  Skills + Commands → 可复用专业知识包      │
├──────────────────────────────────────────┤
│  记忆层 (Memory Layer)                    │
│  CLAUDE.md → 项目级行为规范与上下文注入    │
└──────────────────────────────────────────┘
```

### 3.2 各层深度解析

**记忆层 — CLAUDE.md 最佳实践：**
```markdown
# 项目规范
- 技术栈：Next.js App Router + TypeScript strict + PostgreSQL + Prisma
- 命令：npm run dev / npm run test / npm run lint
- 规则：禁用any、优先小PR、修改后运行类型检查
- 参考文档：[链接]
```
- 写入CLAUDE.md：“如果Claude在同一件事上被纠正了两次，就写入CLAUDE.md”
- 保持简洁锐利，不要成为文档堆砌

**能力层 — Skills 机制：**
- SKILL.md 是提示模板，不是可执行代码
- `allowed-tools` Field 限制工具权限
- `context: fork` 在子代理中自主运行
- `!cmd` 语法：在Claude读取内容前执行shell命令并将结果内联
- Skills 系统 v2.1 将 `.claude/commands/` 自定义命令并入Skills系统

**委派层 — Subagents 实践：**
- `CLAUDE.junior.md`：子代理的行为规范文件
- 每个子代理可配置独立的模型（Haiku快速/Sonnet均衡/Opus深度）
- 子代理结果通过结构化摘要返回主Agent

**自动化层 — Hooks 机制：**
- PreToolUse / PostToolUse：工具调用前后触发
- Notification：完成特定步骤后提醒
- Stop：满足条件时暂停执行

**集成层 — MCP 协议：**
- 工具(Tools)：让Claude执行外部操作
- 资源(Resources)：让Claude访问外部数据
- 提示(Prompts)：预定义的交互模板
- 进阶：采样(Sampling)、通知(Notifications)、文件系统访问、传输机制

---

## 四、Agent Skills 与 Subagents 协同实战

### 4.1 协同工作流

```
用户需求 → Main Agent 解析
              │
              ├── 匹配到 Skill A → 注入专业知识
              │         │
              │         └── Skill配置 `context: fork` → 自动创建Subagent执行
              │
              ├── 匹配到 Skill B → 注入专业知识  
              │         │
              │         └── Skill配置 `context: fork` → 自动创建Subagent执行
              │
              └── Main Agent合并两个Subagent结果 → 最终输出
```

### 4.2 关键设计原则

1. **Skill 是知识注入，Subagent 是任务隔离**：Skills教会Claude怎么做，Subagents让Claude把任务委派给专业分身
2. **渐进式上下文加载**：SKILL.md只写名称和描述触发匹配，详细指令放在子文件中
3. **避免万能Agent反模式**：一个Agent不应处理所有任务，专业化和拆分是效率的关键
4. **ExecCommand + Skill = 自动化流水线**：`!exec` 在Skill中使用，实现预检查/预处理
5. **Judged Execution**：执行后自动验证，确保输出质量

---

## 五、MCP 协议核心技术

### 5.1 三大原语

| 原语 | 方向 | 用途 | 示例 |
|------|------|------|------|
| Tools | 模型→服务器 | 执行操作 | 搜索数据库、发送邮件、创建文件 |
| Resources | 服务器→模型 | 提供数据 | 文件内容、API响应、数据库记录 |
| Prompts | 服务器→用户 | 交互模板 | 预定义的工作流提示词 |

### 5.2 进阶特性

- **Sampling**：MCP服务器可请求LLM进行采样（服务器反向调用模型）
- **Notifications**：服务器可主动向客户端发送通知
- **File System Access**：标准化文件系统读写接口
- **Transport Mechanisms**：stdio/HTTP+SSE 多种传输协议
- **生产部署**：认证、速率限制、监控、错误处理

---

## 六、课程学习路线图（12周）

| 周次 | 阶段 | 课程 |
|------|------|------|
| 1-2 | 基础 | Claude 101 + AI Fluency: Framework |
| 3-5 | API开发 | Building with the Claude API（旗舰8小时课程） |
| 6-7 | MCP协议 | MCP基础 + MCP进阶 |
| 8-9 | Agent Skills | Introduction to Agent Skills |
| 10-11 | Subagents | Introduction to Subagents |
| 12 | 工作流整合 | Claude Code in Action + Claude Cowork |

---

## 七、参考资料

- 官方课程平台：https://anthropic.skilljar.com/
- Anthropic 开发者文档：https://docs.anthropic.com/
- Claude Code 文档：https://docs.anthropic.com/en/docs/claude-code/
- MCP 协议规范：https://modelcontextprotocol.io/
- 官方Skills仓库：包含16个生产级技能库（文档处理、创意设计、开发测试）
- 社区项目：Superpowers（1.6万+ Star）
- Claude Code Webinar 系列：From manual coding to multi-agent orchestration

---

*本知识库由 Marvis 自动检索与整理 | 更新时间：2026-06-14 23:58 CST*
