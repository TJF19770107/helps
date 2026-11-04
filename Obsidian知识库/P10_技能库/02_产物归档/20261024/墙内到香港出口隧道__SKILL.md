---
name: 墙内到香港出口隧道
subject: 网络·出口隧道
belongs_to: 汤小龙 v3.0
version: v1.3.0
updated_at: 2026-10-24
owner: 汤小龙（WorkBuddy 宿主支）
agent_created: true
trigger: [币安打不开, ERR_CONNECTION_RESET, 连接已重置, 代理问题, 香港服务器上不去, 翻墙, 梯子, 走香港出口, binance 被墙, 浏览器代理, GPT浏览器上币安, 带AI标识的浏览器, SPChrome, 标签页同步, 两个浏览器同步, 书签同步, 书签增量同步, 书签迁移, 左侧书签栏没同步, 书签文件夹不见了]
---

# 墙内到香港出口隧道

> 一句话：**本机 DNS 把境外域名污染成 0.0.0.0，所以必须让"域名在服务器端解析"，
> 也就是走 HTTP 代理，而不是 SOCKS5。** 这是全部踩坑的根。

## 一、什么时候用它

- 浏览器打开币安 / 谷歌 / GitHub 报 `ERR_CONNECTION_RESET`、`连接已重置`
- `nslookup www.binance.com` 返回 `0.0.0.0` 或 `::`
- 需要在本机做量化取数、看盘、推 GitHub，但直连不通
- 香港服务器明明能上网，本机却怎么都不通

## 二、链路（四段，缺一段都不通）

```
Chrome / curl
   ↓  http://127.0.0.1:8888        ← 本机无认证入口（bridge）
hk_proxy_bridge.py（注入 Basic 认证）
   ↓  127.0.0.1:3128               ← SSH 本地转发（加密）
ssh -L 3128 隧道
   ↓  服务器 127.0.0.1:3128        ← xray http inbound（带口令）
xray → freedom outbound
   ↓  服务器侧解析 DNS → CloudFront / 币安真实 IP
目标站点
```

**为什么不用 SOCKS5**：本机 DNS 已污染（`0.0.0.0`），SOCKS5 由本地解析必挂；
HTTP CONNECT 只传域名，服务器解析，天然免疫污染。

## 三、标准 SOP（零成本，只需 22 端口）

### 步骤 1 · 先确认服务器侧真的能用（不要跳过）

```bash
ssh -q -i ~/.ssh/id_ed25519 root@43.161.202.206 \
  "curl -s -o /dev/null -w '%{http_code}\n' --max-time 12 https://www.binance.com/"
```

判据：`200` / `202` 都算通（币安对裸 curl 常返 202）。
若这里就不通，问题在服务器/续费/防火墙，别在本机瞎折腾。

### 步骤 2 · 起 SSH 本地转发（必须常驻）

```bash
ssh -N -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes -i ~/.ssh/id_ed25519 \
    -L 127.0.0.1:3128:127.0.0.1:3128 root@43.161.202.206
```

**必须用「后台常驻」方式启动**（见坑 2），不能用 `ssh -f -N`。

### 步骤 3 · 起本地桥接器

```bash
HK_PROXY_USER=<用户> HK_PROXY_PASS=<口令> \
  python hk_proxy_bridge.py --listen 8888 --upstream 127.0.0.1:3128
```

口令走环境变量，**不写进源码**。

### 步骤 4 · 验证四层，缺一层就是假成功

```bash
# ① 端口层
netstat -ano | grep -E ":(3128|8888)"

# ② 连通层（走代理时【不要】加 --noproxy "*"，见坑 4b）
curl -s -o /dev/null -w "%{http_code}\n" \
     -x http://127.0.0.1:8888 https://www.binance.com/

# ③ 出口层（必须是香港 IP）
curl -s -x http://127.0.0.1:8888 https://api.ipify.org

# ④ 页面层（浏览器真加载）
curl -s --noproxy "*" http://127.0.0.1:9222/json/list
```

**② 的参考值（2026-10-23 实测）**：
`binance 202` · `github.com 200` · `raw.githubusercontent.com 301` ·
`api.github.com 200` · `google 200` · 出口 IP `43.161.202.206`

**④ 的判据是 title，不是「窗口有没有开」**：
- ✅ `比特币交易平台 | 数字货币交易平台 | 币安`
- ✅ `币安：全球最值得信赖的加密货币买卖和投资平台`
- ✅ `0.00007130 | NEIROUSDT U本位永续合约图表 | 币安合约`
- ❌ 空标题、`ERR_*`、`Privacy error`

### 步骤 5 · 启动浏览器

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
"C:\Program Files\Google\Chrome\Application\chrome.exe" \
  --proxy-server="http://127.0.0.1:8888" \
  --proxy-bypass-list="127.0.0.1;localhost" \
  --user-data-dir="<独立 profile 目录>" \
  --remote-debugging-port=9222 \
  --no-first-run --no-default-browser-check \
  --start-maximized "https://www.binance.com/zh-CN"
```

用**独立 user-data-dir**，不碰用户日常 profile，零风险、可随时关。

### 步骤 6 · 接管「带 AI 标识的浏览器」（GPT Chrome / SPChrome / GptBrowser）

> **v1.1.0 新增（2026-10-23 实测打通）**。用户日常在用的浏览器往往不是原版 Chrome，
> 而是 360 系定制内核（本例 `D:\Program Files\GptChrome\GptBrowser.exe`，
> 窗口类 `SPChrome_FrameWin_1`，profile 在 `%LOCALAPPDATA%\SPChrome\User Data`）。

**关键结论：这类定制浏览器会完整转发标准 Chromium 开关**，包括
`--proxy-server` / `--proxy-bypass-list` / `--remote-debugging-port` / `--restore-last-session`。
实测命令（用**原 profile**，书签与登录态全保留）：

```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy -u ALL_PROXY -u all_proxy \
"D:/Program Files/GptChrome/GptBrowser.exe" \
  --user-data-dir="C:/Users/Administrator/AppData/Local/SPChrome/User Data" \
  --proxy-server="http://127.0.0.1:8888" \
  --proxy-bypass-list="127.0.0.1;localhost" \
  --remote-debugging-port=9334 \
  --no-first-run --no-default-browser-check
```

三个前置判断（不满足就别硬上）：

| 判断 | 方法 | 本例结果 |
|---|---|---|
| 内核是否支持代理开关 | 在 `chrome.dll` 里搜 **不带 `--` 前缀**的 `proxy-server`（Chromium 存的是 `switches::kProxyServer`） | 全都在 |
| 启动器是否转发参数 | 用临时 profile 起一个实例，看 CDP 是否响应、profile 目录是否真的生成 | 转发正常 |
| 书签能否文件迁移 | 看 `Bookmarks` 首字节是否 `{` | **不合法 → 被加密，禁止拷贝** |

> ⚠️ 书签文件被加密（本例 `Bookmarks` 5.2 MB，首字节 `/WW/8/PQfR9Xjj7o`）时，
> **任何"拷贝 Bookmarks 文件到新 profile"的做法都不成立**。
>
> ✅ **但加密 ≠ 书签搬不过去**（v1.2.0 更正）：磁盘是密文，浏览器内存里是明文。
> 走 **步骤 8** 的 `bookmarks_api.py`，可以在**完全不动 profile 文件**的前提下把 378 个文件夹 /
> 7552 条书签原样搬到另一个浏览器。别再下"只能同 profile 重启或手工导出 HTML"的结论。

### 步骤 7 · 标签页双向镜像（两个浏览器同时看同一批页面）

`tab_mirror.py`（同目录）。两端各开一个 CDP 端口，守护进程轮询 `/json/list`，
把一端的**新增页面**用 `PUT /json/new?<url>` 在另一端打开。

```bash
python tab_mirror.py --a 9334 --b 9222 --interval 5
```

四条设计红线（改动前先读）：

1. **只镜像新增，不镜像关闭** —— 关闭承载用户意图，镜像关闭极易误关对方正在操作的标签。
2. **启动即基线** —— 首轮把两端现有 URL 全记入 known，不推送历史，否则一启动就炸开几十个页。
3. **按规范化 URL 去重**，防 A→B→A 回声循环。
4. **只处理 http/https**，`chrome-extension://` 后台页会疯狂抖动，必须跳过。

实测延迟：**≈ 1 个轮询周期（5s 配置下实测 0.9s 命中第一轮）**。

### 步骤 8 · 书签（左侧书签栏）跨浏览器同步

**先纠正一条错结论**：曾判定「GPT 浏览器的 `Bookmarks` 是 5.2MB 密文，只能同 profile 重启或手工导出 HTML」，
**这是错的**。密文只是磁盘形态，浏览器自己有解密后的内存视图 —— 走 `chrome.bookmarks` API 就能拿明文。

`bookmarks_api.py`（同目录）。**必须进 `chrome://bookmarks` 页面里执行**，普通网页没有这个特权 API。

```bash
PY=quant_env/Scripts/python.exe
# 1) 看两端规模（378 文件夹 / 7552 书签 是实测过的真实量级）
$PY bookmarks_api.py --port 9334 --stat
$PY bookmarks_api.py --port 9222 --stat
# 2) 从源端导出明文树（幂等，只读）
$PY bookmarks_api.py --port 9334 --export bookmarks_gpt.json
# 3) 灌进目标端（分批 400 条，7930 条约 20 秒）
$PY bookmarks_api.py --port 9222 --import bookmarks_gpt.json
# 4) 验收：必须看"真书签栏(id=1)"的子项数，不能只看总数
```

**验收硬指标**（别信"总数对上了"）：
- `chrome.bookmarks.getSubTree('1')` 的 `children.length` 必须等于源端书签栏的顶层条目数（本例 244）
- 目标端总书签数 = 源端总书签数（本例 7552）
- 截图字节数必须与上一次不同；若两次截图字节完全相同 = 页面没变，等于白拍

### 步骤 9 · 书签**双向增量**同步（这才是日常默认，步骤 8 只在首次迁移时用）

**步骤 8 的致命缺点**：它是一次性全量快照，**每跑一次就把 7552 条重建一遍**。
日常每次启动都跑 = 书签越滚越多。日常必须用 `bookmark_delta.py`。

```bash
PY=quant_env/Scripts/python.exe

# 只统计（不动数据）
$PY bookmark_delta.py --stat

# 双向增量：A 有 B 没有的补到 B，B 有 A 没有的补回 A
$PY bookmark_delta.py --sync

# 先看会补多少条，不落盘
$PY bookmark_delta.py --sync --dry-run

# 只要单向
$PY bookmark_delta.py --sync --one-way a2b     # GPT -> 港区
$PY bookmark_delta.py --snapshot               # 只落一份快照
$PY bookmark_delta.py --gc                     # 只做滚动清理
```

**增量原理**：读两边真实树 → 路径键用「根序号 + 逐级标题」（**不能用根标题**，
「书签栏」和「Bookmarks bar」是同一个根，用标题当键会把整棵树重造一遍）
→ 叶子按 `路径+url` 去重 → 只 create 对面没有的。

**自测三段探针**（改完代码必须跑，缺一段等于没测）：

```bash
PYTHONPATH=. $PY _logs/test_delta.py
# 期望：源 7553 -> 新建文件夹 1 / 书签 1 / 跳过 7552 -> GPT +1
#       再跑一次 -> 新建 0（幂等）
#       清理后两边复原 7552
```

**快照体积控制**（汤哥口径，物理上限不是"控制一下"）：

| 项 | 值 |
|---|---|
| 单份上限 | 10 MB（gz 实测约 0.5 MB，远低于上限） |
| 滚动保留 | 最近 10 组（一组 = gpt + hk 两份） |
| 总量封顶 | 100 MB，超限从最旧删 |
| 位置 | `_snapshots/bm_YYYYmmdd_HHMMSS_{gpt,hk}.json.gz` |
| 状态记录 | `_snapshots/last_sync.json`（`--check` 读它显示「差 N 条」） |

**启动时自动跑**：`start_all_hk.py` 第 6 步已经是 `ensure_bookmarks()`，
体检输出从 5 项变 6 项：

```
✅ SSH 隧道 3128 / 桥上代理 8888 / GPT CDP 9334 / 港区 CDP 9222 / 标签镜像 / 书签双向同步（差 0 条 · 时间）
```

跳过用 `--no-bookmark`。浏览器刚拉起时 `chrome://bookmarks` 可能没就绪 → 脚本自带 2 次重试，失败不阻断启动。

## 四、十九个血泪坑（每一个都真实踩过）

| # | 坑 | 真因 | 正确做法 |
|---|---|---|---|
| 1 | `ERR_CONNECTION_RESET` 一直修不好 | 不是"没代理"这么简单，而是**本机 DNS 把币安污染成 0.0.0.0/::**。此时用 SOCKS5 一定挂 | 必须 HTTP 代理，让服务器解析 DNS。先 `nslookup` 定性 |
| 2 | `ssh -f -N` 建完隧道，几秒后端口就没了 | bash 命令返回时，**分叉出去的后台进程被回收** | 用后台常驻任务方式起 ssh，不要 `-f` |
| 3 | Chrome 起来了，截图却是别的窗口 / 进程秒退 | GUI 进程用 `subprocess.Popen` 从命令里启动，**命令一结束就被回收** | 同样走后台常驻方式启动 Chrome |
| 4 | `curl http://127.0.0.1:9222` 报 `upstream connect failed` | 环境里有 `HTTP_PROXY=127.0.0.1:63271` 沙箱代理，**本机回环请求也被它接管** | 访问**本机回环**时加 `--noproxy "*"` |
| 4b | **★ 加了 `--noproxy "*"` 后，经代理访问外网全部 `000`、耗时 0.002s** | **`--noproxy "*"` 与 `-x 代理` 互斥** —— 它把"所有主机都不用代理"也包括了代理本身，curl 直接放弃走代理 | **访问外网走代理时用 `--noproxy ""`（空串）或干脆不加**；`--noproxy "*"` 只用于本机回环。**本轮因此误判"GitHub 网页版不通"，实际 200** |
| 5 | Chrome 挂上代理后弹认证框 | xray 3128 是**带 Basic 认证**的 HTTP inbound，而 `--proxy-server` **不支持内联用户名密码** | 用 `hk_proxy_bridge.py` 在本地注入认证头 |
| 6 | `SetForegroundWindow` 调了但窗口不上来 | Windows **前台锁**：非前台进程不能抢焦点 | `ShowWindow(RESTORE)` → `ShowWindow(MAXIMIZE)` → `SetWindowPos(HWND_TOPMOST)` → `BringWindowToTop`，多步叠加 |
| 7 | 置顶后截到的还是错的窗口 | 按标题模糊匹配，把 **命令行窗口**（路径里含"币安"）也置顶了 | 严格匹配窗口类名 `Chrome_WidgetWin_1`，并排除路径特征 |
| 8 | CDP WebSocket 握手回 **`403 Handshake`**，提示 `Rejected an incoming WebSocket connection from the http://127.0.0.1:9334 origin` | Chromium 111+ **强制校验 WS 的 Origin 头**，没带 `--remote-allow-origins` 就拒 | websocket-client 用 **`suppress_origin=True`**（不发 Origin 头即绕过），**不必重启浏览器** |
| 9 | 从 `Tabs_*` 会话文件读 URL 报 `PermissionError` | 浏览器运行中**独占锁住**会话文件 | 只在**备份副本**上解析；`Tabs_*` 里 URL 是明文 UTF-8，正则可直接捞（本例捞出 90 条） |
| 10 | 重启后标签页全没了，只剩一个空白页 | 用 `taskkill /F` 强杀 + `--restore-last-session` **同时存在时恢复机制失效**（它把上次判为异常退出） | 能干净退就干净退；强杀之后要么手工点「要恢复页面吗？→ 恢复」，要么从备份 `Tabs_*` 捞 URL 重开 |
| 11 | 币安页面中央弹 **`The products and services on this website are not intended for individuals in Hong Kong`**，K 线被遮 | **香港出口 IP 触发币安地区提示**，这是独立于代理的第二层拦截 | `cdp_tool.py click-text --text "I Understand"` 点掉即可；点不到时先查 `window.frames`（弹窗可能在 iframe 里） |
| 12 | 用 `click-text` 点按钮，结果弹出了「修改书签」对话框 | JS 按文本匹配 `[class*="btn"]` 时**误命中书签栏上的同名书签** | 匹配串要**足够独特**（用完整英文句子而非「全部」「确定」）；命中后先 `return 候选数`，候选 >1 时人工确认 |
| 13 | 调 `Bookmarks.getTree` 报 **`-32601 'Bookmarks.getTree' wasn't found`**（浏览器级、页面级都报） | **CDP 官方协议里没有 `Bookmarks` 域**，360 系内核更不会补。`chrome.bookmarks` 是 **WebUI 特权 API**，不是 CDP 域 | 别在 CDP 域里找书签。改成连 `chrome://bookmarks` 标签页的 page websocket，用 `Runtime.evaluate` 执行 `chrome.bookmarks.getTree()` |
| 14 | 在普通网页上执行 `chrome.bookmarks` 得到 `NO_API` | `chrome.bookmarks` 只挂在 **`chrome://` 特权页面**上，普通 https 页面拿不到 | 先 `PUT /json/new?chrome://bookmarks/` 开一个书签页（不影响用户现有标签），再在它上面 eval |
| 15 | `chrome.bookmarks.create` 全部失败：**`Error: Bookmark id is invalid`** | 把 `parentId` 写成 `'bookmark_bar'`。**真实根 id 是 `'1'`（书签栏）/ `'2'`（其他书签）**，`bookmark_bar` 只是 DOM 属性名 | 导入前先 `getTree()` 读目标端真实根 id，再按 title 映射成 `ROOT1/ROOT2/ROOT3` 传进 JS |
| 16 | **★ 总数对上了（7552），但真书签栏里只有 2 个空文件夹** | `flatten` 把**根节点本身**当普通 folder 建了一次，全量书签全落进这个"假根"里。`getTree` 的总数统计照样是 7552，**只有查 `getSubTree('1')` 才露馅** | 根节点（书签栏/其他书签/移动设备书签）**永远不创建**，只当父容器占位。验收必须查 `getSubTree('1').children.length`，与源端顶层条目数逐一比对 |
| 17 | **★ 增量同步写成 `JSON.parse(SRC_JSON)` 报 `"[object Object]" is not valid JSON`** | 用 `.replace()` 把 JSON **文本**注入 JS 时，若再套一层 `JSON.parse()`，参数位置收到的是**对象字面量**而不是字符串 | 字面量直接内联：`var srcTree = SRC_JSON;`，**不要**再 `JSON.parse` |
| 18 | **★ 快照滚动删不干净：说"留 10 份"，实际全天并成 1 组** | 组名用 `bm_20261024_010203_gpt.json.gz`.rsplit('_',2)[0] → 得到 `bm_20261024`，同一天所有快照全归一组 | 先剥 `.json.gz` 后缀，再 `rsplit('_',1)[0]`；改完必须造 12 组假快照实测"删最旧 2 组" |
| 19 | 日常启动越跑书签越多 | 用步骤 8 的全量导入当日常同步，每次重建 7552 条 | 日常只用步骤 9 的 `bookmark_delta.py --sync`（差额补齐 + sha256 幂等） |

## 五、验证器本身也要反测

**「颜色出现过」≠「东西画出来了」**（记忆铁律 §5.4）。
本项目对应的反测：拿 `--proxy-server` 去掉再重跑一次，`title` 必须变成 `ERR_*`。
抓不住，说明这套验证是假的。

## 六、回滚

```bash
# 停桥接器
taskkill /IM python.exe /F   # 或按 PID 精确结束
# 停隧道
taskkill /IM ssh.exe /F
# 浏览器直接关窗口即可，独立 profile 想删就删
```

全程**不写注册表、不改系统代理、不装任何软件**，关掉进程即恢复原状。
这是本方案优于「改 WinINET 系统代理」的核心原因：零全局副作用。

## 七、已知边界（诚实写清）

- 币安对**数据中心 IP** 有风控，裸 `curl` 常返 `202` + 空 body。**这是正常的**，
  浏览器有完整 TLS 指纹与 JS 才能过，所以判据必须用浏览器/CDP，不能只看 curl。
- 香港服务器只有 3.6G 内存，**不要拿它跑大流量下载**（视频、全市场 K 线批量包）。
  批量 K 线仍优先走 `data.binance.vision`（不依赖代理）。
- SSH 隧道是单点：隧道断 → 代理断。别在生产脚本里硬依赖它，要带回退直连判断。
- **桥接器（8888）会被父 shell 的进程树清理带走**：实测用 `subprocess.Popen(DETACHED_PROCESS)`
  起的桥接，父命令一返回就消失（日志里有 `listening`，端口却没了）。**必须用后台常驻任务方式起**。
  → 所以 `start_all_hk.py` 的体检项只能证明"端口在"，**不能证明"能出网"**，
  出网判据永远是 `curl -x http://127.0.0.1:8888 https://www.binance.com/` 返回 `202`。
- **书签同步是单向快照，不是持续同步**：`bookmarks_api.py --import` 是"把源端树灌进目标端"，
  重复执行会**重复创建**（没有去重）。要持续同步得先做"目标端清空 + 重灌"或加增量 diff。

## 八、关联件

- `hk_proxy_bridge.py` —— 本技能核心脚本（同目录）
- `start_hk_browser.py` —— 一键启动器（Chrome，同目录）
- **`tab_mirror.py`** —— 标签页双向镜像守护（v1.1.0 新增）
- **`cdp_tool.py`** —— CDP 轻量工具：list / eval / click-text / newtab（v1.1.0 新增）
- **`bookmarks_api.py`** —— 书签树导出/导入（v1.2.0 新增，走 `chrome://bookmarks` 里的 `chrome.bookmarks` API）
- **`win_click.py`** —— 按截图坐标点击（DPI aware，Chromium 只认真实输入队列）
- 项目侧：`_patches/launch_hk_chrome.py`（带 CDP 三层验证的启动脚本）
- 项目侧：`币安账户数据/binance_account_pull.py`（只读 API 拉历史流水，走 8888 出口）

## 九、版本履历

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0.0 | 2026-10-23 | 初版：四段链路 + Chrome 接管 + 7 坑（含 `--noproxy` 互斥） |
| v1.1.0 | 2026-10-23 | 新增步骤 6（接管带 AI 标识的定制浏览器：参数转发 / 书签加密判定 / 原 profile 重启）+ 步骤 7（标签双向镜像四条红线）+ 坑 8~12（CDP Origin 403 / 会话文件独占锁 / 强杀丢标签 / 地区限制弹窗 / click-text 误命中书签） |
| **v1.2.0** | **2026-10-24** | **新增步骤 8（书签跨浏览器同步）；纠正 v1.1.0 的错结论「书签是密文只能导出 HTML」——磁盘密文不等于内存不可读；新增坑 13~16（CDP 无 Bookmarks 域 / chrome.bookmarks 仅特权页 / 根 id 是 '1' 不是 'bookmark_bar' / 根节点当 folder 建导致全量落进假根）；边界补「桥接器会被进程树清理带走」「书签是单向快照」** |
