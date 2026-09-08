---
name: "lobster_plugin_bridge_v1.0"
description: "跨Agent插件桥接技能：统一插件注册/发现/激活/卸载流程，支持5种Agent类型的插件互操作。"
version: "1.0.0"
layer2: true
layer1_trigger: "跨Agent插件/桥接"
layer1_cost: "low"
layer1_category: "插件桥接"
---

# 龙虾插件桥接技能 v1.0

## 技能概述

跨Agent插件桥接是龙虾群体协作的**能力共享层**，使任一Agent安装的插件可被其他Agent发现并按需调用。本技能定义统一的插件注册、发现、激活和卸载流程，屏蔽Agent类型差异（Hermes/Codex/豆包/OpenClaw/Trae）。

### 插件桥接架构

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Hermes  │    │  Codex   │    │  豆包    │
│ Plugin A │    │ Plugin B │    │ Plugin C │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     └───────────────┼───────────────┘
                     │
          ┌──────────▼──────────┐
          │  Plugin Bridge Hub  │
          │  (注册表 + 路由)     │
          └─────────────────────┘
```

## 触发条件

- 用户指令含「插件桥接」「跨Agent插件」「共享插件」「调用XX的YY插件」
- 当前Agent缺少某能力，但集群中另一Agent已安装对应插件
- 需要统一管理多个Agent的插件清单

## 执行流程

### 阶段一：插件发现

```
1. 查询 Plugin Bridge Hub 注册表
2. 返回匹配能力的插件列表（含所属Agent、版本、状态）
3. 如无匹配，返回空并建议安装方案
```

### 阶段二：桥接路由

```
                  ┌─ 本地插件 → 直接调用
请求 → 路由判定 ──┤
                  └─ 远程插件 → MCP隧道 → 目标Agent → 返回结果
```

### 阶段三：调用与回传

1. 构造桥接请求：`{plugin_id, agent_id, method, params}`
2. 通过MCP隧道发送到目标Agent
3. 目标Agent执行插件并回传结果
4. 桥接层反序列化并返回给请求方

### 阶段四：生命周期管理

```
REGISTER  →  plugin_bridge register --agent-id xxx --plugin-manifest path
DISCOVER  →  plugin_bridge discover --capability "code_review"
ACTIVATE  →  plugin_bridge activate --plugin-id xxx
DEACTIVATE→  plugin_bridge deactivate --plugin-id xxx
UNREGISTER→  plugin_bridge unregister --plugin-id xxx
```

## 输出规范

### 桥接调用结果格式

```json
{
  "bridge_id": "BRIDGE-{uuid}",
  "source_agent": "hermes-01",
  "target_agent": "codex-01",
  "plugin_id": "lobster-code-review-v1.0",
  "method": "review_code",
  "result": { "...": "..." },
  "latency_ms": 320,
  "status": "success|timeout|error"
}
```

### 注册表存储位置

```
E:\龙虾AI主控中心\我的AI分身\技能库\Agent插件集\plugin_registry.json
```

## Token消耗对比：Skills vs MCP

| 维度 | MCP版本 | Skills版本 | 节省 |
|------|:------:|:--------:|:---:|
| 桥接协议定义 | ~2800 tokens | ~900 tokens | -68% |
| 路由规则 | ~1500 tokens | ~400 tokens | -73% |
| 生命周期管理 | ~2000 tokens | ~500 tokens | -75% |
| 错误处理 | ~1800 tokens | ~400 tokens | -78% |
| **首次加载合计** | **~8100 tokens** | **~2200 tokens** | **-73%** |
