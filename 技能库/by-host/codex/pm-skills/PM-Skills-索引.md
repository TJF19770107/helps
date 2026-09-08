# PM Skills — 产品经理技能包完整索引

> 生成日期：2026-06-16 | 目标路径：`E:\龙虾AI主控中心\我的AI分身\技能库\pm-skills\`

---

## 统计概览

| 指标 | 数量 |
|------|------|
| 技能插件（Plugins） | 9 |
| 技能文件（Skills） | 68 |
| 快捷命令（Slash Commands） | 42 |
| 文档（Docs） | 7 |
| PM Brain 模板 | 5 |

---

## 急速索引 — 子指令速查

> 输入 `/pm-skills` 激活聚合技能包，然后输入以下任意子指令直接调用对应功能。

### 按PM阶段分类

| 阶段 | 快捷指令 | 模块 | 技能数 |
|------|---------|------|--------|
| 🧭 产品发现 | `/产品发现` `/discover` `/brainstorm` `/interview` `/triage-requests` `/setup-metrics` | product-discovery | 13 |
| 🎯 产品战略 | `/产品战略` `/strategy` `/business-model` `/market-scan` `/pricing` `/value-proposition` | product-strategy | 12 |
| 🔍 市场研究 | `/市场研究` `/competitive-analysis` `/research-users` `/analyze-feedback` | market-research | 7 |
| ⚡ 执行交付 | `/执行交付` `/write-prd` `/write-stories` `/sprint` `/plan-okrs` `/pre-mortem` `/red-team-prd` `/meeting-notes` | execution | 16 |
| 🚀 市场进入 | `/市场进入` `/plan-launch` `/battlecard` `/growth-strategy` | go-to-market | 6 |
| 📊 数据分析 | `/数据分析` `/analyze-test` `/analyze-cohorts` `/write-query` | data-analytics | 3 |
| 📈 营销增长 | `/营销增长` `/market-product` `/north-star` | marketing-growth | 5 |
| 🤖 AI交付 | `/AI交付` `/ship-check` `/security-audit-static` `/performance-audit-static` | ai-shipping | 2 |
| 🛠 工具箱 | `/工具箱` `/draft-nda` `/privacy-policy` `/proofread` `/review-resume` | toolkit | 4 |

### 链式工作流（一键串联多阶段）

| 工作流指令 | 串联阶段 | 说明 |
|-----------|---------|------|
| `/完整产品落地流程` | 发现→战略→执行→市场→数据 | 从0到1全流程，串联5个阶段子技能 |
| `/新产品立项流程` | 发现→战略→执行 | 新产品从创意验证到PRD交付 |
| `/产品上线流程` | 执行→市场→AI交付 | 开发完成→GTM策略→发布审计 |
| `/市场调研全流程` | 市场研究→战略 | 调研→分析→战略决策输出 |
| `/数据驱动迭代` | 数据→执行 | A/B测试→数据分析→迭代PRD |

### 高频子指令 Top 15

| # | 指令 | 所属模块 | 用途 |
|---|------|--------|------|
| 1 | `/write-prd` | 执行交付 | 撰写产品需求文档 |
| 2 | `/write-stories` | 执行交付 | 生成用户故事 |
| 3 | `/competitive-analysis` | 市场研究 | 竞品分析 |
| 4 | `/brainstorm` | 产品发现 | 头脑风暴 |
| 5 | `/strategy` | 产品战略 | 产品战略规划 |
| 6 | `/plan-okrs` | 执行交付 | OKR规划 |
| 7 | `/research-users` | 市场研究 | 用户调研 |
| 8 | `/analyze-test` | 数据分析 | A/B测试分析 |
| 9 | `/sprint` | 执行交付 | 冲刺规划 |
| 10 | `/pricing` | 产品战略 | 定价策略 |
| 11 | `/business-model` | 产品战略 | 商业模式分析 |
| 12 | `/battlecard` | 市场进入 | 竞争对战卡 |
| 13 | `/meeting-notes` | 执行交付 | 会议纪要 |
| 14 | `/plan-launch` | 市场进入 | 上市计划 |
| 15 | `/ship-check` | AI交付 | 发布检查清单 |

---

## 客户端兼容性标注

| 客户端 | 兼容性 | 说明 |
|--------|--------|------|
| **CC Switch** | ✅ 主适配 | 龙虾AI主控中心多Agent客户端，默认目标平台 |
| Claude Code / Claude Desktop | ✅ 原生 | 源码设计目标平台，全部插件原生支持 |
| Codex (OpenAI) | ✅ 兼容 | 技能文件为 Markdown 格式，可直接导入 |
| Gemini (Google) | ✅ 兼容 | 技能文件可适配 Gemini System Prompt 格式 |
| OpenCode | ✅ 兼容 | 开放标准 Markdown Skills 格式 |
| Hermes | ✅ 兼容 | 开源 Agent 框架，支持 Markdown Skill 加载 |

---

## 一、插件与技能清单

### 1. pm-ai-shipping（AI 交付与发布）
**技能（2项）**

| 技能名 | 文件路径 |
|--------|----------|
| intended-vs-implemented | `skills/pm-ai-shipping/intended-vs-implemented.md` |
| shipping-artifacts | `skills/pm-ai-shipping/shipping-artifacts.md` |

**命令（5项）**

| 命令 | 文件路径 |
|------|----------|
| derive-tests | `slash-commands/pm-ai-shipping/derive-tests.md` |
| document-app | `slash-commands/pm-ai-shipping/document-app.md` |
| performance-audit-static | `slash-commands/pm-ai-shipping/performance-audit-static.md` |
| security-audit-static | `slash-commands/pm-ai-shipping/security-audit-static.md` |
| ship-check | `slash-commands/pm-ai-shipping/ship-check.md` |

---

### 2. pm-data-analytics（数据分析）
**技能（3项）**

| 技能名 | 文件路径 |
|--------|----------|
| ab-test-analysis | `skills/pm-data-analytics/ab-test-analysis.md` |
| cohort-analysis | `skills/pm-data-analytics/cohort-analysis.md` |
| sql-queries | `skills/pm-data-analytics/sql-queries.md` |

**命令（3项）**

| 命令 | 文件路径 |
|------|----------|
| analyze-cohorts | `slash-commands/pm-data-analytics/analyze-cohorts.md` |
| analyze-test | `slash-commands/pm-data-analytics/analyze-test.md` |
| write-query | `slash-commands/pm-data-analytics/write-query.md` |

---

### 3. pm-execution（执行交付）
**技能（16项）**

| 技能名 | 文件路径 |
|--------|----------|
| brainstorm-okrs | `skills/pm-execution/brainstorm-okrs.md` |
| create-prd | `skills/pm-execution/create-prd.md` |
| dummy-dataset | `skills/pm-execution/dummy-dataset.md` |
| job-stories | `skills/pm-execution/job-stories.md` |
| outcome-roadmap | `skills/pm-execution/outcome-roadmap.md` |
| pre-mortem | `skills/pm-execution/pre-mortem.md` |
| prioritization-frameworks | `skills/pm-execution/prioritization-frameworks.md` |
| release-notes | `skills/pm-execution/release-notes.md` |
| retro | `skills/pm-execution/retro.md` |
| sprint-plan | `skills/pm-execution/sprint-plan.md` |
| stakeholder-map | `skills/pm-execution/stakeholder-map.md` |
| strategy-red-team | `skills/pm-execution/strategy-red-team.md` |
| summarize-meeting | `skills/pm-execution/summarize-meeting.md` |
| test-scenarios | `skills/pm-execution/test-scenarios.md` |
| user-stories | `skills/pm-execution/user-stories.md` |
| wwas | `skills/pm-execution/wwas.md` |

**命令（11项）**

| 命令 | 文件路径 |
|------|----------|
| generate-data | `slash-commands/pm-execution/generate-data.md` |
| meeting-notes | `slash-commands/pm-execution/meeting-notes.md` |
| plan-okrs | `slash-commands/pm-execution/plan-okrs.md` |
| pre-mortem | `slash-commands/pm-execution/pre-mortem.md` |
| red-team-prd | `slash-commands/pm-execution/red-team-prd.md` |
| sprint | `slash-commands/pm-execution/sprint.md` |
| stakeholder-map | `slash-commands/pm-execution/stakeholder-map.md` |
| test-scenarios | `slash-commands/pm-execution/test-scenarios.md` |
| transform-roadmap | `slash-commands/pm-execution/transform-roadmap.md` |
| write-prd | `slash-commands/pm-execution/write-prd.md` |
| write-stories | `slash-commands/pm-execution/write-stories.md` |

---

### 4. pm-go-to-market（市场进入）
**技能（6项）**

| 技能名 | 文件路径 |
|--------|----------|
| beachhead-segment | `skills/pm-go-to-market/beachhead-segment.md` |
| competitive-battlecard | `skills/pm-go-to-market/competitive-battlecard.md` |
| growth-loops | `skills/pm-go-to-market/growth-loops.md` |
| gtm-motions | `skills/pm-go-to-market/gtm-motions.md` |
| gtm-strategy | `skills/pm-go-to-market/gtm-strategy.md` |
| ideal-customer-profile | `skills/pm-go-to-market/ideal-customer-profile.md` |

**命令（3项）**

| 命令 | 文件路径 |
|------|----------|
| battlecard | `slash-commands/pm-go-to-market/battlecard.md` |
| growth-strategy | `slash-commands/pm-go-to-market/growth-strategy.md` |
| plan-launch | `slash-commands/pm-go-to-market/plan-launch.md` |

---

### 5. pm-market-research（市场研究）
**技能（7项）**

| 技能名 | 文件路径 |
|--------|----------|
| competitor-analysis | `skills/pm-market-research/competitor-analysis.md` |
| customer-journey-map | `skills/pm-market-research/customer-journey-map.md` |
| market-segments | `skills/pm-market-research/market-segments.md` |
| market-sizing | `skills/pm-market-research/market-sizing.md` |
| sentiment-analysis | `skills/pm-market-research/sentiment-analysis.md` |
| user-personas | `skills/pm-market-research/user-personas.md` |
| user-segmentation | `skills/pm-market-research/user-segmentation.md` |

**命令（3项）**

| 命令 | 文件路径 |
|------|----------|
| analyze-feedback | `slash-commands/pm-market-research/analyze-feedback.md` |
| competitive-analysis | `slash-commands/pm-market-research/competitive-analysis.md` |
| research-users | `slash-commands/pm-market-research/research-users.md` |

---

### 6. pm-marketing-growth（营销增长）
**技能（5项）**

| 技能名 | 文件路径 |
|--------|----------|
| marketing-ideas | `skills/pm-marketing-growth/marketing-ideas.md` |
| north-star-metric | `skills/pm-marketing-growth/north-star-metric.md` |
| positioning-ideas | `skills/pm-marketing-growth/positioning-ideas.md` |
| product-name | `skills/pm-marketing-growth/product-name.md` |
| value-prop-statements | `skills/pm-marketing-growth/value-prop-statements.md` |

**命令（2项）**

| 命令 | 文件路径 |
|------|----------|
| market-product | `slash-commands/pm-marketing-growth/market-product.md` |
| north-star | `slash-commands/pm-marketing-growth/north-star.md` |

---

### 7. pm-product-discovery（产品发现）
**技能（13项）**

| 技能名 | 文件路径 |
|--------|----------|
| analyze-feature-requests | `skills/pm-product-discovery/analyze-feature-requests.md` |
| brainstorm-experiments-existing | `skills/pm-product-discovery/brainstorm-experiments-existing.md` |
| brainstorm-experiments-new | `skills/pm-product-discovery/brainstorm-experiments-new.md` |
| brainstorm-ideas-existing | `skills/pm-product-discovery/brainstorm-ideas-existing.md` |
| brainstorm-ideas-new | `skills/pm-product-discovery/brainstorm-ideas-new.md` |
| identify-assumptions-existing | `skills/pm-product-discovery/identify-assumptions-existing.md` |
| identify-assumptions-new | `skills/pm-product-discovery/identify-assumptions-new.md` |
| interview-script | `skills/pm-product-discovery/interview-script.md` |
| metrics-dashboard | `skills/pm-product-discovery/metrics-dashboard.md` |
| opportunity-solution-tree | `skills/pm-product-discovery/opportunity-solution-tree.md` |
| prioritize-assumptions | `skills/pm-product-discovery/prioritize-assumptions.md` |
| prioritize-features | `skills/pm-product-discovery/prioritize-features.md` |
| summarize-interview | `skills/pm-product-discovery/summarize-interview.md` |

**命令（5项）**

| 命令 | 文件路径 |
|------|----------|
| brainstorm | `slash-commands/pm-product-discovery/brainstorm.md` |
| discover | `slash-commands/pm-product-discovery/discover.md` |
| interview | `slash-commands/pm-product-discovery/interview.md` |
| setup-metrics | `slash-commands/pm-product-discovery/setup-metrics.md` |
| triage-requests | `slash-commands/pm-product-discovery/triage-requests.md` |

---

### 8. pm-product-strategy（产品战略）
**技能（12项）**

| 技能名 | 文件路径 |
|--------|----------|
| ansoff-matrix | `skills/pm-product-strategy/ansoff-matrix.md` |
| business-model | `skills/pm-product-strategy/business-model.md` |
| lean-canvas | `skills/pm-product-strategy/lean-canvas.md` |
| monetization-strategy | `skills/pm-product-strategy/monetization-strategy.md` |
| pestle-analysis | `skills/pm-product-strategy/pestle-analysis.md` |
| porters-five-forces | `skills/pm-product-strategy/porters-five-forces.md` |
| pricing-strategy | `skills/pm-product-strategy/pricing-strategy.md` |
| product-strategy | `skills/pm-product-strategy/product-strategy.md` |
| product-vision | `skills/pm-product-strategy/product-vision.md` |
| startup-canvas | `skills/pm-product-strategy/startup-canvas.md` |
| swot-analysis | `skills/pm-product-strategy/swot-analysis.md` |
| value-proposition | `skills/pm-product-strategy/value-proposition.md` |

**命令（5项）**

| 命令 | 文件路径 |
|------|----------|
| business-model | `slash-commands/pm-product-strategy/business-model.md` |
| market-scan | `slash-commands/pm-product-strategy/market-scan.md` |
| pricing | `slash-commands/pm-product-strategy/pricing.md` |
| strategy | `slash-commands/pm-product-strategy/strategy.md` |
| value-proposition | `slash-commands/pm-product-strategy/value-proposition.md` |

---

### 9. pm-toolkit（工具箱）
**技能（4项）**

| 技能名 | 文件路径 |
|--------|----------|
| draft-nda | `skills/pm-toolkit/draft-nda.md` |
| grammar-check | `skills/pm-toolkit/grammar-check.md` |
| privacy-policy | `skills/pm-toolkit/privacy-policy.md` |
| review-resume | `skills/pm-toolkit/review-resume.md` |

**命令（5项）**

| 命令 | 文件路径 |
|------|----------|
| draft-nda | `slash-commands/pm-toolkit/draft-nda.md` |
| privacy-policy | `slash-commands/pm-toolkit/privacy-policy.md` |
| proofread | `slash-commands/pm-toolkit/proofread.md` |
| review-resume | `slash-commands/pm-toolkit/review-resume.md` |
| tailor-resume | `slash-commands/pm-toolkit/tailor-resume.md` |

---

## 二、42套链式工作流（Slash Commands）

| # | 命令 | 所属插件 | PM阶段 |
|---|------|----------|--------|
| 1 | brainstorm | pm-product-discovery | 发现 |
| 2 | discover | pm-product-discovery | 发现 |
| 3 | interview | pm-product-discovery | 发现 |
| 4 | setup-metrics | pm-product-discovery | 发现 |
| 5 | triage-requests | pm-product-discovery | 发现 |
| 6 | business-model | pm-product-strategy | 战略 |
| 7 | market-scan | pm-product-strategy | 战略 |
| 8 | pricing | pm-product-strategy | 战略 |
| 9 | strategy | pm-product-strategy | 战略 |
| 10 | value-proposition | pm-product-strategy | 战略 |
| 11 | write-prd | pm-execution | 执行 |
| 12 | write-stories | pm-execution | 执行 |
| 13 | sprint | pm-execution | 执行 |
| 14 | plan-okrs | pm-execution | 执行 |
| 15 | pre-mortem | pm-execution | 执行 |
| 16 | red-team-prd | pm-execution | 执行 |
| 17 | meeting-notes | pm-execution | 执行 |
| 18 | stakeholder-map | pm-execution | 执行 |
| 19 | generate-data | pm-execution | 执行 |
| 20 | test-scenarios | pm-execution | 执行 |
| 21 | transform-roadmap | pm-execution | 执行 |
| 22 | analyze-feedback | pm-market-research | 研究 |
| 23 | competitive-analysis | pm-market-research | 研究 |
| 24 | research-users | pm-market-research | 研究 |
| 25 | battlecard | pm-go-to-market | 市场 |
| 26 | growth-strategy | pm-go-to-market | 市场 |
| 27 | plan-launch | pm-go-to-market | 市场 |
| 28 | analyze-cohorts | pm-data-analytics | 数据 |
| 29 | analyze-test | pm-data-analytics | 数据 |
| 30 | write-query | pm-data-analytics | 数据 |
| 31 | market-product | pm-marketing-growth | 增长 |
| 32 | north-star | pm-marketing-growth | 增长 |
| 33 | derive-tests | pm-ai-shipping | 发布 |
| 34 | document-app | pm-ai-shipping | 发布 |
| 35 | performance-audit-static | pm-ai-shipping | 发布 |
| 36 | security-audit-static | pm-ai-shipping | 发布 |
| 37 | ship-check | pm-ai-shipping | 发布 |
| 38 | draft-nda | pm-toolkit | 工具箱 |
| 39 | privacy-policy | pm-toolkit | 工具箱 |
| 40 | proofread | pm-toolkit | 工具箱 |
| 41 | review-resume | pm-toolkit | 工具箱 |
| 42 | tailor-resume | pm-toolkit | 工具箱 |

---

## 三、目录结构总览

```
pm-skills/
├── PM-Skills-索引.md            ← 本文件
├── skills/                      ← 68 项技能（按插件分文件夹）
│   ├── pm-ai-shipping/
│   ├── pm-data-analytics/
│   ├── pm-execution/
│   ├── pm-go-to-market/
│   ├── pm-market-research/
│   ├── pm-marketing-growth/
│   ├── pm-product-discovery/
│   ├── pm-product-strategy/
│   └── pm-toolkit/
├── slash-commands/              ← 42 条快捷命令
│   ├── pm-ai-shipping/
│   ├── pm-data-analytics/
│   ├── pm-execution/
│   ├── pm-go-to-market/
│   ├── pm-market-research/
│   ├── pm-marketing-growth/
│   ├── pm-product-discovery/
│   ├── pm-product-strategy/
│   └── pm-toolkit/
├── plugins/                     ← 9 个完整插件目录
│   ├── pm-ai-shipping/
│   ├── pm-data-analytics/
│   ├── pm-execution/
│   ├── pm-go-to-market/
│   ├── pm-market-research/
│   ├── pm-marketing-growth/
│   ├── pm-product-discovery/
│   ├── pm-product-strategy/
│   └── pm-toolkit/
├── docs/                        ← 项目文档
│   ├── README.md
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   ├── validate_plugins.py
│   └── marketplace.json
└── pm-brain/                    ← PM 知识库
    ├── README.md
    ├── INDEX.md
    ├── PRD模板.md
    ├── 复盘模板.md
    └── 市场分析模板.md
```

---

## 四、技能覆盖矩阵（PM 全流程）

| PM 阶段 | 插件 | 技能数 | 命令数 | 核心能力 |
|---------|------|--------|--------|----------|
| 产品发现 | pm-product-discovery | 13 | 5 | 头脑风暴、用户访谈、假设验证、需求优先级 |
| 产品战略 | pm-product-strategy | 12 | 5 | SWOT、波特五力、精益画布、定价策略 |
| 市场研究 | pm-market-research | 7 | 3 | 竞品分析、用户画像、市场细分 |
| 执行交付 | pm-execution | 16 | 11 | PRD、OKR、冲刺规划、复盘、用户故事 |
| 市场进入 | pm-go-to-market | 6 | 3 | GTM策略、增长循环、客群画像 |
| 数据分析 | pm-data-analytics | 3 | 3 | A/B测试、队列分析、SQL查询 |
| 营销增长 | pm-marketing-growth | 5 | 2 | 北极星指标、定位、价值主张 |
| AI 交付 | pm-ai-shipping | 2 | 5 | 安全审计、性能检查、发布清单 |
| 工具箱 | pm-toolkit | 4 | 5 | NDA、隐私政策、简历审阅 |
| **合计** | **9 插件** | **68** | **42** | — |

---

*索引文件由龙虾AI主控中心自动生成。文件路径均为相对于 `E:\龙虾AI主控中心\我的AI分身\技能库\pm-skills\` 的相对路径。*
