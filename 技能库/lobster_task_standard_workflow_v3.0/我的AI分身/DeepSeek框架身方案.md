# 汤小龙 · DeepSeek 框架身方案（2026-08-27）

## 目标
让汤小龙从「定义+脚本」升级为「真框架型智能体」，可跑在 DeepSeek/Codex/Claude Code 任意运行时。

## 原理（灵魂不换，身体可换）
- 灵魂：SOUL.md（画像/红线/八识）——不变。
- 身体：宿主框架的运行时（工具循环、MCP、会话、插件）——由谁打开谁提供。
- 桥梁：AGENTS.md —— 让任意 Agent 打开本目录就加载汤小龙。

## 三种框架身（按落地难度）
| 方案 | 说明 | 难度 | 推荐 |
|------|------|------|------|
| A. AGENTS.md 挂载 | 用 Codex/Claude Code/DeepSeek Agent 打开本目录即成为汤小龙 | 低 | ✅ 立即做（已建） |
| B. Agent SDK 引擎 | 用 OpenAI Agents SDK/LangGraph 写 avatar 的 tool-loop + MCP 客户端 | 中 | 下一步 |
| C. DeepSeek Harness | 用 DeepSeek「一切皆插件」harness，把汤小龙 SOUL+工具+MCP 打包成 persona/插件 | 高 | 远期 |

## 落地步骤（方案 A，已完成）
1. `AGENTS.md`（本目录）= 框架身入口，含灵魂/技能/四库/红线。
2. 全局 AGENTS 加「启动汤小龙」触发。
3. `启动汤小龙.cmd` 一键拉起。

## 下一步（方案 B，可选）
- 把 avatar.py 换成 Agents SDK：定义 `!web`/`!edit`/`!render_video` 为真 tool，接 MCP client，自带会话记忆。