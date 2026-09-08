# Chatbox 配置指南 — 统一聊天窗口（4 Tab + 可随时扩展）

> 配套：多智能体舰队编排 v1.1 ｜ 更新：2026-07-14
> 目标：把 Codex / Claude / Hermes / Ollama 都变成「可贴截图的聊天窗口」，不再困在 IDE 里。

---

## 一、下载安装

- 官网：**https://chatboxai.app**（桌面端，免费，Win/Mac/Linux）
- 安装 → 打开 → 左上角「会话」旁点「+ 添加模型提供方」即可新增 Tab
- 每个 Tab = 一个独立后端连接，互相隔离，可随时加/删

---

## 二、4 个核心 Tab 配置

### 🟠 Tab 1 · MiMO V2.5 Pro（主力推理 / 编码）
| 项 | 值 |
|----|----|
| 模型提供方 | OpenAI 兼容 |
| API 域名 (Base URL) | `https://token-plan-cn.xiaomimimo.com/v1` |
| API 密钥 | 你的 MiMO Token Plan Key（=`$MIMO_API_KEY`） |
| 模型 | `mimo-v2.5-pro` |

### 🔵 Tab 2 · Claude Code（多模态截图核查）
| 项 | 值 |
|----|----|
| 模型提供方 | Anthropic |
| API 域名 | `https://token-plan-cn.xiaomimimo.com/anthropic/v1`（走 MiMO 协议转换） |
| API 密钥 | 同 MiMO Key |
| 模型 | `claude-sonnet-4-8`（或 MiMO 路由的 claude 型号） |

### 🟢 Tab 3 · Hermes（大脑 / 规划）
| 项 | 值 |
|----|----|
| 模型提供方 | 按 Hermes 实际端点填（OpenAI 兼容 / 自定义） |
| API 域名 | `<Hermes 提供的 Base URL>` |
| API 密钥 | `<Hermes Key>` |
| 模型 | `<Hermes 模型名>` |

> ⚠️ Hermes 端点需你确认。若暂未配置，可先建空 Tab 占位，连通后填。

### ⚪ Tab 4 · Ollama 本地（免费热备）
| 项 | 值 |
|----|----|
| 模型提供方 | Ollama |
| API 域名 | `http://localhost:11434` |
| 模型 | `gemma4:e4b`（拉取后）或 `qwen3.5:2b`（已在本地，立即可用） |

---

## 三、随时扩展（不止 4 个）

Chatbox 支持任意数量 Tab。建议后续加：
- **Tab 5 · DeepSeek V4 Pro** — 二级数学推理专员（补 MiMO 数学短板）
- **Tab 6 · WorkBuddy / Hy3** — 如需在 Chatbox 内用（一般不必要，WorkBuddy 本身是独立入口）

新增方式：设置 → 添加模型提供方 → 填对应 Base/Key/Model → 保存即多一个 Tab。

---

## 四、与 WorkBuddy 的配合（前端策略，2026-07-14 拍板）

| 场景 | 用谁 | 成本 |
|------|------|------|
| 日常聊天 / Codex 前端 / 调 Agent | **WorkBuddy（我）** | 花 Hy3 积分（系数仅 0.02x，极低） |
| 积分告急 / 长程长跑 | **Chatbox Tab1（MiMO）** | 零积分，走 Token Plan |

**本质**：WorkBuddy = 高上下文便利入口（能读仓库、一键调 Agent、贴截图）；Chatbox+MiMO = 低成本长跑入口。两者互补，不冲突。

---

## 五、排错速查

| 现象 | 可能原因 | 处理 |
|------|---------|------|
| Tab1/2 连不上 | MiMO 到期 / 端口崩 | 检查 18808、确认 Token Plan 续费 |
| Tab4 无模型 | Ollama 未启动 | `ollama serve` 或重开 Ollama 客户端 |
| Tab4 找不到 gemma | 未拉取 | 按 ollama-bridge 技能部署到 G 盘后 `ollama pull gemma4:e4b` |
| 所有 Tab 超时 | 代理/网络断 | 检查 Clash 是否开启系统代理 |
