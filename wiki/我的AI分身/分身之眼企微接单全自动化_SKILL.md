---
name: 分身之眼企微接单全自动化
description: 用 Orca computer-use + 窗口截图 + OCR 自动操控企业微信接单群：进群、滚动消息、进接单大厅、展开分类、截图归档、整理可接/不可接订单表。v1.1 起融合"眼睛扩展模块"：浏览器窗口RPA、进程定位、GitHub云上自动化，供汤小龙接单筛选与云上交付使用。
version: v1.1
distilled_at: 2026-09-07
distilled_by: 汤小龙 · 1234 · 四化迭代知识库
---

# 分身之眼企微接单全自动化

## 定位
分身之眼负责“看”：进群、看消息、点开大厅、截屏、OCR、整理订单表。
模型负责“判”：哪些能接、哪些不能接、哪些高性价比。
汤哥或 Codex 负责“审”：审核通过后才允许对外申请接单或回复客户。

## 标准流程
1. 确认 Orca runtime ready：`orca status --json`，限时 5 秒；失败后立即切换通道（系统级窗口截图/OCR → Win32 API → 用户可视化确认），任务标准不降低、子任务不跳过、不标记失败，直到目标页面截图和 OCR 全部完成
2. 确认企业微信运行：`Get-Process -Name WXWork`
3. 置前企微窗口：`AppActivate` + `SetForegroundWindow`
4. 截取窗口本体：`PrintWindow` 保存 PNG
5. OCR 定位群名/订单卡/按钮：`tesseract ... tsv`
6. 用坐标点击进入群聊、滚动消息、进入接单大厅、展开分类
7. 每个关键页面保存截图并 OCR
8. 归档到 `Obsidian\wiki\AI工具运维\`
9. 输出筛选表：可接 / 不可接 / 待确认 / 高性价比
10. 审核通过前，不代替汤哥对外申请接单

## 关键命令
```powershell
orca status --json
orca computer get-app-state --app WXWork --restore-window --json
& 'C:\Program Files\Tesseract-OCR\tesseract.exe' screenshot.png stdout -l chi_sim+eng --psm 6
```

## 截图锚点
- 群内订单卡：`20260906_新人接单31群_群内订单卡截图.png`
- 历史订单：`20260906_新人接单31群_历史订单截图.png`
- 接单大厅：`20260906_接单大厅_单条订单截图.png`
- 分类菜单：`20260906_接单大厅_分类菜单截图.png`

## 边界
- 企微安全验证不能绕过，必须由汤哥手机扫码。
- 坐标会随窗口大小/缩放变化，每次先截图+OCR定位，不要沿用旧坐标硬点。
- 只能只读收集信息，申请接单/回复客户前必须人工审核。

---

## 眼睛扩展模块（v1.1 · 2026-09-07 实战融合）

> 定位升级：分身之眼 = 汤哥 AI 分身的**眼睛**（看清页面）+ **手**（像人一样操控桌面）+ **云腿**（把成果自动送上云端）。
> 以下三招全部来自 2026-09-06/07 GptBrowser 扩展安装 + GitHub 交付实战，零积分、纯本地。

### 模块 A：浏览器窗口 RPA（看清任意浏览器页面）
1. **定位目标浏览器**：枚举进程命令行（ctypes `NtQueryInformationProcess`），按 `--user-data-dir` / `--profile-directory` 匹配，绝不猜路径。
   - 兜底：主进程没写 user-data-dir 时，找配套 `crashpad-handler.exe` 的 `--user-data-dir`，它一定写。
   - 本机对照：GptBrowser=`...\SPChrome\User Data`；#2本地=`...\Chrome\LocalProfile`；香港代理=`...\Chrome\ProxyProfile`。
2. **截渲染面**：渲染面 = 子窗口 `Chrome_RenderWidgetHostHWND`。
   - ⚠️ GPU 硬件加速窗口 `PrintWindow` 会返回**空白图** → 改**屏幕 BitBlt**：`SetForegroundWindow` + `ShowWindow(9)`还原再`(3)`最大化后，抓桌面 DC 的窗口矩形。
3. **导航**：地址栏用快捷键 **Ctrl+L** 聚焦（比点坐标 (700,40) 稳），输入 URL + Enter，等标题变化确认。
4. 脚本复用：`E:\lobster_ai_temp_fleet\scripts\capture_all_v2.py`、`capture_hkproxy_bitblt.py`、`scan_chrome_cmdlines.py`。

### 模块 B：GitHub 云上自动化（凭证自检 → 自建仓 → 窗口推送）
1. **凭证自检（不弹窗不打印密钥）**：`git credential fill` 取已存凭证 → API `/user` 鉴权 → 只输出状态码+用户名，**token 本体绝不打印**。
   - "Repository not found" 404 ≠ 凭证失效，GitHub 对「不存在」和「私有未授权」都返回同句 404 → 必须先 `/user` 鉴权再下结论。
2. **仓库不存在（404）且 scopes 含 repo** → 直接 `POST /user/repos` 自动建仓（含中文 description 注解）；改名/改描述/改可见性用 `PATCH /repos/{owner}/{repo}`。
3. **GFW 抖动推送**：直连时通时断时 → ①`netstat` 查本地代理端口是否活着 ②Python socket 测 github.com 各 IPv4 的 443 连通 ③趁窗口期 `git push`，推完 `git ls-remote` 回查 HEAD 指纹核实（快递单号回查签收）。
4. 凭证弹窗坑：gh-proxy 只支持拉取**不支持推送**，卡死产生的 GCM 弹窗直接杀进程+点×，勿填。

### 模块 C：触发词
| 汤哥说 | 动作 |
|---|---|
| 分身之眼看XX页面 | 模块A：定位进程→BitBlt 截图→OCR |
| 上传GitHub / 传GitHub | 模块B：凭证自检→建仓(如缺)→推送→ls-remote核实 |
| 分身之眼进化 | 本模块 = v1.1 眼睛扩展能力清单 |
