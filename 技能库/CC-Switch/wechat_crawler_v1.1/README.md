# wechat_crawler_v1.1

Hermes 可直接调用的公众号历史消息全量爬虫技能。

## 特性

- 输入 `mp.weixin.qq.com` 历史消息主页链接即可执行。
- 自动翻页、去重、反爬延时、异常重试、断点续爬。
- 自动落盘 Markdown 与 `index.csv`。
- 自动提取关键词与核心观点。
- 自动写入 Trae 技能知识文件与 Hermes 知识库。
- 自动同步到 `.trae/skills` 与 `.hermes/skills` 双目录。

## 对外调用

```python
from skill_entry import skill_wechat_crawler

result_md = skill_wechat_crawler("https://mp.weixin.qq.com/...")
print(result_md)
```

## Hermes API 调用（由主服务提供）

```bash
curl -X POST http://127.0.0.1:8080/hermes/skill/wechat_crawler ^
  -H "Content-Type: application/json" ^
  -d "{\"mp_url\":\"https://mp.weixin.qq.com/...\"}"
```

## 依赖

- `requests`
- `beautifulsoup4`
- `playwright`

技能会在运行时自动安装缺失依赖，并尝试安装 `playwright chromium`。
