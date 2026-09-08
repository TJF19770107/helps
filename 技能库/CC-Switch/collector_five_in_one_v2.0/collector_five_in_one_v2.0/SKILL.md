---
name: "collector_five_in_one_v2.0"
description: "五合一统一采集总调度（全网页+公众号/抖音/快手/视频号/小红书）跨浏览器适配并去重增量入库。Invoke when you need daily 5am silent run or emergency manual run with limited rounds."
---

# Collector Five-in-One v2.0

## 升级点

- 全浏览器通用适配：Playwright 引擎支持 chromium / firefox / webkit，并可选 channel（chrome/msedge）
- 覆盖范围扩容：任意网页 URL best-effort；视频平台优先 yt-dlp 抽取文案/简介/元信息
- 平台纳入：新增快手（Kuaishou）生态入口（链接级采集），并保留 v1.0 兼容回退
- 风控红线：自动模式每日仅 1 轮；手动模式必须显式指定轮数，且默认仍受“每日上限”约束

## 统一入口

- 函数入口：`skill_collector_five_in_one(req: dict) -> dict`
- Hermes API：`POST /hermes/skill/collector_five_in_one`（服务端优先调用 v2.0，失败回退 v1.0）

## 配置与状态（不含任何密钥）

- 采集清单（sources）：`核心程序/data/collector_five_in_one_sources.json`
- 状态文件：`核心程序/data/collector_five_in_one_state.json`
- 归档目录：`核心程序/data/archive/collector_five_in_one/`

## sources 结构（关键字段）

```json
{
  "type": "kuaishou|douyin|xiaohongshu|netdisk|web|wechat_mp",
  "title": "可选",
  "url": "任意网页/作品链接",
  "mp_url": "仅公众号需要",
  "method": "auto|ytdlp|html|browser",
  "cookies_env": "可选：环境变量名（JSON）",
  "headers_env": "可选：环境变量名（JSON）",
  "browser_engine": "chromium|firefox|webkit（可选）",
  "browser_channel": "chrome|msedge（可选）",
  "headless": true
}
```

## 环境变量（可选）

- `HERMES_BROWSER_ENGINE`：默认浏览器引擎（chromium/firefox/webkit，默认 chromium）
- `HERMES_BROWSER_CHANNEL`：可选 channel（chrome/msedge；仅 chromium 引擎生效）
- `HERMES_BROWSER_USER_DATA_DIR`：可选持久化用户数据目录（用于弱登录态/会话复用；不写入任何文件）
- `HERMES_COLLECTOR_DAILY_ENABLE`：是否启用每日自动轮（1/0，默认 1）
- `HERMES_COLLECTOR_DAILY_HOUR`：自动轮小时（默认 5）
- `HERMES_COLLECTOR_DAILY_JITTER_S`：自动轮抖动秒数（默认 900）

