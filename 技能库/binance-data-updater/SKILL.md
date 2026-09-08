---
name: binance-data-updater
description: 币安 K 线数据全量下载与增量更新技能，支持现货和 U 本位永续合约，落盘到指定 CSV 目录。
version: v1.0
distilled_at: 2026-09-04
distilled_by: 汤小龙 · 四化迭代知识库
---

# 币安数据下载更新技能

## 用途

一句话触发「更新币安数据」时，按本技能执行：

1. 读取数据目录里现有 CSV 的表尾时间。
2. 从表尾之后开始增量拉取币安公开 K 线。
3. 去重合并回原表，保持原有 12 列结构不变。
4. 目录里没有历史文件的币种，自动从币安可查的最早数据开始拉全量。

## 关键事实（已验证）

- 数据目录：`E:\龙虾AI主控中心\我的AI分身\CODEX量化策略20260615\币安\我的黑马策略\币安15m_K线数据`
- 现有文件是 CSV，不是 XLS。
- 表头 12 列：`timestamp,open,high,low,close,volume,close_time,quote_volume,trades,taker_buy_volume,taker_buy_quote_volume`
- `timestamp` / `close_time` 已转为北京时间（UTC+8）字符串，例如 `2026-06-16 06:15:00`，新增数据必须保持同一时区。
- 命名规范：
  - 主命名：`{SYMBOL}_永续_{interval}_全历史.csv`，如 `BTCUSDT_永续_15min_全历史.csv`
  - 旧别名：`{BASE}-USDT永续_{interval}_全历史.csv`，内容同源，只做备份不合并，防止误删。
  - 现货命名建议：`{SYMBOL}_现货_{interval}_全历史.csv`
- 币安 K 线接口是公开接口，行情下载不需要 API Key。账户/交易接口才需要 Key，且密钥只从环境变量读取，禁止写入本技能目录和知识库。

## 接口

- 现货：`https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=1000`
- U 本位永续：`https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=15m&limit=1000`
- 币安返回毫秒时间戳；本技能统一转成 UTC+8 再落盘。

## 执行方式

```powershell
# 增量更新目录下所有已有永续文件
python "E:\龙虾AI主控中心\我的AI分身\技能库\binance-data-updater\scripts\binance_update.py" --dir "E:\龙虾AI主控中心\我的AI分身\CODEX量化策略20260615\币安\我的黑马策略\币安15m_K线数据"

# 新增/补齐指定币种
python binance_update.py --dir <数据目录> --symbols BTCUSDT,ETHUSDT --market futures --interval 15m

# 现货
python binance_update.py --dir <数据目录> --symbols BTCUSDT --market spot --interval 15m
```

## 网络要点（2026-09-04 实测）

- 本机直连 `api.binance.com` / `fapi.binance.com` 会被重置（WinError 10054/10060）。
- 可用通道：本机代理 `socks5h://127.0.0.1:1081`（脚本默认走它）；`--proxy none` 切回直连。
- 直连备用镜像：`data-api.binance.vision`（现货数据）实测可通，但脚本主通道是代理。

## 增量规则

1. 找主命名文件，读 `timestamp` 最大值作为起点。
2. 拉取起点之后的数据，直到当前时间。
3. 按 `timestamp` 去重后追加，保持时间升序。
4. 现有 12 列不增不删不改名。
5. 单次请求 `limit=1000`，分页拉完。

## 安全与边界

- 只写数据目录里的 CSV，不碰别的目录。
- 不删除旧别名文件；确认主命名文件完整后，旧文件才可人工归档。
- 密钥零落盘：`BINANCE_API_KEY` 等只允许环境变量。
- 下载失败重试 3 次，仍失败则停在该币种并报错，不写入半截数据。
