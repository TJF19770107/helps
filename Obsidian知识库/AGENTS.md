---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_af2f8895684011f1a99c5254007bceed
    ReservedCode1: ZfUf4PDjMoS4Ja9iEenE/yZtc93wxcNy4dQAZnodDsZtpSyDUPIGsr3CgpngRRnr+nZibDOuYRvr7Wy0PKrg8tSAKI6ZVAFDSsOlMvdt8mkTNAQbFXuwakKKmoXy3ZrjC10LV3NsFMKI8rPNA5kONMTs/FefPqOWpRraAeGNW0csBai0ngT3meL+TaI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_af2f8895684011f1a99c5254007bceed
    ReservedCode2: ZfUf4PDjMoS4Ja9iEenE/yZtc93wxcNy4dQAZnodDsZtpSyDUPIGsr3CgpngRRnr+nZibDOuYRvr7Wy0PKrg8tSAKI6ZVAFDSsOlMvdt8mkTNAQbFXuwakKKmoXy3ZrjC10LV3NsFMKI8rPNA5kONMTs/FefPqOWpRraAeGNW0csBai0ngT3meL+TaI=
---

# AGENTS.md — 子代理管理与自动化配置

> 来源：Anthropic 官方课程（Managed Agents 三层架构 + Subagent YAML + Managed Settings + Hooks）
> 版本：v1.0 | 创建日期：2026-06-15

---

## 一、项目级 Agent 配置清单

### 1.1 目录结构

```
项目根目录/
├── .claude/
│   ├── agents/                    # 子代理定义
│   │   ├── security-reviewer.md
│   │   ├── doc-writer.md
│   │   └── data-query.md
│   ├── skills/                    # 技能
│   │   └── deploy/SKILL.md
│   ├── commands/                  # 斜杠命令
│   ├── hooks/                     # 事件处理器
│   ├── workflows/                 # 已保存工作流脚本
│   └── settings.local.json       # 项目级设置
├── .mcp.json                     # MCP 配置
└── CLAUDE.md                     # 项目级提示
```

### 1.2 Subagent 定义模板

```markdown
---
name: [agent-name]
description: [触发描述，Claude 主会话据此自动委托]
tools: [工具白名单，如 Read, Grep, Glob, Bash]
model: [sonnet | haiku | opus]
memory: [user | project | none]
permissionMode: [plan | default | acceptEdits | auto]
maxTurns: [最大回合数]
disallowedTools: [工具黑名单，与 tools 二选一]
---

[系统提示词：角色 + 任务流程 + 输出格式]
```

### 1.3 内置 Agent 触发条件

| Agent | 触发条件 | 自动/手动 |
|-------|---------|----------|
| **Explore** | 代码库探索/文件搜索 | 自动 |
| **Plan** | Plan Mode 下代码研究 | 自动 |
| **General-purpose** | 复杂多步骤操作 | 自动 |
| **statusline-setup** | 状态栏配置 | 自动 |
| **Claude Code Guide** | 内置问答 | `/` 调用 |

---

## 二、权限配置矩阵

### 2.1 六档权限模式

```json
// .claude/settings.local.json
{
  "permissions": {
    "permissionMode": "acceptEdits",
    "allow": [
      "Agent(security-reviewer)",
      "Agent(doc-writer)",
      "Agent(data-query)"
    ],
    "deny": [
      "Agent(general-purpose)"
    ]
  }
}
```

| 模式 | 行为 | 适用场景 |
|------|------|---------|
| `plan` | 只读探索 | 研究阶段 |
| `default` | 每步确认 | 高风险操作 |
| `acceptEdits` | 编辑自动批准 | 日常开发（企业推荐默认） |
| `auto` | 全部自动 | CI/CD 流水线 |
| `bypassPermissions` | 跳过所有确认 | 受控环境 |
| 组织锁定 | `allowManagedPermissionRulesOnly: true` | 企业统一管控 |

### 2.2 组织级 Managed Settings

```json
// C:\Program Files\ClaudeCode\managed-settings.json (Windows GPO)
{
  "permissions": {
    "allowManagedPermissionRulesOnly": true,
    "allow": ["Agent(security-reviewer)", "Agent(doc-writer)"],
    "deny": ["Agent(general-purpose)"]
  }
}
```

下发渠道：
- Windows：`C:\Program Files\ClaudeCode\managed-settings.json` 或 GPO 注册表 `HKLM\Software\Policies\Anthropic\ClaudeCode`
- macOS MDM：Jamf / Kandji
- Anthropic 管理后台

---

## 三、Hooks 自动化配置

### 3.1 四事件点

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "./hooks/validate-command.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "./hooks/auto-format.sh $FILE"
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "command": "./hooks/session-init.sh"
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "command": "./hooks/session-cleanup.sh"
      }
    ]
  }
}
```

### 3.2 安全校验 Hook 示例

```bash
#!/bin/bash
# validate-readonly-query.sh - PreToolUse Hook
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP)\b' > /dev/null; then
  echo "已拦截写操作" >&2
  exit 2  # 非零退出 → 阻止工具执行
fi
exit 0  # 零退出 → 允许执行
```

### 3.3 拦截层级

```
PreToolUse Hook → 工具执行 → PostToolUse Hook
     ↓ 可阻止        ↓ 执行态      ↓ 通知/格式化
```

---

## 四、MCP 配置最佳实践

### 4.1 最小化原则

```json
// .mcp.json - 仅配置 2-3 个核心 MCP
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

### 4.2 成本管理

| 策略 | 预期节省 |
|------|---------|
| 仅配置 2-3 个核心 MCP | 避免 10,000-20,000 Token 开销 |
| 启用 Tool Search 按需加载 | 减少 ~85% MCP Token 开销 |
| 流程验证后提取为 Python Skill | 从 20,000 Token 降至 <100 Token |

---

## 五、Workflow 自动化编排

### 5.1 保存工作流

```bash
# 工作流执行后
/workflows → 选择运行 → 按 s 保存

# 保存位置
.claude/workflows/     # 项目级（团队共享）
~/.claude/workflows/   # 用户级（所有项目可用）

# 调用
/<workflow-name> on [args]
```

### 5.2 规模化约束

```
并发上限：16 Agent
总量上限：1000 Agent / 运行
中间结果：脚本变量（不进入 Claude 上下文）
中断恢复：同一会话内可恢复
无直接文件系统访问：仅通过 Agent 间接操作
```

### 5.3 关闭 Workflow

```
/claude/config → Dynamic workflows OFF
settings.json: "disableWorkflows": true
Env: CLAUDE_CODE_DISABLE_WORKFLOWS=1
```

---

## 六、Skills 自动化配置

### 6.1 标准结构

```
.claude/skills/deploy/
├── SKILL.md          # name + description (frontmatter) + 指令正文
├── scripts/          # 辅助脚本（按需加载）
└── resources/        # 参考文件（按需加载）
```

### 6.2 SKILL.md 模板

```markdown
---
name: deploy
description: Deploy to production following our release process. Use when user mentions "deploy" or "release".
---

1. Run `npm test` — all tests must pass
2. Build: `npm run build`
3. Deploy to staging first: `./scripts/deploy-staging.sh`
4. Smoke tests: `./scripts/smoke-test.sh`
5. Promote to production: `./scripts/deploy-prod.sh`

On failure at any step, stop and report the error. Do not proceed.
```

### 6.3 跨平台兼容

Skills 采用 Agent Skills 标准（已被 Codex、Gemini CLI 等工具采用）。同一 `SKILL.md` 文件在 Claude.ai / Claude Code / API 上通用。

---

## 七、Git Worktrees 自动化（Agent Teams 必备）

### 7.1 创建独立工作区

```bash
# 为每个 Agent Team 成员创建独立 Worktree
git worktree add ../project-security feature/security-review
git worktree add ../project-perf     feature/perf-review
git worktree add ../project-test     feature/test-review

# 完成后合并最佳版本
git merge feature/security-review
```

### 7.2 清理

```bash
git worktree remove ../project-security
git worktree prune
```

---

## 八、Effort Levels 自动化调配

| 级别 | 推理投入 | Token 消耗 | 适用场景 |
|------|---------|-----------|---------|
| **Low** | 最小 | 最低 | 格式化、翻译 |
| **Medium** | 标准 | 中等 | 日常编码、文档 |
| **High** | 深度 | 较高 | 架构设计、安全审查 |
| **Ultra** | 最大(+自动Workflow) | 最高 | 编译器级项目、跨系统重构 |

```bash
/effort low      # 日常简单任务
/effort medium   # 标准开发（默认）
/effort high     # 深度分析
/effort ultra    # 复杂编排（自动启动 Workflow）
```

---

## 九、Agent 记忆配置

### 9.1 记忆隔离

```yaml
# 用户级记忆（跨项目可用）
memory: user
# 存储位置: ~/.claude/agent-memory/<agent-name>/

# 项目级记忆（纳入 .gitignore）
memory: project
# 存储位置: .claude/agent-memory/<agent-name>/

# 无记忆（无状态 Agent）
memory: none
```

### 9.2 Automemory 结构化记忆

格式：**规则 + 动机 + 应用场景**

- 不仅"记住这个"，还包括"为什么记住"和"何时使用"
- 跨对话上下文自动加载
- 支持 Dreaming 机制：Agent 空闲时自主反思优化

---

## 十、典型团队配置模板

### 10.1 小型团队（2-5 人）

```json
{
  "agents": ["security-reviewer", "doc-writer"],
  "mcp": ["github", "filesystem"],
  "skills": ["deploy", "code-review"],
  "hooks": ["PreToolUse: lint"],
  "effort": "medium"
}
```

### 10.2 中型团队（5-20 人）

```json
{
  "agents": ["security-reviewer", "doc-writer", "data-query", "test-generator"],
  "mcp": ["github", "filesystem", "context7"],
  "skills": ["deploy", "code-review", "migrate"],
  "hooks": ["PreToolUse: lint", "PostToolUse: test"],
  "effort": "high",
  "managed_settings": true
}
```

### 10.3 企业级团队（20+ 人）

```json
{
  "managed_settings": {
    "allowManagedPermissionRulesOnly": true,
    "allow": ["Agent(security-reviewer)", "Agent(doc-writer)", "Agent(data-query)"],
    "deny": ["Agent(general-purpose)"],
    "disableWorkflows": false
  },
  "mcp": ["github", "filesystem", "context7", "playwright"],
  "skills": ["deploy", "code-review", "migrate", "onboard"],
  "hooks": ["PreToolUse: lint", "PostToolUse: test", "SessionEnd: cleanup"],
  "workflows": ["/deep-research", "/code-audit", "/release-checklist"],
  "deployment": "MDM (Jamf/Kandji) + GPO"
}
```

---

> **AGENTS.md v1.0 完成** | 覆盖 Subagent 定义 / 权限配置 / Hooks / MCP / Workflow / Skills / Git Worktrees / Effort / 记忆 / 团队模板
> 来源：Anthropic 官方课程 R85 版本
*（内容由AI生成，仅供参考）*

---

## Anthropic 官方课程·R86 更新 (2026-06-15)

### 新增：子代理管理与自动化配置升级

#### 1. 自定义 Sub-agent 完整 Frontmatter 矩阵
| 字段 | 类型 | 说明 | 本次新增 |
|------|------|------|---------|
| 
ame | 必需 | 小写+连字符唯一ID | - |
| description | 必需 | 触发条件描述 | - |
| 	ools | 可选 | 允许工具列表/Agent(type) 限制生成 | ✅ Agent(type) 语法 |
| disallowedTools | 可选 | 禁止工具列表 | - |
| model | 可选 | sonnet/opus/haiku/ID/inherit | ✅ 完整模型ID支持 |
| permissionMode | 可选 | 6种权限模式 | ✅ plan 模式新增 |
| skills | 可选 | 启动时预加载的技能 | ✅ 全新字段 |
| mcpServers | 可选 | 内联定义或引用 MCP 服务器 | ✅ 内联定义 |
| hooks | 可选 | 限定于此代理的生命周期 hooks | ✅ 全新字段 |
| memory | 可选 | user/project/local 持久记忆 | ✅ 全新字段 |
| ackground | 可选 | true 时始终后台运行 | ✅ 全新字段 |
| effort | 可选 | low/medium/high/xhigh/max | ✅ 全新字段 |
| isolation | 可选 | worktree 隔离模式 | ✅ 全新字段 |
| color | 可选 | UI 显示颜色 | - |
| initialPrompt | 可选 | 主会话代理的首个自动提示 | ✅ 全新字段 |

#### 2. 五级存储位置优先级（更新）
`
1. 托管设置 (managed-settings.d/) — 企业不可覆盖策略
2. --agents CLI 标志 — 会话级临时定义
3. .claude/agents/ — 项目级（可提交到版本控制）
4. ~/.claude/agents/ — 用户级（跨项目共享）
5. Plugin agents/ 目录 — 插件分发
`

#### 3. 自动化配置模板更新

**企业级托管子代理模板**：
`yaml
---
name: enterprise-code-reviewer
description: Mandatory code review for all PRs
tools: Read, Glob, Grep, Bash
model: sonnet
permissionMode: acceptEdits
memory: project
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "npx eslint --fix"
---
`

**Agent SDK 嵌入式子代理**：
`yaml
---
name: ci-test-runner
description: Runs test suites in CI pipelines
tools: Bash, Read
model: haiku
permissionMode: auto
background: true
effort: high
isolation: worktree
---
`

#### 4. Computer Use 自动化配置（全新）
`yaml
---
name: gui-tester
description: Tests desktop GUI applications
tools: ComputerUse, Read, Bash
permissionMode: acceptEdits
# 按应用审批：仅允许指定应用
---
`

#### 5. Auto Mode 分类器与权限矩阵（更新）
| 模式 | 自动接受 | 分类器审查 | 写入受保护目录 | 适用场景 |
|------|---------|-----------|---------------|---------|
| default | 否 | 否 | 提示 | 交互式开发 |
| acceptEdits | 编辑+工作区 | 否 | 提示 | 日常编码 |
| auto | - | ✅ 是 | 分类器判定 | 半自主运行 |
| dontAsk | - | - | 自动拒绝 | 只读分析 |
| bypassPermissions | ✅ 全部 | - | ✅ 允许 | 全自主管道 |

---

## Anthropic 子代理管理与自动化

> 来源：Claude Code Advanced Patterns (2026.06)
> 更新：2026-06-15

### 五大机制
| 机制 | 用途 | 绕过模型？ |
|------|------|-----------|
| CLAUDE.md | 硬性规则(≤200行) | 否 |
| Skills | 流程知识(≤500行) | 否 |
| Subagents | 委派工作 | 否 |
| Hooks | 确定性自动化 | **是** |
| MCP | 外部访问 | 否 |

### 目录结构
`.claude/agents/`(项目级) + `~/.claude/agents/`(用户级)

### 权限最小化
code-reviewer: read/grep/glob(Haiku) | test-runner: bash/read(Haiku) | debugger: read/bash/grep(Sonnet)

### Hooks关键用例
PostToolUse: 自动lint | PreToolUse: 拦截危险命令 | SessionStart: 注入进度

### 子代理上限
1-3(小型) → 3-5(中型) → 5-8(大型) | 最大并行≤12 | 深度≤2层
| plan | - | - | 只读 | 分析和规划 |


---

## 子代理管理与自动化升级（R89轮 · 2026-06-17）

> **来源**：Anthropic 官方文档 + claude-world.com Agents完整指南 + CSDN Managed Agents企业IT指南 + claudecode.xyz Hooks完全指南
> **新增要点**：8种内置Subagent配置规范 / Managed Settings企业级下发 / Hooks自动化配置模板 / 并发与隔离规则

---

### 一、8 种内置 Subagent 配置规范

**完整配置矩阵**：

| 类型 | 模型 | 工具建议 | permissionMode | maxTurns | 适用场景 |
|------|------|---------|---------------|----------|---------|
| **Explore** | haiku | Read, Grep, Glob | plan | 15 | 快速代码库导航（三级彻底度） |
| **general-purpose** | sonnet | 继承所有工具 | acceptEdits | 40 | 复杂多步骤实现 |
| **code-reviewer** | sonnet | Read, Grep, Glob | plan | 25 | PR 审查、模式检查 |
| **security-auditor** | sonnet | Read, Grep, Glob | plan | 30 | 认证/注入/权限漏洞检测 |
| **test-runner** | haiku | Read, Bash, Grep | acceptEdits | 30 | 测试执行与分析 |
| **debugger** | sonnet | Read, Bash, Grep, Glob | acceptEdits | 35 | Bug 根因调查 |
| **refactor-assistant** | sonnet | Read, Write, Edit, Bash | acceptEdits | 40 | 代码清理与结构优化 |
| **doc-writer** | haiku/sonnet | Read, Grep, Glob | acceptEdits | 20 | README/API 文档生成 |

**配置示例 — 安全审查子代理**：
```yaml
---
name: security-auditor
description: Mandatory security review for authentication, injection, and authorization risks
tools: Read, Grep, Glob
model: sonnet
permissionMode: plan
memory: project
maxTurns: 30
isolation: worktree
---
```

**配置示例 — 企业级只读探索代理**：
```yaml
---
name: enterprise-explorer
description: Read-only codebase exploration, no file modifications allowed
tools: Read, Grep, Glob
model: haiku
permissionMode: plan
maxTurns: 15
background: false
---
```

---

### 二、Managed Settings 企业级下发

**三层下发体系**（优先级从高到低）：

```
1. Managed Settings（最高优先级，不可覆盖）
   └─ managed-settings.json 或 MDM 下发
2. 项目级 .claude/agents/（Git 版本控制）
3. 用户级 ~/.claude/agents/（个人自定义）
```

**managed-settings.json 模板**：
```json
{
  "permissions": {
    "allowManagedPermissionRulesOnly": true,
    "allow": [
      "Agent(security-reviewer)",
      "Agent(doc-writer)",
      "Agent(explore)"
    ],
    "deny": [
      "Agent(general-purpose)"
    ]
  },
  "mcpServers": {
    "github": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"]},
    "filesystem": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]}
  },
  "hooks": {
    "PreToolUse": [{"matcher": "Bash", "command": "/managed/hooks/block-risky.sh"}]
  }
}
```

**下发渠道**：
| 平台 | 方式 |
|------|------|
| Windows | `C:\Program Files\ClaudeCode\managed-settings.json` 或 GPO 注册表 |
| macOS | Jamf / Kandji MDM |
| 通用 | Anthropic 管理后台 |

**关键约束**：
- `allowManagedPermissionRulesOnly: true` 时，下级配置中的权限规则被忽略
- 用户无法覆盖 Managed Settings 中禁用的工具或代理
- MDM 更新自动推送至组织内所有机器

---

### 三、Hooks 自动化配置模板

**17 种生命周期事件中关键 4 种配置模板**：

**1. PreToolUse — 安全阻拦**：
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/block-dangerous.sh"
      }]
    }]
  }
}
```
**拦截脚本逻辑**：检测 `rm -rf`、`DROP TABLE`、`DELETE FROM` 等危险模式 → 返回 `permissionDecision: "deny"`。

**2. PostToolUse — 质量检查**：
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npx eslint --fix $FILE",
        "async": true
      }]
    }]
  }
}
```
**最佳实践**：异步执行避免阻塞关键路径。

**3. SessionStart — 状态加载**：
```json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/session-init.sh"
      }]
    }]
  }
}
```
**加载内容**：Git 状态、未完成 TODO 数量、当前分支信息。

**4. Stop — 任务通知**：
```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/notify.sh",
        "async": true
      }]
    }]
  }
}
```

**Hook 退出码含义**：
| 退出码 | 含义 |
|--------|------|
| `0` | 成功，允许操作继续 |
| 非 `0` | 失败，具体行为取决于事件类型 |
| JSON 输出 | 返回结构化决策（如 permissionDecision: "deny"） |

---

### 四、并发与隔离规则

**多 Agent 编排规则**（CLAUDE.md 配置片段）：
```markdown
## Multi-Agent Rules
- Maximum 5 concurrent sub-agents
- Each sub-agent works on ONE file or ONE module
- Sub-agents do NOT modify files another agent is working on
- Orchestrator verifies all sub-agent outputs before committing
- If two agents need the same file, serialize their work
```

**任务分配策略**：
1. 定义精确范围（哪些文件、哪些函数）
2. 提供该范围的 CLAUDE.md 相关章节
3. 设定验收标准（测试通过、类型检查通过等）
4. 指定子代理应回报的内容

**隔离级别**：
| 级别 | 机制 | 适用场景 |
|------|------|---------|
| **上下文隔离** | 独立上下文窗口，摘要回传 | Subagent（默认） |
| **文件系统隔离** | 独立 Git Worktree | Agent Teams 协作 |
| **权限隔离** | 工具白名单 + 权限模式 | 所有子代理 |

**子代理嵌套限制**：
- 子代理可理论嵌套，但实际最多 2 层（编排器 + 工作者）
- Plan Mode 下防止无限嵌套：子代理不能再派生子代理
- 超过 2 层嵌套几乎从不需要

---

> **R89 轮新增** | 基于 Anthropic 2026 年 6 月最新公开文档的子代理管理与自动化配置升级
> **R99 更新 (2026-06-18)**：嵌套子代理自动化配置 — Agent 工具权限接入 + Post-Session Hook 事件点；Fable 5 模型加入 model 字段可选值
> *（内容由AI生成，仅供参考）*
