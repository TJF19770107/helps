---
title: 迭代记录·NVIDIA/GLM免费接入Codex provider（四化）
tags: [四化迭代, NVIDIA, GLM, provider, Codex, 免费大脑]
source: 汤哥指令「把NVIDIA免费也配到Codex对话框/找0.01折v4flash配置」
distilled_at: 2026-08-27
protocol: 全域模板#321 + 1234「4」四化迭代
---

# 迭代记录 · NVIDIA/GLM 免费 provider 接入（2026-08-27）

## 智能化
- 定位「配上没用上」根因：config 已是 custom→15721(MiMo 代理)，非 NVIDIA；GLM_API_KEY 在用户级注册表但当前 shell 子进程环境未刷新，分身回退 NVIDIA。
- 纠正：分身默认 NVIDIA 免费 = Llama-3.2 vision，不是 GLM。

## 定制化
- config.toml 新增 model_providers.nvidia_free（Llama vision, NVIDIA）与 glm_free（智谱 GLM），TOML 解析通过（custom/nvidia_free/glm_free）。
- key 存用户级环境变量 NVIDIA_API_KEY / GLM_API_KEY。

## 全自动化
- 历史会话确认旧配置 model_provider=CodexPlusPlus（Codex++→DeepSeek V4 Flash）；「0.01折」为 Codex++ 界面标签，非配置字面量。
- 切换需改 model_provider 并重启 Codex（会断当前对话），故先只新增 provider，未擅自切换。

## 自我净化
- 明确启用路径与重启副作用，不误导。

## 结果路径
- 配置：`C:\Users\Administrator\.codex\config.toml`（备份 C:\tmp\codex_config_backup_20260827_212312.toml）
- Obsidian：`Obsidian\wiki\我的AI分身\`