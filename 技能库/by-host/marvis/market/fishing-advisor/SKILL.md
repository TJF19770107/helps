---
name: fishing-advisor
description: 钓鱼天气顾问技能。当用户提到"钓鱼"、"钓鱼指数"、"钓鱼天气"、"今天适合钓鱼吗"、"去哪里钓鱼"、"鱼口怎么样"、"钓什么鱼"等垂钓相关问题时触发此技能。自动解析用户IP定位城市，爬取fishweather.cn专业垂钓气象数据，生成包含钓鱼指数、三要素变化分析、鱼种推荐的交互式HTML报告。
---

# 钓鱼天气顾问 (Fishing Advisor)

## 技能概述

根据用户地点，爬取 fishweather.cn 专业垂钓气象平台数据，输出钓鱼指数、气象详情、鱼种推荐，并生成深色星空主题的交互式 HTML 报告。

**核心能力**：
- IP 自动定位 → 城市识别
- fishweather.cn 爬虫 → 钓鱼指数 + 气象 + 溶氧 + 水温
- 三要素变化分析 → 溶氧/水温/气压日内趋势
- 鱼种网络搜索 → 当地活跃鱼种推荐
- HTML 可视化报告 → 深色星空主题 + 环形仪表盘

## 使用方式

### 完整流程（一条命令）

```bash
python3 {SKILL_DIR}/scripts/fishing_main.py --city "惠州"
```

用户不指定城市时，自动通过 IP 定位：

```bash
python3 {SKILL_DIR}/scripts/fishing_main.py
```

### 分步使用

```bash
# 1. IP定位获取城市
python3 {SKILL_DIR}/scripts/ip_location.py
# 输出: {"city": "惠州", "province": "广东", "lat": 23.11, "lon": 114.41}

# 2. 爬取fishweather数据
python3 {SKILL_DIR}/scripts/fishweather_spider.py --city "惠州"
# 输出: JSON格式的完整钓鱼+气象数据

# 3. 生成HTML报告
python3 {SKILL_DIR}/scripts/generate_html.py --data-file /path/to/fishing_data.json
# 输出: HTML文件路径
```

### 自定义输出目录

```bash
python3 {SKILL_DIR}/scripts/fishing_main.py --city "深圳" --output-dir /path/to/output
```

## 输出说明

脚本执行后会输出两部分内容：

### 1. 文字摘要（直接输出到stdout）
包含：今日钓鱼指数、评级、最佳时段、水温、溶氧、气压趋势、活跃鱼种、出钓建议等核心信息。
**请将此文字摘要直接展示给用户**。

### 2. HTML交互报告
自动保存到输出目录（默认 `~/fishing_advisor_output/`），路径会在stdout中打印。
**请告知用户 HTML 文件路径，用户可在浏览器中打开查看完整报告**。

## 触发关键词

- "钓鱼"、"钓鱼天气"、"钓鱼指数"
- "今天适合钓鱼吗"、"明天能钓鱼吗"
- "鱼口怎么样"、"鱼好不好钓"
- "钓什么鱼"、"去哪里钓鱼"
- "溶氧量"、"水温"、"气压对钓鱼的影响"

## 注意事项

- 首次使用需要安装依赖：`pip install playwright pypinyin && playwright install chromium`
- fishweather.cn 为 SPA 页面，必须使用 Playwright 无头浏览器爬取
- 数据缓存 30 分钟，避免频繁爬取
- 鱼种推荐每次都会网络搜索，确保信息最新
- HTML 报告为深色星空主题，参考钓鱼天气 App 设计风格
- 兼容 Python 3.7+，支持 Linux / macOS / Windows
