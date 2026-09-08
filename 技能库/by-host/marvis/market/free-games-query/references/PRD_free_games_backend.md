# 限免游戏数据服务 — 后台接口需求

| 字段 | 内容 |
|------|------|
| 需求提出人 | pecentlv |
| 需求日期 | 2026-04-10 |
| 优先级 | P1 |
| 状态 | 待评审 |

---

## 一、需求背景

应用宝 AI 助手提供"喜加一速报"功能，需要定时获取 Steam / Epic 平台的限时免费游戏数据。现需后台提供数据爬取入库和查询接口，用户侧通过调用后台接口获取数据。

---

## 二、功能目标

1. **定时爬取**：后台定时从 Steam、Epic 官方接口获取限时免费游戏数据，清洗后入库
2. **查询接口**：提供 HTTP API，支持按平台、状态过滤查询已入库的限免游戏列表
3. **数据完整**：每条游戏数据需包含游戏名、平台、原价、是否支持中文、限免时间、商店链接等字段

---

## 三、交互流程

```
服务端定时任务（每小时）
    │
    ├─→ 爬取 Steam / Epic 官方接口
    ├─→ 数据清洗（去重、过滤永久F2P、统一格式）
    └─→ 写入数据库（UPSERT）
              │
              ↓
用户侧请求 GET /api/free-games
              │
              ↓
返回 JSON（已入库的限免游戏列表）
```

---

## 四、需求功能点概述

| 编号 | 功能点 | 简要说明 |
|------|--------|----------|
| F1 | Steam 数据爬取 | 定时调用 Steam 官方接口，获取限时免费游戏并入库 |
| F2 | Epic 数据爬取 | 定时调用 Epic 官方接口，获取当前限免 + 即将限免游戏并入库 |
| F3 | GamerPower 兜底 | 定时调用 GamerPower API 作为补充源，与主源去重后入库 |
| F4 | 数据清洗 | 去重、过滤永久F2P、统一数据格式、清理已过期数据 |
| F5 | 查询接口 | 提供 HTTP API，支持按平台和状态过滤，返回限免游戏列表 |
| F6 | 容错与降级 | 接口不可用时使用上次入库数据，字段缺失填 null 不阻塞入库 |

---

## 五、功能点详细描述

### F1：Steam 数据爬取

**爬取频率**：每小时 1 次

**数据源接口**：

| 接口 | 地址 | 用途 |
|------|------|------|
| featuredcategories | `store.steampowered.com/api/featuredcategories?cc=cn&l=schinese` | 获取特惠/限免分类列表 |
| appdetails | `store.steampowered.com/api/appdetails?appids={id}&cc=cn&l=schinese` | 获取游戏详情（价格、语言支持等）|

均为 Steam 公开接口，无需 API Key。

**爬取逻辑**：

1. 调用 `featuredcategories`，从返回的特惠分类中筛选当前价格为 0（折扣 100%）的游戏
2. 对每个游戏调用 `appdetails` 补充详情
3. 过滤永久免费游戏（`is_free=true` 且 `price_overview.initial=0`，即原价就是 0 的游戏）
4. 入库

**需提取的字段**：

| 字段 | 取值来源 | 说明 |
|------|----------|------|
| name | `appdetails.name` | 游戏名称 |
| original_price_cents | `price_overview.initial` | 原价（单位：分）|
| has_chinese | `supported_languages` 中是否包含"简体中文" | 中文支持 |
| store_link | 拼接 `https://store.steampowered.com/app/{appid}` | 商店链接 |
| cover_image | `header_image` | 封面图 |

**频率限制**：每次 `appdetails` 请求间隔 ≥ 1 秒，避免触发 Steam 频控。

---

### F2：Epic 数据爬取

**爬取频率**：每小时 1 次

**数据源接口**：

| 接口 | 地址 | 用途 |
|------|------|------|
| freeGamesPromotions | `store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN` | 获取当前限免 + 即将限免 |

公开接口，无需认证。

**爬取逻辑**：

1. 调用 `freeGamesPromotions`
2. 从 `promotions.promotionalOffers` 提取当前限免（`discountPercentage=0` 表示免费）
3. 从 `promotions.upcomingPromotionalOffers` 提取即将限免
4. 商店链接 slug 按三级降级取值：`offerMappings[].pageSlug` → `catalogNs.mappings[].pageSlug` → `productSlug`
5. 中文支持检测：从 `customAttributes` 中获取语言信息；如无法获取，标记为 `null`（**不爬 HTML**）
6. 入库

**需提取的字段**：

| 字段 | 取值来源 | 说明 |
|------|----------|------|
| name | `title` | 游戏名称 |
| original_price_cents | `price.totalPrice.originalPrice` | 原价（单位：分）|
| has_chinese | `customAttributes` 中语言字段，无法获取则为 `null` | 中文支持 |
| start_time | `promotionalOffers[].startDate` | 限免开始时间 |
| end_time | `promotionalOffers[].endDate` | 限免结束时间 |
| store_link | 拼接 `https://store.epicgames.com/zh-CN/p/{slug}` | 商店链接 |
| cover_image | `keyImages` 中 type 为 `OfferImageWide` 的 URL | 封面图 |

---

### F3：GamerPower 兜底

**爬取频率**：每 6 小时 1 次

**数据源接口**：

| 接口 | 地址 |
|------|------|
| giveaways | `gamerpower.com/api/giveaways?platform=steam&type=game&sort-by=value` |

**定位**：备选补充源，不作为主数据来源。用于发现 Steam/Epic 主源可能遗漏的限免活动。

**处理逻辑**：爬取后与已入库的主源数据按游戏名去重，仅补充主源中没有的游戏。

---

### F4：数据清洗

在每次爬取写入数据库前，执行以下清洗：

| 步骤 | 说明 |
|------|------|
| 去重 | 同一游戏被多个数据源返回时，优先保留主源（Steam/Epic官方接口）数据 |
| 过滤永久 F2P | 原价为 0 的永久免费游戏不入库 |
| 统一数据格式 | 所有数据源统一为同一 JSON 结构（见 F5 响应字段） |
| 过期数据处理 | 已过期活动不再通过 API 返回，数据库中保留 30 天后清理 |

**数据库唯一键**：`(platform, app_id)`，写入使用 UPSERT。

---

### F5：查询接口

#### 接口地址

```
GET /api/free-games
```

#### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| platform | string | 否 | 过滤平台：`steam` / `epic` / `all`（默认 `all`）|
| status | string | 否 | 过滤状态：`current`（当前限免）/ `upcoming`（即将限免）/ `all`（默认 `all`）|

#### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "update_time": "2026-04-10T16:00:00+08:00",
    "games": [
      {
        "name": "Graveyard Keeper",
        "platform": "steam",
        "status": "current",
        "original_price_cents": 7600,
        "original_price_display": "¥76",
        "currency": "CNY",
        "has_chinese": true,
        "start_time": "2026-04-07T00:00:00+08:00",
        "end_time": "2026-04-13T23:59:00+08:00",
        "store_link": "https://store.steampowered.com/app/599140",
        "cover_image": "https://cdn.cloudflare.steamstatic.com/steam/apps/599140/header.jpg",
        "app_id": "599140",
        "source": "steam_api"
      }
    ]
  }
}
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| update_time | string | 数据最近一次更新时间（ISO 8601） |
| name | string | 游戏名称（英文原名）|
| platform | string | 平台：`steam` / `epic` |
| status | string | `current`（当前限免）/ `upcoming`（即将限免）|
| original_price_cents | int | 原价，单位：分（如 7600 = ¥76）|
| original_price_display | string | 原价展示文本（如 "¥76"）|
| currency | string | 货币类型，默认 `CNY` |
| has_chinese | bool / null | 是否支持简体中文。`true` / `false` / `null`（未知）|
| start_time | string | 限免开始时间（ISO 8601）|
| end_time | string | 限免结束时间（ISO 8601）|
| store_link | string | 商店页链接 |
| cover_image | string | 游戏封面图 URL |
| app_id | string | 平台侧游戏 ID（Steam 为数字 appid，Epic 为 slug）|
| source | string | 数据来源标识：`steam_api` / `epic_api` / `gamerpower` |

#### 错误响应

```json
{
  "code": -1,
  "message": "数据获取失败，请稍后重试",
  "data": null
}
```

---

### F6：容错与降级

| 场景 | 处理方式 |
|------|----------|
| Steam API 超时/不可用 | 使用上次成功入库的数据，`update_time` 保持上次时间 |
| Epic API 超时/不可用 | 同上 |
| 某个字段获取失败（如 has_chinese） | 该字段填 `null`，不阻塞整条数据入库 |
| GamerPower 不可用 | 跳过，不影响主流程 |
| 连续 3 次爬取失败 | 告警通知 |
| 数据超过 3 小时未更新 | 告警通知 |

---

## 六、里程碑建议

| 阶段 | 内容 | 预计周期 |
|------|------|----------|
| M1 | 爬取模块开发（F1 + F2）| 3~5 天 |
| M2 | 数据库设计 + 查询接口（F4 + F5）| 2~3 天 |
| M3 | 联调 | 1~2 天 |
| M4 | GamerPower 兜底 + 容错告警（F3 + F6）| 2~3 天 |

---

## 附录：现有脚本参考

当前用户侧已有一版 Python 爬虫脚本（`free-games-query/scripts/query_free_games.py`），其中的接口调用和字段解析逻辑可供参考：

- Steam `appdetails` 字段解析（永久免费过滤、中文检测、价格提取）
- Epic `freeGamesPromotions` 的 promotionalOffers 解析逻辑
- Epic 商店链接 slug 三级降级：`offerMappings` → `catalogNs.mappings` → `productSlug`
