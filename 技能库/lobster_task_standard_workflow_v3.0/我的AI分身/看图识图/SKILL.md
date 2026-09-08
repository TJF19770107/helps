---
title: 看图识图（眼睛）
summary: 截图+读图合并：PowerShell 截屏 → NVIDIA 免费视觉模型 → 中文描述。让分身看屏幕/读图
tags: [看图, 截屏, 视觉, 多模态, NVIDIA, llama-vision]
version: v1.0
distilled_at: 2026-08-27
home: 技能库\lobster_task_standard_workflow_v3.0\我的AI分身\看图识图
---

# 看图识图（眼睛）v1.0

## 用法（一个动作：截图+读图）
```bash
python "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体\scripts\capture_and_read.py" "读一下屏幕上有什么"
```
只读图不截图：
```bash
python "...\AI分身实体\scripts\vision_read.py" "图片路径.png" "描述这张图"
```

## 依赖
- 脚本：`AI分身实体\scripts\capture_and_read.py` + `vision_read.py`
- Python：workbuddy 3.13.12（含 ssl）
- 视觉模型：`meta/llama-3.2-11b-vision-instruct`（免费，已验证）
  备选：`meta/llama-3.2-90b-vision-instruct`（强但慢）/ `microsoft/phi-3-vision-128k-instruct`
- 注意：`z-ai/glm-5.2` 已于 2026-08-21 在 NVIDIA 下架

## 边界
- 本体（DeepSeek V4 Flash）无视觉，本技能走「外部视觉模型中转」看图。
- 要让本体直接看图，需把 Codex model provider 切到多模态模型。