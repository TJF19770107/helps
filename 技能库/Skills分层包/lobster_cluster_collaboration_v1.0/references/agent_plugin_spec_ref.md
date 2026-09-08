# Agent Plugin Spec Reference

> Layer3 引用文档 — 龙虾Agent插件规范

## 插件清单结构 (plugin_manifest.json)

```json
{
  "plugin_id": "lobster-{category}-v{major}.{minor}",
  "plugin_name": "人类可读名称",
  "version": "1.0.0",
  "agent_target": ["hermes", "codex", "doubao", "openclaw", "trae"],
  "capability_add": ["新增能力"],
  "entry_point": "plugin_main.py|plugin_main.ps1",
  "dependencies": {
    "python": [">=3.10"],
    "pip": ["requests>=2.28"],
    "mcp": false
  },
  "config_schema": {
    "required": ["param1"],
    "optional": {"param2": "default_value"}
  },
  "permissions": ["file_read", "file_write", "shell_exec"],
  "risk_level": "low|medium|high",
  "fallback": "本地等效方案描述"
}
```

## 插件生命周期

```
REGISTER → VALIDATE → ACTIVATE → EXECUTE → DEACTIVATE → UNREGISTER
```

### 各阶段钩子

| 阶段 | 钩子函数 | 说明 |
|------|---------|------|
| REGISTER | `on_register()` | 向集群注册插件 |
| VALIDATE | `validate_config()` | 校验配置参数 |
| ACTIVATE | `on_activate()` | 激活插件，建立连接 |
| EXECUTE | `execute(task)` | 执行任务 |
| DEACTIVATE | `on_deactivate()` | 安全关闭 |
| UNREGISTER | `on_unregister()` | 清理注册信息 |

## 插件安装命令示例

```powershell
# 安装插件到指定Agent
Install-LobsterPlugin -PluginPath "E:\...\plugins\lobster-code-review-v1.0" -TargetAgent "codex"

# 激活插件
Enable-LobsterPlugin -PluginId "lobster-code-review-v1.0" -AgentId "codex-01"

# 查询已安装插件
Get-LobsterPlugin -AgentId "codex-01" -Status "active"
```
