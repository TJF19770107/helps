# Agent-Reach CC Switch 路由规则说明

> 版本: 1.0.0 | 日期: 2026-06-14

---

## 一、概述

CC Switch 是龙虾AI主控中心的智能路由调度层，负责根据请求类型自动将任务分发到最合适的执行节点。`agent-reach-network` 节点是全域联网读取的默认路由目标。

### 路由决策流程

```
用户请求 → CC Switch → 意图识别 → 匹配路由规则 → agent-reach-network → 返回结果
                                    ↓ (异常)
                              Playwright 兜底节点
```

---

## 二、路由规则矩阵

### 2.1 网页读取类

| 触发模式 | 路由目标 | 优先级 |
|----------|----------|--------|
| 读取网页 / 打开链接 / 这个网址 | `agent-reach web read --url` | 100 |
| fetch / curl 类请求 | `agent-reach web read --url` | 100 |
| 网页内容提取 / 正文提取 | `agent-reach web read --url --format markdown` | 100 |

### 2.2 视频内容类

| 触发模式 | 路由目标 | 优先级 |
|----------|----------|--------|
| 视频讲了什么 / 视频内容总结 | `agent-reach video subtitle` | 90 |
| YouTube 链接 | `agent-reach youtube subtitle --url` | 90 |
| B站视频 / bilibili | `agent-reach bilibili subtitle --url` | 90 |
| 提取字幕 / 视频字幕 | `agent-reach video subtitle` | 90 |

### 2.3 代码仓库类

| 触发模式 | 路由目标 | 优先级 |
|----------|----------|--------|
| GitHub 仓库 / 这个项目 | `agent-reach github read --repo` | 85 |
| GitHub 搜索 | `agent-reach github search --query` | 85 |
| Issue / PR 读取 | `agent-reach github issue --repo` | 85 |

### 2.4 RSS 订阅类

| 触发模式 | 路由目标 | 优先级 |
|----------|----------|--------|
| RSS / 订阅源 / Feed | `agent-reach rss parse --url` | 80 |

### 2.5 全网搜索类

| 触发模式 | 路由目标 | 优先级 |
|----------|----------|--------|
| 搜索一下 / 全网搜索 / 查资料 | `agent-reach search semantic --query` | 75 |

### 2.6 社交平台类

| 触发模式 | 路由目标 | 优先级 |
|----------|----------|--------|
| 推文 / Twitter / X.com | `agent-reach twitter read` | 70 |
| 小红书内容 | `agent-reach xiaohongshu read` | 70 |
| 微博内容 | `agent-reach weibo read` | 70 |

---

## 三、权限分级

### 3.1 全开权限（无需配置即可使用）

- 任意网页读取（Jina Reader）
- YouTube 字幕提取与搜索
- B站字幕提取（本地环境）
- RSS/Atom 源解析
- 全网语义搜索（MCP 自动接入）
- GitHub 公开仓库读取与搜索
- 微信公众号搜索与全文阅读
- 微博公开内容
- V2EX 热门帖子
- 雪球公开行情
- 小宇宙播客
- LinkedIn 公开页面

### 3.2 配置后解锁权限

- Twitter/X 搜索、时间线（需 Cookie）
- 小红书阅读、搜索（需 Cookie）
- 抖音视频解析（需 Cookie）
- GitHub 私有仓库（需 Token）
- Reddit 搜索与帖子（需 Cookie + 代理）
- 知乎内容读取（建议配置 Cookie）

### 3.3 禁止权限

- 任何平台的写入操作（发帖、评论、点赞、关注）
- GitHub 私有仓库写入
- 远程文件删除
- 大文件下载（>50MB）
- 内网地址访问（192.168.x.x / 10.x.x.x / 172.16-31.x.x）
- 政府网站（*.gov.cn）的非公开页面
- 银行/金融网站的任何自动化访问

---

## 四、异常处理与兜底切换

### 4.1 触发条件

以下任一条件满足时，自动切换至 Playwright 兜底节点：

| 条件 | 阈值 |
|------|------|
| 请求超时 | 30 秒 |
| 连续失败次数 | 3 次 |
| HTTP 403 / 429 | 立即切换 |
| 返回"Blocked" / "Captcha" | 立即切换 |
| Cookie 过期提示 | 通知用户后切换 |

### 4.2 切换流程

```
agent-reach-network 异常
       ↓
CC Switch 检测到异常信号
       ↓
自动路由至 Playwright 节点 (http://127.0.0.1:9222)
       ↓
Playwright 执行请求并返回结果
       ↓
记录异常日志供排查
```

### 4.3 恢复策略

- agent-reach-network 每 5 分钟自动健康检查
- 连续 3 次健康检查通过后，自动恢复路由
- 用户也可手动执行 `agent-reach doctor` 恢复

---

## 五、多 Agent 并发调度

### 5.1 请求队列

当多个 Agent 同时发起网络请求时，CC Switch 采用 FIFO 队列调度：

- 最大并发请求数：3
- 队列长度上限：50
- 超时未处理请求自动降级至 Playwright

### 5.2 Agent 优先级

| Agent | 优先级 | 说明 |
|-------|--------|------|
| Claude Code | 高 | 主开发Agent |
| Hermes | 高 | 主搜索Agent |
| OpenClaw | 中 | 跨平台Agent |
| Codex | 中 | 代码专项Agent |
| Gemini | 中 | Google生态Agent |
| TRAE | 低 | 翻译Agent |
| Marius | 低 | 媒体Agent |
| Workbody | 低 | 文档Agent |
| 豆包PC | 低 | 办公Agent |

---

## 六、配置文件说明

`mcp-node-config.json` 中各字段含义：

| 字段 | 说明 |
|------|------|
| `node_name` | 节点唯一标识 |
| `node_type` | 节点类型：network-skill |
| `routing.rules` | 意图识别模式与路由目标 |
| `permissions.allow` | 白名单操作 |
| `permissions.deny` | 黑名单操作 |
| `permissions.restricted_sites` | 受限站点列表 |
| `fallback` | 兜底方案配置 |
| `monitoring` | 健康检查与监控配置 |
