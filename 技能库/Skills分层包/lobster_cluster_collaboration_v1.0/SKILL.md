---
name: "lobster_cluster_collaboration_v1.0"
description: "龙虾群体协作核心技能：7种标准协作模式统一调度，多Agent协同编排，支持MCP+Agent插件+API脚本三通道。"
version: "1.0.0"
layer2: true
layer1_trigger: "群体协作/多Agent调度"
layer1_cost: "low"
layer1_category: "协作框架"
---

# 龙虾群体协作核心技能 v1.0

## 技能概述

本技能定义龙虾AI分身集群中**7种标准协作模式**的全套执行规范，覆盖从轻量信息传递到深度联合推理的完整协作谱系。每个Agent（Hermes/Codex/豆包/OpenClaw/Trae）均可按需加载本技能进入协作模式。

### 7种标准协作模式

| 编号 | 模式名称 | 英文标识 | 通信带宽 | 典型Token消耗 | 适用场景 |
|:----:|---------|---------|:--------:|:------------:|---------|
| 1 | 信息传递 | INFO_PASS | 低 | ~200 | 共享上下文摘要、任务状态广播 |
| 2 | 任务委派 | TASK_DELEGATE | 中 | ~800 | 主Agent拆分任务、指派子Agent执行 |
| 3 | 并行分治 | PARALLEL_DIVIDE | 中 | ~600 | 多个Agent同时处理不同子任务 |
| 4 | 流水线接力 | PIPELINE_HANDOFF | 中 | ~1000 | Agent A产出物作为Agent B输入 |
| 5 | 共识校验 | CONSENSUS_CHECK | 中 | ~1200 | 多Agent独立推理后交叉验证 |
| 6 | 互为MCP | MUTUAL_MCP | 高 | ~2000 | Agent互相暴露工具能力、深度互调 |
| 7 | 集群辩论 | CLUSTER_DEBATE | 高 | ~3000 | 多方观点碰撞、综合决策 |

## 触发条件

- 用户指令中包含「协作」「集群」「多Agent」「并行」「委派」「分工」等关键词
- 当前任务超出单个Agent能力边界，需要拆解分派
- 任务需要多视角交叉验证（金融决策/安全审计/代码审查）
- 上游Agent产出的中间结果需要下游Agent继续处理

## 执行流程

### 阶段一：协作模式判定

```
┌──────────────────────────────────┐
│ 输入任务描述 → 分析复杂度/并行度/依赖关系 │
│      ↓                               │
│ 对照7种模式匹配 → 输出推荐模式+备选    │
│      ↓                               │
│ 确认参与Agent清单 + 通信通道分配      │
└──────────────────────────────────┘
```

判定矩阵：

| 条件 | 推荐模式 |
|------|---------|
| 单一信息广播、状态同步 | INFO_PASS |
| 主Agent明确知道子任务归属 | TASK_DELEGATE |
| 子任务完全独立、无数据依赖 | PARALLEL_DIVIDE |
| 产出物需串行传递加工 | PIPELINE_HANDOFF |
| 需要一致性/安全性双重验证 | CONSENSUS_CHECK |
| 需要深度工具互调和能力互补 | MUTUAL_MCP |
| 需要多视角决策权衡 | CLUSTER_DEBATE |

### 阶段二：通信通道建立

根据协作模式选择通信通道：

```
INFO_PASS       → 共享内存文件 / GStack 消息总线
TASK_DELEGATE   → .cc-switch 任务队列 + task_id 追踪
PARALLEL_DIVIDE → GStack 并行管道 + 结果聚合器
PIPELINE_HANDOFF→ 中间产物目录接力 + 标准化输入输出契约
CONSENSUS_CHECK → 独立推理 → 共享结果 → 差异对比
MUTUAL_MCP      → MCP Server/Client 双向暴露
CLUSTER_DEBATE  → 辩论记录文件 + 投票/加权综合机制
```

### 阶段三：执行与监控

1. 广播 `CLUSTER_TASK_START` 事件 → 携带 task_id、mode、deadline
2. 各Agent按模式执行 → 周期性心跳 `HEARTBEAT {agent_id} {status} {progress%}`
3. 异常处理：
   - 任一Agent超时无心跳 → 触发 `FALLBACK` 降级（切换本地执行）
   - 任一Agent返回错误 → 根据模式决定重试/跳过/切换模式
   - 连续3次失败 → 触发 `ESCALATE` 升级到更高协作模式

### 阶段四：结果聚合与归档

1. 主Agent收集所有子Agent输出
2. 按模式生成聚合报告
3. 写入协作档案：`E:\龙虾AI主控中心\我的AI分身\技能库\协作档案\{task_id}\`
4. 更新 `CLUSTER_TASK_LOG.jsonl` 任务日志

## 输出规范

### 标准输出格式

```json
{
  "task_id": "CLUSTER-20260621-001",
  "mode": "CONSENSUS_CHECK",
  "participants": ["hermes", "codex", "doubao"],
  "result": {
    "consensus": true,
    "confidence": 0.94,
    "summary": "三方一致认为...",
    "details": { "...": "..." }
  },
  "artifacts": ["E:\\...\\report.md"],
  "duration_ms": 4200,
  "token_cost": {"hermes": 340, "codex": 520, "doubao": 410}
}
```

### 协作档案目录结构

```
E:\龙虾AI主控中心\我的AI分身\技能库\协作档案\
└── {task_id}/
    ├── task_manifest.json      # 任务清单
    ├── mode_decision.md        # 模式判定理由
    ├── agent_outputs/          # 各Agent原始输出
    ├── aggregated_result.md    # 聚合结果
    └── cluster_task_log.jsonl  # 追加到全局日志
```

## Token消耗对比：Skills vs MCP

| 维度 | MCP版本 | Skills版本 | 节省 |
|------|:------:|:--------:|:---:|
| 协作模式定义加载 | ~3500 tokens | ~1200 tokens | -65% |
| 通信协议声明 | ~2500 tokens | ~600 tokens | -76% |
| 输出格式规范 | ~1800 tokens | ~400 tokens | -78% |
| 错误处理流程 | ~2000 tokens | ~500 tokens | -75% |
| YAML frontmatter | ~400 tokens | ~300 tokens | -25% |
| **首次加载合计** | **~10200 tokens** | **~3000 tokens** | **-71%** |
| 后续调用（缓存命中） | ~6000 tokens | ~1500 tokens | -75% |

Skills版本通过Layer1 metadata预筛选 + Layer2按需加载 + Layer3引用外置，相比MCP全量加载降低71%首次Token消耗。

## 版本兼容

- 兼容 `lobster_task_standard_workflow_full_v2.1` 五步法
- 兼容 `lobster_tripartite_handshake_v1.0` 三方握手
- 兼容 GStack 标准工作流模板
