---
title: "量化仪表盘主页"
category: Dashboard
subcategory: "仪表盘主页"
created: "2026-05-31 02:13"
updated: "2026-05-31 12:00"
tags: [仪表盘, 量化, 主页, 总览]
related: ["[[量化资产总览]]", "[[策略回测结果仪表盘]]", "[[交易记录仪表盘]]", "[[_MOC_量化交易总导航]]"]
description: "量化交易三大仪表盘的聚合主页，关键指标一目了然"
---

# 量化仪表盘主页

> 🕐 最后刷新: `= dateformat(date(now), "yyyy-MM-dd HH:mm")`

---

## 全局关键指标

```dataview
TABLE 
  length(rows) as "总文件数",
  round(sum(rows.file.size) / 1024, 1) as "总大小(KB)"
FROM "共享技能库/binance_skills/quant_data"
GROUP BY true as ""
```

---

## 仪表盘入口

| 仪表盘 | 功能 | 状态 |
|--------|------|------|
| [[量化资产总览仪表盘]] | 文件分类统计、时间线、标签分组 | ✅ 已激活 |
| [[策略回测结果仪表盘]] | 策略绩效矩阵、对比分析、优化路线图 | ✅ 已激活 |
| [[交易记录仪表盘]] | DOGE时间线、账户快照、仓位优化 | ✅ 已激活 |

---

## 策略状态速览

| 策略 | 版本 | 状态 |
|------|------|------|
| 龙虾黑马策略 | v1.0 / v3.0 | 🟡 待回测验证 |
| 龙虾通用趋势策略 | v1.0 / v3.0 | 🟡 待回测验证 |
| DOGE微账户作战方案 | v2.0 | 🟢 运行中 |

🟢运行中 | 🟡优化中 | 🔴已停用

---

## Phase1 进度追踪

```dataview
TASK
FROM "共享技能库/binance_skills/quant_data"
WHERE contains(tags, "phase1") OR contains(text, "Phase1")
LIMIT 20
```

---

## 快速导航

### 知识库核心文件

| 文件 | 类型 | 说明 |
|------|------|------|
| [[AI量化全链路执行计划_总览与风险矩阵]] | plan | 全局路线图与风险矩阵 |
| [[龙虾AI量化全链路体系_最终归档报告_v3.0]] | report | 全链路完整归档 |
| [[DOGE_Quant_Knowledge_Base]] | knowledge_base | DOGE策略知识库 |
| [[_MOC_量化交易总导航]] | moc | 全局知识导航 |

### PARA分区

- 📁 [[Projects/Quant-Phase1/README]] — 当前项目主页
- 📁 Areas/Quant-Trading — 量化交易领域
- 📁 Resources/Quant-References — 参考资源
- 📁 Archives/Quant-History — 历史归档

---

## 风险监控

| 风险项 | 等级 | 状态 |
|--------|------|------|
| 合约集中度超标 | 🔴 高 | ⚠️ 需立即调整 |
| 策略过拟合 | 🔴 高 | ⏳ 待回测验证 |
| 流动性枯竭 | 🔴 高 | ⚠️ 仅0.57 USDT |
| 情绪过热 | 🟡 中 | 👀 监控中 |

---

## 营收目标追踪

| 阶段 | 目标 | 当前 | 进度 |
|------|------|------|------|
| Phase 1 (Week 1-4) | 基础设施就绪 | 🟡 进行中 | ~40% |
| Phase 2 (Month 2-3) | 月收入 ¥5k+ | ⏳ 未开始 | 0% |
| Phase 3 (Month 4-6) | 月收入 ¥10k | ⏳ 未开始 | 0% |

---

> **MOC入口**: [[_MOC_量化交易总导航]] | **项目主页**: [[Projects/Quant-Phase1/README]]
