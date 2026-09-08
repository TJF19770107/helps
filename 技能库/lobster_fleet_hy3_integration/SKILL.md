---
name: "lobster_fleet_hy3_integration"
description: "多Agent舰队接入腾讯云混元3 (hy3-preview) 第三方模型：能力对比、Anthropic直连架构、环境变量注入、Token额度隔离、切换回滚SOP。触发词：接入混元3 / hy3-preview / 切换模型 / 第三方模型接入 / Codex切模型 / Claude Code切模型 / 额度隔离"
version: "1.0.0"
date: "2026-07-19"
category: "model-integration"
related_protocols: ["#293 多Agent舰队第三方模型接入规范", "#288 模型后端切换", "#290 ORCA工作树自动填充配置规范"]
related_skills: ["orca-agent-connection-fix"]
primary_path: "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_fleet_hy3_integration\SKILL.md"
plan_doc: "E:\龙虾AI主控中心\我的AI分身\docs\多Agent舰队编排\混元3接入计划.md"
---

# 多Agent舰队混元3 (hy3-preview) 接入技能

## 核心结论（一句话）
hy3-preview 是**标准 Anthropic 兼容 API** → **Claude Code 直连、无需协议桥**；256K 上下文 + Agent 专项强化，是舰队主力模型的优选；额度与 Qwen2.5 必须隔离统计。

## 模型能力对比（速查）
| 维度 | hy3-preview | Qwen2.5-72B |
|------|------------|-------------|
| 上下文 | **256K** | 128K |
| 代码/Agent | 专项强化(495步工作流) | 强但非专项 |
| 推理 | 复杂STEM领先 | 强 |
| 成本 | 输入~1元/百万 | 额度制 |
| 许可 | Apache 2.0 | 多许可 |

## 接入架构（直连优先）
- **Claude Code**：`ANTHROPIC_BASE_URL` → hy3 `/v1/messages`（直连，停用 15721 桥接转发）
- **Codex**：若 hy3 暴露 OpenAI 端点 → `base_url` 直连；否则经 `lobster_protocol_bridge.py`（翻转方向收 OpenAI→转 Anthropic→hy3）
- **Hermes**：后端变量指向 hy3（灰度阶段）
- **WorkBuddy**：本机运行时，本次不动

## 关键脚本（plan_doc 同目录 scripts/）
- `hy3_env_linux.sh` — 云端注入
- `hy3_env_windows.ps1` — 本地注入
- `claude_code_hy3.json` / `codex_hy3.toml` / `cursor_hy3.json` — 配置模板
- `hy3_token_monitor.py` — 额度隔离监控告警（hy3/qwen 分账，50/80/95% 分级告警，<5% 强制回滚）

## 切换/回滚铁律
1. 切换前快照 Qwen 配置（`settings.backup_qwen.json` / `config.backup_qwen.toml`）
2. 切换 = 应用 hy3 模板；回滚 = 还原快照（秒级）
3. 触发回滚：额度剩余<5% / endpoint 连续报错 / 试点成功率低于 Qwen 基线
4. 详细 SOP 见 `hy3_switch_rollback_sop.md`

## 四阶段落地
测试验证(Phase0) → 单Agent试点 Codex+Claude Code(Phase1) → 全舰队灰度+Hermes(Phase2) → 全量上线(Phase3)

## 执行前必做
从 CloudBase 控制台获取 hy3 **真实 endpoint + API Key**，替换所有 `<<HY3_ANTHROPIC_URL>>` / `<<HY3_API_KEY>>` 占位符。
