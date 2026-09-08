---
name: "lobster_api_script_engine_v1.0"
description: "API脚本调用引擎：标准化脚本模板、流水线编排、参数传递、结果校验。支持Python+PowerShell双语言。"
version: "1.0.0"
layer2: true
layer1_trigger: "API脚本/流水线"
layer1_cost: "low"
layer1_category: "脚本引擎"
---

# 龙虾API脚本调用引擎 v1.0

## 技能概述

API脚本调用引擎是龙虾群体协作的**自动化执行层**。本技能提供标准化的脚本模板、流水线编排规范和参数传递协议，使协作模式中的可编程操作（信息广播、共识校验、产物传递等）均可通过统一脚本接口执行。

### 核心能力

- **双语言模板**：Python（跨平台首选） + PowerShell（Windows原生）
- **流水线编排**：支持顺序/并行/条件分支三种编排模式
- **参数标准化**：JSON Schema 校验入参/出参
- **结果校验**：内置断言和输出格式验证
- **错误降级**：3次失败自动切换本地 fallback

## 触发条件

- 用户指令含「运行脚本」「执行流水线」「API调用」「自动化」
- 协作模式需要代码化执行（INFO_PASS广播/PIPELINE_HANDOFF传递等）
- 需要编排多个脚本按序执行

## 执行流程

### 阶段一：脚本模板匹配

```
输入: 协作模式 + 任务参数
  ↓
匹配模板:
  INFO_PASS       → lobster_info_broadcast_v1.0.py
  TASK_DELEGATE   → lobster_task_delegate_v1.0.py
  PARALLEL_DIVIDE → lobster_parallel_divide_v1.0.py
  PIPELINE_HANDOFF→ lobster_pipeline_handoff_v1.0.py
  CONSENSUS_CHECK → lobster_consensus_check_v1.0.py
  MUTUAL_MCP      → lobster_mutual_mcp_bridge_v1.0.py
  CLUSTER_DEBATE  → lobster_cluster_debate_v1.0.py
```

### 阶段二：参数注入与校验

```json
{
  "script_name": "lobster_consensus_check_v1.0.py",
  "params": {
    "task_id": "CLUSTER-20260621-001",
    "participants": ["hermes-01", "codex-01", "doubao-01"],
    "question": "某量化策略在2025年收益预测是否合理?",
    "threshold": 0.67
  },
  "validation": {
    "schema": "consensus_check_params_schema.json",
    "passed": true
  }
}
```

### 阶段三：执行与监控

```
EXECUTE → 实时stdout/stderr流式输出 → 周期性心跳
   ↓
ON_ERROR → 记录错误栈 → 重试(max 3次) → FALLBACK
   ↓
ON_SUCCESS → 解析stdout JSON → 写入结果文件
```

### 阶段四：产出物回传

脚本执行结果写入指定产物目录，由协作框架的 PIPELINE_HANDOFF 或主Agent读取。

## 输出规范

### 脚本标准输出格式

```json
{
  "script": "lobster_consensus_check_v1.0.py",
  "version": "1.0.0",
  "task_id": "CLUSTER-20260621-001",
  "status": "success|failure|timeout",
  "exit_code": 0,
  "stdout_summary": "3/3 agents consensus reached",
  "result": {},
  "duration_ms": 2340,
  "logs_path": "E:\\...\\logs\\script_20260621.log"
}
```

## Token消耗对比：Skills vs MCP

| 维度 | MCP版本 | Skills版本 | 节省 |
|------|:------:|:--------:|:---:|
| 脚本模板定义 | ~3000 tokens | ~800 tokens | -73% |
| 流水线编排 | ~2200 tokens | ~500 tokens | -77% |
| 参数校验规则 | ~1600 tokens | ~300 tokens | -81% |
| 错误降级流程 | ~1400 tokens | ~400 tokens | -71% |
| **首次加载合计** | **~8200 tokens** | **~2000 tokens** | **-76%** |
