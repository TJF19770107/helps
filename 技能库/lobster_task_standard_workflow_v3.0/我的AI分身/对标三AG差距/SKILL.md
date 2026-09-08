---
title: 对标三AG差距清单（分身 vs Codex/Claude Code/Hermes）
summary: 逐项列出汤小龙与三AG的差距、弥补路径（零积分优先）、验收标准
tags: [对标, 差距, Codex, ClaudeCode, Hermes, 三AG, 弥补路径]
version: v1.0
distilled_at: 2026-08-27
home: 技能库\lobster_task_standard_workflow_v3.0\我的AI分身\对标三AG差距
---

# 对标三AG差距清单 v1.0

> 三AG = Codex（执行落地）/ Claude Code（审核把关）/ Hermes（大脑研判）。
> 汤小龙目标：灵魂独有 + 能力逐项追平三AG。

## 一、能力逐项对比

| 能力项 | Codex | Claude Code | Hermes | 汤小龙现状 | 差距 | 弥补路径（零积分优先） |
|--------|-------|-------------|--------|-----------|------|------------------------|
| **代码编辑** | ✅ 强（apply_patch/多文件） | ✅ 强 | 🔶 一般 | 🔶 基础（subprocess调脚本） | 缺原生多文件编辑 | 接 `workspace-tools` 或直接调 PowerShell 批处理 |
| **终端执行** | ✅ 原生 | ✅ 原生 | ✅ 原生 | ✅ 已有（subprocess） | 追平 | 已通 |
| **视觉看图** | ❌ 本体无（DeepSeek V4 Flash） | ❌ 本体无 | ❌ 本体无 | ✅ 已有（NVIDIA llama-vision 中转） | **反超** | 已通（capture_and_read.py） |
| **大脑模型** | DeepSeek V4 Flash | GLM/deepseek | glm-5.2/deepseek | NVIDIA llama-vision | 模型选择面窄 | 挂接 AtomCode 13460（Qwen3-VL/GLM）作为备选大脑 |
| **MCP生态** | ✅ 20+连接器 | ✅ 20+ | ✅ 20+ | 🔶 继承宿主（WorkBuddy） | 缺独立MCP管理 | 统一登记 `MCP_插件\`，逐步独立加载 |
| **记忆持久化** | 🔶 会话级 | 🔶 会话级 | ✅ 有 | ✅ 四库+日志 | **追平并超** | 已通 |
| **灵魂/人格** | ❌ 无 | ❌ 无 | 🔶 弱 | ✅ SOUL.md + 心理画像 | **独有优势** | 保持并深化（实时增量 + 月度画像回灌） |
| **多Agent编排** | 🔶 接收信号 | 🔶 接收信号 | ✅ 主控 | 🔶 待接入ORCA | 缺编排能力 | 接 ORCA msgbus（30天内，路线图Phase2） |
| **自愈/守护** | ✅ fleet_guardian | 🔶 一般 | 🔶 一般 | ❌ 无 | 缺守护进程 | 复用 fleet_guardian.py 注册分身守护任务 |
| **快照回滚** | ✅ 有 | ✅ 有 | ✅ 有 | ✅ 已有（make_avatar_snapshot.py 0.02MB） | 追平 | 已通 |

## 二、差距总纲（一句话）

> **汤小龙独有：灵魂（画像+红线+修行）。**
> **汤小龙领先：看图识图（三AG本体都无视觉）。**
> **汤小龙要追：代码编辑力 + 独立MCP管理 + 多Agent编排 + 守护自愈。**

## 三、弥补优先级（零积分路径）

| 优先 | 缺口 | 动作 | 验收 |
|------|------|------|------|
| P0 | 守护自愈 | 注册 `schtasks` 定时任务：每30分钟检测分身进程，挂掉自动重启 | 杀掉 nvidia_avatar 进程后 30 分钟内自动拉起 |
| P1 | 多Agent编排 | 接 ORCA msgbus 消费信号文件 | 分身能读 `fleet_exchange/doing/*.json` 并响应 |
| P2 | 独立MCP | 在 `MCP_插件\` 建 connector 注册表 + 启动器 | 分身独立调 IMA/乐享 不依赖宿主 |
| P3 | 代码编辑力 | 封装 PowerShell 多文件编辑为 `!edit` 工具 | 能改文件+写回+验证 |

## 四、执行机制

每轮任务完成后三问（persona-gap-closer 实时层）：
1. 这轮暴露了什么新差距？
2. 这轮追平了哪项？
3. 差距分数微调多少？