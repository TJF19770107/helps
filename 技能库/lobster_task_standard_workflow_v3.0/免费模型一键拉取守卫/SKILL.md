---
name: 免费模型一键拉取守卫
description: 一键恢复 Codex 下拉框的 0.01 折/免费模型（deepseek-v4-flash-free / glm-5.3-flash-free / deepseek-v4-pro-free），防止退出后模型消失；附带轻量快照与回滚指引。
version: v1.0
distilled_at: 2026-09-06
distilled_by: 汤小龙 · 四化迭代知识库
---

# 免费模型一键拉取守卫

## 用途

退出 Codex / 被网关覆盖后，快速把三个免费/0.01 折模型恢复到下拉框：
`deepseek-v4-flash-free`、`glm-5.3-flash-free`、`deepseek-v4-pro-free`。

## 一键执行

```powershell
C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体\扫描宿主能力.py"
```

此脚本会做三层守卫：

1. 默认模型行：`C:\Users\Administrator\.codex-orch\config.toml` 的 model 写回 `gpt-5.6-luna`。
2. 下拉框目录：`backups_state\teamorouter-fast\model-catalog.json` 补回三个免费模型，缺失时从 `MCP服务\model-catalog.M001.candidate.json` 恢复。
3. 网关别名表：`teamorouter-http-proxy.json` 的 alias_map 强制为免费映射。

## 巡检

计划任务 `Lobster_AvatarCapabilitySync` 每 15 分钟自动补一次；手动说「启用汤小龙」或「四化迭代知识库」也会触发同一守卫。

## 快照与回滚

- 最新快照目录：`E:\龙虾AI主控中心\MCP服务\snapshots\`
- 最近基线：`snapshot_20260906_063700.tar.gz`（<20MB）
- 回滚后必须再跑一次上面的守卫脚本，避免恢复把新修复覆盖掉。

## 实测锚点

- 2026-09-06 验证：Orca 重启后 runtime ready；企业微信窗口可被识别/截图，OCR 读到“接单群”“客服”等真实信息。
- 截图证据：`E:\龙虾AI主控中心\Obsidian\wiki\AI工具运维\20260906_分身之眼_企业微信接单群截图.png`
