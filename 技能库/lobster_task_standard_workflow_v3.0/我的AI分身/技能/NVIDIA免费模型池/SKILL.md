---
title: NVIDIA免费模型池接入协议
summary: 说「启动我的AI分身」自动拉起 NVIDIA 免费池(127.0.0.1:13331)，自动切换7个免费模型，无Docker低内存
tags: [NVIDIA, 免费模型, 自动切换, 代理, 协议]
version: v1.0
distilled_at: 2026-08-29
protocol: 全域模板#321 + 龙虾五步法
---

# NVIDIA 免费模型池接入协议 v1.0

## 触发
「启动我的AI分身 / 启动汤小龙」→ 自动拉起 nvidia_free_proxy.py（无需双击）。

## 端点
- 代理：127.0.0.1:13331/v1（OpenAI 兼容）
- 自动切换链：deepseek-v4-pro → deepseek-v4-flash → llama-3.2-11b-vision → mistral-large → gemma-4-31b → mistral-nemo → llama-3.2-90b-vision
- Codex provider：nvidia_free_pool（model=auto）
- 任意 OpenAI 兼容 Agent 可指向该端点（Codex/Claude/OpenCode/WorkBuddy 等）。

## 沉淀
- 四化迭代归档 Obsidian；本协议入五步法/全域模板。