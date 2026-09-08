---
title: 开口（大脑）
summary: NVIDIA 免费大脑让分身开口。nvidia_avatar.py 复用 avatar.py 灵魂+工具，零成本
tags: [开口, 大脑, NVIDIA, llama, 分身启动]
version: v1.0
distilled_at: 2026-08-27
home: 技能库\lobster_task_standard_workflow_v3.0\我的AI分身\开口
---

# 开口（大脑）v1.0

## 用法
```bash
# 单轮
python "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体\nvidia_avatar.py" "一句话指令"
# 交互对话（输入 !工具名 调工具，/quit 退出）
python "...\AI分身实体\nvidia_avatar.py"
# 一键启动
双击 "...\AI分身实体\启动AI分身_NVIDIA.bat"
```

## 大脑路由
- 默认：NVIDIA 免费（`meta/llama-3.2-11b-vision-instruct`，已验证能开口）
- 现有默认 avatar.py 按 MiMo→DeepSeek→Ollama 探测；MiMo key 已失效、DeepSeek 占位、Ollama 未装，故新增 NVIDIA 大脑。

## 安全
- NVIDIA key 优先读环境变量 `NVIDIA_API_KEY`；未设置时从 atomcode_proxy.py 运行时读取，不在本文件硬编码。