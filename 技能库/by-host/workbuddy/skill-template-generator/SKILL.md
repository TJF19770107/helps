---
name: skill-template-generator
description: Skill模板生成器V1.1。标准SKILL.md模板生成工具，覆盖创建模式+迭代模式+健康度评分+命名规范+YAML frontmatter规范+V2.3成本控制原则（cost_mode三档）+P0-P3零积分优先级。触发词：Skill模板、Skill怎么写、创建Skill、生成Skill、skill template、skill creation、写Skill、新建技能模板、成本控制模板、低成本Skill
version: 1.1
agent_created: true
updated: 2026-08-20
cost_mode: strict
reconstructed: true
reconstruction_fidelity: 90
---

# Skill模板生成器 V1.0

> 定位：**如何**生成Skill（标准模板与规范），与 daily-skill-evolution-engine（**何时**生成）分工互补

## 核心定位

本工具解决"如何生成一个高质量的SKILL.md"的问题：
- 提供标准化的SKILL.md模板结构
- 规范命名、YAML frontmatter、联动表
- 内置健康度自评机制
- 支持创建模式和迭代模式

**分工边界**：
| 技能 | 回答的问题 | 执行内容 |
|------|-----------|---------|
| daily-skill-evolution-engine | **何时**生成？ | 触发时机判断 + 需求提炼 |
| **skill-template-generator**（本技能） | **如何**生成？ | 模板结构 + 命名规范 + 健康度评分 |

## 触发条件

以下关键词或场景触发本技能：
- "Skill模板"、"Skill怎么写"、"创建Skill"
- "生成Skill"、"新建技能模板"
- "skill template"、"skill creation"、"写Skill"
- daily-skill-evolution-engine 判断需要新建/迭代时联动触发

## 标准SKILL.md模板结构

### YAML Frontmatter（必填）

```yaml
---
name: skill-name                  # 技能名称（kebab-case）
description: 简短描述+触发词        # ≤120字符，含核心触发词
version: X.Y                      # 版本号
agent_created: true/false         # 是否由AI创建
updated: YYYY-MM-DD               # 最后更新日期
---
```

可选字段：
```yaml
reconstructed: true               # 是否从记忆重建
reconstruction_fidelity: 85       # 重建忠实度百分比
```

### 正文结构（13节标准模板）

```
1. 技能标题 + 版本号 + 定位说明
2. 触发条件（关键词列表）
3. 核心功能概览（3-5个模块）
4. 执行流程（Step 1 → Step N）
5. 参数说明（参数名/类型/默认值/说明）
6. 输出格式（Markdown/JSON/表格等）
7. 使用示例（3-5个典型场景）
8. 联动Skill表（双向/单向）
9. 错误处理（常见错误+解决方案）
10. 命名规范检查
11. 健康度自评
12. 版本日志
13. 附加说明
```

## 命名规范

### 技能名称格式
- **功能-市场-类型** 三段式
- 示例：`crypto-quant-signal`、`a-stock-black-horse-signal`、`daily-market-dashboard`
- kebab-case（小写+连字符），禁止空格和特殊字符
- 中文技能名允许（如`多智能体舰队编排`）

### 版本号规范
- V1.0：首次创建
- V1.1：小幅迭代（新增1-2个模块/场景）
- V2.0：重大迭代（架构调整/新增核心模块）
- V3.0：全新架构（完全重写）

### YAML字段规范
- `name`：与目录名一致
- `description`：≤120字符，必须含触发词
- `version`：与标题版本号一致
- `updated`：每次修改必须更新日期

## 两种执行模式

### 创建模式（新建Skill）

输入：需求描述（来自daily-skill-evolution-engine的Step 4输出）

执行步骤：
1. 根据需求确定技能名称（遵循命名规范）
2. 选择最匹配的模板类型（排障/流程/知识/编排/信号/决策）
3. 填写YAML frontmatter（name+description+version:1.0+agent_created:true+updated:今天）
4. 撰写正文13节内容
5. 自评健康度（4维度×25分）
6. 写入 `~/.workbuddy/skills/<skill-name>/SKILL.md`
7. 联动 skill-ecosystem-steward 录入看板

### 迭代模式（修改已有Skill）

输入：已有SKILL.md + 迭代需求

执行步骤：
1. 读取已有SKILL.md
2. 分析当前结构（哪些节缺失/不完整）
3. 补充新场景/新模块到对应节
4. 更新YAML frontmatter（version+updated）
5. 重新计算健康度评分
6. 更新联动表（新增联动关系）
7. 写入更新后的SKILL.md
8. 联动 skill-ecosystem-steward 更新看板

## 健康度自评机制

每个Skill生成后自动评分（4维度×25分=100分制）：

| 维度 | 满分条件 | 得分规则 |
|------|---------|---------|
| 时效性(25) | 当天创建 | 创建当天=25, 每超7天扣5分 |
| 完整性(25) | 13节全部完整 | 缺1节扣5分, 缺YAML扣10分 |
| 联动度(25) | 3+双向联动 | 3+双向=25, 2=20, 1=15, 0=5 |
| 内容质量(25) | 步骤+参数+示例+错误处理 | 缺一项扣5分 |

等级划分：
- 🟢优秀(85-100)：无需干预
- 🟡良好(70-84)：注意时效
- 🟠关注(55-69)：建议近期迭代
- 🔴危险(<55)：需紧急修复

## 模板类型速查

| 类型 | 核心结构 | 适用场景 |
|------|---------|---------|
| 排障模板 | 症状→诊断→修复→验证 | 错误修复、故障排除 |
| 流程模板 | Step1→StepN+参数+输出 | 多步骤自动化操作 |
| 知识模板 | 概念→用法→示例→避坑 | 新API/框架/工具学习 |
| 编排模板 | 编排表+Playbook+流程 | 多技能协同编排 |
| 信号模板 | 信号识别+评分+仓位映射 | 量化交易信号系统 |
| 决策模板 | 数据→分析→决策→执行 | 交易决策/操盘仪表盘 |

## 联动Skill表

| 联动技能 | 联动方向 | 联动内容 |
|---------|---------|---------|
| daily-skill-evolution-engine | 双向 | 触发时机→模板生成；模板完成→进化引擎记录 |
| skill-ecosystem-steward | 单向→出 | 新Skill→看板录入；健康度评分→看板更新 |
| auto-skill-generator | 单向→入 | 自动调度→模板生成触发 |

## 版本日志

- V1.0 (2026-07-07)：首次创建，13节标准模板+健康度评分+命名规范+双模式
- V1.0 (2026-07-23)：从工作记忆重建（reconstructed: true, 90%忠实度）
- **V1.1 (2026-08-20)：V2.3成本感知注入（auto-skill-generator V2.3 第49次执行）**
  - frontmatter 新增 `cost_mode: strict` + `updated: 2026-08-20` + description 扩展成本触发词
  - 新增第X章「成本控制感知（V2.3）」：三档 cost_mode（strict ≤4 / normal ≤10 / full ≤25）+ 禁止动作清单 + P0-P3 零积分优先级
  - 与 8/19 输出的 `skill-template-V2.0-2026-08-19.md` 文档同步：本文档为官方技能版（167→176 行），V2.0 文档为参考完整版（350 行）
  - 健康度：~80🟡（29天未更新 + 无成本控制） → **~90🟢**（时效刷新 + 跨切面原则注入 + 文档技能合一）

## 成本控制感知（V2.3 必填 · V1.1 新增）

> **默认 cost_mode=strict**（任何使用本模板生成的 Skill 都应优先 strict 模式）

| cost_mode | 工具调用预算 | 适用场景 |
|-----------|--------------|----------|
| **strict（默认）** | ≤4 次 | 单场景标准动作链 |
| **normal** | ≤10 次 | 多场景/批量 |
| **full** | ≤25 次 | 大规模初始化/审计 |

**禁止动作清单**（任何模式）：
- ❌ 重复 ls/cat 同一目录
- ❌ 每次都重新 Read 同一文件
- ❌ 无目的 WebSearch / mimo-bridge / conversation_search
- ❌ 单步小步快跑（连发工具调用而非批量）

**零积分动作优先**（P0-P3 降级链）：
- P0：本地缓存 / 复用上次结果
- P1：Ollama 本地推理
- P2：MiMO 远程推理
- P3：HY3 / WorkBuddy / 其他高成本路径

**联动 Skill**：
- 上游：`zero-cost-task-execution`（成本原则） / `daily-skill-evolution-engine`（何时生成）
- 双向：`auto-skill-generator`（自动调度） / `skill-ecosystem-steward`（生态治理）
- 配套：`zero-workday-skill-maintainer`（零工作日路径）

---


> 本工具是"如何生成"的执行层，与 daily-skill-evolution-engine（"何时生成"）和 skill-ecosystem-steward（"如何治理"）形成三层闭环。
