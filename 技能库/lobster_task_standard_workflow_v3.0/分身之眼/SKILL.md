---
name: 分身之眼
description: 汤小龙AI分身的视觉感知与桌面操控能力（UFO + Orca computer-use），看屏幕、读应用、点按钮、提取信息。
version: v1.0
distilled_at: 2026-09-05
distilled_by: 汤小龙 · 四化迭代知识库
---

# 分身之眼（AI分身视觉与桌面操控）

## 定位

分身之眼 = 眼睛（截图识图）+ 大脑（LLM规划）+ 手（模拟键鼠）。
它是汤小龙AI分身的原生视觉器官，不是外部工具。

## 触发逻辑（自动扫描）

用户说「启动我的AI分身 / 汤小龙 / 调用1234 / 四化迭代知识库 / 龙虾五步法 / 全域模板」时，
自动扫描当前任务是否涉及 GUI 操作（桌面应用、群消息、弹窗、界面数据）。
匹配即挂载，无需用户点名。

## 双引擎

| 引擎 | 路径 | 适用 |
|---|---|---|
| Orca computer-use | Codex 内置 | 即时单次操作：点弹窗、读屏幕、填表单 |
| 微软 UFO | `我的AI分身\tools\UFO` | 编排长任务、定时无人值守、多步骤流程 |

## 启动命令（UFO）

```powershell
cd E:\龙虾AI主控中心\我的AI分身\tools\UFO
.\.venv\Scripts\python.exe -m ufo -t <任务名> -r "<自然语言指令>"
```

## 模型链路

UFO → TeamoRouter（https://teamorouter.cn/v1/chat/completions）→ glm-5.3-flash（视觉已实测）
API Key 走环境变量 `TEAMOROUTER_API_KEY`，零落盘。
免费额度每日 0 点重置，白天自动落 5 折付费档（单次约 0.0002 美元）。

## 部署事实（2026-09-05）

- Python 3.10.11：`C:\Users\Administrator\.workbuddy\binaries\python\versions\3.10.11\`（UFO 不支持 3.13）
- venv：`tools\UFO\.venv\`（依赖已装齐）
- 配置：`tools\UFO\config\ufo\agents.yaml`（五个 Agent 全部指向 TeamoRouter）
- GitHub 克隆走 socks5h://127.0.0.1:1081 代理

## 标准应用：企微接单群信息提取

1. 启动 UFO，指令：打开企业微信 → 定位接单群 → 滚动读取最新消息
2. 截图交视觉模型 → 提取结构化字段（客户/需求/价格/时间/联系人）
3. 落盘 `Obsidian wiki/Projects/企微接单流水/` 按日期归档

## 边界

- 长链路任务必须拆短段，单段成功率高，几十步连续操作会迷路。
- 企微历史库（message.db）是 SQLCipher 加密，直读不可行，视觉读取是主路线。
- 不依赖香港服务器：模型走 TeamoRouter 国内直连，本地只跑 UFO 框架本身。

## 实测归档（2026-09-06）

- Orca computer-use 已重启并验证 runtime ready，可识别 WXWork 主窗口。
- 截图证据：`Obsidian\wiki\AI工具运维\20260906_分身之眼_企业微信接单群截图.png`
- 详细记录：`Obsidian\wiki\AI工具运维\20260906_分身之眼企业微信实测_四化迭代.md`
- 边界：Orca 默认截图是可见桌面区域，目标被遮挡时会拍错；窗口本体可用 PrintWindow 补抓。
