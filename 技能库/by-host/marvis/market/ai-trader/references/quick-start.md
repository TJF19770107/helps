# AI-Trader Quick Start

Get AI-Trader running in 5 minutes.

## 1. Clone and Install

```bash
# Clone the project
git clone https://github.com/HKUDS/AI-Trader.git
cd AI-Trader

# Install dependencies
pip install -r requirements.txt

# For A-share support (optional)
pip install tushare efinance
```

## 2. Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Required
OPENAI_API_KEY=sk-...           # OpenAI API key
ALPHAADVANTAGE_API_KEY=...      # Alpha Vantage (free tier)
JINA_API_KEY=...                # Jina AI (free tier)

# Optional for A-shares
TUSHARE_TOKEN=...               # Tushare token
```

## 3. Prepare Data

### US Stocks (NASDAQ 100)

```bash
cd data
python get_daily_price.py       # Download price data
python merge_jsonl.py           # Convert to unified format
cd ..
```

### A-Shares (SSE 50)

```bash
cd data/A_stock
python get_daily_price_tushare.py
python merge_jsonl_tushare.py
cd ../..
```

### Cryptocurrency

```bash
cd data/crypto
python get_daily_price_crypto.py
python merge_crypto_jsonl.py
cd ../..
```

## 4. Start MCP Services

```bash
cd agent_tools
python start_mcp_services.py
```

Keep this terminal running. Open a new terminal for next step.

## 5. Run Trading

### Option A: Use Default Config

```bash
# US stocks
python main.py

# A-shares
python main.py configs/default_astock_config.json

# Cryptocurrency
python main.py configs/default_crypto_config.json
```

### Option B: Use Custom Config

```bash
# Edit configs/my_config.json, then:
python main.py configs/my_config.json
```

## 6. View Results

Results are stored in:

- **US stocks**: `data/agent_data/{model-name}/position/position.jsonl`
- **A-shares**: `data/agent_data_astock/{model-name}/position/position.jsonl`
- **Cryptocurrency**: `data/agent_data_crypto/{model-name}/position/position.jsonl`

Each line in `position.jsonl` contains:
- `date`: Trading date
- `this_action`: Buy/sell action
- `positions`: Current holdings and cash

## One-Line Commands

### Full US Stock Experiment

```bash
cd AI-Trader && pip install -r requirements.txt && cd data && python get_daily_price.py && python merge_jsonl.py && cd ../agent_tools && python start_mcp_services.py &
cd AI-Trader && python main.py
```

### Full A-Share Experiment

```bash
cd AI-Trader && pip install -r requirements.txt tushare efinance && cd data/A_stock && python get_daily_price_tushare.py && python merge_jsonl_tushare.py && cd ../../agent_tools && python start_mcp_services.py &
cd AI-Trader && python main.py configs/default_astock_config.json
```

## Using the Skill

When the `ai-trader` skill is loaded, you can ask:

- "Run AI trading experiment with GPT-4 and Claude"
- "Backtest A-shares trading from Jan 1 to Jan 31"
- "Compare LLM performance on cryptocurrency trading"
- "Show me the trading results from yesterday"

The skill will:
1. Check environment and dependencies
2. Prepare data if needed
3. Start MCP services
4. Run trading with specified configuration
5. Present results

## Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install langchain langchain-openai langchain-mcp-adapters fastmcp
```

**"API key missing"**
Check `.env` file exists and has valid keys.

**"MCP connection refused"**
Ensure `python start_mcp_services.py` is running in another terminal.

**"No price data"**
Run data preparation scripts first.

**Port conflicts**
Change `*_HTTP_PORT` values in `.env`.