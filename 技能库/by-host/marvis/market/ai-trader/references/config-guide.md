# AI-Trader Configuration Guide

## Configuration File Structure

All config files are in `configs/` directory. Main fields:

```json
{
  "agent_type": "BaseAgent",
  "market": "us",
  "date_range": {
    "init_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "models": [
    {
      "name": "gpt-4o",
      "basemodel": "openai/gpt-4o",
      "signature": "gpt-4o",
      "enabled": true,
      "openai_base_url": "https://api.openai.com/v1",
      "openai_api_key": "sk-..."
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "max_retries": 3,
    "base_delay": 1.0,
    "initial_cash": 10000.0,
    "verbose": false
  },
  "log_config": {
    "log_path": "./data/agent_data"
  }
}
```

## Agent Types and Market Mapping

| Agent Type | Market | Initial Cash | Data Path | Notes |
|------------|--------|--------------|-----------|-------|
| `BaseAgent` | `"us"` | $10,000 | `./data/agent_data` | NASDAQ 100 daily |
| `BaseAgent_Hour` | `"us"` | $10,000 | `./data/agent_data` | NASDAQ 100 hourly |
| `BaseAgentAStock` | `"cn"` | ¥100,000 | `./data/agent_data_astock` | SSE 50 daily |
| `BaseAgentAStock_Hour` | `"cn"` | ¥100,000 | `./data/agent_data_astock_hour` | SSE 50 hourly (10:30, 11:30, 14:00, 15:00) |
| `BaseAgentCrypto` | `"crypto"` | 50,000 USDT | `./data/agent_data_crypto` | BITWISE10 crypto daily |

**Note**: For A-share agents, `market` is automatically set to `"cn"` regardless of config value. For crypto, `market` is automatically `"crypto"`.

## Date Formats

- **Daily**: `"YYYY-MM-DD"` (e.g., `"2025-01-01"`)
- **Hourly**: `"YYYY-MM-DD HH:MM:SS"` (e.g., `"2025-01-01 10:30:00"`)

## Model Configuration

### Supported Model Providers

| Provider | `basemodel` Format | Example |
|----------|-------------------|---------|
| OpenAI | `"openai/model-id"` | `"openai/gpt-4o"` |
| Anthropic | `"anthropic/model-id"` | `"anthropic/claude-3-7-sonnet"` |
| Qwen | `"qwen/model-id"` | `"qwen/qwen3-max"` |
| DeepSeek | `"deepseek/model-id"` | `"deepseek/deepseek-chat-v3.1"` |
| Google | `"google/model-id"` | `"google/gemini-2.5-flash"` |
| MiniMax | `"MiniMax/model-id"` | `"MiniMax/MiniMax-M2"` |
| Zhipu | `"zhipu/model-id"` | `"zhipu/glm-4.6"` |

### Model Fields

- `name`: Human-readable name (e.g., `"gpt-4o"`)
- `basemodel`: Provider/model ID (e.g., `"openai/gpt-4o"`)
- `signature`: Unique identifier for logging (e.g., `"gpt-4o"`)
- `enabled`: `true`/`false` to include/exclude
- `openai_base_url`: Optional, for custom endpoints
- `openai_api_key`: Optional, overrides global `.env` key

## Predefined Config Files

| File | Purpose | Agent Type | Market |
|------|---------|------------|--------|
| `default_config.json` | US stocks daily | `BaseAgent` | `"us"` |
| `default_hour_config.json` | US stocks hourly | `BaseAgent_Hour` | `"us"` |
| `default_astock_config.json` | A-shares daily | `BaseAgentAStock` | `"cn"` |
| `astock_hour_config.json` | A-shares hourly | `BaseAgentAStock_Hour` | `"cn"` |
| `default_crypto_config.json` | Cryptocurrency | `BaseAgentCrypto` | `"crypto"` |
| `astock_config.json` | Example A-share config | `BaseAgentAStock` | `"cn"` |

## Environment Variables

`.env` file required:

```env
# AI Model API
OPENAI_API_BASE="https://api.openai.com/v1"
OPENAI_API_KEY="sk-..."

# Data Sources
ALPHAADVANTAGE_API_KEY="your-key"  # NASDAQ 100 + crypto
JINA_API_KEY="your-key"            # Market news
TUSHARE_TOKEN="your-token"         # A-share data (optional)

# MCP Service Ports
MATH_HTTP_PORT=8000
SEARCH_HTTP_PORT=8001
TRADE_HTTP_PORT=8002
GETPRICE_HTTP_PORT=8003
CRYPTO_HTTP_PORT=8005

# System
AGENT_MAX_STEP=30
RUNTIME_ENV_PATH="./runtime_env.json"
```

## Advanced Configuration

### Custom Stock Pools

For `BaseAgent` (US stocks), override `stock_symbols` in agent instantiation. Default is NASDAQ 100.

### Custom Crypto Pools

For `BaseAgentCrypto`, default is BITWISE10: `["BTC", "ETH", "XRP", "SOL", "ADA", "SUI", "LINK", "AVAX", "LTC", "DOT"]`.

### Logging Configuration

```json
"log_config": {
  "log_path": "./data/agent_data",
  "log_level": "INFO",
  "rotate_size_mb": 100
}
```

### Performance Tuning

```json
"agent_config": {
  "max_steps": 50,           # Max reasoning steps per decision
  "max_retries": 5,          # Retry on API failures
  "base_delay": 0.5,         # Delay between steps (seconds)
  "initial_cash": 10000.0,   # Starting capital
  "verbose": false,          # Debug output
  "enable_news": true,       # Use Jina search
  "enable_technical": false  # Technical indicators (future)
}
```

## Example Configurations

### Multi-Model Competition

```json
{
  "agent_type": "BaseAgent",
  "market": "us",
  "date_range": {
    "init_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "models": [
    {
      "name": "gpt-4o",
      "basemodel": "openai/gpt-4o",
      "signature": "gpt-4o",
      "enabled": true
    },
    {
      "name": "claude-3.7-sonnet",
      "basemodel": "anthropic/claude-3.7-sonnet",
      "signature": "claude-3.7-sonnet",
      "enabled": true
    },
    {
      "name": "qwen3-max",
      "basemodel": "qwen/qwen3-max",
      "signature": "qwen3-max",
      "enabled": true
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "initial_cash": 10000.0
  }
}
```

### A-Share Hourly Trading

```json
{
  "agent_type": "BaseAgentAStock_Hour",
  "date_range": {
    "init_date": "2025-10-09 10:30:00",
    "end_date": "2025-10-31 15:00:00"
  },
  "models": [
    {
      "name": "claude-3.7-sonnet",
      "basemodel": "anthropic/claude-3.7-sonnet",
      "signature": "claude-3.7-sonnet-astock-hour",
      "enabled": true
    }
  ],
  "agent_config": {
    "initial_cash": 100000.0
  },
  "log_config": {
    "log_path": "./data/agent_data_astock_hour"
  }
}
```

### Cryptocurrency Trading

```json
{
  "agent_type": "BaseAgentCrypto",
  "date_range": {
    "init_date": "2025-10-20",
    "end_date": "2025-10-31"
  },
  "models": [
    {
      "name": "gpt-4o",
      "basemodel": "openai/gpt-4o",
      "signature": "gpt-4o-crypto",
      "enabled": true
    }
  ],
  "agent_config": {
    "initial_cash": 50000.0
  },
  "log_config": {
    "log_path": "./data/agent_data_crypto"
  }
}
```

## Validation Rules

1. `init_date` ≤ `end_date`
2. Hourly configs must use `BaseAgent_Hour` or `BaseAgentAStock_Hour`
3. A-share configs must use `BaseAgentAStock` or `BaseAgentAStock_Hour`
4. Crypto configs must use `BaseAgentCrypto`
5. At least one model must be `"enabled": true`
6. `initial_cash` > 0
7. `max_steps` ≥ 1

## Common Errors

- **"Unsupported agent type"**: Check `agent_type` matches `AGENT_REGISTRY` in `main.py`
- **"Position file not found"**: Run data preparation scripts first
- **"MCP connection refused"**: Start MCP services with `python start_mcp_services.py`
- **"API key missing"**: Verify `.env` file exists and keys are set
- **"Date format invalid"**: Use `"YYYY-MM-DD"` or `"YYYY-MM-DD HH:MM:SS"`