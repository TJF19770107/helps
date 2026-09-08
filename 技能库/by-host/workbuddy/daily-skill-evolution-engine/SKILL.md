---
name: daily-skill-evolution-engine
description: 每日技能进化引擎。识别何时需要生成新Skill或迭代已有Skill，将当天工作流沉淀为可复用技能。5步工作流+7类触发场景（含成本控制场景）+与skill-template-generator分工。触发词：技能进化、Skill迭代、工作流沉淀、Skill什么时候生成、怎么把工作变成Skill、skill evolution
version: 1.2
agent_created: true
updated: 2026-08-07
---

# 每日技能进化引擎 V1.2

> 定位：**何时**生成Skill（触发时机判断），与 skill-template-generator（**如何**生成Skill）分工互补

## 核心定位

本引擎解决"何时需要生成新Skill"的问题：
- 监测日常工作中的可沉淀模式
- 判断是否需要创建新Skill vs 迭代已有Skill
- 触发 skill-template-generator 执行具体的Skill生成

**分工边界**：
| 技能 | 回答的问题 | 执行内容 |
|------|-----------|---------|
| **daily-skill-evolution-engine**（本技能） | **何时**生成？ | 触发时机判断 + 需求提炼 |
| **skill-template-generator** | **如何**生成？ | 模板结构 + 命名规范 + 健康度评分 |

## 触发条件

以下关键词或场景触发本技能：
- "技能进化"、"Skill迭代"、"工作流沉淀"
- "Skill什么时候生成"、"怎么把工作变成Skill"
- "Skill模板"、"Skill怎么写"（→联动skill-template-generator）
- 用户完成8+步复杂任务后（自动触发）
- 用户修复棘手错误后（自动触发）

## 5步工作流

### Step 1：扫描当日工作记录
```
读取 .workbuddy/memory/YYYY-MM-DD.md → 提取当天工作内容
读取 conversation_search 最近对话 → 识别高频操作模式
```

### Step 2：识别可沉淀模式
7类触发场景：
1. **高频重复操作**：同类型操作3次以上 → 创建自动化Skill
2. **棘手错误修复**：排查过程超过3步 → 创建排障Skill
3. **多步骤流程**：步骤≥8步 → 创建流程Skill
4. **领域知识发现**：新API/新框架/新工具用法 → 创建知识Skill
5. **跨技能协作**：需要2+技能协同完成 → 创建编排Skill
6. **已有Skill缺场景**：现有Skill覆盖不足 → 触发迭代
7. **成本控制场景**（V1.2新增）：发现高积分消耗模式/确立跨切面成本原则 → 创建成本约束Skill 或 迭代现有Skill注入成本控制

### Step 3：决策：新建 vs 迭代 vs 跳过
决策规则：
- 无已有Skill覆盖 → **新建**
- 已有Skill覆盖但缺场景 → **迭代**
- 已有Skill覆盖且足够 → **仅记录**（不生成）
- 操作是纯一次性任务 → **跳过**（不值得沉淀）
- 涉及高积分消耗或成本优化 → **先联动 zero-cost-task-execution 评估最低成本路径**，再决定是否生成

### Step 4：提炼需求
将识别的模式转化为Skill需求描述：
- 技能名称（遵循命名规范：功能-市场-类型）
- 适用场景（3-5个典型场景）
- 触发关键词
- 核心执行逻辑（步骤化描述）
- 需要的参数

### Step 5：触发执行
- **新建** → 联动 `skill-template-generator` 生成完整SKILL.md
- **迭代** → 直接修改已有SKILL.md，补充新场景/简化操作
- **记录** → 写入工作日志备忘，下次审计再评估

## 触发场景速查

| 场景 | 触发条件 | 决策 | 联动 |
|------|---------|------|------|
| 高频重复 | 同类型操作≥3次 | 新建/迭代 | skill-template-generator |
| 棘手排障 | 排查≥3步 | 新建排障Skill | skill-template-generator |
| 多步流程 | 步骤≥8 | 新建流程Skill | skill-template-generator |
| 新知识发现 | 新API/框架用法 | 新建知识Skill | skill-template-generator |
| 跨技能协作 | 需2+技能协同 | 新建编排Skill | skill-template-generator |
| Skill缺场景 | 覆盖不足 | 迭代已有Skill | 直接修改SKILL.md |
| 成本控制 | 高积分消耗/成本原则确立 | 新建/迭代成本相关Skill | zero-cost-task-execution |

## 联动Skill表

| 联动技能 | 联动方向 | 联动内容 |
|---------|---------|---------|
| skill-template-generator | 双向 | 本引擎触发时机→模板生成；模板生成完成→进化引擎记录 |
| auto-skill-generator | 双向 | 自动调度→进化引擎触发；进化引擎决策→迭代建议反馈 |
| skill-ecosystem-steward | 单向→入 | 矩阵看板→判断Skill覆盖度 |
| trading-journal-ai | 单向→入 | 工作日志→识别可沉淀模式 |
| zero-cost-task-execution | 双向 | 成本原则→决策是否生成；新沉淀→反馈成本技巧 |

## 与 skill-template-generator 分工说明

```
用户工作 → [daily-skill-evolution-engine] → 识别"何时"+"什么需求"
                                          ↓
                              [skill-template-generator] → 生成"如何"+"完整模板"
                                          ↓
                              新SKILL.md 写入 ~/.workbuddy/skills/
                                          ↓
                              [skill-ecosystem-steward] → 录入看板+健康度评分
```

完整闭环：何时生成 ↔ 如何生成 ↔ 如何治理 ↔ 元调度 ↔ 成本约束

## 使用示例

### 自动触发（工作完成后）
完成8+步任务 → 自动扫描工作记录 → 判断是否需要沉淀 → 触发生成

### 手动触发
> "把今天的工作流沉淀成Skill" → 执行5步工作流

### 判断是否需要迭代
> "Skill迭代建议" → 扫描已有Skill + 当天工作 → 输出迭代建议清单

## 版本日志

- V1.0 (2026-06-27)：首次创建，5步工作流+6类触发场景
- V1.1 (2026-07-07)：新增与skill-template-generator分工说明，补充触发词"Skill模板、Skill怎么写"
- V1.1 (2026-07-23)：从工作记忆重建（reconstructed: true, 90%忠实度）
- V1.2 (2026-08-07)：新增第7类触发场景"成本控制"；决策规则新增成本评估；联动表新增 zero-cost-task-execution；闭环扩展为"+ 成本约束"

---

> 本引擎是"何时生成"的决策层，与 skill-template-generator（"如何生成"）、skill-ecosystem-steward（"如何治理"）和 zero-cost-task-execution（"成本约束"）形成四层闭环。
