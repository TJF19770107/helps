---
title: 迭代记录·FreeLLMAPI恢复+CNB DeepSeek方案（四化）
tags: [四化迭代, FreeLLMAPI, Docker, CNB, DeepSeek, 方案]
source: 汤哥指令「恢复FreeLLMAPI/配给Codex/分析CNB DeepSeek接入」
distilled_at: 2026-08-28
protocol: 全域模板#321 + 1234「4」四化迭代
---

# 迭代记录 · FreeLLMAPI 恢复 + CNB 方案（2026-08-28）

## 智能化
- 根因定位：FreeLLMAPI 连不上 = Docker Desktop 未运行（非端口错；端口是3001非53001）。
- 启动 Docker → freellmapi 容器 Up → 127.0.0.1:3001 /api/ping 200。

## 定制化
- Codex config 新增 freellmapi provider（base_url 3001/v1，env FREELLMAPI_API_KEY）；providers 现有 custom/nvidia_free/glm_free/freellmapi。
- /v1 返回 401：需在面板录入厂商Key并生成API key。

## 全自动化
- Docker 引擎就绪(35s)，compose up 恢复。

## 自我净化
- CNB DeepSeek 方案写入：A.FreeLLMAPI聚合 / B.AtomCode-CodingPlan登录 / C.CNB官方文档；需用户确认路径。

## 结果路径
- 方案：`AI分身实体\CNB_DeepSeek方案.md`
- provider：`~/.codex/config.toml`
- Obsidian：`Obsidian\wiki\我的AI分身\`