---
name: "lobster_mutual_mcp_v1.0"
description: "互为MCP深度协作技能：Agent互相暴露MCP工具能力，实现跨Agent透明工具调用、能力互补和联合推理。"
version: "1.0.0"
layer2: true
layer1_trigger: "互为MCP/深度协作"
layer1_cost: "medium"
layer1_category: "深度协作"
---

# 龙虾互为MCP深度协作技能 v1.0

## 技能概述

互为MCP（Mutual MCP）是龙虾群体协作中的**最高带宽协作模式**。在此模式下，每个Agent同时扮演MCP Server和MCP Client双重角色，将自己的工具能力暴露给集群中其他Agent，实现跨Agent透明工具调用和能力互补。

### 架构示意

```
   Hermes                           Codex
┌──────────┐                    ┌──────────┐
│ MCP Server├─── tool_expose ──→│ MCP Client│
│           │                    │           │
│ MCP Client│←── tool_expose ───│ MCP Server│
└──────────┘                    └──────────┘
       │                              │
       └──────────┬───────────────────┘
                  │
        ┌─────────▼─────────┐
        │  Mutual MCP Hub   │
        │  (工具注册+路由)   │
        └───────────────────┘
```

## 触发条件

- 用户指令含「互为MCP」「深度协作」「联合推理」「能力互补」
- 单个Agent缺少某工具能力，另一Agent已暴露该工具
- 需要多Agent工具链组合完成复杂操作
- 协作模式自动升级：CONSENSUS_CHECK 连续失败 → 升级为 MUTUAL_MCP

## 执行流程

### 阶段一：能力发现与匹配

```
1. Agent A 扫描自身缺失能力 → 生成 capability_gap 清单
2. 查询 Mutual MCP Hub → 获取具备该能力的 Agent 列表
3. 按延迟/负载/可用性排序 → 选择最优目标 Agent
4. 建立 MCP 双向隧道
```

### 阶段二：工具暴露注册

```json
{
  "agent_id": "hermes-01",
  "exposed_tools": [
    {
      "tool_name": "read_file",
      "description": "读取复杂文件为Markdown",
      "input_schema": { "...": "..." },
      "rate_limit": {"max_per_minute": 20},
      "cost_estimate": "low"
    }
  ],
  "capability_tags": ["file_ops", "document_parsing"],
  "health_check_endpoint": "http://localhost:9101/health"
}
```

### 阶段三：透明工具调用

```
Agent A 需要 tool_X → 
  local_check(has_tool_X?) → 
    Yes → 本地执行
    No  → mutual_mcp_call(agent=Agent B, tool=tool_X, params={...}) →
            Agent B 执行 tool_X →
            结果序列化回传 Agent A
```

### 阶段四：联合推理编排

```
任务: 量化策略完整回测
  ├─ Hermes: read_file 读取历史数据文件
  ├─ Codex: python_executor 运行回测脚本
  ├─ 豆包: ai_search 搜索同类策略benchmark
  └─ Hermes(聚合): 对比回测结果 vs benchmark → 输出结论
```

## 输出规范

### 互调请求/响应格式

```json
// Request
{
  "call_id": "MUTUAL-{uuid}",
  "source_agent": "hermes-01",
  "target_agent": "codex-01",
  "tool_name": "python_executor",
  "params": {"code": "print('hello')"},
  "timeout_ms": 30000,
  "priority": "normal"
}

// Response
{
  "call_id": "MUTUAL-{uuid}",
  "status": "success",
  "result": {"stdout": "hello\n", "stderr": "", "exit_code": 0},
  "duration_ms": 340,
  "agent_load": 0.23
}
```

## 安全约束

- 工具暴露采用白名单机制，Agent必须显式声明 `exposed_tools` 清单
- 敏感工具（delete/shell_executor/write_file）默认不暴露，需额外授权
- 跨Agent调用日志全量记录到 `mutual_mcp_audit.jsonl`
- 连续3次超时/错误自动熔断，冷却60秒

## Token消耗对比：Skills vs MCP

| 维度 | MCP版本 | Skills版本 | 节省 |
|------|:------:|:--------:|:---:|
| 互调协议定义 | ~3500 tokens | ~1000 tokens | -71% |
| 工具暴露规范 | ~2500 tokens | ~600 tokens | -76% |
| 安全白名单规则 | ~2000 tokens | ~500 tokens | -75% |
| 联合推理编排 | ~3000 tokens | ~700 tokens | -77% |
| **首次加载合计** | **~11000 tokens** | **~2800 tokens** | **-75%** |
