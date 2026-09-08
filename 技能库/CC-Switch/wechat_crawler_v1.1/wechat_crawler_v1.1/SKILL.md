---
name: "wechat_crawler_v1.1"
description: "全量抓取微信公众号历史文章并自动入库 Hermes。Invoke when user提供 mp.weixin.qq.com 主页链接并要求批量爬取、续爬、修复或更新。"
---

# Wechat Crawler v1.1

## 能力

- 输入公众号历史消息主页链接后，自动抓取历史文章。
- 自动处理翻页、去重、随机延时、异常重试、断点续爬。
- 自动生成 `hermes_skills/crawler_output/` 下 Markdown 文件与 `index.csv` 索引。
- 自动提取关键词与核心观点并写入 Trae 技能知识文件。
- 自动调用 Hermes `/hermes/learn/file` 将文章导入 Hermes 知识库。

## 调用方式

```python
from skill_entry import skill_wechat_crawler

markdown_result = skill_wechat_crawler("https://mp.weixin.qq.com/...")
print(markdown_result)
```

## 统一入口

- 函数入口：`skill_wechat_crawler(mp_url, max_pages=None, resume=True)`
- JSON 入口：`skill_wechat_crawler_json(mp_url, max_pages=None, resume=True)`

## 输出

- 文章 Markdown：`hermes_skills/crawler_output/<发布时间>_<标题>.md`
- 索引文件：`hermes_skills/crawler_output/index.csv`
- 运行报告：`hermes_skills/crawler_output/last_run_report.json`
- 技能知识文件：`kb/trae_skill_kb.jsonl`

## 注意事项

- 需要可访问 `mp.weixin.qq.com` 的网络环境。
- 若公众号触发强风控，抓取会自动重试，必要时可延后再执行续爬。
