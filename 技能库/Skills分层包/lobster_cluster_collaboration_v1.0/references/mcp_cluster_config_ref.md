# MCP Cluster Config Reference

> Layer3 引用文档 — 龙虾群体协作 MCP 配置模板

## MCP Server 配置模板

```json
{
  "mcpServers": {
    "lobster-cluster-coordinator": {
      "command": "python",
      "args": ["-m", "lobster_mcp.coordinator"],
      "env": {
        "CLUSTER_ID": "lobster-ai-cluster-01",
        "COORDINATOR_PORT": "9100",
        "HEARTBEAT_INTERVAL": "5",
        "MAX_AGENTS": "10",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Agent 注册数据结构

```json
{
  "agent_id": "hermes-01",
  "agent_type": "hermes",
  "capabilities": ["code_gen", "reasoning", "file_ops"],
  "exposed_tools": ["read_file", "write_file", "shell_executor"],
  "mcp_endpoint": "http://localhost:9101",
  "status": "online",
  "registered_at": "2026-06-21T00:00:00Z"
}
```

## 通信消息格式

```json
{
  "message_id": "MSG-{uuid}",
  "task_id": "CLUSTER-{date}-{seq}",
  "from_agent": "hermes-01",
  "to_agent": "codex-01",
  "mode": "INFO_PASS|TASK_DELEGATE|...",
  "payload": {},
  "timestamp": "ISO8601",
  "ttl_seconds": 300
}
```

## MCP 工具暴露清单（协作专用）

| tool_name | mode | 说明 |
|-----------|------|------|
| `cluster_status` | ALL | 查询集群Agent在线状态 |
| `task_delegate` | TASK_DELEGATE | 委派任务到指定Agent |
| `consensus_check` | CONSENSUS_CHECK | 发起共识校验 |
| `pipeline_handoff` | PIPELINE_HANDOFF | 流水线产物传递 |
| `mutual_tool_call` | MUTUAL_MCP | 跨Agent工具互调 |
| `cluster_debate_start` | CLUSTER_DEBATE | 发起集群辩论 |
