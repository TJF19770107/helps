---
description: "Auto-generated skill"
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_29508ed1693211f1a99c5254007bceed
    ReservedCode1: 9QGErYMsW6dMhWvVQ6tXOS+oUOeKWrqh+4l0DWd7BfbgBzg/eojqjNVbqSnCmYrVcCEE+mao57lZnTsQX0RmLaNO3wrde6MLbpHy2lxgfVis5ephvZXZWsfEfe9+VSff04miw97nJPO+If1wmWQ/jD1XIGZLl7WnFZ2si42CF7Jf3bjX+7pU9rQ/XPw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_29508ed1693211f1a99c5254007bceed
    ReservedCode2: 9QGErYMsW6dMhWvVQ6tXOS+oUOeKWrqh+4l0DWd7BfbgBzg/eojqjNVbqSnCmYrVcCEE+mao57lZnTsQX0RmLaNO3wrde6MLbpHy2lxgfVis5ephvZXZWsfEfe9+VSff04miw97nJPO+If1wmWQ/jD1XIGZLl7WnFZ2si42CF7Jf3bjX+7pU9rQ/XPw=
---

# PM-Skills 产品经理全技能包

> 聚合入口技能：一个技能入口，68项子技能内部调用，CC Switch面板仅显示1项。
> 触发指令：`/pm-skills`

---

## 技能概览

| 属性 | 值 |
|------|-----|
| 技能名称 | PM-Skills 产品经理全技能包 |
| 技能标识 | pm-skills |
| 触发指令 | `/pm-skills` |
| 子技能总数 | 68 |
| 链式工作流 | 42 |
| 插件模块 | 9 |
| 版本 | 1.0.0 |
| 来源 | GitHub: phuryn/pm-skills (MIT) |

---

## 9大产品模块

### 1. 产品发现 (pm-product-discovery) — 13技能
触发指令：`/产品发现` `/discover` `/brainstorm` `/triage-requests` `/interview` `/setup-metrics`
- 头脑风暴（新产品/现有产品）、实验设计、假设识别与优先级排序
- 机会解决方案树（Teresa Torres）、功能请求分析、用户访谈脚本与总结
- 指标看板设计（北极星指标+输入指标+告警阈值）

### 2. 产品战略 (pm-product-strategy) — 12技能
触发指令：`/产品战略` `/strategy` `/business-model` `/market-scan` `/pricing` `/value-proposition`
- Ansoff矩阵、波特五力、SWOT分析、PESTLE分析
- 精益画布、商业模式、盈利策略、定价策略
- 产品愿景、价值主张、启动画布

### 3. 市场研究 (pm-market-research) — 7技能
触发指令：`/市场研究` `/competitive-analysis` `/research-users` `/analyze-feedback`
- 竞品分析、用户画像、市场细分、市场规模估算
- 客户旅程地图、情感分析、用户细分

### 4. 执行交付 (pm-execution) — 16技能
触发指令：`/执行交付` `/write-prd` `/write-stories` `/sprint` `/plan-okrs` `/pre-mortem` `/red-team-prd` `/meeting-notes` `/stakeholder-map` `/generate-data` `/test-scenarios` `/transform-roadmap`
- PRD撰写、用户故事、Job Stories、OKR头脑风暴
- 冲刺规划、复盘、利益相关者地图、发布说明
- 预尸检分析、策略红队审查、WWAS框架

### 5. 市场进入 (pm-go-to-market) — 6技能
触发指令：`/市场进入` `/plan-launch` `/battlecard` `/growth-strategy`
- GTM策略、增长循环、竞争对战卡
- 滩头阵地区隔、理想客户画像

### 6. 数据分析 (pm-data-analytics) — 3技能
触发指令：`/数据分析` `/analyze-test` `/analyze-cohorts` `/write-query`
- A/B测试分析、队列分析、SQL查询

### 7. 营销增长 (pm-marketing-growth) — 5技能
触发指令：`/营销增长` `/market-product` `/north-star`
- 北极星指标、定位创意、价值主张语句
- 产品命名、营销创意

### 8. AI交付 (pm-ai-shipping) — 2技能
触发指令：`/AI交付` `/ship-check` `/security-audit-static` `/performance-audit-static` `/document-app` `/derive-tests`
- 意图vs实现审查、交付产物清单
- 安全静态审计、性能静态审计

### 9. 工具箱 (pm-toolkit) — 4技能
触发指令：`/工具箱` `/draft-nda` `/privacy-policy` `/proofread` `/review-resume` `/tailor-resume`
- NDA起草、隐私政策、语法检查、简历审阅

---

## 链式工作流

输入以下指令自动触发全流程串行执行：

| 工作流指令 | 串联模块 | 说明 |
|-----------|---------|------|
| `/完整产品落地流程` | 发现→战略→执行→市场→数据 | 从0到1全流程 |
| `/新产品立项流程` | 发现→战略→执行 | 新产品从创意到PRD |
| `/产品上线流程` | 执行→市场→AI交付 | 开发完成到上线 |
| `/市场调研全流程` | 市场研究→战略 | 调研到战略决策 |
| `/数据驱动迭代` | 数据→执行 | A/B测试驱动迭代 |

---

## 使用方式

1. **激活聚合技能**：在对话中输入 `/pm-skills`
2. **查看分类菜单**：自动展示9大模块分类索引
3. **调用子技能**：输入对应子指令（如 `/write-prd` `/竞品分析` `/swot分析`）
4. **执行链式流**：输入链式工作流指令（如 `/完整产品落地流程`）

---

## 子技能索引

完整68项子技能映射详见：[PM-Skills-索引.md](./PM-Skills-索引.md)

---

*技能包基于 phuryn/pm-skills (MIT License)，由龙虾AI主控中心聚合部署。*
*68项子技能全部封装在内部，CC Switch面板仅显示1个聚合入口。*
*（内容由AI生成，仅供参考）*
