# 🦞 AI 分身实体 · 使用说明（v1.0 · 2026-08-27）

> **回答汤哥的灵魂拷问：现在这个「我的AI分身」是不是 AI agent？**
> 之前的答案是**定义态**（灵魂+技能+四库，寄居在 WorkBuddy 里的角色配置）。
> **本目录 = 运行时态**——一个像 Codex / Claude Code 一样**独立进程、独立大脑**的 agent，不依赖 WorkBuddy。

## 三具身体（灵魂同一个：SOUL.md）

| 身体 | 大脑 | 启动方式 | 成本 | 状态 |
|------|------|----------|------|------|
| **avatar.py**（自建CLI） | Ollama 本地（deepseek-r1:7b 等） | 双击 `启动AI分身.bat` | **0 元 / 离线** | ✅ 本目录，可直接跑 |
| **Claude Code** | CC-Switch 网关 15721 → GLM | `cd 本目录 && claude` | 走网关 | ✅ 已配 |
| **Codex CLI** | Ollama / 网关 | `cd 本目录 && codex` | 走网关 | 🔌 可选 |

## 快速开始（avatar.py）

```
双击 启动AI分身.bat
或命令行：python avatar.py "帮我把X主题出成30秒口播"

换大脑：python avatar.py --brain qwen3:0.6b
        （本机已有：deepseek-r1:7b / qwen3:0.6b / gemma4:e4b / qwen2.5vl:7b / minicpm-v 视觉 / 云端 deepseek-v4-flash / kimi-k2.6 / minimax-m2.7）
```

## 内置工具（输入 `!工具名 参数`）

- `!render_video make_koubo_sample3.py` —— 零成本出片
- `!note 今天完成了X` —— 写工作日志
- `!search_kb 关键词` —— 查 Obsidian 我的AI分身库

## 换大脑为云端（当 Ollama 不够强时）

1. **MiMo V2.5 Pro**：设环境变量 `MIMO_API_KEY`（token-plan-cn 的新 token 需重新申请，旧的已 401 过期）
2. **DeepSeek**：设 `DEEPSEEK_API_KEY`（platform.deepseek.com 申请，sk- 开头）
3. **HY3 混元**：设 `HY3_API_KEY`（CloudBase 中继，10亿免费token）

> ⚠️ 密钥只放环境变量，绝不写进本目录任何文件（安全红线）。

## 多大脑自动探测（v1.1）

`avatar.py` 启动时按顺序自动选可用的：
`--brain` 显式指定 → MiMo（有 MIMO_API_KEY）→ DeepSeek（有 DEEPSEEK_API_KEY）→ Ollama 本地

**当前状态（2026-08-27 实测）**：
- ✅ 实体（SOUL.md 灵魂 + avatar.py 身体 + 工具 + bat）—— 全部就绪
- ❌ MiMo key 已过期（401）→ 需新 token
- ❌ DeepSeek 环境变量是占位符（atomical... 无效）→ 需真 sk- key
- ❌ Ollama 本地模型 blob 损坏（E:\Ollama\models 缺文件）→ 需重新 pull 或修复
- ❌ Claude Code 网关 15721 会话未注入（CC-Switch 客户端需重启激活）

**解锁 = 一个有效令牌**。给任意一个（MiMo 新 token / DeepSeek sk- key），汤小龙立即开口。

## 灵魂可移植

`SOUL.md` 就是灵魂。任何 agent（Claude Code / Codex / WorkBuddy / 未来的 ORCA 舰队）加载它 = 成为汤小龙。
**灵魂不换，身体可换。**

## 进化

每轮任务 = 一次学习（四化闭环）。技能沉淀进 `E:\龙虾AI主控中心\我的AI分身\AI分身接单出片Skill库\`。
