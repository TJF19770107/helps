# Script Template Reference

> Layer3 引用文档 — 7种协作模式脚本模板速查

## 1. INFO_PASS — 信息广播脚本

```python
# lobster_info_broadcast_v1.0.py
import json, sys, argparse
from datetime import datetime

def broadcast(title: str, content: str, recipients: list[str]) -> dict:
    """向指定Agent广播信息"""
    msg = {
        "type": "INFO_PASS",
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "content": content,
        "ttl_minutes": 30
    }
    # 写入共享消息总线
    return {"status": "broadcasted", "recipients": recipients, "message": msg}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--recipients", required=True)  # JSON array string
    args = parser.parse_args()
    result = broadcast(args.title, args.content, json.loads(args.recipients))
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 2. TASK_DELEGATE — 任务委派脚本

```python
# lobster_task_delegate_v1.0.py
# 关键结构：
delegate_payload = {
    "task_id": "CLUSTER-20260621-001",
    "parent_task_id": "PARENT-001",
    "assigned_agent": "codex-01",
    "sub_task": {"description": "...", "expected_output": "...", "deadline": "ISO8601"},
    "callback": {"on_success": "aggregate_results", "on_failure": "escalate"}
}
```

## 3. PARALLEL_DIVIDE — 并行分治脚本

```python
# lobster_parallel_divide_v1.0.py
# 关键结构：
parallel_config = {
    "task_id": "CLUSTER-20260621-001",
    "sub_tasks": [
        {"id": "sub-1", "agent": "hermes-01", "task": {...}},
        {"id": "sub-2", "agent": "codex-01", "task": {...}},
        {"id": "sub-3", "agent": "doubao-01", "task": {...}}
    ],
    "aggregation": "wait_all",  # wait_all | wait_any | wait_n(2)
    "timeout_seconds": 300
}
```

## 4. PIPELINE_HANDOFF — 流水线接力脚本

```python
# lobster_pipeline_handoff_v1.0.py
# 关键结构：
pipeline_stages = [
    {"stage": 1, "agent": "hermes-01", "action": "extract_data", "output_key": "raw_data"},
    {"stage": 2, "agent": "codex-01", "action": "analyze", "input_key": "raw_data", "output_key": "analysis"},
    {"stage": 3, "agent": "doubao-01", "action": "report", "input_key": "analysis", "output_key": "final_report"}
]
```

## 5. CONSENSUS_CHECK — 共识校验脚本

```python
# lobster_consensus_check_v1.0.py
def check_consensus(results: list[dict], threshold: float = 0.67) -> dict:
    """简单多数一致判定"""
    n = len(results)
    if n == 0:
        return {"consensus": False, "reason": "no_results"}
    agree_count = sum(1 for r in results if r.get("agreement", False))
    ratio = agree_count / n
    return {
        "consensus": ratio >= threshold,
        "agreement_ratio": ratio,
        "agree_count": agree_count,
        "total_participants": n,
        "threshold": threshold
    }
```

## 6. MUTUAL_MCP — 互为MCP桥接脚本

```python
# lobster_mutual_mcp_bridge_v1.0.py
def bridge_call(source_agent: str, target_agent: str, tool_name: str, params: dict) -> dict:
    """跨Agent MCP工具调用"""
    request = {
        "bridge_id": f"BRIDGE-{uuid4().hex[:8]}",
        "source": source_agent,
        "target": target_agent,
        "tool": tool_name,
        "params": params,
        "timeout_ms": 15000
    }
    # 通过MCP隧道发送
    return send_via_mcp_tunnel(request)
```

## 7. CLUSTER_DEBATE — 集群辩论脚本

```python
# lobster_cluster_debate_v1.0.py
debate_config = {
    "topic": "是否采用策略A替代策略B",
    "participants": ["hermes-01", "codex-01", "doubao-01"],
    "rounds": 3,
    "voting": {"method": "weighted_majority", "weights": {"hermes-01": 1.0, "codex-01": 1.2, "doubao-01": 0.8}},
    "output": "debate_summary.md"
}
```

## 流水线编排配置模板 (pipeline_config.json)

```json
{
  "pipeline_id": "PIPE-20260621-001",
  "mode": "sequential",
  "stages": [
    {"script": "lobster_info_broadcast_v1.0.py", "params": {...}, "depends_on": []},
    {"script": "lobster_parallel_divide_v1.0.py", "params": {...}, "depends_on": [0]},
    {"script": "lobster_consensus_check_v1.0.py", "params": {...}, "depends_on": [1]}
  ],
  "on_failure": "fallback_local",
  "artifacts_dir": "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\协作脚本\\output"
}
```
