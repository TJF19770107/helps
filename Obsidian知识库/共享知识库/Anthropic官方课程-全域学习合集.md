# Anthropic 官方课程 & Claude Code 扩展体系 全域学习合集

> 生成日期：2026-06-05 | 每2小时自动更新 | 来源：Anthropic官方文档 + 中文社区深度解读

---

## 一、Anthropic 官方课程目录（Skilljar）

以下课程来自 Anthropic Skilljar 官方学习平台，目前共约 30+ 门课，覆盖 Claude 入门到高级 Agent 工程：

| 序号 | 课程名称 | 难度 | 时长 | 核心内容 |
| --- | --- | --- | --- | --- |
| 1 | Introduction to Subagents | 中级-高级 | ~2h | 如何在Claude Code中使用和创建Subagents；上下文管理和任务委派；Subagents如何与Skills结合；构建专业化工作流 |
| 2 | AI Fluency for Students | 初级 | ~2h | 学生如何负责任地使用AI；AI在学习、职业规划中的应用；AI流利度核心技能 |
| 3 | Prompt Engineering Foundation | 初级 | ~1.5h | 提示词工程基础；结构化提示；思维链 |
| 4 | Building with Claude API | 中级 | ~3h | Messages API使用；工具调用；流式响应 |
| 5 | Claude Code Masterclass | 高级 | ~4h | CLAUDE.md配置；Skills/Subagents/Hooks/MCP全栈 |
| 6 | Agent Teams Workshop | 高级 | ~3h | 多Agent编排；共享任务列表；并行协调 |
| 7 | MCP Server Development | 高级 | ~3h | MCP协议规范；Server实现；工具注册 |
| 8 | Claude for Enterprise | 中级 | ~2h | 企业部署；安全合规；成本优化 |
| 9 | LLM Evaluation & Testing | 高级 | ~3h | Eval方法；A/B测试；回归测试 |
| 10 | Responsible AI with Claude | 初级-中级 | ~2h | AI伦理；宪法AI；安全对齐 |

---

## 二、Claude Code 扩展体系七层架构

Claude Code 的核心是「模型 + 内置工具」构成的智能体循环。所有扩展都是往这个循环的不同位置插入能力：

### 2.1 七层架构速查表

| 层级 | 特性 | 能力 | 触发机制 | 上下文成本 |
| --- | --- | --- | --- | --- |
| L1 | **CLAUDE.md** | 持久上下文 | 会话开始自动加载 | 每请求都带着 |
| L2 | **Skills** | 可复用知识/流程/指令 | 手动 /skill 或模型自动触发 | 低（开始仅加载描述） |
| L3 | **Subagents** | 隔离上下文独立执行 | 被主Agent派生 | 与主会话隔离 |
| L4 | **Agent Teams** | 多独立Claude会话协作 | 手动编排/自协调 | 显著较高 |
| L5 | **MCP** | 连接外部服务 | 按需调用工具 | 用到具体工具前很低 |
| L6 | **Hooks** | 生命周期事件自动化 | 事件触发（确定性） | 零（外部运行） |
| L7 | **Plugins** | 打包分发层 | 安装后激活 | 取决于内容 |

### 2.2 各层详解

#### L1: CLAUDE.md — 永远在线的项目须知

- 每次会话自动全量加载
- 适用场景：编码约定、构建命令、项目结构、"绝不做X"规则
- 最佳实践：控制在200行以内 → 膨胀时拆入 `.claude/rules/` 或 Skills
- `rules` 支持 `paths` frontmatter 实现文件匹配式加载，进一步节省上下文

#### L2: Skills — 可复用的命令与知识库

目录结构：
```
.claude/skills/<name>/
  SKILL.md          # 必须：YAML frontmatter + Markdown正文
  template.ts       # 可选：模板文件
  example-output.md # 可选：示例输出
```

SKILL.md Frontmatter 字段：
| 字段 | 必填 | 说明 |
| --- | --- | --- |
| name | 是 | 命令名，调用时用 /name 触发 |
| description | 是 | Claude判断自动触发的依据 |
| allowed-tools | 否 | 执行期间自动放行的工具列表 |
| disable-model-invocation | 否 | true=禁止自动触发，只能手动 /name |
| user-invocable | 否 | false=从/菜单隐藏 |
| context | 否 | fork=在隔离子代理中运行 |
| agent | 否 | 指定子代理类型（Explore/Plan/...） |

**使用原则**：
- 只读类 Skill：开放 allowed-tools（Read/Glob/Grep），允许自动触发
- 写入/副作用类 Skill：设置 disable-model-invocation: true，只能手动触发
- Context fork：适合大吞吐研究工作，在隔离上下文中运行不污染主会话
- 上下文优化：设置 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量控制预算

#### L3: Subagents — 隔离上下文中的专职Worker

核心概念：
- 在独立上下文窗口中执行任务
- 主对话只收到摘要结果，不污染主上下文
- 支持预加载特定 Skills（通过 `skills:` 字段）
- 支持不同 agent 类型（Explore/Plan/General）

典型使用场景：
- 搜索代码库，只返回关键发现
- 研读大量文件生成摘要报告
- 并行处理多个独立子任务
- 上下文窗口即将溢出时的卸载

与 Skills 的关键区别：
- **Skill** = 可复用内容（加载进当前上下文）
- **Subagent** = 隔离Worker（独立上下文，只返回摘要）
- 两者可组合：Subagent 预加载 Skill；Skill 使用 context: fork 在隔离子代理中运行

#### L4: Agent Teams — 多Agent协作编排

三个核心组件：
| 组件 | 角色 |
| --- | --- |
| 团队领导 | 主 Claude Code 会话，创建团队、生成队友、分配任务、综合结果 |
| 队友 | 独立 Claude 实例，拥有自己的上下文窗口，可独立工作并相互通信 |
| 共享任务列表 | 中心协调机制，状态：待处理/进行中/已完成，自动依赖解除阻塞 |

Agent Teams vs Subagent：
| 特性 | Subagents | Agent Teams |
| --- | --- | --- |
| 通信 | 仅向主Agent汇报 | 直接相互发送消息 |
| 上下文 | 共享会话 | 每个Agent独立会话 |
| 协调 | 主Agent编排 | 自协调 |
| 适用场景 | 快速聚焦任务 | 复杂并行工作 |
| Token使用 | 较低 | 显著较高 |

**任务分解最佳实践**：
- ✅ 好分解：模块级分工（认证审查员/数据库审查员/API审查员），可并行执行
- ❌ 差分解：太宽泛（"修复所有bug"）或不必要依赖（"等待X完成"）

#### L5: MCP — 连接外部服务的协议层

- 将 Claude 连接到数据库、Slack、浏览器等外部系统
- 工具名在会话开始时加载，完整 schema 按需加载
- 上下文成本：用到具体工具前很低

**MCP + Skill 组合模式**：MCP 提供连接，Skill 提供"怎么用好这个连接"的知识

#### L6: Hooks — 生命周期事件自动化

Hook 事件完整清单：
| 事件 | 触发时机 | 频率 |
| --- | --- | --- |
| SessionStart | 会话开始或恢复 | 每会话一次 |
| UserPromptSubmit | 提交提示词后、Claude处理前 | 每轮一次 |
| PreToolUse | 工具调用执行前，可阻止 | 每工具调用 |
| PostToolUse | 工具调用成功后 | 每工具调用 |
| PostToolUseFailure | 工具调用失败后 | 每工具调用 |
| PermissionRequest | 权限对话框出现时 | 按需 |
| PermissionDenied | 工具调用被自动模式拒绝 | 按需 |
| Notification | Claude Code发送通知时 | 按需 |
| SubagentStart | 子代理被派生时 | 每子代理 |
| SubagentStop | 子代理完成时 | 每子代理 |
| Stop | Claude响应结束时 | 每轮 |
| StopFailure | 轮次因API错误结束 | 按需 |
| InstructionsLoaded | CLAUDE.md/rules加载时 | 每会话+延迟加载 |
| ConfigChange | 配置文件变更时 | 按需 |
| CwdChanged | 工作目录变更时 | 按需 |
| FileChanged | 监控文件变更时 | 按需 |

Hook 触发方式：Shell命令（stdin接收JSON）/ HTTP端点（POST） / LLM提示

**核心原则：护栏用 Hook，不用 Prompt**。
- Prompt 只是"请求"，Hook 才是"强制"
- 例如："永远别改 .env" 写在 Skill 里只是建议；用 PreToolUse Hook 拦截才是真正防护

#### L7: Plugins — 打包分发层

- 将 Skills、Hooks、Subagents、MCP server 捆成可安装单元
- 插件内技能自动加命名空间（如 /my-plugin:review）
- 适用场景：多仓库复用配置、团队分发

---

## 三、核心设计原则与最佳实践

### 3.1 扩展层逐步搭建原则

按「触发信号」自然演进，而非开局配满：

| 触发信号 | 该加什么 |
| --- | --- |
| Claude 把某个约定搞错两次 | 写进 CLAUDE.md |
| 反复敲同一段开场 prompt | 存成 Skill |
| 第三次粘同一份多步流程 | 沉淀成 Skill |
| 总从 Claude 看不到的浏览器里抄数据 | 接成 MCP server |
| Claude 为找符号定义读了一堆文件 | 装 Code Intelligence |
| 支线任务刷满主对话 | 改用 Subagent |
| 希望某件事每次都自动发生 | 写 Hook |
| 第二个仓库需要同样配置 | 打包成 Plugin |

### 3.2 三问决策法

1. **Claude 该不该永远知道这件事？** → 是 → CLAUDE.md（或拆进 rules）
2. **这是有时才需要的知识/可触发的流程吗？** → 是 → Skill；要隔离上下文 → Subagent；要多方协作 → Agent Team；要连外部 → MCP
3. **这件事必须每次自动、确定性地发生吗？** → 是 → Hook

### 3.3 特性叠加规则

- **CLAUDE.md**：叠加式，所有层级内容同时进入上下文
- **Skills/Subagents**：按名字覆盖（managed > CLI flag > project > user > plugin）
- **MCP server**：按名字覆盖（local > project > user）
- **Hooks**：合并执行，不分来源

### 3.4 上下文成本管理

| 特性 | 加载时机 | 上下文成本 | 优化建议 |
| --- | --- | --- | --- |
| CLAUDE.md | 会话开始 | 高（每请求） | 控制在200行内 |
| Skills | 开始+使用时 | 低（仅描述） | disable-model-invocation归零成本 |
| MCP server | 会话开始 | 低（按需加载） | 工具数控制 |
| Subagent | 派生时 | 隔离（与主会话无关） | 适合卸载重任务 |
| Hook | 触发时 | 零（外部运行） | 默认不占上下文 |

---

## 四、Agent Teams 实战案例

### 4.1 16 Agent 构建 C 编译器

- 16 个 Claude Agent 并行工作，从零构建 Rust C 编译器
- ~2,000 个 Claude Code 会话，约 $20,000 API 费用
- 产出 100,000+ 行 Rust 代码
- 能在 x86、ARM 和 RISC-V 上编译 Linux 6.9
- 代理自主协调：一个处理解析，另一个处理代码生成，另一个处理优化遍历

### 4.2 代码库安全审查 Teams 示例

```
创建一个代理团队来审查此代码库的安全漏洞。
生成 4 个队友：
1. 认证审查员 - 专注于认证流程和会话处理
2. 输入验证审查员 - 检查所有用户输入
3. 数据库安全审查员 - 分析查询和数据访问
4. 集成审查员 - 查看 API 边界和外部调用
让他们分享发现并质疑彼此的结论。
```

---

## 五、与龙虾体系的对标映射

| Anthropic 概念 | 龙虾体系对应 | 说明 |
| --- | --- | --- |
| CLAUDE.md | 角色总说明书 / 全域模板 | 永久在线的持续上下文 |
| Skills | 技能库 (SKILL.md) | 可复用知识/流程/工作流 |
| Subagents | 子Agent体系 | 隔离上下文的专职Worker |
| Agent Teams | 多Agent协作调度 | 独立会话自协调 |
| MCP | 工具协议层 | 连接外部数据源和服务 |
| Hooks | 定时任务 / 事件触发器 | 生命周期自动化 |
| Plugins | 技能包分发 | 多分身统一部署 |

---

## 六、迭代记录

| 日期 | 更新内容 | 来源 |
| --- | --- | --- |
| 2026-06-05 第N轮 | 全量整合七层架构详解 + Agent Teams案例 + 对标映射 | docs.anthropic.com / code.claude.com + 社区深度解读 |
