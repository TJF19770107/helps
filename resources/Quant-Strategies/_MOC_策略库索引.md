---
title: "MOC — 策略库索引"
category: MOC
subcategory: "策略索引"
created: "2026-05-31 12:00"
updated: "2026-05-31 12:00"
tags: [MOC, 策略库, 索引, 回测]
related: ["[[_MOC_量化交易总导航]]", "[[DOGE交易总览]]", "[[策略回测结果仪表盘]]"]
description: "所有量化策略的详细索引入口，按策略类型分组，含Dataview动态查询"
---

# MOC — 策略库索引

> 龙虾AI量化策略库的全量索引

---

## 策略分类总览

### 趋势跟踪策略
```dataview
TABLE version, description, file.mtime as "更新时间"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE contains(tags, "趋势跟踪") AND category = "Strategy"
SORT file.mtime DESC
```

### 事件驱动策略
```dataview
TABLE version, description, file.mtime as "更新时间"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE contains(tags, "事件驱动") AND category = "Strategy"
SORT file.mtime DESC
```

### 网格策略
```dataview
TABLE version, description, file.mtime as "更新时间"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE contains(tags, "网格") AND category = "Strategy"
SORT file.mtime DESC
```

### 马丁策略
```dataview
TABLE version, description, file.mtime as "更新时间"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE contains(tags, "马丁") AND category = "Strategy"
SORT file.mtime DESC
```

### 套利策略
```dataview
TABLE version, description, file.mtime as "更新时间"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE contains(tags, "套利") AND category = "Strategy"
SORT file.mtime DESC
```

---

## 全部策略清单
```dataview
TABLE 
  tags as "标签", 
  version as "版本", 
  file.mtime as "最后更新"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE category = "Strategy"
SORT file.mtime DESC
```

---

## 策略性能排名 (按夏普比率)
```dataview
TABLE 
  sharpe_ratio as "夏普比率",
  total_return as "收益率",
  max_drawdown as "最大回撤",
  win_rate as "胜率"
FROM "Resources/Quant-Strategies" OR "Areas/DOGE-Trading"
WHERE category = "Strategy" AND sharpe_ratio
SORT sharpe_ratio DESC
```

---

> **导航**: [[_MOC_量化交易总导航]] | [[DOGE交易总览]]
