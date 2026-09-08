---
name: wecom-crosscorp-robot-create
version: 1.0.0
description: 跨企业企微智能机器人全自动创建RPA：支持切换不同企业微信主体、扫码登录目标企业后台、API长连接机器人创建/凭证抓取、权限校验、长连接连通性测试；重点解决"A企业机器人无法读取B企业群聊"的跨企业隔离坑点。
trigger: ["跨企业企微机器人", "企微机器人跨企业", "wecom crosscorp", "瀚文苏机器人", "多企业机器人", "企微长连接机器人创建", "小龙虾接单助手", "企业微信机器人凭证", "BotID Secret 提取"]
author: WorkBuddy Agent (TJF19770107 · 龙虾AI主控中心)
created: 2026-08-21
updated: 2026-08-21
status: active
---

# wecom-crosscorp-robot-create v1.0

## 一、核心能力

1. **多企业主体切换**：区分 TJF19770107、瀚文苏、瑞度等多个企业主体，绝不混用登录态。
2. **浏览器扫码 RPA**：Playwright 打开 `work.weixin.qq.com` 登录页，截图二维码，等待目标企业管理员扫码。
3. **企业身份强校验**：登录后台后，检测当前企业名；**非目标企业立即退出并截图留证**。
4. **API 模式 + 使用长连接**：自动选择「API 模式」和「使用长连接」，无需公网回调地址。
5. **真实凭证提取**：严格校验 BotID（`aib` 开头、约 22 位纯字母数字）和 Secret（≥30 位）。
6. **多企业 config.yaml**：保留原有 TJF19770107 机器人，追加新企业机器人配置。
7. **长连接服务 `wecom_ws_bot.py`**：基于 `wecom-aibot-python-sdk`（导入名 `aibot`），多 bot 独立长连接并发监听。
8. **非管理员协作方案**：当当前身份不是目标企业管理员时，生成标准话术请目标企业管理员创建机器人并回发凭证。

## 二、关键坑点（血泪教训 2026-08-21）

### 坑点 1：企微机器人强绑定所属企业

> **A 企业创建的机器人，只能访问 A 企业的群聊；完全无法读取 B 企业的任何消息。**
>
> 长连接认证时，企微服务端会根据 BotID/Secret 所属企业过滤消息。跨企业消息天然隔离，没有后门。

### 坑点 2：扫码登录后台，只显示"有管理员权限"的企业

> 手机企微扫码登录 `work.weixin.qq.com` 时，「选择管理的企业」下拉框**只出现你担任管理员的企业**。
>
> 如果目标企业（如瀚文苏）没出现在下拉框，说明：**当前微信/企微身份不是该企业的管理员**。
>
> 此时无论如何切换客户端、重新扫码，都不可能进入目标企业后台。不要重复尝试，直接走「管理员协作方案」。

### 坑点 3：不要复用跨企业 profile

> 不同企业必须使用独立的浏览器 profile（如 `wecom_hanwensu` vs `wecom_tjf`）。
>
> 复用 profile 会导致 cookie/登录态串味，RPA 看到的企业后台还是原来的企业。

### 坑点 4：API 模式创建时「使用长连接」是必选项

>  webhook/callback 模式需要公网域名和证书，成本高。
>
> 对于本地 Agent 监听接单群，**必须选「使用长连接」**：`wss://openws.work.weixin.qq.com`，无需公网 IP。

### 坑点 5：WorkBuddy / MAXCLAW1 BOT 可能已占用一条长连接

> 同一个机器人 BotID 同时只允许 **1 条 WebSocket 长连接**（新连接会踢掉旧连接）。
>
> 如果 WorkBuddy 桌面端或 MAXCLAW1 已用该机器人建立长连接，自己的 `wecom_ws_bot.py` 启动后会把它们踢下线。
>
> 解决方案：为 Agent 创建独立的机器人（推荐），或在 MAXCLAW1 之外单独申请一个机器人。

### 坑点 6：`wecom-aibot-python-sdk` 导入名不是 `wecom_aibot`

> 正确导入：`import aibot`
>
> 错误导入：`import wecom_aibot`（会报 `No module named 'wecom_aibot'`）
>
> 核心类：`from aibot import WSClient, WSClientOptions`

## 三、使用前提

- Python 3.10+
- `wecom-aibot-python-sdk` 已安装
- Playwright + Chromium 已安装
- 官方 Chrome 浏览器（非便携版，路径 `C:/Program Files/Google/Chrome/Application/chrome.exe`）
- 目标企业的管理员身份（或能得到管理员配合）

## 四、文件位置

| 文件 | 路径 |
|------|------|
| 跨企业创建脚本 | `E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline/tools/wecom_robot_create_crosscorp.js` |
| 多企业长连接服务 | `E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline/tools/wecom_ws_bot.py` |
| 启动脚本 | `E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline/tools/start_wecom_bot.cmd` |
| 配置文件 | `E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline/config.yaml` |
| 输出凭证 | `E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline/outputs/wecom_robot_hanwensu_credential.json` |

## 五、如果你是目标企业管理员

### 5.1 启动创建 RPA

```bash
cd "E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline"
export NODE_PATH="C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules"
node tools/wecom_robot_create_crosscorp.js
```

### 5.2 手动操作（手机端）

1. 手机企微 App → 切换当前企业到目标企业（如瀚文苏）。
2. 扫 RPA 弹出的二维码。
3. 手机出现「选择管理的企业」→ 手动确认选中目标企业 → 点「登录」。
4. 等待 RPA 自动创建机器人并提取 BotID/Secret。

### 5.3 RPA 输出示例

```json
{
  "bot_name": "小龙虾接单助手",
  "corp": "瀚文苏",
  "bot_id": "aibQaQYuRgLkObvNnqUJTttxuaXCxjRG7A5",
  "bot_secret": "sbIAWQ103GJuRVrYBfa6rVurcsjzD7v5b5Gk3WAQMv2",
  "created_at": "2026-08-21T17:00:00.000Z",
  "method": "企微后台·API模式·长连接·真实扫码创建",
  "note": "跨企业创建：机器人仅属于【瀚文苏】企业，无法读取 TJF19770107 群聊"
}
```

## 六、如果你不是目标企业管理员（常见场景）

### 6.1 判断标准

扫码后手机端「选择管理的企业」下拉框里**没有目标企业**。

### 6.2 标准协作话术

把下面这段话发给目标企业管理员（已和 MAXCLAW1 BOT 验证可用）：

```
小霞你好，有个事需要你帮忙操作一下，大概 3 分钟搞定：

我们想在瀚文苏企业下创建一个企业微信机器人，用来接入接单群自动处理订单，提高效率。

需要你帮忙做两件事：

第 1 步：创建机器人
1. 电脑打开浏览器访问：work.weixin.qq.com
2. 用你的微信扫码登录（选瀚文苏企业）
3. 进入「管理工具」→「智能机器人」
4. 点击「创建机器人」
5. 名称填：小龙虾接单助手
6. 连接方式选：「使用长连接」
7. 点击确定

第 2 步：把 BotID 和 Secret 发给我
创建成功后，页面会显示 BotID 和 Secret，复制发给我就行。

剩下的我来配置，弄好后机器人就能自动进群接单了。麻烦你了🙏
```

### 6.3 管理员回发凭证后

把凭证填入 `config.yaml`：

```yaml
wecom:
  enabled: true
  method: "websocket"
  listen_keywords: ["电商", "AI生成", "短视频", "AI Agent", "淘宝", "TikTok", "打豆包", "视频号", "接单", "设计", "详情页"]
  reply_mention: "@用户 小龙虾AI助手"
  silent_mode: true
  log_dir: "./logs/wecom"

  bots:
    - corp: "TJF19770107"
      name: "汤晋峰的机器人"
      bot_id: "aibQaQYuRgLkObvNnqUJTttxuaXCxjRG7A5"
      bot_secret: "sbIAWQ103GJuRVrYBfa6rVurcsjzD7v5b5Gk3WAQMv2"
      active: true
      silent_mode: true
      note: "已验证长连接认证通过（2026-08-21）"

    - corp: "瀚文苏"
      name: "小龙虾接单助手"
      bot_id: "aibXXXXXXXXXXXXXXXXXXXX"      # 管理员提供
      bot_secret: "XXXXXXXXXXXXXXXXXXXXXXXX"  # 管理员提供
      active: true
      silent_mode: true
      target_groups: ["平面设计【新人接单总群】"]
      note: "由瀚文苏管理员 A-管理小霞 创建（2026-08-21），待填入真实凭证"
```

## 七、启动长连接服务

```bash
cd "E:/龙虾AI主控中心/我的AI分身/网盘课程资源知识萃取与沉淀体系建设/jiedan_pipeline"
"C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" tools/wecom_ws_bot.py
```

或双击 `tools/start_wecom_bot.cmd`。

### 7.1 验证方式

1. 启动后观察日志：每个 bot 应输出 `✅ authenticated: ...`
2. 在目标群（瀚文苏接单群）@机器人发送 `测试`
3. 若 `silent_mode=true`，机器人只会打印日志不会回复；日志中应出现 `收到消息` 和消息内容。
4. 若 `silent_mode=false`，机器人会根据关键词生成回复并发送。

## 八、config.yaml 多企业结构说明

```yaml
wecom:
  # 全局配置
  enabled: true
  method: "websocket"
  listen_keywords: [...]
  reply_mention: "@用户 小龙虾AI助手"
  silent_mode: true
  log_dir: "./logs/wecom"

  # 机器人列表（多企业）
  bots:
    - corp: "TJF19770107"   # 企业标识，日志/过滤用
      name: "..."           # 机器人名称，可读
      bot_id: "..."
      bot_secret: "..."
      active: true          # 是否启用该 bot
      silent_mode: true     # 该企业 bot 是否静默
      target_groups: []     # 可选：只监听指定群名
      note: "..."
```

**旧字段保留兼容**：如果只用单个机器人，旧的 `bot_id`/`bot_secret` 仍可读取。

## 九、与 MAXCLAW1 BOT / OpenClaw 的关系

- **MAXCLAW1 BOT**：瀚文苏企业下已有的智能机器人（可能由 WorkBuddy 或 OpenClaw 创建）。
- **OpenClaw**：第三方 AI Agent 框架，提供 `npx -y @wecom/wecom-openclaw-cli install` 一键创建机器人能力，本质上也是调用企微官方协议。
- **本 Skill**：不依赖 OpenClaw，直接用 Playwright + 官方 SDK 操作，适用于已有环境或需要自主控制凭证的场景。

**推荐组合**：
- 瀚文苏管理员用本 RPA 或 OpenClaw CLI 创建「小龙虾接单助手」
- 拿到 BotID/Secret 后，用 `wecom_ws_bot.py` 建立独立长连接
- 把机器人拉进「平面设计【新人接单总群】」

## 十、错误排查

| 现象 | 原因 | 修复 |
|------|------|------|
| 扫码后下拉框没有目标企业 | 当前身份不是目标企业管理员 | 请目标企业管理员创建机器人 |
| RPA 截图 `03_WRONG_CORP.png` | 扫码后登录了错误企业 | 手机端重新扫码并选择目标企业 |
| `BotID 格式非法` | 抓取到了非 BotID 字段 | 检查详情页，BotID 应为 `aib` 开头 |
| 长连接认证失败 | BotID/Secret 错误，或机器人被其他连接占用 | 核对凭证；停用其他长连接 |
| 群里 @ 机器人无反应 | 机器人未进群 / 未授权消息能力 / silent_mode=true | 拉机器人进群；后台授权消息能力；检查日志 |
| `No module named 'wecom_aibot'` | 导入名错误 | 改为 `import aibot` |

## 十一、四端同步

本 Skill 已通过 `four-end-sync v1.0` 同步至：
- E 盘项目层：`E:/龙虾AI主控中心/我的AI分身/技能库/Skills_Backup/user_level/wecom-crosscorp-robot-create/SKILL.md`
- CNB/Git 本地 commit
- Obsidian：`E:/龙虾AI主控中心/Obsidian/Skills/wecom-crosscorp-robot-create.md`
- IMA 知识库：已灌入索引
- 乐享知识库：已同步

## 十二、版本记录

- **v1.0.0 (2026-08-21)**：首版，沉淀跨企业创建坑点与管理员协作方案。
