---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_0f5078b2736911f1aabe5254007bceed
    ReservedCode1: 8wlJmnbiCPpLZl3/Ps6uYGY94wApPOTvLFqDrdT4qNPhMG+Pss5Ksd8HWEf56093DEpDFvBmvzPFrGPa/MjoOGxnR9eFu/ASBOy6M6XgC2p+6x4RrzhwCufOVADyfy2k2D6Kn05HRAWL0EPNCBzHQF15GYS61v3K00SegWeLZsKrMPRYCv0nMWe/rTM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_0f5078b2736911f1aabe5254007bceed
    ReservedCode2: 8wlJmnbiCPpLZl3/Ps6uYGY94wApPOTvLFqDrdT4qNPhMG+Pss5Ksd8HWEf56093DEpDFvBmvzPFrGPa/MjoOGxnR9eFu/ASBOy6M6XgC2p+6x4RrzhwCufOVADyfy2k2D6Kn05HRAWL0EPNCBzHQF15GYS61v3K00SegWeLZsKrMPRYCv0nMWe/rTM=
---

# MT5 交易指令模板 v1.0

技能名称：MT5双端交易指令模板
技能标识：MT5_Trade_Command_Templates_v1.0
适用范围：Claude Code + Codex 双端 MT5 交易指令标准化
版本号：v1.0
更新时间：2026-06-29
生效范围：全域 / 永久 / Claude Code + Codex + Marvis 统一

---

## 一、参考对标说明

参考截图显示：
- 参考使用 `ariadng/metatrader-mcp-server` v0.5.1（与现有环境一致）
- Claude Desktop 配置格式：`mcpServers.metatrader`，args 含 `--login` / `--password` / `--server` / `--terminal`
- Claude Code 设置界面确认 metatrader MCP Server 已配置，工具含 `get_candle` / `get_symbols` 等
- 视频确认 "MCP 服务器成功识别"，账户为 IC Markets / IC-MT5-2

---

## 二、双端指令模板

### 2.1 Claude Code 端（方案A STDIO模式 → sim模拟盘）

格式说明：Claude Code 通过 STDIO MCP 直接调用 metatrader-mcp-server 内置 32 个工具函数。

| 操作 | 自然语言指令 | 底层函数 |
|------|-------------|----------|
| 实时行情 | "查询 XAUUSD 实时报价" | `get_symbol_price` |
| K线数据 | "获取 EURUSD H1周期最近100根K线" | `get_candles` |
| 账户信息 | "显示当前账户余额和净值" | `get_account_info` |
| 模拟开仓 | "模拟买入0.01手EURUSD市价单" | `create_market_order` |
| 模拟平仓 | "模拟平仓EURUSD全部持仓" | `close_position` |
| 挂单 | "EURUSD挂限价买单0.01手，价格1.0500" | `create_limit_order` |
| 撤单 | "撤销所有EURUSD挂单" | `cancel_order` |
| 持仓查询 | "列出当前所有持仓" | `get_positions` |
| 修改止损 | "EURUSD持仓止损调整至1.0450" | `modify_position` |

---

### 2.2 Codex 端（方案B HTTP API模式 → real实盘只读）

格式说明：Codex 通过 HTTP API :8000 调用，实盘环境 `MT5_TRADE_MODE=readonly` 硬锁定。

| 操作 | 自然语言指令 | API端点 |
|------|-------------|---------|
| 实时行情 | "读取黄金实时行情" | `GET /api/v1/market/price?symbol=XAUUSD` |
| K线数据 | "读取EURUSD日线最近30天" | `GET /api/v1/market/candles?symbol=EURUSD&tf=D1` |
| 账户查询 | "显示账户余额净值保证金" | `GET /api/v1/account/info` |
| 持仓查询 | "列出当前所有持仓" | `GET /api/v1/trading/positions` |
| 历史订单 | "查询本周已平仓订单" | `GET /api/v1/trading/history` |
| 点差查询 | "查询EURUSD当前点差" | `GET /api/v1/market/spread?symbol=EURUSD` |
| 技术指标 | "计算XAUUSD的RSI(14)" | `GET /api/v1/analysis/rsi?symbol=XAUUSD&period=14` |

---

### 2.3 Marvis 中转调度模板

| 用户输入 | Marvis路由 | 风险拦截 |
|----------|-----------|----------|
| "查XAUUSD行情" | → Codex (HTTP/8000) | 无 |
| "模拟买入0.01手EURUSD" | → Claude Code (STDIO/sim) | 无 |
| "开仓做多黄金" (未标注模拟) | → 垂询确认 | 阻断 |
| "回测MA5策略" | → Codex (HTTP/8000) | 无 |

---

## 三、双链路安全约束

1. real实盘环境：永久锁定 `readonly`，仅查询/回测权限
2. sim模拟盘：完整交易测试权限
3. 所有交易指令日志脱敏，仅保留指令标识
4. 凭证（`LOGIN` / `PASSWORD` / `SERVER`）仅存于 `.env` 文件，禁止在日志/指令中明文传输

---

## 四、Claude Code 和 Codex 配置对照表

| 配置项 | Claude Code (方案A) | Codex (方案B) |
|--------|-------------------|---------------|
| MCP传输 | STDIO | HTTP API |
| 配置文件 | `.claude/mcp.json` | `.codex/mcp.json` |
| 服务启动 | `metatrader-mcp-server` (STDIO) | `metatrader-http-server :8000` |
| 端口 | 无固定端口 | 8000 |
| 环境 | sim/模拟盘 | real/实盘(只读) |
| 凭证方式 | CLI `--login` / `--password` / `--server` | `.env` 文件 |

---

## 五、版本历史

| 版本 | 日期 | 变更 |
|:---:|------|------|
| v1.0 | 2026-06-29 | 初始版本，固化双端指令模板 |
*（内容由AI生成，仅供参考）*
