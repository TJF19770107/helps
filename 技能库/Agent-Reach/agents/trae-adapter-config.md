# TRAE Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

TRAE 是龙虾AI主控中心的翻译与本地化Agent，负责多语言翻译、文档本地化和跨语言信息获取。Agent-Reach 为其提供外文原文获取和多语言资源读取能力。

---

## 二、调用方式

### 2.1 自然语言触发

```
"帮我翻译这个英文网页的内容 https://docs.python.org/3/"
"看看这篇日语技术博客讲了什么 https://qiita.com/xxx"
"读取这篇 arXiv 论文的摘要 https://arxiv.org/abs/xxx"
```

### 2.2 Shell 命令调用

```powershell
# 英文原文获取
agent-reach web read --url "https://docs.python.org/3/whatsnew/3.12.html" --format markdown

# 多语言网站读取
agent-reach web read --url "https://qiita.com/tags/python" --format markdown

# arXiv 论文
agent-reach web read --url "https://arxiv.org/abs/2401.xxxxx"

# RSS 订阅外文博客
agent-reach rss parse --url "https://blog.rust-lang.org/feed.xml" --limit 5
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "web_read",
  "params": {
    "url": "https://arxiv.org/abs/2401.xxxxx",
    "format": "markdown"
  }
}
```

---

## 三、典型场景映射

| 场景 | 命令 | 说明 |
|------|------|------|
| 外文文档获取 | `web read --url` | 获取原文供翻译 |
| 论文摘要提取 | `web read --url` | arXiv 等学术网站 |
| 多语言博客 | `web read --url` | 日语/韩语/法语等 |
| 技术博客订阅 | `rss parse --url` | 外文技术博客 RSS |

---

## 四、手机端 Mavis 远程调用配置

```yaml
# Mavis remote.yaml (TRAE 节点)
agent: "trae"
cc_switch_endpoint: "http://<内网IP>:18789"
preferred_format: "markdown"
target_langs: ["zh-CN", "en", "ja", "ko"]
```

---

## 五、兜底方案：Playwright 切换

```powershell
cc-switch route set --agent trae --node playwright --duration 30m
```

---

## 六、适配验证清单

- [ ] 英文网页读取正常
- [ ] 非英文网页读取正常
- [ ] arXiv 论文获取正常
- [ ] RSS 外文博客解析正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
