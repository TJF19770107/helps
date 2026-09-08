# AtomCode 免费模型（DeepSeek-v4）接入配置说明书

> 版本：v1.0 | 日期：2026-08-12
> 适用范围：Hermes Studio（hermes / CLAUDE CODE / codex 等 OpenAI 兼容客户端）通过本地代理免费使用 AtomGit CodingPlan 的 DeepSeek-v4-flash 模型
> 配套：一键拉起脚本 `start_atomcode_proxy.bat`、轻量快照 `atomcode_backup_20260812.zip`

---

## 1. 架构总览

```
Hermes Studio / 任意 OpenAI 兼容客户端
        │  HTTP(S) 调用 127.0.0.1:13460/v1/chat/completions
        ▼
┌─────────────────────────────────────┐
│  atomcode_proxy.py（本地代理，Python）│  ← 监听 127.0.0.1:13460
│  · 支持 /v1/models /v1/chat/completions
│  · 支持 SSE 流式响应（stream=true）
│  · 长 prompt 走 --prompt-file（规避命令行长度上限）
└─────────────────────────────────────┘
        │  subprocess 调用（一次性、带 --prompt-file）
        ▼
┌─────────────────────────────────────┐
│  atomcode.exe（AtomCode CLI）        │  ← E:\龙虾AI主控中心\我的AI分身\AtomCode\bin\
│  · 走 AtomGit CodingPlan 免费额度    │
│  · OAuth 登录态存于 auth.toml        │
└─────────────────────────────────────┘
```

**关键文件清单**

| 文件 | 作用 |
|---|---|
| `E:\...\AtomCode\scripts\atomcode_proxy.py` | 本地代理脚本（核心） |
| `E:\...\AtomCode\bin\atomcode.exe` | AtomCode CLI（调用免费模型） |
| `E:\...\AtomCode\.atomcode\config.toml` | AtomCode 配置（provider/model） |
| `E:\...\AtomCode\.atomcode\auth.toml` | OAuth 登录凭据（**敏感，勿外传**） |
| `E:\...\AtomCode\scripts\logs\atomcode_proxy.log` | 代理运行/错误日志 |
| `C:\Users\Administrator\.hermes-web-ui\config.json` | Hermes Studio 的 provider 显示配置 |

---

## 2. 首次配置步骤

### 2.1 登录并申领免费额度
```bash
atomcode login
```
自动完成：AtomGit OAuth 授权 → 申领 CodingPlan 免费额度 → 配置 provider/model。

查看状态：`atomcode status`（登录信息）；TUI 内 `/status`、`/usage`（额度用量与过期时间）。

### 2.2 启动本地代理
```bash
cd E:\龙虾AI主控中心\我的AI分身\AtomCode\scripts
python atomcode_proxy.py 13460
```
验证：浏览器/命令访问 `http://127.0.0.1:13460/health` 应返回 `{"status":"ok",...}`。

### 2.3 Hermes Studio 添加 Provider
- 类型：自定义（OpenAI 兼容）
- 显示名称：`atomcode-v4-local`（内部 ID：`custom:atomcode-v4-local`）
- Base URL：`http://127.0.0.1:13460/v1`
- API Mode：`Chat Completions`
- Provider 首选模型：`deepseek-v4-flash`
- API Key：任意值（代理不校验），填一个即可

---

## 3. 问题修复记录（本次配置踩坑全记录）

### 3.1 问题一：`HTTP 500: [WinError 206] 文件名或扩展名太长`

- **现象**：客户端发长消息时报 HTTP 500，错误为 `WinError 206`。
- **根因**：代理用 `-p <prompt>` 把**整个 prompt 拼进命令行**传给 `atomcode.exe`。Windows CreateProcess 命令行上限 **32767 字符**，prompt（系统提示词+历史）一长即超限，subprocess 抛 `WinError 206`。
- **修复**：改为把 prompt 写入**临时文件**，用 `atomcode.exe --prompt-file <path>` 传入；调用后自动清理临时文件。命令行只剩固定参数，长度不再是瓶颈。
- **验证**：50,004 字符超长 prompt 实测调用成功。

### 3.2 问题二：`Provider returned an empty stream with no finish_reason`

- **现象**：客户端（Hermes 用 openai SDK，默认 `stream=true`）报空流错误。
- **根因**：代理只返回普通 JSON，不支持 SSE 流式格式；openai SDK 按 SSE 解析失败。
- **修复**：代理识别请求中的 `stream` 字段，为 true 时按 OpenAI 标准 SSE 输出：内容 chunk → `finish_reason:"stop"` chunk → `data: [DONE]`。
- **验证**：`stream=true` 实测返回合法 SSE 帧序列，客户端正常解析。

### 3.3 附带改进：异常不再静默断连

- `do_POST` 外层 try/except：异常写日志（`scripts/logs/atomcode_proxy.log`）并返回带错误信息的 500 JSON，客户端不再看到空响应。
- 日志用 `logging.basicConfig` 落盘，无论从控制台还是计划任务启动都能查错。

### 3.4 排查中的坑：Windows 下 curl 中文按 GBK 发送

- 在 Git Bash / cmd 用 `curl -d` 发中文时，中文字节按系统代码页（GBK/CP936）编码，代理按 UTF-8 `json.loads` 会报 `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbb...`。
- **结论**：这不是代理 bug。真实客户端（openai SDK）一律发 UTF-8，不受影响。测试时用英文 prompt 或确保 UTF-8 编码即可。

---

## 4. 启动与运维

### 4.1 推荐启动方式：计划任务（脱离终端、稳定常驻）

```bat
:: 创建（只建一次）
schtasks /create /tn "AtomCodeProxy" /tr "\"<python.exe路径>\" \"E:\龙虾AI主控中心\我的AI分身\AtomCode\scripts\atomcode_proxy.py\" 13460" /sc once /st 23:59 /f
:: 启动
schtasks /run /tn "AtomCodeProxy"
:: 禁用（防误触发，不影响已运行进程）
schtasks /change /tn "AtomCodeProxy" /disable
:: 删除
schtasks /delete /tn "AtomCodeProxy" /f
```

> 用 Git Bash 执行时需加 `MSYS_NO_PATHCONV=1` 前缀防止路径转换。
> 不要用 `&` 后台或 `Start-Process` 从 Git Bash 拉起——bash 会等待其进程树并连带清理；计划任务方式启动的进程独立、稳定。

### 4.2 一键拉起脚本
见配套 `start_atomcode_proxy.bat`：双击即可自动检测并启动代理（已运行则跳过）。

### 4.3 排错速查表

| 症状 | 检查项 |
|---|---|
| 连不上 / Connection error | `netstat -ano \| findstr 13460` 是否有 LISTENING；`curl http://127.0.0.1:13460/health` |
| HTTP 500 | 看 `scripts\logs\atomcode_proxy.log` 最新 traceback |
| 客户端空流 | 确认代理已更新（含 SSE 支持）；看代理日志是否有 `proxy internal error` |
| 额度相关 | AtomCode TUI 内 `/status`（过期时间）、`/usage`（套餐额度）；额度按 5 小时滚动窗口计量 |

---

## 5. 免费额度说明（CodingPlan）

| 方案 | 有效期 | 领取条件 | 支持模型 |
|---|---|---|---|
| Lite | 30 天 | 免费，限量 1000 人/日 | deepseek-v4-flash、Qwen3-VL-8B |
| Pro 体验版 | 7 天 | 免费，每日 10:00 限量 100 人 | 额外支持 GLM-5.2 |
| Pro | 30 天 | 免费，需活动仓库合入 PR | 额外支持 GLM-5.2 |

- 系统自动发放当前可获得最高权益；额度按 **5 小时滚动窗口**计量。
- 有效期内重复 `/login` 不会重复申领（幂等）。
- 到期后可直接重跑 `/login` 尝试续领（以 CodingPlan 页面最新规则为准）。
- **注意**：客户端界面里的 `82.6k/1m tok (8%)` 是**上下文窗口占用**（deepseek-v4-flash 上下文 100 万 token），与免费额度无关；到 100% 用 `/compact` 压缩或 `/clear` 开新会话即可。

---

## 6. 备份与回滚

- 快照文件：`atomcode_backup_20260812.zip`（≤20MB），包含：代理脚本、配置（config.toml / auth.toml）、说明书、一键拉起脚本、Hermes Studio provider 配置。
- **回滚方法**：解压快照到对应目录覆盖即可。改脚本前先备份 `atomcode_proxy.py`。
- auth.toml 含登录凭据：快照请存放于本机可信位置，勿上传网盘/仓库。

---

## 7. 经验共享（写给 MARVIS 与后续 Agent）

1. **命令行长度坑**：Windows 上任何"把长文本塞进 CLI 参数"的方案都会撞 32767 字符上限（WinError 206）。长文本一律走临时文件参数（`--prompt-file` / `@file` / stdin）。
2. **SSE 坑**：openai 兼容客户端默认流式请求。做 OpenAI 兼容服务端时，必须同时实现 SSE 响应（`data: {...}` + `[DONE]`），否则客户端报"empty stream"。
3. **日志优先**：服务端进程的异常要落盘（logging 到文件），否则从计划任务/守护进程启动时 traceback 会丢失，排查无从下手。
4. **进程管理坑**：从 Git Bash 后台拉起常驻服务会被 bash 进程树连带清理；用计划任务（schtasks）方式启动最稳。
5. **编码坑**：Windows 控制台/curl 中文默认 GBK，Python `json.loads` 按 UTF-8 解析会报 UnicodeDecodeError——真实 SDK 客户端不受影响，测试时注意区分。
