---
title: 龙虾知识总导航（总MOC）
category: MOC
tags: [MOC, 导航, 总览, Karpathy架构]
created: 2026-07-31
---

# 龙虾知识总导航

> AI Agent舰队的第二大脑 · Karpathy LLM Wiki架构 · 三层分离

## 架构说明

| 层级 | 目录 | 用途 |
|------|------|------|
| **Raw层** | `raw/` | 原始资料（B站视频、公众号文章、自己的笔记） |
| **Wiki层** | `wiki/` | AI编译后的结构化知识 |
| **Schema层** | `wiki/*/` 内部模板 | 各领域的知识页模板规范 |
| **Daily** | `daily/` | 每日笔记、日志 |
| **Snapshots** | `snapshots/` | 轻量快照备份 |

---

## Raw层（原始资料）

- [[raw/B站视频/B站视频索引|B站视频索引]] — 视频课程笔记
- [[raw/公众号文章/公众号文章索引|公众号文章索引]] — 文章摘要与笔记
- `raw/自己的笔记/` — 自由笔记

## Wiki层（编译后的知识）

- [[wiki/index|Wiki全局MOC]] — Wiki层总索引
- [[wiki/AI工具/AI工具选型|AI工具选型]] — WorkBuddy/Codex/Claude对比
- [[wiki/量化交易/策略库总览|量化策略库]] — 量化策略知识
- [[wiki/副业变现/副业项目总览|副业项目总览]] — 副业变现知识
- [[wiki/项目交付/项目规范总览|项目规范总览]] — 接项目规范
- [[wiki/个人成长/用户画像|用户画像]] — 用户蒸馏画像

## Daily

- `daily/` — 每日笔记目录（YYYY-MM-DD.md 格式）

## 仪表盘（待创建）

- Dashboards/知识库总览
- Dashboards/学习进度看板

---

> **工作流**: Raw采集 → AI编译入Wiki → Daily记录 → 定期Snapshot
