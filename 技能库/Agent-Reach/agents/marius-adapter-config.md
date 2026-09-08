# Marius Agent — Agent-Reach 适配配置

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、Agent 定位

Marius 是龙虾AI主控中心的媒体处理Agent，负责图片、视频、音频等多媒体内容的处理和分析。Agent-Reach 为其提供在线媒体资源获取和平台内容读取能力。

---

## 二、调用方式

### 2.1 自然语言触发

```
"这个 B站视频的封面图帮我下载分析一下"
"YouTube 上搜索关于摄影技巧的最新视频"
"这个小红书帖子里的图片风格是什么"
```

### 2.2 Shell 命令调用

```powershell
# YouTube 视频信息
agent-reach youtube subtitle --url "https://www.youtube.com/watch?v=xxx" --lang zh-CN

# B站视频字幕
agent-reach bilibili subtitle --url "https://www.bilibili.com/video/BVxxx"

# 抖音视频解析（需 Cookie）
agent-reach douyin video --url "https://www.douyin.com/video/xxx"

# 网页图片提取
agent-reach web read --url "https://unsplash.com/" --format markdown
```

### 2.3 MCP 调用示例

```json
{
  "mcp": "agent-reach-network",
  "action": "bilibili_subtitle",
  "params": {
    "url": "https://www.bilibili.com/video/BVxxx"
  }
}
```

---

## 三、典型场景映射

| 场景 | 命令 | 说明 |
|------|------|------|
| 视频内容提取 | `youtube/bilibili subtitle` | 字幕+元数据 |
| 社交平台内容 | `xiaohongshu/douyin read` | 需 Cookie |
| 图片资源获取 | `web read --url` | 网页内图片 |
| 播客内容 | `xiaoyuzhou podcast` | 音频转文字 |

---

## 四、手机端 Mavis 远程调用配置

```yaml
# Mavis remote.yaml (Marius 节点)
agent: "marius"
cc_switch_endpoint: "http://<内网IP>:18789"
media_download: false  # 手机端不下载大文件
max_video_length: 30   # 仅处理30分钟以内视频
```

---

## 五、兜底方案：Playwright 切换

```powershell
cc-switch route set --agent marius --node playwright --duration 30m
```

---

## 六、适配验证清单

- [ ] YouTube 字幕提取正常
- [ ] B站字幕提取正常
- [ ] 社交平台内容读取（需Cookie）正常
- [ ] 网页内媒体资源获取正常
- [ ] Mavis 远程调用正常
- [ ] Playwright 兜底切换正常
