# Mutual MCP Config Reference

> Layer3 引用文档 — 互为MCP配置模板与白名单规则

## 双向MCP Server配置

```json
{
  "mcpServers": {
    "lobster-mutual-mcp-hermes": {
      "command": "python",
      "args": ["-m", "lobster_mcp.mutual_server"],
      "env": {
        "AGENT_ID": "hermes-01",
        "MUTUAL_MCP_PORT": "9201",
        "PEER_AGENTS": "codex-01:9202,doubao-01:9203",
        "WHITELIST_PATH": "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\MCP\\mutual_whitelist.json",
        "AUDIT_LOG_PATH": "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\协作档案\\mutual_mcp_audit.jsonl",
        "MAX_CONCURRENT_CALLS": "5",
        "HEARTBEAT_INTERVAL": "3"
      }
    }
  }
}
```

## 工具白名单配置 (mutual_whitelist.json)

```json
{
  "whitelist_version": "1.0",
  "default_policy": "deny",
  "agents": {
    "hermes-01": {
      "exposed_tools": [
        {
          "tool_name": "read_file",
          "risk_level": "low",
          "rate_limit": {"max_per_minute": 30, "burst": 5},
          "allowed_callers": ["codex-01", "doubao-01", "openclaw-01", "trae-01"]
        },
        {
          "tool_name": "read_text",
          "risk_level": "low",
          "rate_limit": {"max_per_minute": 30, "burst": 5},
          "allowed_callers": ["codex-01", "doubao-01", "openclaw-01", "trae-01"]
        },
        {
          "tool_name": "search_file",
          "risk_level": "low",
          "rate_limit": {"max_per_minute": 20, "burst": 3},
          "allowed_callers": ["codex-01"]
        }
      ],
      "restricted_tools": [
        {
          "tool_name": "shell_executor",
          "risk_level": "high",
          "requires_explicit_auth": true,
          "allowed_callers": []
        },
        {
          "tool_name": "write_file",
          "risk_level": "medium",
          "requires_explicit_auth": true,
          "allowed_callers": ["codex-01"]
        }
      ]
    },
    "codex-01": {
      "exposed_tools": [
        {
          "tool_name": "python_executor",
          "risk_level": "medium",
          "rate_limit": {"max_per_minute": 15, "burst": 3},
          "allowed_callers": ["hermes-01", "doubao-01"]
        }
      ]
    }
  }
}
```

## 审计日志格式 (mutual_mcp_audit.jsonl)

```jsonl
{"timestamp":"2026-06-21T01:00:00Z","call_id":"MUTUAL-a1b2c3d4","source":"hermes-01","target":"codex-01","tool":"python_executor","status":"success","duration_ms":340}
{"timestamp":"2026-06-21T01:00:05Z","call_id":"MUTUAL-e5f6g7h8","source":"hermes-01","target":"codex-01","tool":"shell_executor","status":"denied","reason":"not_in_whitelist"}
```

## 熔断器配置

```yaml
circuit_breaker:
  per_agent:
    failure_threshold: 3          # 连续失败3次触发熔断
    timeout_threshold: 5          # 连续超时5次触发熔断
    cooldown_seconds: 60          # 熔断冷却时间
    half_open_max_calls: 2        # 半开状态最大试探调用
  global:
    max_concurrent_bridges: 10    # 全局最大并发桥接数
    max_pending_requests: 50      # 最大排队请求数
    default_timeout_ms: 30000     # 默认超时
```

## 能力发现API

```
GET /mutual-mcp/capabilities
Response:
{
  "agents": {
    "hermes-01": {"tools": ["read_file", "read_text", "search_file"], "load": 0.15},
    "codex-01": {"tools": ["python_executor", "ai_search"], "load": 0.42},
    "doubao-01": {"tools": ["write_file", "analyze_image"], "load": 0.08}
  },
  "capability_index": {
    "file_read": ["hermes-01:read_file", "hermes-01:read_text"],
    "code_exec": ["codex-01:python_executor"],
    "visual_analysis": ["doubao-01:analyze_image"]
  }
}
```
