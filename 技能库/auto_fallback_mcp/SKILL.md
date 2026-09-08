# 自动降级容错技能

> 版本：v1.0 | 创建时间：2026-08-03
> 用途：Ollama Cloud 429限流时自动切换到官方DeepSeek API

---

## 一、功能描述

当Ollama Cloud返回429限流报错时，自动切换到官方DeepSeek原生API重试任务，不中断量化与接单流水线。

### 1.1 降级规则

```
Ollama Cloud API调用
    ↓
┌─────────────────────────────────────┐
│  成功 → 返回结果                    │
│  429  → 自动切官方DS API重试        │
│  503  → 自动切官方DS API重试        │
│  其他  → 报错终止                   │
└─────────────────────────────────────┘
    ↓
重试成功 → 返回结果
重试失败 → 报错终止
```

### 1.2 触发条件

- 当前模型为Ollama Cloud DeepSeek
- API返回429（Too Many Requests）或503（Service Unavailable）
- 配置文件中FALLBACK_ENABLED=true

---

## 二、实现逻辑

### 2.1 伪代码

```python
def api_call_with_fallback(prompt, max_retries=3):
    """
    带降级容错的API调用
    """
    # 首先尝试Ollama Cloud
    try:
        response = call_ollama_cloud(prompt)
        return response
    except RateLimitError as e:
        # 429限流，自动降级
        print(f"[降级] Ollama Cloud限流，切换到官方API...")
        
        # 切换到官方DeepSeek API
        try:
            response = call_official_deepseek(prompt)
            return response
        except Exception as fallback_error:
            raise Exception(f"降级也失败: {fallback_error}")
    
    except ServiceUnavailableError as e:
        # 503服务不可用，自动降级
        print(f"[降级] Ollama Cloud服务不可用，切换到官方API...")
        
        try:
            response = call_official_deepseek(prompt)
            return response
        except Exception as fallback_error:
            raise Exception(f"降级也失败: {fallback_error}")
```

### 2.2 配置参数

```env
# 降级配置
FALLBACK_ENABLED=true
FALLBACK_TARGET=official_ds
FALLBACK_ERROR_CODES=429,503
FALLBACK_MAX_RETRIES=3
FALLBACK_DELAY_SECONDS=2
```

---

## 三、集成方式

### 3.1 代理层集成

在Anthropic代理和Codex代理中集成降级逻辑：

```python
# anthropic_proxy_15721.py 中添加
def handle_api_error(error_code):
    if error_code in [429, 503] and FALLBACK_ENABLED:
        # 切换到备用线路
        switch_to_fallback()
        # 重试请求
        return retry_request()
```

### 3.2 配置文件

```json
{
  "fallback": {
    "enabled": true,
    "target": "official_ds",
    "error_codes": [429, 503],
    "max_retries": 3,
    "delay_seconds": 2
  }
}
```

---

## 四、监控与日志

### 4.1 降级事件日志

```
[2026-08-03 19:37:15] [降级] Ollama Cloud返回429，切换到官方API
[2026-08-03 19:37:17] [降级] 官方API调用成功，耗时2.3秒
[2026-08-03 19:37:15] [降级] Ollama Cloud返回503，切换到官方API
[2026-08-03 19:37:18] [降级] 官方API调用成功，耗时3.1秒
```

### 4.2 统计指标

- 降级次数
- 降级成功率
- 平均降级延迟

---

## 五、配置位置

- 技能文件：E:\龙虾AI主控中心\我的AI分身\技能库\auto_fallback_mcp\SKILL.md
- 代理配置：E:\龙虾AI主控中心\MCP服务\anthropic_proxy_15721.py

---

**文档生成**：Hermes Agent | 自动降级容错技能
**版本控制**：v1.0 | 2026-08-03