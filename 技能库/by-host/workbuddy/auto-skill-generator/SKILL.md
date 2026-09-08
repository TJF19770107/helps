---
name: auto-skill-generator
description: 自动化Skill生成器。每日05:00自动分析工作记录，识别高频操作与待解决问题，生成或迭代可复用专属Skill。四模式决策树+健康度评分+跨技能协同审计+版本升级决策+自我进化机制+成本感知执行。触发词：自动生成Skill、skill自动生成、技能自动迭代、auto skill、每日Skill
version: 2.3
agent_created: true
updated: 2026-08-06
reconstructed: true
reconstruction_fidelity: 95
---

# 自动化Skill生成器 V2.3

> 定位：每日05:00自动执行的元调度引擎，分析工作内容并决策是否生成/迭代Skill
> V2.3核心升级：**成本感知执行模式** — 响应"成本控制置顶"原则，自身率先践行零积分/低成本执行

## 触发条件

- 每日05:00定时自动触发（automation任务）
- 用户显式请求"基于当天工作生成/迭代Skill"

## 四模式决策树

```
执行开始
  ↓
Step 0: 成本预算（V2.3新增）
  - 预估本次执行工具调用次数（目标≤15次）
  - 优先批量读取/并行调用，减少串行轮次
  - 审计模式采用快速抽样（重点🟠/🟡技能）而非全量详评
  ↓
读取 .workbuddy/automations/skill/memory.md（上次执行历史）
读取 .workbuddy/memory/YYYY-MM-DD.md（当天工作记录）
读取 conversation_search（最近对话）
  ↓
距上次实际工作天数？
  ├─ 0-1天 → 🆕创建/迭代模式
  ├─ 2-3天 → 🔍巡检模式（快速健康度扫描）
  ├─ 4-6天 → 🏥审计模式（全量健康度评分+联动诊断）
  └─ 7+天 → 🏥审计模式（加重时效衰减扣分+成本高效抽样）
  ↓
距上次审计天数？
  ├─ <3天 → 跳过审计，仅执行创建/巡检
  ├─ 3-6天 → 正常审计
  └─ 7+天 → 加重审计（含降级建议机制+快速抽样模式）
```

### 🆕创建/迭代模式
- 有新工作内容 → 分析高频操作、重复场景、待解决问题
- 识别Skill需求 → 新建Skill 或 迭代已有Skill
- 输出完整SKILL.md
- **成本约束（V2.3）**：优先迭代已有技能而非新建；新建前确认无同类可复用技能

### 🔍巡检模式
- 无新工作内容 → 快速健康度扫描
- 时效衰减追踪（每7天扣5分）
- 降级预警（连续🟡/🟠次数）
- 无新Skill生成、无迭代
- **成本约束（V2.3）**：仅扫描最近7天跨阈值技能，不做全量重算

### 🏥审计模式
- 全量健康度评分（4维度×25分）
- 跨技能协同审计（5维度）
- 联动链路诊断
- 降级建议机制激活
- 输出审计报告Markdown
- **成本约束（V2.3）**：采用分层审计策略
  - 第一层：快速扫描全部技能frontmatter（1次Bash ls）
  - 第二层：仅详评🟠/🟡/跨阈值技能（目标≤10个）
  - 第三层：🟢技能仅追踪是否跨阈值降级，不重新详评

## 健康度评分（4维度×25分=100分制）

| 维度 | 满分条件 | 扣分规则 |
|------|---------|---------|
| 时效性(25) | 7天内更新 | 每7天未更新扣5分，上限25分 |
| 完整性(25) | YAML+13节全完整 | 缺YAML字段扣5分/个，缺节扣5分/个 |
| 联动度(25) | 3+双向联动 | 3+双向=25, 2=20, 1=15, 单向=10, 无=5 |
| 内容质量(25) | 步骤+参数+示例+错误处理全完整 | 缺一项扣5分 |

等级：
- 🟢优秀(85-100)
- 🟡良好(70-84)
- 🟠关注(55-69)
- 🔴危险(<55)

## 跨技能协同审计（5维度）

1. **双向引用**：A引用B时，B是否也引用A？
2. **参数标准化**：联动接口参数名/格式是否一致？
3. **数据流闭环**：数据→信号→分析→决策→沉淀，有无断裂？
4. **版本兼容**：联动技能版本号是否匹配？
5. **功能冗余**：是否有两个技能覆盖相同场景？

## 版本升级决策引擎

| 触发条件 | 升级类型 | 优先级 |
|---------|---------|--------|
| 连续2次🟠 | 紧急迭代 | P0 |
| 新场景覆盖需求 | 功能扩展 | P1 |
| 30天时效衰减 | 维护更新 | P2 |
| 联动链路断裂 | 修复补丁 | P1 |
| 用户显式请求 | 按需迭代 | P1 |
| **跨切面原则变更**（V2.3） | **架构升级** | **P0** |

> V2.3新增触发条件：当用户确立新的跨切面原则（如成本控制、安全策略等）时，元调度引擎应率先迭代自身以体现该原则。

优先级计算公式：
```
优先级得分 = 紧急度(0-3) × 3 + 需求度(0-3) × 2 + 覆盖度(0-3) × 1
P0: 得分≥12, P1: 得分7-11, P2: 得分≤6
```

## 自我进化机制

### 经验积累
每次执行后记录到 `.workbuddy/automations/skill/memory.md`：
- 执行模式、上下文、产出
- 发现的问题、采用的策略
- **实际工具调用次数与成本复盘（V2.3）**

### 里程碑触发
- 技能矩阵完整度100% → 触发全量健康度审计
- 连续5次零会话 → 触发降级建议机制
- 新建Skill≥3个/周 → 触发技能合并评估
- **跨切面原则确立 → 元技能率先迭代（V2.3）**

### 版本日志规范
每次迭代记录版本号+日期+变更内容

## 执行流程

### Step 0：成本预算（V2.3新增）
```
预估工具调用次数：
- 上下文读取：3-4次（memory.md + 日志 + conversation_search + skills目录）
- 决策分析：0次（纯推理）
- 执行操作：根据模式不同
  - 🆕创建/迭代：3-8次（写入Skill文件 + 报告 + 记忆更新）
  - 🔍巡检：2-4次（报告 + 记忆更新）
  - 🏥审计：5-12次（详评 + 报告 + 记忆更新）
- 总预算：≤20次工具调用（V2.2无预算约束时常达30-40次）
```

### Step 1：读取上下文（批量并行）
```
并行读取（1次轮次完成）：
  .workbuddy/automations/skill/memory.md → 上次执行历史
  .workbuddy/memory/YYYY-MM-DD.md → 当天工作记录
  conversation_search → 最近对话
  ~/.workbuddy/skills/ → 存活技能列表（Bash ls 一次完成）
```

### Step 2：决策模式
根据距上次工作天数和距上次审计天数，选择四模式之一

### Step 3：执行模式（成本高效）
- 🆕模式：分析工作→识别需求→生成/迭代Skill（优先迭代已有，新建需确认无同类）
- 🔍模式：快速健康度扫描→仅追踪跨阈值技能→降级预警
- 🏥模式：分层审计（快速扫描→详评🟠/🟡→🟢仅追踪阈值）→治理建议→审计报告

### Step 4：输出交付
- Skill文件：写入 `~/.workbuddy/skills/<name>/SKILL.md`
- 审计报告：写入 `automation-20260515020232/skill-health-audit-YYYY-MM-DD.md`
- 巡检报告：写入 `automation-20260515020232/skill-patrol-YYYY-MM-DD.md`

### Step 5：更新记忆
- 写入 `.workbuddy/automations/skill/memory.md` 执行摘要（含成本数据）
- 更新 `.workbuddy/memory/MEMORY.md` 技能矩阵状态
- 更新 `.workbuddy/memory/YYYY-MM-DD.md` 当天工作日志

### Step 6：成本复盘（V2.3新增）
```
【成本复盘】
- 预算工具调用：X次
- 实际工具调用：Y次
- 节省/超支：原因
- 下次优化：...
```

## 联动Skill表

| 联动技能 | 联动方向 | 联动内容 |
|---------|---------|---------|
| skill-ecosystem-steward | 双向 | 审计结果→治理建议输入；治理结果→看板更新 |
| daily-skill-evolution-engine | 双向 | 触发时机→进化引擎判断；进化决策→迭代建议反馈 |
| skill-template-generator | 双向 | 需求描述→模板生成触发；模板完成→自动录入 |
| **zero-cost-task-execution** | **双向（V2.3）** | **成本原则→本引擎率先践行；执行经验→成本技巧沉淀** |
| **zero-workday-skill-maintainer** | **双向（V2.3-patch）** | **零工作日判定→路由到本Skill；本Skill执行结果→反馈到成本复盘** |

## 降级建议机制

- 连续3次🟠 → 建议降级（降低优先级层级）
- 连续5次🟡 → 建议合并（与相关技能合并）
- 60天无引用 → 建议归档（移入archived目录）

## 审计周期自适应规则

| 距上次实际工作 | 审计间隔 | 审计深度 |
|--------------|---------|---------|
| 0-3天 | 3天 | 全量详评 |
| 4-7天 | 5天 | 分层抽样 |
| 8-14天 | 7天 | 分层抽样+加重衰减 |
| >14天 | 7天 | 快速抽样+严重加重衰减 |

## 已知技能矩阵（V2.3更新）

### 核心量化技能（13个）
crypto-quant-signal V2.0 | a-stock-black-horse-signal V2.0 | daily-market-dashboard V3.1 | position-sizing-engine V2.0 | trading-risk-radar V2.0 | trading-journal-ai V2.0 | macro-market-linkage V2.0 | neodata-westock-dual-query V2.1 | weekly-strategy-reset V2.0 | auto-skill-generator V2.3 | daily-skill-evolution-engine V1.1 | skill-ecosystem-steward V1.0 | skill-template-generator V1.0

### 舰队基础设施技能（15个）
mimo-bridge V1.2 | ollama-bridge V1.0-dep | 多智能体舰队编排 V1.1 | orca-agent-connection-fix V1.2 | tat-adhoc-exec V1.0 | fleet-devops-orchestrator V1.0 | browser-auto-universal V1.0 | orca_scaffold_silent V1.2 | codex-mimo-link-repair V1.7 | orca-fleet-dual-control V1.1 | windows-lnk-sandbox-safe V1.0 | cloudbase-hy3-relay V1.1 | opencode-third-path V1.0 | powershell-windows-encoding-fix V1.0 | 多智能体舰队编排调度技能 V1.1

### 新增技能（3个，7/30-8/6）
ccgui-orca-bridge V1.0 | github-release-verify-download V1.0 | **zero-cost-task-execution V1.0** 🆕

### 辅助技能（2个）
local-llm-integration-fix V4.0 | deerflow-g-deploy V2.0

## 版本日志

- V1.0 (2026-05-21)：首次创建，基础功能（分析+生成+迭代）
- V2.0 (2026-06-11)：元技能自我升级（四模式决策树+健康度评分+协同审计+升级决策+自我进化）
- V2.1 (2026-06-24)：审计模板标准化+技能依赖拓扑图+审计周期自适应+降级建议机制
- V2.2 (2026-06-30)：新增管理类联动（skill-ecosystem-steward），打破元技能孤岛
- V2.2 (2026-07-23)：从工作记忆重建（reconstructed: true, 90%忠实度）
- V2.3 (2026-08-06)：**成本感知执行模式** — 响应"成本控制置顶"原则
  - 新增Step 0成本预算（目标≤20次工具调用，较V2.2减少40%+）
  - 新增Step 6成本复盘（强制输出实际vs预算）
  - 审计模式改为分层抽样（🟢仅追踪阈值，不再全量详评）
  - 新增联动：zero-cost-task-execution（双向）
  - 新增触发条件：跨切面原则变更→元技能率先迭代（P0）
  - 更新技能矩阵知识库（33个技能，含3个新增）
  - reconstruction_fidelity: 90→95（经多轮迭代忠实度提升）

---

> 本引擎是元调度层，每日05:00自动执行。与 skill-ecosystem-steward（手动治理）、daily-skill-evolution-engine（何时生成）、skill-template-generator（如何生成）、zero-cost-task-execution（成本约束）形成完整闭环：**元调度 ↔ 何时生成 ↔ 如何生成 ↔ 如何治理 ↔ 成本约束**
