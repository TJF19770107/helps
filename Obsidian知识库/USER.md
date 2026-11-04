---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_ae958188684011f1a0095254002afed2
    ReservedCode1: B6OWWKQ7tGHYN6zG+vixIqmOP3YpJmOwSW7yARGaq0KepU8HeEmrZjCO+5q+Nl/+05MSu/fu9xVGtX29a8lLoi5XTSkJYgtQx+Vu+/DmOKeVja1guP86e3D+vjp4BMvIoWQW51UrYT5x8vtAqsvbTkcgPaYoiX5HKaXmSOsPQ4V+m0GZpu2kUytwUwY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_ae958188684011f1a0095254002afed2
    ReservedCode2: B6OWWKQ7tGHYN6zG+vixIqmOP3YpJmOwSW7yARGaq0KepU8HeEmrZjCO+5q+Nl/+05MSu/fu9xVGtX29a8lLoi5XTSkJYgtQx+Vu+/DmOKeVja1guP86e3D+vjp4BMvIoWQW51UrYT5x8vtAqsvbTkcgPaYoiX5HKaXmSOsPQ4V+m0GZpu2kUytwUwY=
---

# USER.md — 多 Agent 协作流程

> 来源：Anthropic 官方课程（Managed Agents / Agent Teams / Workflows / Skills / Hooks）
> 版本：v1.0 | 创建日期：2026-06-15

---

## 一、多 Agent 协作模式选择流程图

```
任务需求
  │
  ├─ 简单单步任务 → 主 Agent 直接处理
  │
  ├─ 需专职处理但只需结果 → Subagent
  │   └─ 工具白名单 + 独立上下文 + 摘要回传
  │
  ├─ 需多角色协商/讨论 → Agent Teams（实验性）
  │   └─ P2P Mailbox + 共享任务列表 + 独立 Worktree
  │
  ├─ 大规模批量（数十~数百Agent）→ Dynamic Workflow
  │   └─ JS脚本编排 + 后台执行 + 可保存复用
  │
  └─ 可标准化流程 → Skill + Hooks 组合
      └─ 程序性知识 + 确定性动作
```

---

## 二、Subagent 委派流程

### 2.1 触发条件

Claude 主会话遇到匹配 Subagent `description` 的任务时，自动委托。

### 2.2 执行规则

1. Subagent 获得**独立上下文窗口**
2. 仅访问 `tools` 白名单（或 `disallowedTools` 黑名单）
3. 执行完成后**摘要汇报**给主会话
4. **禁止嵌套**：Subagent 不能派生新 Subagent
5. 遵循 `maxTurns` 限制，防止失控

### 2.3 三大内置 Subagent

| Subagent | 模型 | 用途 | 限制 |
|----------|------|------|------|
| **Explore** | Haiku | 只读文件搜索与代码库分析 | 可避免污染主会话 |
| **Plan** | 主模型 | Plan Mode 下代码库研究 | 禁止嵌套 |
| **General-purpose** | 主模型 | 复杂多步骤操作 | 继承所有工具 |

### 2.4 自定义 Subagent 创建

```bash
# 交互式
/agents → 选择位置 → 生成提示词 → 选择工具 → 指定模型 → 保存

# 版本控制
.claude/agents/security-reviewer.md:
---
name: security-reviewer
description: 审查代码安全漏洞
tools: Read, Grep, Glob
model: sonnet
memory: project
---
```

---

## 三、Agent Teams 协作流程（实验性）

### 3.1 启用

```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### 3.2 协作机制

1. Lead Agent 派发任务到共享任务列表
2. Teammate 自主认领
3. 通过 Mailbox 系统 P2P 直接通信
4. 各自独立上下文，互不继承
5. 必须搭配独立 Git Worktree 防文件冲突

### 3.3 适用场景

- 多视角代码审查（安全性/性能/测试覆盖 → 并行）
- 竞争假设调试（多个独立假设同时验证）
- 架构方案竞选（多个独立设计→合并最佳）

### 3.4 当前限制

- 任务状态滞后
- 无法恢复会话
- 不推荐生产环境

---

## 四、Dynamic Workflow 编排流程

### 4.1 启动方式

| 方式 | 示例 |
|------|------|
| 关键词 | `ultracode: 审计 src/routes/ 下所有 API 端点` |
| 自然语言 | "使用工作流审计所有端点" |
| 全局模式 | `/effort ultracode`（整个会话自动） |
| 复用调用 | `/<saved-workflow-name> on topics A, B, C` |

### 4.2 执行流程

```
用户输入 → Claude 编写 JS 编排脚本 → 审批(权限模式决定)
→ 运行时后台执行 → 每阶段扇出/收集 Agent 结果
→ Claude 上下文仅接收最终报告
```

### 4.3 监控指令

| 指令 | 功能 |
|------|------|
| `/workflows` | 列出运行中和已完成的工作流 |
| 选择工作流 → Enter | 打开进度视图 |
| `p` | 暂停/恢复 |
| `x` | 停止 Agent 或整个工作流 |
| `s` | 保存脚本为命令 |

### 4.4 规模化约束

- 最多 16 并发 Agent
- 单次最多 1000 Agent
- 脚本中间结果不进入 Claude 上下文
- 同一会话内可恢复

---

## 五、Skills + Hooks 自动化流程

### 5.1 Skill 生命周期

```
元数据扫描(30-50 tokens) → 相关性匹配 → 加载完整指令 → 执行
```

### 5.2 Hooks 四事件流

```
PreToolUse: 工具调用前校验（可阻止）
  ↓
工具执行
  ↓
PostToolUse: 执行后通知/格式化
  ↓
SessionStart/SessionEnd: 会话级钩子
```

### 5.3 典型自动化流水线

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "command": "npm run lint --fix $FILE"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "./scripts/notify-slack.sh 'File: $FILE'"
      }
    ]
  }
}
```

### 5.4 Skills 七条最佳实践

1. 保持范围集中：一个 Skill 一个领域
2. 使用具体触发描述：明确"何时加载"
3. 渐进式揭示：元数据→详情→资源
4. 包含示例：正例和反例
5. 提供验证标准：何时完成
6. 指定依赖：所需的 MCP 或工具
7. 可跨平台：SKILL.md 标准被 Claude.ai / Claude Code / API 通用

---

## 六、企业级部署流程

### 6.1 三层推送体系

```
Managed Settings（最高优先级，不可覆盖）
  ↓ 通过 MDM / GPO / Anthropic 管理后台下发
项目级 .claude/agents/
  ↓ Git 版本控制，团队共享
用户级 ~/.claude/agents/
  ↓ 个人自定义
```

### 6.2 安全控制四维

| 维度 | 机制 |
|------|------|
| 工具隔离 | `tools` 白名单 / `disallowedTools` 黑名单 |
| 权限模式 | plan / default / acceptEdits / auto / bypass |
| Hooks 拦截 | PreToolUse 前置校验脚本 |
| 组织锁定 | `allowManagedPermissionRulesOnly: true` |

### 6.3 Device Farm 远程测试流程

适用于无本地模拟器的 iOS 真机测试：
1. 在本地 Claude Code 开发
2. Subagent 将构建产物推送到云端 Device Farm
3. 远端执行测试，截图返回分析
4. 热修复建议由主 Agent 汇总

---

## 七、成本管控流程

### 7.1 Subagent 成本

| 手段 | 效果 |
|------|------|
| 轻量任务指定 `model: haiku` | 显著降低单价 |
| 工具白名单缩小范围 | 减少工具定义 Token 消耗 |
| `maxTurns` 限制 | 防止失控循环 |

### 7.2 Workflow 成本

- 先小切片验证：一个目录而非整个仓库
- `/workflows` 实时查看 Token 用量
- 可随时停止，不丢失已完成工作
- 轻量阶段指定小模型

### 7.3 MCP 成本陷阱

2-3 个大型 MCP 服务器 → 尚未输入即消耗 10,000-20,000 Tokens。

**优化路径**：MCP 原型 → 验证流程 → 提取为 Python 脚本 → 封装为 Skill → Token 从 20,000 降至 <100。

---

## 八、上下文管理流程

### 8.1 三阶段操作

| 阶段 | 指令 | 时机 |
|------|------|------|
| 监控 | `/context` | 定期检查 Token 用量 |
| 压缩 | `/compact [保留]` | 上下文 50% 时执行 |
| 清空 | `/clear` | 切换到全新任务 |

### 8.2 多 Agent 上下文隔离原则

- 每个 Agent 独立上下文窗口
- 编排器过滤和摘要输出
- 防止交叉污染和幻觉级联

---

> **USER.md v1.0 完成** | 覆盖 Subagent 委派 / Agent Teams / Workflow / Skills+Hooks / 企业部署 / 成本 / 上下文
> 来源：Anthropic 官方课程 R85 版本
*（内容由AI生成，仅供参考）*

---

## Anthropic 官方课程·R86 更新 (2026-06-15)

### 新增：Agent Teams 完整协作流程（实验性功能）

#### 1. Agent Teams 启用与配置
`ash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=true
`

#### 2. 三阶段协作流水线
`
阶段1：任务分解 → 主代理分解大型任务为原子子任务
阶段2：并行委派 → 3-5 个队友同时从共享任务列表领取工作
阶段3：结果整合 → 主代理收集中间结果并合成最终输出
`

#### 3. 队友间直接通信协议
- 队友可 ping 其他队友协调依赖关系
- 共享任务列表支持动态抢占（非固定分配）
- tmux/iTerm2 分窗模式实时监控队友状态

#### 4. Sub-agent 定义复用为队友
- 队友继承 sub-agent 的 	ools 和 model 配置
- sub-agent markdown 正文作为队友的附加系统提示
- 统一 CLAUDE.md 确保全队一致性

#### 5. 四大标准协作场景
| 场景 | 并行度 | 关键约束 |
|------|--------|---------|
| 大型重构 | 5+ 文件并行 | 确保编辑文件集不相交 |
| 并行搜索 | 多维度并行 | 汇总后交叉验证去重 |
| PR 审查 | 安全+性能+风格 | 多角度评审合并 |
| 迁移项目 | 多模块并行 | 统一迁移规范 |

#### 6. Orchestrator-Subagent 生产级模式
`	ypescript
// 编排器 → 并行子代理 → 整合器
const subtasks = await orchestrator.decompose(complexTask);
const results = await Promise.all(
  subtasks.map(t => subagentPool.execute(t))
);
const final = await integrator.synthesize(results);
// 成本：~.019/次 | 模型：Sonnet(编排)+Haiku(执行)
`

#### 7. Skills 预加载到子代理（新增功能）
子代理可通过 skills frontmatter 字段在启动时预加载完整技能内容到上下文，消除执行期间的技能发现和加载延迟。

---

## Anthropic 多Agent协作流程

> 来源：Anthropic Agent SDK + 5 Subagent Patterns (2026.06)
> 更新：2026-06-15

### 五大子代理模式
1. **分而治之** — 父拆解→N子并行→汇总（20文件摘要成本节省86%）
2. **专家路由** — 分类→专项子代理（各有独立Prompt+工具列表）
3. **并行研究** — 多角度同时调查→合成报告
4. **评判-迭代** — Writer→Judge→修订（最多3轮）
5. **错误恢复** — 捕获错误→Debugger子代理→隔离调试

### 硬约束
- 最大并行: 8-12 | 最大深度: 2层 | 模型: Haiku轻/Sonnet核/Opus慎
- 工具最小化: 摘要器不给bash，翻译器不给web_search
- 返回格式: `{result, citations?, confidence}`

### 长期运行驾驭
初始化Agent(feature_list+init.sh) → 编码Agent(每次会话一个功能+git+progress)


---

## 多Agent协作流程升级（R89轮 · 2026-06-17）

> **来源**：Anthropic 官方博客 + claudecodeguides.com 多Agent架构指南 + 53ai.com 动态工作流六大模式 + lushbinary.com Harness指南
> **新增要点**：六大动态工作流调用模式 / 8种Subagent选型 / 成本控制规则 / Agent Teams协作协议

---

### 一、动态工作流调用模式

复杂任务不再使用固定流水线，改用 Claude 自建 JS harness 的**六大模式组合**。根据任务特征选择模式：

| 任务特征 | 推荐模式 | 说明 |
|---------|---------|------|
| 输入类型多样 | Classify-and-act | 先分类再路由到不同处理代理 |
| 可分解为独立小步骤 | Fan-out-and-synthesize | 每步独立代理 + 最后合成 |
| 产出需严格验证 | Adversarial verification | 产出代理 ≠ 验证代理 |
| 需批量候选+筛选 | Generate-and-filter | 批量生成 → 按标准过滤去重 |
| 需最优方案选择 | Tournament | N 代理竞标 → 两两比较决出胜者 |
| 工作量不确定 | Loop-until-done | 循环生成代理直到停止条件满足 |

**实际用例**：
- 迁移和重构：Bun 从 Zig 重写到 Rust 使用动态工作流完成
- 大规模代码审计：一次审计 462 个代码库的安全漏洞

**启动方式**：
| 方式 | 示例 |
|------|------|
| 关键词触发 | `ultracode: 审计 src/ 下所有 API 端点` |
| 自然语言 | "使用工作流审计所有端点" |
| 全局模式 | `/effort ultracode`（整个会话自动启用） |
| 复用调用 | `/<saved-workflow-name> on topics A, B, C` |

---

### 二、Subagent 选型规范

**8 种 Subagent 类型选择决策树**：

```
任务性质分析
  │
  ├─ 快速定位文件/函数？ → Explore (Haiku 4.5)
  │   └─ 三级彻底度：quick(10-30s) / medium(30-60s) / very thorough(60-120s)
  │
  ├─ 代码质量审查？ → code-reviewer (Sonnet 4.5)
  │
  ├─ 安全漏洞检测？ → security-auditor (Sonnet 4.5)
  │   └─ 专注：认证/注入/权限三类风险
  │
  ├─ 测试执行与分析？ → test-runner (Haiku 4.5)
  │
  ├─ Bug 根因分析？ → debugger (Sonnet 4.5)
  │
  ├─ 代码重构/清理？ → refactor-assistant (Sonnet 4.5)
  │
  ├─ 文档生成？ → doc-writer (Haiku/Sonnet)
  │
  └─ 复杂多步骤实现？ → general-purpose (Sonnet 4.5)
```

**模型选型原则**：
- 探索/测试类 → Haiku（低成本高速度）
- 实现/分析/审查 → Sonnet（最佳性价比）
- 架构/最复杂推理 → Opus（仅必要时）

---

### 三、成本控制规则

**多 Agent 成本模型**（每个子代理独立上下文包含）：
- 系统提示词（~4K tokens）
- CLAUDE.md 内容（~2K tokens）
- 相关文件内容（不定量）
- 任务指令（~500 tokens）

**核心规则**：
1. **5-Agent 并行约 5x Token 消耗**，但速度约 3x
2. **仅在速度优先于 Token 成本时使用多 Agent 模式**
3. **小任务（<10 行改动）不拆 Agent**——一个子代理的开销远超任务本身
4. **顺序依赖任务不并行化**——Task B 需要 Task A 的输出时，串行执行
5. **轻量阶段指定小模型**——探索用 Haiku，实现用 Sonnet，仅在必要时用 Opus

**实践案例**：为 5 个模型生成 CRUD API + 测试
- 单 Agent 顺序：~45 分钟
- 5 Agent 并行：~15 分钟（3x 速度，5x Token）
- 决策：速度优先 → 多 Agent；成本优先 → 单 Agent

---

### 四、Agent Teams 协作协议

**适用场景**：需要多角色协商、交叉验证、竞争假设调试的场景。

**核心机制**：

| 组件 | 职责 |
|------|------|
| **Team Lead** | 任务分解、资源分配、进度监控、冲突解决、最终结果合成 |
| **Teammates** | 多子 Agent，每个负责一个具体领域（Frontend/Backend/Testing/Security） |
| **Communication Bus** | 所有 Agent 通过 sendMessage 工具实时对话，支持 @提到和广播 |
| **Shared Workspace** | 共享同一 Git 仓库、CLAUDE.md 和 memory 文件 |
| **Mailbox 系统** | P2P 直连通信，无需 Lead 中转 |
| **共享任务列表** | Teammates 自主认领任务（非固定分配） |

**典型协作场景**：
- 多视角代码审查：安全+性能+测试覆盖 → 并行审查 → 合并结果
- 竞争假设调试：多个独立假设同时验证 → 比较结果
- 架构方案竞选：多个独立设计 → 评估 → 合并最佳

**启用方式**：`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`（实验性功能，不推荐生产环境）

---

> **R89 轮新增** | 基于 Anthropic 2026 年 6 月最新公开文档
> **R99 更新 (2026-06-18)**：嵌套子代理协作流程补充 — v2.1.172 支持子代理委派子代理（2层限制）；Post-Session Hook 协作收尾
> *（内容由AI生成，仅供参考）*
