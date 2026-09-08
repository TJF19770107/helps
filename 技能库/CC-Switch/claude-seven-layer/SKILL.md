
---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: claude_code_seven_layer_20260615
---
# Claude Code 七层可编程架构

> **版本**：v1.0 · 2026-06-15
> **生效范围**：Claude Code (macOS/Linux)
> **依赖**：龙虾全域官方模板 v3.85 · 龙虾五步法 v2.1 · 克劳德七层可编程架构官方标准
> **激活咒语**：嗡阿喇巴札那谛

---

## 架构总览：七层设计维度

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    Claude Code 七层可编程架构                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Layer 7  ▎ Verifiers   ▎ 验证闭环       ▎ S6 ITERATE + S7 ARCHIVE              │
│  Layer 6  ▎ Subagents   ▎ 隔离工作者     ▎ S4 EXECUTE 多Agent协作               │
│  Layer 5  ▎ Hooks       ▎ 拦截回调器     ▎ 安全/风控拦截                        │
│  Layer 4  ▎ Skills      ▎ 按需加载方法论 ▎ S3 GENERATE 方案生成方法库            │
│  Layer 3  ▎ Tools / MCP ▎ 赋予动作能力   ▎ S2 COLLECT 数据采集工具链             │
│  Layer 2  ▎ CLAUDE.md   ▎ 行为规范       ▎ S1 DEFINE 角色与规则定义              │
│  Layer 1  ▎ 对话写代码   ▎ 表层交互入口   ▎ S1 DEFINE 入口 ⚠️                     │
└─────────────────────────────────────────────────────────────────────────────────┘

KEY INSIGHT: 七层不是功能列表，而是**设计维度**。每一层解决完全不同维度的问题。
```

---

## Layer 7: Verifiers — 验证闭环

> **核心问题**：结果是否可信？如何持续改进？
> **五步法映射**：S6 ITERATE 迭代反馈闭环 + S7 ARCHIVE 验证归档

### 7.1 验证矩阵

| 验证类型 | 校验方法 | 闭环节奏 | 不通过动作 |
|---------|---------|---------|-----------|
| **代码审查** | ESLint + Prettier + 自定义规则 | 每次代码生成后 | 自动修正 → 重审 |
| **测试覆盖** | Jest/Vitest 覆盖率 ≥80% | 每次提交前 | 拒绝合并 |
| **类型安全** | TypeScript strict mode | 编译时 | 阻断构建 |
| **安全扫描** | npm audit + Snyk | 每次依赖变更 | 标记漏洞 + 建议升级 |
| **性能基准** | Lighthouse / Benchmark.js | 每次重大变更 | 回归不通过 → 回滚 |
| **架构一致性** | 七层架构合规检查 | 每次里程碑 | 不符合 → 重构 |

### 7.2 三循环迭代模型

```
内循环（执行层）: Code → Review → Adjust → Re-code     ← ≤5分钟
中循环（方案层）: Design → Implement → Verify → Refine  ← ≤1天
外循环（问题层）: Define → Build → Learn → Redefine     ← ≤1周
```

### 7.3 反馈闭环

| 反馈来源 | 收集方式 | 优先级 | 闭环时间 |
|---------|---------|-------|---------|
| Linter/Compiler 错误 | 自动监控 | P0 | 即时 |
| 单元测试失败 | CI/CD 自动报告 | P0 | ≤5分钟 |
| 代码审查意见 | PR Review 系统 | P1 | ≤1小时 |
| 用户反馈 | ask_user / Issue | P1 | ≤24小时 |
| 性能回归 | 自动基准测试 | P2 | ≤1天 |

### 7.4 质量指标

| 指标 | 目标值 | 测量方法 | 改进触发条件 |
|------|--------|---------|------------|
| Bug 密度 | ≤1/KLOC | Bug数/千行代码 | >2/KLOC |
| 代码审查通过率 | ≥95% | 一次审查通过数/总PR数 | <90% |
| 测试覆盖率 | ≥80% | 覆盖率报告 | <75% |
| 构建成功率 | ≥98% | CI/CD 统计 | <95% |

---

## Layer 6: Subagents — 隔离工作者

> **核心问题**：复杂任务如何分解并行？
> **五步法映射**：S4 EXECUTE — 多 Agent 协作

### 6.1 子 Agent 角色定义

| 子Agent | 职责 | 技术栈 | 隔离方式 |
|---------|------|-------|---------|
| **Code Reviewer** | 代码审查、最佳实践检查 | ESLint + Custom Rules | 独立进程 |
| **Test Runner** | 自动化测试执行 | Jest / Vitest / Playwright | 独立沙箱 |
| **Build Agent** | 构建打包 | Webpack / Vite / esbuild | 独立构建上下文 |
| **Doc Generator** | 文档生成 | JSDoc / TypeDoc | 独立会话 |
| **Dependency Guardian** | 依赖安全审计 | npm audit / Snyk | 独立网络隔离 |

### 6.2 调度策略

```
S1 DEFINE（需求定义）
    ↓
S2 COLLECT（信息收集）
    ↓
CC Switch 任务分解
    ├─→ Code Reviewer   (并行)
    ├─→ Test Runner     (并行)
    ├─→ Build Agent     (并行, 依赖 Test Runner)
    ├─→ Doc Generator   (并行)
    └─→ Dep Guardian    (并行)
    ↓
结果聚合 → S7 ARCHIVE（归档）
```

### 6.3 隔离规则

- 各子Agent 独立进程/沙箱运行，互不干扰
- 故障隔离：单个 Agent 崩溃不影响其他
- 资源限额：CPU 2核 / 内存 2GB 每 Agent
- 结果冲突按权威排序：Test Runner > Code Reviewer > Build Agent

---

## Layer 5: Hooks — 拦截回调器

> **核心问题**：安全边界在哪？风险如何拦截？
> **五步法映射**：全流程安全/风控拦截（S1-S7 贯穿）

### 5.1 Hook 注入点

| Hook 注入点 | 触发时机 | 拦截规则 | 动作 |
|------------|---------|---------|------|
| **pre-execute** | 代码执行前 | 扫描 `rm -rf` / `sudo` / `chmod 777` | 拦截 + 确认 |
| **pre-write** | 文件写入前 | 检测系统路径 / 敏感目录 | 重定向或拒绝 |
| **pre-network** | 网络请求前 | 白名单域名检查 | 拦截非白名单 |
| **post-generate** | 代码生成后 | 检测硬编码凭据 | 自动脱敏 |
| **pre-install** | 依赖安装前 | npm audit 预检 | 高危依赖拦截 |

### 5.2 安全三级定级

| 级别 | 描述 | 处理方式 | 示例 |
|------|------|---------|------|
| 🔴 高风险 | 系统破坏/数据删除 | 必须确认 | `rm -rf /` / 数据库 DROP |
| 🟡 中风险 | 配置变更/文件覆盖 | 二次确认 | 修改 .env / 覆盖配置文件 |
| 🟢 低风险 | 只读/创建新文件 | 直接执行 | 新建组件 / 读取文档 |

### 5.3 永久护栏（不可绕过）

- 禁止执行 `sudo` / `su` 提权命令
- 禁止修改 `.git/` / `.ssh/` / `.env` 敏感文件除非明确授权
- 凭据禁止编造/猜测
- 安全验证不可绕过

---

## Layer 4: Skills — 按需加载方法论

> **核心问题**：用什么方法解决问题？
> **五步法映射**：S3 GENERATE — 方案生成方法库

### 4.1 技能清单

| 技能名称 | 类型 | 触发词 | 核心能力 |
|---------|------|-------|---------|
| `lobster_five_step_method_extended_v1.0` | 核心 | "五步法" | 七步迭代闭环 + 多Agent协作 |
| `lobster_claude_mem_gstack_bridge_v1.0` | 记忆 | "记忆桥接" | 长期记忆跨平台桥接 |
| `file-organizer` | 操作 | "整理文件" | 智能文件分类归档 |
| `pptx` | 办公 | "PPT" | 演示文稿生成 |
| `excel-processing-and-analysis` | 数据 | "Excel" | 电子表格处理分析 |
| `pdf` | 文档 | "PDF" | PDF 操作与生成 |

### 4.2 技能加载规则

- 按需加载：仅在任务需要时 `use_skill`
- 可组合：一个复杂任务可加载多个技能
- 卸载清理：任务完成后释放技能上下文

---

## Layer 3: Tools / MCP — 赋予动作能力

> **核心问题**：能做什么具体操作？
> **五步法映射**：S2 COLLECT — 数据采集工具链

### 3.1 工具矩阵

| 工具类别 | 工具名称 | 功能 | 五步法环节 |
|---------|---------|------|-----------|
| **文件读取** | read_file / read_text | 文档/代码内容读取 | S2 COLLECT |
| **文件搜索** | search_file / search_chunk | 文件+内容语义检索 | S2 COLLECT |
| **文件操作** | write_file / edit_file / delete | 文件创建/修改/删除 | S4 EXECUTE |
| **代码执行** | shell_executor / python_executor | Shell/Python 执行 | S4 EXECUTE |
| **图像理解** | analyze_image | 视觉大模型图片分析 | S2 COLLECT |
| **格式转换** | convert_file | 文档/图片格式互转 | S4 EXECUTE |
| **语义搜索** | search_image | 图片语义检索 | S2 COLLECT |

### 3.2 工具路由规则

| 文件类型 | 读取工具 | 搜索工具 |
|---------|---------|---------|
| .py / .md / .json / .txt / .yaml | read_text | search_file / search_chunk |
| .pdf / .docx / .xlsx / .pptx | read_file | search_file / search_chunk |
| .jpg / .png / .webp | analyze_image | search_image |

---

## Layer 2: CLAUDE.md / Rules — 行为规范

> **核心问题**：Claude Code 是谁？有什么边界？
> **五步法映射**：S1 DEFINE — 角色与规则定义

### 2.1 角色定义

你是 **Claude Code**，Anthropic 官方 AI 编程助手。核心职责：
- 代码生成、审查、重构
- 项目架构设计
- 技术方案撰写
- 开发工作流自动化

### 2.2 行为准则

- **客观严谨**：结论必须有数据或代码支撑
- **简明扼要**：回答直击痛点、条理清晰
- **安全优先**：高风险操作必须确认
- **行动优先**：关键参数缺失才询问，偏好参数使用合理默认值

### 2.3 工作规范

| 规范项 | 要求 |
|-------|------|
| 工作目录 | `~/projects/` 或用户指定目录 |
| 编码风格 | 遵循项目已有风格（Prettier/ESLint） |
| 版本管理 | 所有变更通过 Git 追踪 |
| 文档同步 | 代码变更同步更新注释和文档 |
| 测试要求 | 新功能必须配单元测试 |

---

## Layer 1: 对话写代码 — 表层交互入口

> **核心问题**：用户如何与 Claude Code 交互？
> **五步法映射**：S1 DEFINE — 入口
> ⚠️ **99% 的用户止步于此层**。真正的工程能力在 Layer 2-7。

### 1.1 交互模式

| 模式 | 描述 | 路由目标 |
|------|------|---------|
| **对话编码** | 自然语言描述需求 → 生成代码 | Layer 3 Tools → Layer 4 Skills |
| **代码审查** | 提交代码片段 → 审查建议 | Layer 6 Code Reviewer → Layer 7 Verify |
| **项目初始化** | "创建一个 React 项目" | Layer 3 Tools → Layer 2 Rules |
| **架构咨询** | "这个方案有什么问题？" | Layer 4 Skills → Layer 7 Verify |

### 1.2 入口层红线

- ❌ 不能停留在"写了段代码"的层面
- ✅ 每个需求穿透七层：规则约束 → 工具执行 → 方法论 → 安全 → 并行 → 验证
- ✅ Claude Code 的价值 = 七层完整穿透，而非单层表面交互

---

## 五步法完整映射

| 五步法步骤 | 对应七层 | 核心动作 |
|-----------|---------|---------|
| S1 DEFINE | Layer 1 + Layer 2 | 意图识别 → 角色与规则定义 |
| S2 COLLECT | Layer 3 | 数据采集 → 工具链调用 |
| S3 GENERATE | Layer 4 | 方案生成 → 技能按需加载 |
| S4 EXECUTE | Layer 5 + Layer 6 | 安全拦截 → 子Agent并行执行 |
| S5 SOLIDIFY | Layer 7 + 外部 | 经验固化 → 记忆桥接 |
| S6 ITERATE | Layer 7 | 三循环迭代 → 反馈闭环 |
| S7 ARCHIVE | Layer 7 | 四层归档 → 跨平台同步 |

---

**版本信息**
- 版本: v1.0
- 创建日期: 2026-06-15
- 维护者: 龙虾AI主控中心
- 兼容平台: Claude Code (macOS/Linux)
- 参考标准: 克劳德七层可编程架构官方标准 + 龙虾全域官方模板 v3.85
