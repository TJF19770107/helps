# 🎣 钓鱼天气顾问 (Fishing Advisor)

> 一个基于 fishweather.cn 数据的智能钓鱼天气分析 Skill，自动爬取专业垂钓气象数据，生成包含钓鱼指数、三要素趋势分析、鱼种推荐的交互式 HTML 报告。

## ✨ 功能特性

- **IP 自动定位**：无需手动输入城市，自动通过 IP 识别当前所在城市
- **专业数据源**：从 fishweather.cn 爬取全量垂钓气象数据（钓鱼指数、气压、水温、溶氧、月相等）
- **三要素趋势分析**：溶氧/水温/气压 24 小时变化趋势，平滑曲线展示，支持点击切换
- **鱼种智能推荐**：多搜索引擎（Bing → 搜狗 → 百度）搜索当地活跃鱼种，含区域兜底数据库
- **7 天钓鱼预报**：展示未来一周钓鱼指数变化趋势
- **月相信息**：优先使用爬取数据，计算公式作为兜底
- **交互式 HTML 报告**：深色星空主题，环形仪表盘，24h/7d Tab 切换，hover 显示详细数据
- **渐变色带**：按小时展示钓鱼窗口期，直观呈现最佳垂钓时段

## 📋 环境要求

- **Python**：3.7 及以上版本
- **操作系统**：Linux / macOS / Windows
- **依赖包**：
  - `playwright` — 无头浏览器，用于爬取 SPA 页面
  - `pypinyin` — 城市名转拼音

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install playwright pypinyin
playwright install chromium
```

### 2. 运行

```bash
# 自动 IP 定位
python3 scripts/fishing_main.py

# 指定城市
python3 scripts/fishing_main.py --city "惠州"

# 指定输出目录
python3 scripts/fishing_main.py --city "深圳" --output-dir ./output
```

### 3. 查看结果

脚本运行后会输出：
1. **文字报告**（stdout）— 钓鱼指数、天气、鱼种推荐等核心信息
2. **HTML 报告**（文件）— 在浏览器中打开可查看完整交互式报告

## 📁 项目结构

```
fishing-advisor/
├── SKILL.md                      # Skill 定义文件（触发词、用法）
├── README.md                     # 项目说明文档（本文件）
├── scripts/
│   ├── fishing_main.py           # 主入口，编排全流程
│   ├── fishweather_spider.py     # fishweather.cn 爬虫模块
│   ├── ip_location.py            # IP 定位模块
│   ├── do_calculator.py          # 溶氧计算模块（Weiss 1970 公式）
│   ├── three_elements.py         # 三要素（溶氧/水温/气压）分析
│   ├── generate_html.py          # HTML 报告生成器
│   └── __init__.py
└── templates/                    # （预留）模板目录
```

## 🔧 模块说明

### fishing_main.py — 主入口

编排完整流程：IP 定位 → fishweather 爬取 → 鱼种搜索 → 三要素分析 → 文字报告 → HTML 生成。

主要功能：
- `ensure_dependencies()` — 自动检测并安装缺失依赖
- `get_city()` — 获取城市（优先参数，其次 IP 定位）
- `search_fish_species()` — 多引擎搜索当地鱼种
- `merge_fish_species()` — 合并爬取和搜索的鱼种数据
- `format_text_report()` — 生成文字摘要报告
- `compute_moon_phase()` — 月相计算（兜底方案）

### fishweather_spider.py — 数据爬虫

基于 Playwright 无头浏览器爬取 fishweather.cn SPA 页面，通过正则解析页面文本提取：
- 天气详情（温度、湿度、风向风力、气压）
- 钓鱼指数（当前/实时/评级）
- 48 小时逐时数据（温度、气压）
- 7 天钓鱼指数预报
- 今日建议文本
- 月相数据（名称、评分、照明度、月龄、趋势）
- 活跃鱼种（含水层深度、推荐饵料）
- 出钓装备建议（钓位、饵料、线组）
- 附近钓点

数据缓存 30 分钟（缓存目录：`~/.fishing_advisor_cache/`），避免频繁爬取。

### do_calculator.py — 溶氧计算

采用 Weiss (1970) 公式计算饱和溶氧量，再根据气压修正：
- 0°C → 14.62 mg/L
- 20°C → 9.09 mg/L  
- 25°C → 8.26 mg/L

### three_elements.py — 三要素分析

基于 fishweather 爬取的 48 小时气压数据和温度数据，结合溶氧计算：
- 逐时溶氧/水温/气压分析
- 正弦平滑模型（锚定实测值）
- 综合评分和星级评定
- 颜色编码（绿/黄绿/黄/橙/红）

### generate_html.py — 报告生成

生成单文件 HTML 交互式报告：
- 深色星空主题（#0a1628 背景）
- 环形仪表盘（分段弧线渐变，兼容所有浏览器）
- Canvas bezierCurveTo 平滑曲线
- 24h/7d Tab 切换
- 点击图例切换曲线显示/隐藏
- Hover 显示详细数值 Tooltip
- 渐变色带展示逐时钓鱼窗口期
- 7 天柱状图预报

输出目录默认：`~/fishing_advisor_output/`

## 🎨 HTML 报告预览

报告包含以下模块（从上到下）：

1. **钓鱼指数仪表盘** — 环形渐变仪表 + 当前分数 + 黄金垂钓时段
2. **今日建议** — fishweather.cn 原文建议
3. **天气概览** — 横向滚动卡片（天气/气温/水温/溶氧/气压）
4. **趋势分析** — 24h 平滑曲线 + 渐变色带 / 7d 柱状图（Tab 切换）
5. **活跃鱼种** — 双列网格，含奖牌排名和活跃度标签
6. **出钓建议** — 钓位、饵料、线组推荐
7. **月相信息** — 月相名称、垂钓评价、评分、照明度、月龄
8. **附近钓点** — 可折叠列表

## ⚠️ 注意事项

1. **首次运行**需安装 Chromium 浏览器（`playwright install chromium`），约 100MB
2. **网络要求**：需能访问 fishweather.cn 和搜索引擎（用于鱼种搜索）
3. **缓存机制**：数据缓存 30 分钟，缓存文件位于 `~/.fishing_advisor_cache/`
4. **鱼种搜索**：每次运行都会联网搜索，确保推荐信息时效性
5. **区域兜底**：当搜索无结果时，内置华南/长三角/北方区域鱼种数据库兜底

## 📄 许可

本项目仅供学习和个人使用，数据来源于 fishweather.cn。
