---
title: 迭代记录·GLM-5.3-flash接入分身大脑（四化）
tags: [四化迭代, GLM, 5.3-flash, 大脑, 智谱, 汤小龙]
source: 汤哥提供 GLM Coding 7天体验卡，要求配置 GLM-5.3-flash
distilled_at: 2026-08-27
protocol: 全域模板#321 + 1234「4」四化迭代
---

# 迭代记录 · GLM-5.3-flash 接入分身大脑（2026-08-27）

## 智能化
- 验证 GLM key 有效，列出模型含 glm-5.3 / glm-5.3-flash。
- 识别 glm-5.3-flash 为推理模型：输出在 reasoning_content，需给足 max_tokens。

## 定制化
- key 存用户级环境变量 GLM_API_KEY（不落盘到代码/版本库）。
- nvidia_avatar.py 增加 glm_chat 路由 + 默认优先 GLM；启动我的AI分身.py 同步。

## 全自动化
- 启动我的AI分身 → 大脑显示 glm-5.3-flash，实测开口。
- 到期(2026-09-03)后无 GLM_API_KEY 自动回退 NVIDIA llama-vision。

## 自我净化
- 说明：分身已用上 GLM；若让 Codex 会话本体也切 GLM，需改 config.toml 并重启（会断当前会话），故先配到分身。

## 结果路径
- 大脑：`AI分身实体\nvidia_avatar.py`（glm_chat）
- 环境变量：GLM_API_KEY（用户级）
- Obsidian：`Obsidian\wiki\我的AI分身\`