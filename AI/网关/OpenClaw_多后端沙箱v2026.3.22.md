# OpenClaw 多后端沙箱 v2026.3.22

> **来源**: OpenClaw GitHub Release Notes, 2026-03-23
> **豆包关联**: R29深度迭代报告 · 协议#103
> **MOC**: [[_MOC_网关与协议]] · [[OpenClaw Gateway控制面]]

---

## Breaking Change概述

OpenClaw v2026.3.22是重大架构改版，引入8项Breaking Changes，其中最核心的是沙箱体系从单一路线走向**多后端可插拔架构**。

## 三后端沙箱架构

```
Sandbox Backend Layer
├── Docker Backend: 容器隔离，适合Linux/macOS
├── SSH Backend: 远程执行，secret-backed密钥，适合企业内网
└── OpenShell Backend: 轻量级，支持mirror/remote workspace，适合Windows
```

## 8大Breaking Changes

| # | 变更项 | 影响 |
|---|--------|------|
| 1 | 插件安装路径 ClawHub优先 | 插件发现/安装/更新统一入口 |
| 2 | 浏览器连接机制变化 | Chromium家族全支持（Brave/Edge等） |
| 3 | 图片生成输出路径统一 | 所有图片统一输出目录 |
| 4 | 插件SDK API变更 | 类型化/版本化插件槽位 |
| 5 | 沙箱多后端体系 | Docker→SSH/OpenShell/Docker三后端 |
| 6 | Per-agent模型默认值 | thinking/reasoning/fast独立配置 |
| 7 | 技能/插件市场正式化 | ClawHub 5,400+技能+VirusTotal扫描 |
| 8 | GPT-5.4默认模型 | 新一代默认模型 |

## 安全增强

- 可插拔后端：按场景选择隔离层级
- Per-agent执行环境注入限制
- Secret-backed密钥认证（SSH后端）
- 沙箱资源限额（CPU/内存/网络）

## 产品演进方向

主动清理旧设计、统一新入口、收紧安全边界、推动插件和技能体系走向下一阶段。

---

**标签**: #AI/网关 #OpenClaw #沙箱 #多后端 #BreakingChange #协议103
