---
title: "MOC — 量化交易知识总导航"
category: MOC
subcategory: "全局导航"
created: "2026-05-31 02:14"
updated: "2026-05-31 12:00"
tags: [MOC, 量化交易, 导航, 仪表盘]
related: ["[[DOGE交易总览]]", "[[策略库索引]]", "[[量化资产总览]]", "[[仪表盘主页_Dashboard_Home]]"]
description: "量化交易知识库的全局导航地图，覆盖PARA四分区、策略库、数据资产与仪表盘入口"
---

# MOC — 量化交易知识总导航

> 龙虾AI量化主控中心的知识地图（Map of Content）

---

## PARA 分区入口

| 分区 | 内容 | 入口 |
|------|------|------|
| Projects | 当前进行中的量化项目 | [[Projects/Quant-Phase1/README]] |
| Areas | 持续维护的量化交易领域知识 | [[Areas/DOGE-Trading/DOGE量化策略总纲]] |
| Resources | 参考材料与工具文档 | [[Resources/Quant-Strategies/_MOC_策略库索引]] |
| Archives | 历史项目与旧版策略 | [[Archives/归档索引]] |

---

## 核心文件导航

### 策略资产
```dataview
TABLE category, description, file.mtime as "最后修改"
FROM "Areas/DOGE-Trading" OR "Resources/Quant-Strategies"
WHERE category = "Strategy"
SORT file.name ASC
```

### 市场数据
```dataview
TABLE file.name, round(file.size/1024,1) as "KB", file.mtime as "修改时间"
FROM "Resources/Market-Data"
SORT file.name ASC
```

### 仪表盘
```dataview
TABLE description, file.mtime as "最后刷新"
FROM "Dashboards"
WHERE category = "Dashboard"
SORT file.name ASC
```

---

## 最新更新 (最近10个文件)
```dataview
LIST file.mtime
FROM ""
SORT file.mtime DESC
LIMIT 10
```

---

## 仪表盘入口

| 仪表盘 | 入口 |
|--------|------|
| 仪表盘主页 | [[仪表盘主页_Dashboard_Home]] |
| 资产总览 | [[量化资产总览]] |
| 策略回测 | [[策略回测结果仪表盘]] |
| 交易记录 | [[交易记录仪表盘]] |

---

> **最后更新**: 2026-05-31
