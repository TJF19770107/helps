# Gemini Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

Gemini 是龙虾AI主控中心的 Google 生态Agent，负责 Google 服务集成、多模态处理和 Google 生态内的信息获取。Agent-Reach 为其补充非 Google 生态的网络读取能力。

---

## 二、调用方式

### 2.1 自然语言触发

```
"帮我看看这个网页讲了什么"
"搜索一下 GitHub 上最火的 Android 开源项目"
"这个 YouTube 视频有中文字幕吗"
"看看这个 RSS 订阅源最近更新了什么"
```

### 2.2 Shell 命令调用

```powershell
# 网页读取
agent-reach web read --url "https://developer.android.com/" --format markdown

# YouTube 字幕（Gemini 主力使用）
agent-reach youtube subtitle --url "https://www.youtube.com/watch?v=xxx" --lang zh-CN

# GitHub 仓库
agent-reach github read --repo "google/generative-ai-docs"

# RSS 订阅
agent-reach rss parse --url "https://android-developers.googleblog.com/feeds/posts/default"
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "youtube_subtitle",
  "params": {
    "url": "https://www.youtube.com/watch?v=xxx",
    "lang": "zh-CN"
  }
}
```

---

## 三、典型场景映射

| 场景 | 命令 | 说明 |
|------|------|------|
| Android 开发文档 | `web read --url` | 实时获取最新文档 |
| YouTube 技术分享 | `youtube subtitle --lang` | 提取字幕总结 |
| GitHub 开源项目 | `github read --repo` | 谷歌开源项目 |
| 技术博客跟踪 | `rss parse --url` | Google Blog RSS |
| 跨平台搜索 | `search semantic --query` | 非 Google 平台 |

---

## 四、手机端 Mavis 远程调用配置

```yaml
# Mavis remote.yaml (Gemini 节点)
agent: "gemini"
cc_switch_endpoint: "http://<内网IP>:18789"
default_lang: "zh-CN"  # 字幕默认中文
preferred_sources: ["youtube", "github", "web"]
```

---

## 五、兜底方案：Playwright 切换

Gemini 使用 Playwright 的额外配置：

```powershell
# Gemini 可用 Google Chrome 作为 Playwright 浏览器引擎
cc-switch playwright start --browser chromium --channel chrome
```

---

## 六、适配验证清单

- [ ] 网页读取正常
- [ ] YouTube 字幕提取正常
- [ ] GitHub 仓库读取正常
- [ ] RSS 订阅解析正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
