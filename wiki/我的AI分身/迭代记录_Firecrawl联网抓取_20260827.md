---
title: 迭代记录·Firecrawl/联网抓取接入（四化）
tags: [四化迭代, Firecrawl, 联网抓取, MCP, web, 汤小龙]
source: 汤哥指令「把Firecrawl配置到我的AI分身 / 放E盘避免C盘爆满」
distilled_at: 2026-08-27
protocol: 全域模板#321 + 1234「4」四化迭代
---

# 迭代记录 · Firecrawl / 联网抓取接入（2026-08-27）

## 智能化
- 分析 Firecrawl 能力（清洗网页→Markdown、MCP 原生、反爬、自托管/云双模式）。
- 结合本机实情决策：E 盘仅剩 2.5GB、无 Firecrawl key → 先走云端配置 + 内置抓取兜底，不自托管占盘。

## 定制化
- 给汤小龙分身新增 `!web` 工具：有 `FIRECRAWL_API_KEY` 走 Firecrawl 云端（清洗 Markdown），无 key 走内置 urllib 抓取（零成本立即可用）。
- 实测：`!web https://example.com` 成功抓取正文，工具集现为 render_video/note/search_kb/web。

## 全自动化
- Firecrawl MCP 配置片段已写好：`MCP_插件\firecrawl_mcp.yaml`（可粘贴豆包/Claude/Codex）。
- `connectors.json` 已登记 Firecrawl 连接器。
- 未改动 `.codex/config.toml` 的 provider 字段（守 AGENTS 红线）。

## 自我净化
- 修正「放E盘避免C盘爆满」误区：实测 E 盘只剩 2.5GB，比 C 盘(28GB)更紧，故不建议本地自托管，改用云端+内置抓取零占盘。

## 结果路径
- 工具：`AI分身实体\avatar_tools_web.py`
- 配置：`MCP_插件\firecrawl_mcp.yaml` + `connectors.json`
- Obsidian：`Obsidian\wiki\我的AI分身\`