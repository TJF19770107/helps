---
name: "cloudbase-hy3-relay"
description: "部署并运维「CloudBase 云函数 hy3-relay-proxy」——通过小程序成长计划 10 亿免费 Token 调用腾讯混元 hy3-preview。覆盖：小程序成长计划 SSO 入口 → 普通云函数代码包部署(避开 HTTP 云函数 scf_bootstrap 坑) → HTTP 网关路由(公网 URL) → 本地独立代理 :15731(Anthropic 协议) 全链路。当用户说'用混元/HY3/CloudBase 免费额度建代理'或'把云函数建完/重部署 hy3-relay-proxy'时激活。"
version: "1.1.0"
date: "2026-07-21"
author: "WorkBuddy + 龙虾AI主控中心"
tags: ["cloudbase", "hy3", "hunyuan", "腾讯云", "免费额度", "云函数", "代理", "小程序成长计划"]
primary_path: "~/.workbuddy/skills/cloudbase-hy3-relay/SKILL.md"
shared_path: "E:/龙虾AI主控中心/我的AI分身/技能库/cloudbase-hy3-relay/SKILL.md (沙箱禁止写入该受管目录，需用户本机执行镜像命令，见第七节)"
---

# CloudBase × 混元 HY3 免费额度中继

> **目的**：把腾讯混元 `hy3-preview` 大模型通过「小程序成长计划」的 **10 亿免费 Token** 接入本地 Agent 体系，
> 完全绕开 Hy3/WorkBuddy 积分与直调 403(`AI_CHANNEL_NOT_ALLOWED`) 限制。
> **架构**：`Claude Code → :15731 本地代理(hy3_proxy.py) → CloudBase 云函数 hy3-relay-proxy → app.ai().createModel("cloudbase").generateText → hy3-preview(免费额度)`

---

## 一、铁律 / 关键事实（必读）

| 项 | 值 |
|---|---|
| 环境 EnvID | `tjf19770107-d0gcttvcmca9c4a3c` |
| HTTP 网关默认域名 | `tjf19770107-d0gcttvcmca9c4a3c-1455836530.ap-shanghai.app.tcloudbase.com` ⚠️ 带 `-1455836530` 后缀 |
| 云函数名 | `hy3-relay-proxy`（普通云函数，非 HTTP 云函数） |
| 路由路径 | `/hy3-relay-proxy` |
| **公网 URL** | `https://tjf19770107-d0gcttvcmca9c4a3c-1455836530.ap-shanghai.app.tcloudbase.com/hy3-relay-proxy` |
| 本地代理 | `G:\龙虾AI主控中心\HY3混元代理\hy3_proxy.py` 端口 `:15731`（固定，与 ORCA/协议桥 15721 隔离） |
| GPT 浏览器壳 | `D:\Program Files\GptChrome\GptBrowser.exe`（Profile：`C:\Users\Administrator\AppData\Local\SPChrome\User Data`） |
| Node 运行时 | 托管版 `22.22.2`；Playwright 在 `C:\Users\Administrator\.workbuddy\binaries\node\workspace\node_modules` |

### 🔴 四大天坑（踩过，必须规避）

1. **入口必须走「小程序成长计划」SSO，不能直登 `tcb.cloud.tencent.com`**
   直登会跳登录墙。正确链路：`mp.weixin.qq.com` → 点「小程序成长计划」→ 在 `iframe[name=mpdevplan]` 内定位 `button.weui-desktop-btn_primary` 文本含「去使用」→ `handle.click({force:true})` 可信点击 → 落到 CloudBase 控制台。**该 SSO 会话不持久化，每次重走。**
2. **必须用「普通云函数」(事件函数)，绝不能用「HTTP 云函数」**
   HTTP 云函数 = SCF Web Function，要求 zip 内含 `scf_bootstrap`，否则报 `ResourceNotFound.BootstrapFile`。普通云函数用 `index.main` handler，匹配 `exports.main`。
3. **`@cloudbase/node-sdk` 必须 ≥ 3.16.0**（实测 2.11.0 时 `app.ai()`/`app.openai` 均为 `undefined`）。正确调用：
   ```js
   const cloudbase = require('@cloudbase/node-sdk');
   const app = cloudbase.init({ env: 'tjf19770107-d0gcttvcmca9c4a3c', timeout: 120000 });
   const ai = app.ai();
   const m = ai.createModel('cloudbase');
   const result = await m.generateText({ model: 'hy3-preview', messages, maxTokens: 1024 });
   // result.text / result.usage
   ```
4. **TDesign 下拉选项在 portal 内，被弹窗遮罩拦截 → 必须 `force:true` 点击**
   `li:has-text("xxx")` 若命中弹窗背后元素会报 "tea-overlay-root intercepts pointer events"。解决：`dropdown.click({force:true})` + `ul.tea-list--option li:has-text("xxx").click({force:true})`。

---

## 二、函数代码（v4.0.0，见 `scripts/index.js` + `scripts/package.json`）

- 接收 **Anthropic `/v1/messages`** 格式 body → 转 `generateText` → 把结果包回 **Anthropic 格式**（由本地代理负责 SSE 流式化）。
- `package.json` 依赖 `@cloudbase/node-sdk: ^3.18.3`（≥3.16.0 即可）。
- 部署包只含 `index.js` + `package.json`（不要 `cloudbaserc.json`，会冲突 runtime 字符串）。

---

## 三、首次部署 Runbook（全自动化，零手工）

> 所有脚本用托管 Node 运行：
> `NODE_PATH=C:/Users/Administrator/.workbuddy/binaries/node/workspace/node_modules C:/Users/Administrator/.workbuddy/binaries/node/versions/22.22.2/node.exe <script.js>`

### 步骤 1：创建云函数（普通云函数 + 代码包）
参照 `scripts/deploy_function.js`（SSO → 云函数/托管 → 新建云函数 → 通过代码包创建 → 函数名 `hy3-relay-proxy` → 上传 clean.zip → 运行环境默认 `Node.js 20.19` → 执行超时 `30` → 创建）。
验证：函数状态「正常」（普通云函数常态即"正常"非"运行中"）。

### 步骤 2：创建 HTTP 网关路由（拿公网 URL）
参照 `scripts/create_route.js`（SSO → 左侧「HTTP 网关」→ 路由管理「添加路由」）：
- 域名：选默认 `tjf19770107-d0gcttvcmca9c4a3c-1455836530.ap-shanghai.app.tcloudbase.com`
- 访问路径：`/hy3-relay-proxy`
- 关联资源：类型「云函数」（默认是"云托管"，**必须改**）→ 实例 `hy3-relay-proxy`
- 提交「确定」。公网 URL 即上方铁律表地址。

### 步骤 3：写入本地代理目标 URL
编辑 `G:\龙虾AI主控中心\HY3混元代理\hy3_proxy.py` 的 `CLOUD_FUNCTION_URL`（已固化真实地址；可用环境变量 `HY3_CLOUD_FUNCTION_URL` 覆盖）。同时修正 `/health` 里的 `DEFAULT_MODEL` 拼写（v1.0 有笔误 `DEFAULT_MODEl`）。

### 步骤 4：启动 + 验证
```bash
# 启动代理（后台）
python G:/龙虾AI主控中心/HY3混元代理/hy3_proxy.py

# 直连云函数 health（应返回 version:4.0.0, ai:true）
curl -X POST <公网URL> -H 'Content-Type: application/json' -d '{"__health_check":true}'

# 经代理非流式
curl -X POST http://127.0.0.1:15731/v1/messages -H 'Content-Type: application/json' -d '{"model":"hy3-preview","max_tokens":128,"messages":[{"role":"user","content":"你好"}]}'

# 经代理流式（SSE，Claude Code 实际用法）
curl -X POST http://127.0.0.1:15731/v1/messages -H 'Content-Type: application/json' -d '{"model":"hy3-preview","max_tokens":128,"stream":true,"messages":[{"role":"user","content":"你好"}]}'
```

---

## 四、重部署 / 改代码 Runbook（本地上传 zip）

SSO → 函数管理(`#/scf`) → 点 `hy3-relay-proxy` → 「函数代码」标签 → 提交方法下拉（默认"前端编辑器"）切到「本地上传」→ `input[type=file].setInputFiles(clean.zip)` → 点「保存并安装依赖」→ 等 45s+ 自动安装 `@cloudbase/node-sdk`。
脚本见 `scripts/redeploy.js`（含部署后 health 轮询 + 真实调用验证）。

---

## 五、排错

| 现象 | 根因 | 解决 |
|---|---|---|
| 直登 `tcb.cloud.tencent.com` 跳登录 | SSO 会话不持久 | 重走「小程序成长计划→去使用」 |
| 创建函数报 `ResourceNotFound.BootstrapFile` | 误选 HTTP 云函数 | 删掉改用普通云函数 |
| 调用报 `Cannot read properties of undefined (reading 'completions')` | SDK <3.16.0，`app.ai` 不存在 | package.json 升到 `^3.18.3` 并重部署 |
| 调用返回 **HTTP 429** | 免费额度低 QPS 限流（瞬时） | **重试即可**，非故障（实测隔 10-15s 重试通过） |
| 返回 `usage:{input_tokens:0,output_tokens:0}` | CloudBase `result.usage` 该版本未填充 | 无害，文本正确即可 |
| 下拉选项点击报 overlay 拦截 | TDesign portal 选项被弹窗盖住 | 所有选项点击加 `force:true` |

### 步骤 5：代理保活（登录拉起 + 每5分钟自愈，零手工干预）⭐

代理进程若仅后台启动，会话结束即退出。用看门狗 + 计划任务实现生产级保活（参照 lobster_protocol_bridge 模式）：

- `hy3_watchdog.py`：探测 `127.0.0.1:15731`，未存活则以 `DETACHED` 方式拉起 `hy3_proxy.py`（脱离父进程常驻）。
- `setup_watchdog_task.ps1`：注册 Windows 计划任务 `Hy3ProxyWatchdog`，触发条件 = **登录时 + 每5分钟重复**，动作 = 运行看门狗。

```powershell
# 一键注册（需以 Administrator 运行）
powershell -ExecutionPolicy Bypass -File "C:/Users/Administrator/.workbuddy/skills/cloudbase-hy3-relay/scripts/setup_watchdog_task.ps1"
```

验证：
```bash
# 手动运行看门狗（代理已存活时应输出 "OK :15731 代理已存活，无需操作"）
python "G:/龙虾AI主控中心/HY3混元代理/hy3_watchdog.py"
# 查看计划任务
schtasks /Query /TN Hy3ProxyWatchdog
```

---

## 六、已验证状态（2026-07-21 v1.1.0）

✅ 云函数「正常」✅ HTTP 路由 `hasRoute:true` ✅ health `version:4.0.0,ai:true`
✅ 真实 hy3-preview 调用返回正确中文 ✅ 代理非流式 200 ✅ 代理流式 SSE 完整
✅ **代理保活已落地**：`Hy3ProxyWatchdog` 计划任务（登录拉起 + 每5分钟自愈，LastTaskResult=0 已验证），`hy3_watchdog.py` 探测存活无扰动。
✅ 端到端全链路（云函数直连 / 本地代理 :15731）均 HTTP 200 返回正确中文，10 亿免费 Token 可用。

---

## 七、镜像到共享技能库（可选，沙箱外执行）

用户级技能（`~/.workbuddy/skills/cloudbase-hy3-relay/`）已可直接被 WorkBuddy 调用，**无需镜像**。
若需同步到 `E:/龙虾AI主控中心/我的AI分身/技能库/`（舰队共享），**该目录属沙箱禁止写入的受管目录**，
必须由用户在**本机（非沙箱）**执行以下一条命令完成镜像：

```powershell
Copy-Item -Recurse "C:\Users\Administrator\.workbuddy\skills\cloudbase-hy3-relay" "E:\龙虾AI主控中心\我的AI分身\技能库\cloudbase-hy3-relay"
```

> 说明：WorkBuddy 沙箱对 `技能库/`、`Obsidian知识库/`、`龙虾全域官方模板-最终版.md` 等受管目录的写入被显式拒绝，
> 这是用户在早期会话中授权的保护策略。如需让 Agent 以后能自动镜像，需先在沙箱权限中放行该路径。

