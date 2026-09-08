---
name: ai-trader
description: Multi-agent stock/crypto trading and backtesting system from HKU. Runs fully autonomous trading competitions across 5+ AI models (GPT, Claude, Qwen, Gemini, DeepSeek) in NASDAQ 100, SSE 50, and cryptocurrency markets with MCP toolchain. Use when user asks to run AI trading experiments, backtest trading strategies, compare LLM trading performance, analyze stock/crypto markets with AI agents, launch multi-model trading arenas, or work with AI-Trader project. Triggers on mentions of AI trading, AI-Trader, stock backtesting, multi-agent trading, LLM trading competition.
---

# AI-Trader

Multi-agent autonomous trading arena. Let 5+ AI models compete in realistic market environments across US stocks, A-shares, and cryptocurrencies.

## Project Location

AI-Trader source code is at: `{workspace}/AI-Trader/AI-Trader-main/`

All commands must be executed from this directory.

## Quick Start - Launch Trading Experiment

### 1. Environment Setup (one-time)

```bash
pip install langchain langchain-openai langchain-mcp-adapters fastmcp python-dotenv requests numpy pandas
```

For A-share support:
```bash
pip install tushare efinance
```

Configure `.env` file with API keys:
```env
OPENAI_API_BASE="https://api.openai.com/v1"
OPENAI_API_KEY="your-key"
ALPHAADVANTAGE_API_KEY="your-key"
JINA_API_KEY="your-key"
TUSHARE_TOKEN="your-token"
```

### 2. Data Preparation

**US stocks (NASDAQ 100):**
```bash
cd data
python get_daily_price.py
python merge_jsonl.py
```

**A-shares (SSE 50):**
```bash
cd data/A_stock
python get_daily_price_tushare.py
python merge_jsonl_tushare.py
```

**Cryptocurrency:**
```bash
cd data/crypto
python get_daily_price_crypto.py
python merge_crypto_jsonl.py
```

### 3. Start MCP Services

```bash
cd agent_tools
python start_mcp_services.py
```

### 4. Run Trading

```bash
# US stocks
python main.py configs/default_config.json

# A-shares
python main.py configs/default_astock_config.json

# Cryptocurrency
python main.py configs/default_crypto_config.json
```

## Architecture

### Agent Types (5 in total)

| Agent | File | Market | Frequency |
|-------|------|--------|-----------|
| BaseAgent | `agent/base_agent/base_agent.py` | US stocks | Daily |
| BaseAgent_Hour | `agent/base_agent/base_agent_hour.py` | US stocks | Hourly |
| BaseAgentAStock | `agent/base_agent_astock/base_agent_astock.py` | A-shares | Daily |
| BaseAgentAStock_Hour | `agent/base_agent_astock/base_agent_astock_hour.py` | A-shares | Hourly |
| BaseAgentCrypto | `agent/base_agent_crypto/base_agent_crypto.py` | Crypto | Daily |

### MCP Toolchain

- **Trade Tool** (`tool_trade.py`): buy/sell execution, position management
- **Price Tool** (`tool_get_price_local.py`): price queries from local data
- **Search Tool** (`tool_jina_search.py`): market news search
- **Math Tool** (`tool_math.py`): financial calculations

## Configuration

See [references/config-guide.md](references/config-guide.md) for complete configuration options.

Minimal config:
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
    }
  ],
  "agent_config": {
    "max_steps": 30,
    "initial_cash": 10000.0
  }
}
```

## Results

After each run, results are stored in:
- US: `data/agent_data/{signature}/position/position.jsonl`
- A-shares: `data/agent_data_astock/{signature}/position/position.jsonl`
- Crypto: `data/agent_data_crypto/{signature}/position/position.jsonl`

Performance metrics: Sharpe ratio, max drawdown, annualized returns.

## Adding Custom Strategies

Create a new agent inheriting from BaseAgent:
```python
from agent.base_agent.base_agent import BaseAgent

class MyStrategy(BaseAgent):
    pass
```

Register in `AGENT_REGISTRY` in `main.py`, then reference in config JSON.

## Adding New LLM Models

Add to config's `models` array:
```json
{
  "name": "your-model",
  "basemodel": "provider/model-id",
  "signature": "your-model-signature",
  "enabled": true
}
```

Supports any OpenAI-compatible API via `openai_base_url` and `openai_api_key` fields.

## Troubleshooting

- **Port conflicts**: Change `*_HTTP_PORT` values in `.env`
- **Missing data**: Run data preparation scripts first
- **API errors**: Verify API keys in `.env`
- **MCP connection failures**: Ensure services are running before `main.py`