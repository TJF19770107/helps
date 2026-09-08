# Plugin Manifest Reference

> Layer3 引用文档 — 插件清单模板与注册表结构

## 插件清单模板 (单个插件)

```json
{
  "plugin_id": "lobster-{category}-v{major}.{minor}",
  "plugin_name": "人类可读名称",
  "author": "lobster-ai-cluster",
  "version": "1.0.0",
  "schema_version": "1.0",
  "description": "插件功能简述",
  "agent_compatibility": {
    "hermes": {"min_version": "2.0", "tested": true},
    "codex": {"min_version": "1.5", "tested": true},
    "doubao": {"min_version": "1.0", "tested": false},
    "openclaw": {"min_version": "1.0", "tested": false},
    "trae": {"min_version": "1.0", "tested": false}
  },
  "capabilities": ["code_review", "security_scan"],
  "entry_point": "plugin_main.py",
  "dependencies": {
    "python": ">=3.10",
    "pip": ["ast-grep>=0.20", "bandit>=1.7"]
  },
  "permissions": ["file_read", "shell_exec"],
  "risk_level": "low",
  "rate_limit": {"max_calls_per_minute": 10},
  "timeout_ms": 30000,
  "fallback": "手动运行 pylint + bandit"
}
```

## 全局注册表结构 (plugin_registry.json)

```json
{
  "registry_version": "1.0",
  "last_updated": "2026-06-21T00:00:00Z",
  "agents": {
    "hermes-01": {
      "agent_type": "hermes",
      "plugins": ["lobster-code-review-v1.0", "lobster-file-organizer-v1.0"]
    },
    "codex-01": {
      "agent_type": "codex",
      "plugins": ["lobster-quant-backtest-v1.0", "lobster-data-fetch-v1.0"]
    },
    "doubao-01": {
      "agent_type": "doubao",
      "plugins": ["lobster-content-writer-v1.0", "lobster-translator-v1.0"]
    }
  },
  "capability_index": {
    "code_review": ["hermes-01:lobster-code-review-v1.0"],
    "backtest": ["codex-01:lobster-quant-backtest-v1.0"],
    "content_gen": ["doubao-01:lobster-content-writer-v1.0"]
  }
}
```

## 桥接路由规则

```yaml
bridge_routing:
  default_timeout_ms: 15000
  retry:
    max_attempts: 2
    backoff_ms: 1000
  circuit_breaker:
    failure_threshold: 5
    cooldown_seconds: 60
  capability_match:
    strategy: "exact_match"  # exact_match | fuzzy_match | fallback
  local_priority: true       # 优先使用本地插件
```
