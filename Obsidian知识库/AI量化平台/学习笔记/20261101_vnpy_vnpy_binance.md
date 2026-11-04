---
日期: 2026-11-01
仓库: vnpy/vnpy_binance
核心文件: vnpy_binance/linear_gateway.py（1770 行）
轮次: 第 21 轮（周日）
tags: [AI量化平台, 夜学, 代码拆解, 网关, 一致性, 联合挂单]
---

# 20261101 · vnpy/vnpy_binance · linear_gateway.py

## 0. 一句话结论

> **交易所网关的 bug 不长成「报错」，长成「两条通道各说各话」。**
> 1770 行里没有一处会抛异常的设计，但 **11 类缺陷、12 个站点** 全部是「同一个字段/同一个函数
> 在两个入口有两条定义」——`sign` 有/没有时钟校正、`frozen` 用 `available`/用 `crossWallet`、
> `datetime` 用事件时间/用订单时间、`keepAlive` 按秒/按计数。
> 单独看每一处都"能用"，合起来就是「一半通一半不通，且日志全绿」。
> ⇒ 我方的执行层验收标准必须从「跑通」升级为「**两条通道读数逐字段相等**」。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：执行层（交易所网关）。它是 vnpy 与币安 U 本位永续之间的**唯一翻译层**。
- **上下游**：
  - 上游依赖 → `vnpy.trader.gateway.BaseGateway` / `vnpy.trader.websocket.WebsocketClient` / `vnpy.trader.object.*`
  - 下游被谁调用 → `MainEngine.add_gateway()` → CTA/组合策略的 `send_order` / `cancel_order` / `subscribe`
- **四件套分层**（这是本文件真正的架构，值得抄）：

  | 组件 | 行号 | 连接对象 | 职责 |
  |---|---|---|---|
  | `BinanceLinearGateway` | 114 | — | 生命周期编排（connect/close/process_timer_event） |
  | `RestApi` | 336 | HTTPS | 合约查询、账户/持仓/订单查询、listenKey 增改、历史 K 线 |
  | `UserApi` | 920 | WS（用户流） | `ORDER_TRADE_UPDATE` / `ACCOUNT_UPDATE` 推送 |
  | `MdApi` | 1130 | WS（行情） | ticker / depth / markPrice / kline 推送 |
  | `PublicApi` | 1419 | WS（公共） | 与 MdApi 拆开的第二路公共流 |
  | `TradeApi` | 1451 | WS（交易） | `order.place` / `order.cancel`（**币安新版 WS API**） |

  ★ **值得抄的点**：行情流拆成 `MdApi` + `PublicApi` **两路独立 WS**。
  一路刷得慢（ticker 1s）一路刷得快（depth），拆开后慢的不拖累快的。
  我方 `core/events.py` 目前是单流，多标的满仓时会互相阻塞。

---

## 2. 调用链（文字版时序图）

### 2.1 启动（顺序是刻意的，别乱改）

```
gateway.connect(settings)
  ├─ RestApi.connect()  → 发 GET /fapi/v1/time  → on_query_time
  │     └─ time_offset = local - server        ← ★ 必须先有时钟校正
  │        └─ query_contract()  → on_query_contract
  │              ├─ 解析 filters: PRICE_FILTER.tickSize / LOT_SIZE.minQty,maxQty
  │              └─ 若 key&secret: query_order() · query_account() · query_position() · start_user_stream()
  │                    └─ on_start_user_stream → listenKey
  │                          └─ UserApi.connect(url?listenKey=xxx&events=...)
  ├─ MdApi.connect(server, kline_stream, ...)  → 自有 WS + PublicApi 第二个 WS
  └─ TradeApi.connect(key, secret, server, ...) → REAL_TRADE_HOST / TESTNET_TRADE_HOST
```

★ **顺序依赖是硬约束**：`query_contract` 的末尾才发私有查询 —— 因为**私有请求要签名，
签名要用 `time_offset`**。这个「先公共对时 → 再私有」的顺序是对的，值得抄。

### 2.2 下单（WS API 版）

```
策略 send_order(req)
  └─ TradeApi.send_order
       ├─ get_contract_by_symbol（拿不到 → 直接返回 ""，不抛）
       ├─ order_count += 1; orderid = order_prefix + str(order_count)   ← 本地 clientOrderId
       ├─ req.create_order_data(orderid) → gateway.on_order(order)      ← ★ 先落库再发请求
       ├─ 组装 params{apiKey, symbol, side, quantity, newClientOrderId}
       ├─ 【分支】MARKET → type=MARKET
       │         STOP   → type=STOP_MARKET + stopPrice
       │         其它   → ORDERTYPE_VT2BINANCE[req.type] → (type, timeInForce) 二元组
       ├─ self.sign(params)          ← ★★ 这里没有 time_offset 校正（见 D101）
       ├─ reqid += 1; reqid_callback_map[reqid] = on_send_order
       └─ send_packet({id, method:"order.place", params})
            ↓
       on_packet 按 reqid 派发 → on_send_order
            └─ if not error: return     ← ★★ 成功分支什么都不做（见 D107）
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 / 行号 |
|---|---|---|---|
| `STATUS_BINANCE2VT` | dict 常量 | 币安六态 → vnpy `Status` | 46-53；`EXPIRED → CANCELLED`（合并语义） |
| `ORDERTYPE_VT2BINANCE` | dict 常量 | `OrderType` → `(type, timeInForce)` | 59-64；**二元组**做双向映射，设计好 |
| `ORDERTYPE_BINANCE2VT` | dict 常量 | 反向，键是 `(type, timeInForce)` | 66-71 |
| `RestApi.sign` | method | HMAC-SHA256 + **time_offset 校正** | 375-437；`offset>0 → ts-=abs(offset)` |
| `RestApi.on_query_time` | callback | `time_offset = local - server` | 587；随后链式 `query_contract()` |
| `RestApi.keep_user_stream` | method | listenKey 续期 | 559-585；★ **按计数 600 判**（D102） |
| `RestApi.query_history` | method | 历史 K 线 | 818；`limit=1500` + `sleep(0.5)` + 末尾 `pop(-1)` 剔未闭合 |
| `UserApi.on_account` | callback | 余额/持仓推送 | 997；★ `frozen=wb-cw`（D103）、`if account.balance:`（D104） |
| `UserApi.on_order` | callback | 订单/成交推送 | 1042；★ `orderid=str(c)`、`datetime=generate_datetime(packet["E"])`（D105） |
| `MdApi.get_public_channels` | method | 深度通道 | 1197；★ 硬编码 `@depth10`（D110） |
| `MdApi.resubscribe_*` | method | 断线重连重建订阅 | 1226/1240；★ 遍历 `self.ticks.keys()`（D109） |
| `MdApi.on_packet` | callback | 行情解析 | 1314-1408；按 `stream.split("@",1)` 分支 |
| `TradeApi.sign` | method | WS 下单签名 | 1525；★★ **无 time_offset**（D101） |
| `TradeApi.send_order` | method | 下单 | 1542；先 `on_order` 再 `send_packet`（与我方 D26 一致） |
| `TradeApi.on_send_order` | callback | 下单回执 | 1663；★ 只处理 error（D107）、`error_code: str`（D108） |
| `format_float` | func | `format_float_positional(f, trim="-")` | 1755；防 `-1111` 精度超限，**值得抄** |

---

## 4. 可迁移设计点（D101~D112，本轮 11 类 / 12 站点）

> 编号纪律：第 18/19 轮都用了 D82~D90（撞号），第 20 轮起 D91，**本轮以 D100 为基**。

### D101 ★★ 双签名路径不一致 —— 签名必须单一真源
- **证据**：`RestApi.sign:375-437` 有 `time_offset` 双向校正；`TradeApi.sign:1525` 只有
  `params["timestamp"] = int(time.time()*1000)`，**零校正**。
- **为什么好（错得隐蔽）**：同一网关同一把密钥，**REST 全通、WS 下单必报 -1021**。
  本地时钟偏 3 秒，`query_account` 正常返回，`order.place` 全部被拒 ——
  现场表现是「能看账户不能下单」，极易被误判为权限/IP 白名单问题。
- **可迁移动作**：我方 `core/live.py` 与 `quant_app` 侧**只能有一个 `sign()`**，
  且参数里必须带 `offset_ms`。已落地 `gateway_consistency_guard.sign_once()`。

### D102 ★★ listenKey 保活按「timer 计数」而非「墙钟秒数」
- **证据**：`keep_user_stream:570` `self.keep_alive_count += 1; if < 600: return`。
- **本轮的二次发现（重要）**：`6s × 600 = 3600s`，而 listenKey 寿命**正好 3600s**
  ⇒ 这不是「安全余量」，是 **零余量**：续期请求只要慢一拍，key 先过期、续期白跑。
  第 20 轮我以为「差 30 分钟」，是因为拿自己的建议值 1800s 当判据 ——
  **判据必须锚在交易所的硬事实上，不是我的建议值**（见 §8 坑 #2）。
- **可迁移动作**：`ListenKeyKeeper.due()` 用 `now - last_ok >= refresh_every_s`；
  并区分 `refresh`（还没过期）与 `rebuild`（已过期，续期无意义）。

### D103 frozen 两条通道两套定义
- **证据**：REST `on_query_account:620` = `max(walletBalance - availableBalance, 0)`；
  WS `on_account:1012` = `wb - cw`（`cw` 是 **crossWalletBalance**）。
- **后果**：同一时刻两个冻结额，谁的 down-stream 用 frozen 谁受害。
  我方 `core/risk.py` 的可用额度推导正是靠它。
- **可迁移动作**：`normalize_frozen()` 只认 `wallet - available`，
  `cross` 分支必须**显式传参**（缺参抛错，不静默）。

### D104 ★ 余额归零事件被真值过滤吞掉
- **证据**：`on_account:1016` `if account.balance: self.gateway.on_account(...)`。
- **后果**：爆仓/清空后前端仍显示旧余额，直到下一次非零变化（可能永不再来）。
  与 D29「持仓归零必须推送」同族 —— vnpy 在**余额侧**再犯一次。

### D105 时间字段两套语义
- **证据**：WS `on_order:1082` 用 `packet["E"]`（**事件推送时间**）；
  REST `on_query_order:697` 用 `d["time"]`（**订单创建时间**）。同写 `OrderData.datetime`。
- **后果**：拿 `order.datetime` 算滑点/延迟/持仓时长时，同名字段两个含义，
  语义差可达秒级 —— 对「持仓 N 根 bar」判定是**实打实的偏差**（我方铁律「量纲先核实」同族）。
- **可迁移动作**：`OrderStamp(created_ms, event_ms)` 两个时刻分开存，`latency_ms` 显式派生。

### D106 映射表裸下标 ⇒ 交易所新增枚举值即打断整批推送
- **证据**：`on_query_order:694` / `on_order:1076` 都是 `STATUS_BINANCE2VT[d["status"]]`。
- **后果**：币安新增一个状态（如 `NEW_INSURANCE`）→ `KeyError` 抛在 `for` 循环里
  ⇒ **整批**推送中断，不只是那一条。而且 `write_log` 那行永远走不到。
- **可迁移动作**：一律 `safe_map(tbl, key)`；未知值**记日志 + 继续**，不中断循环。

### D107 ★ 成功响应里的交易所真订单号被丢弃
- **证据**：`on_send_order:1663` `if not error: return` —— 成功分支**什么都不做**。
- **后果**：`result.orderId`（交易所真实 ID）不进本地，只有 `newClientOrderId` 是链条。
  对账时只能靠 clientOrderId 反查，一旦下游改写/截断就彻底失联。
  **`core/live.py` 的 `reconcile_orders` 正是靠 ID 对账** —— 这条必须抄。
- **可迁移动作**：`parse_ack(packet)` 成功也要解析，`exchange_id` 必落库。

### D108 错误码类型标注 `str`，实际返回 `int`
- **证据**：`on_send_order:1669` / `on_cancel_order:1700` 都有 `error_code: str = error["code"]`。
- **后果**：注解是假的（Python 不强制），但会误导后续按 str 做 `startswith("-")` 之类判断。
  属「**类型判据不得用字段真值**」的又一处（第 20 轮 D97 同族）。

### D109 ★ 重连重建订阅以「已有 tick」为基准
- **证据**：`resubscribe_market_channels:1226` / `resubscribe_public_channels:1240`
  都遍历 `self.ticks.keys()`；`on_connected:1269` 还有 `if self.ticks:` 前置判断。
- **真相勘误（本轮纠正自己的初判）**：`subscribe()` 里 `ticks[symbol] = tick` 建在
  `send_subscribe_packet` **之前**，所以「订阅成功但还没 tick」的合约其实**已被记账**，
  首版我以为会丢订阅，**查完代码发现侥幸成立**。
  但 `on_connected` 的 `if self.ticks:` 在外层 ——
  **一次连接都没成功过就断线**（启动即失败）时，`ticks` 为空 ⇒ 重连后**整批订阅全丢**，
  日志仍写 "MD API connected"。⇒ **缺陷真实存在，但触发条件比我初判窄得多**。
- **可迁移动作**：订阅真源 = **我声明过的意图集合**，与「是否收到过数据」完全解耦。
  已落地 `SubscriptionRegistry.rebuild()`，参数 `seen_ticks` 仅作审计对照。

### D110 深度档位硬编码 `@depth10`
- **证据**：`get_public_channels:1199` `return [f"{name.lower()}@depth10"]`。
- **后果**：我方盘口建模要 bid5/ask5（记忆第 17 轮 D81 挂账）时无法对接；
  想要 20 档也接不上。**参数化成本极低，收益是「能接别的场景」**。

### D111 市价单在映射表里就宣言了 `timeInForce`
- **证据**：`ORDERTYPE_VT2BINANCE[MARKET] = ("MARKET", "GTC")`。
- **细节勘误**：`send_order:1588` 对 MARKET 走了**单独分支**只发 `type`，
  所以**当前实现不发病**；但**契约本身是错的** —— 任何按该表通用构造参数的调用方
  都会给市价单塞 `timeInForce=GTC`。
- **可迁移动作**：`market_order_params()` 显式不含 TIF/price。

### D112 ★★★ 全网关无 `reduceOnly` / `positionSide` —— 平台反超网关的实证
- **证据**：`grep -rn "reduceOnly\|positionSide\|closePosition"` 在 `vnpy_binance/` 下**零命中**。
- **后果**：不能下「只平仓」单，不能在 Hedge Mode 下工作。
  ⇒ 止损单和开仓单在交易所侧**同为普通单**，一旦方向判断错就变成反向开仓。
- **★ 我方已反超**：`core/risk.py` 第 9 轮加 `reduce_only`（16/16），
  `core/live.py:166 submit_order` 已透传。**这是本轮最有价值的对照结论：
  在「风控语义」这一层，我们不是追赶者。**
- **必须守住的验收**：`reduce_only_params()` 的 `reduceOnly=True` 不可省。

---

## 5. 可复用代码片段

**来源**：`ai_quant_lab/20261101_vnpy_vnpy_binance/gateway_consistency_guard.py`（本轮落地，selftest **75/75**）

```python
# 单一签名入口：timestamp 必须带 time_offset 校正（对应 D101）
def sign_once(params, secret, offset_ms=0, now_ms=None):
    clock = now_ms or (lambda: int(time.time() * 1000))
    ts = int(clock())
    if offset_ms > 0:
        ts -= abs(int(offset_ms))
    elif offset_ms < 0:
        ts += abs(int(offset_ms))
    out = {str(k): v for k, v in params.items()}
    out["timestamp"] = ts
    payload = "&".join(f"{k}={out[k]}" for k in sorted(out))
    out["signature"] = hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return out

# 保活按墙钟秒数，与 timer 节拍解耦（对应 D102）
class ListenKeyKeeper:
    def due(self):
        return self._last_ok is None or (self._clock() - self._last_ok) >= self.refresh_every_s
    def expired(self):
        return self._last_ok is None or (self._clock() - self._last_ok) >= self.expire_s
    def tick(self):
        if self.expired(): return "rebuild"
        if self.due():     return "refresh"
        return "idle"

# 下单回执：成功也要解析，交易所真 ID 必须留存（对应 D107/D108）
def parse_ack(packet):
    err = packet.get("error")
    if err:
        return OrderAck(False, err_code=err.get("code"), err_msg=str(err.get("msg", "")))
    body = (packet.get("result") or {}) or packet
    eid = body.get("orderId")
    return OrderAck(True, client_id=str(body.get("clientOrderId", "")),
                    exchange_id=int(eid) if eid is not None else None)
```

模块还提供：`normalize_frozen()` / `account_events()` / `OrderStamp` / `safe_map()` /
`SubscriptionRegistry` / `depth_channels()` / `market_order_params()` / `reduce_only_params()` /
`audit_gateway(profile)`（一次性体检，返回 `{findings, by_code, worst, ok}`）。

**加载验证**：`from core import lab_bridge; lab_bridge.get("gateway_consistency_guard")` → 零警告，75/75。

---

## 6. B站学习（本日 30% 权重）

- **状态**：**第 10 轮起已结案降级**，本轮仍无可用字幕源（B 站接口需登录态 + 音频转录被明确禁止）。
- **本轮替代**：读同仓库 `inverse_gateway.py`(1699) / `spot_gateway.py`(1523) /
  `portfolio_gateway.py`(2146) 的对应函数，做**跨网关一致性对照** —— 效果比看视频更直接。
  - 三份网关**同样**在 `process_timer_event` 里调 `rest_api.keep_user_stream()`
    ⇒ D102 是**同族复制**，不是单文件失误。
  - 三份网关**同样**无 `reduceOnly` ⇒ D112 是**架构级缺口**。
- **如实记账**：本轮 30% 权重实质折算为「跨文件对照」，
  **不计入 B 站学习完成度**，与本项目历史口径一致。

---

## 7. 对黑马策略的启发（落到具体动作）

### 7.1 新假设 **H-043：入场折价 × 出场加价「同时」挂单，净效应是相加、抵消还是非线性？**

这条直接来自第 20 轮 P1 挂账「入场/出场**联合挂单**效应未测」，
而 `linear_gateway.py:59-64` 的 `(type, timeInForce)` 二元组映射
逼出一个必须回答的工程问题：**两边都挂 maker 时，成交是「两个独立概率」还是「同一个逆向选择」？**

- **可回测动词句**：对四只 15m 永续全历史跑 `StrategyParams()` 默认策略取成交，
  对每笔把「信号当根收盘价市价买入」改为「`signal_close×(1−d)` 挂限价买、4 根内 `low≤limit` 成交」，
  **同时**把「出场当根收盘价市价卖出」改为「`exit_close×(1+e)` 挂限价卖、4 根内 `high≥limit` 成交」，
  `d,e ∈ {0.1%,0.3%,0.5%}` 共 9 格。
- **结果：搁置（方向不一致）** —— 但**每格数字都是有信息的**，见下表。

| 标的 | 基线净单笔 | 中档 (0.3%/0.3%) 联合成交率 | 中档 Δpp | Δpp>0 格数 | 中档相对单边 H-042(+0.4039pp) |
|---|---|---|---|---|---|
| BTCUSDT | +1.8916pp | 61.72% | **+1.2243** | 6/9 | **+0.8204** |
| ETHUSDT | +1.9107pp | 69.05% | +0.2480 | 8/9 | −0.1559 |
| BNBUSDT | +2.1319pp | 66.83% | +0.0256 | 5/9 | −0.3783 |
| DOGEUSDT | +0.4679pp | 76.22% | **+0.9327** | 8/9 | **+0.5288** |

- **三条不能忽略的副作用（比 Δpp 本身更重要）**：
  1. **Δpp 是「联合成交样本内」的均值，不是账户收益。** 中档合计放弃率 **38.28%(BTC) / 30.95%(ETH) /
     33.17%(BNB) / 23.78%(DOGE)** —— 近三分之一到四成的机会被放弃，
     这些资金**闲置**。与 H-042 同一口径局限（单笔层面，不含资金复用）。
  2. **深档崩塌**：`0.5%/0.5%` 档 BTC **−1.7407pp**、BNB **−1.5815pp**，
     成交率只剩 38~49% ⇒ 「挂得越深越赚」在联合口径下**完全不成立**。
  3. **入场那一侧确实是拖累**：`in 0.3% / out 0.1%` 在 BNB 上 **−0.4944pp**、
     ETH 上只剩 +0.1083pp —— 出场只加 0.1% 时，入场的逆向选择就把它吃光了。
     **这从第二个独立角度再次印证 H-041 的「入场折价=逆向选择」。**
- **为什么判搁置而不是验证**：3/4 标的 Δpp>0 格数≥6 ✅、中档 Δpp>0 **4/4** ✅，
  但「中档优于单边」只有 **2/4** ⇒ 支持条件（≥3/4）未达成，证伪条件（≥3/4 劣于单边）也未达成。
  **方向不一致 = 不构成结论，也不构成证伪** —— 按台账纪律如实标「搁置」，
  不硬凑成「已验证」。
- **解锁条件（写清，不留悬空）**：补**样本外**（滚动前推）+ `min_trades ≥ 100` 闸
  + 把「放弃机会的资金闲置成本」计入 ⇒ 再看中档是否仍优于单边。
- **若成立，改哪**：`core/backtest.py` 加 `entry_limit_discount` + `exit_limit_premium`
  两个开关（第 20 轮 P0 已挂），**同时**加 `joint_fill_rate` / `abandoned_pct` 两个计数器 ——
  否则永远只能在 lab 里「独立复刻」，进不了引擎。

### 7.2 与 P0 挂账的直接对接

| 第 20 轮挂账 | 本轮进展 |
|---|---|
| P0 `core/backtest.py` 加 `exit_limit_premium` 开关 | **未做**（本轮 70% 权重给了网关精读）；H-043 反而证明「加开关前必须先想清两边联合」 |
| P1 H-042 补样本外 + `min_trades ≥100` 闸 | **未做**，但 H-043 已暴露「min_trades 闸」的必要性（BNB 203 笔 < 其余） |
| P1 入场/出场联合挂单未测 | ✅ **本轮已测**（H-043，9 格 × 4 标的） |

---

## 8. 未完成 / 失败区（诚实留痕）

### 8.1 第零步 AtomCode guard：**连续第 11 轮推理层失败**
- `atomcode_quota_guard.py --json` 首次 → `proxy_listening: false, verdict: "proxy_down"`
- 后台拉起 `atomcode_proxy.py 13460` → 6 秒后复测：`proxy_listening: true`、`health_http: 200`、
  `logged_in: true`（账号 `gcw_1D1KA17b`）
- **但最小推理实测仍失败**：`{"ok": false, "http": 0, "elapsed_s": 240.0, "reason": "TimeoutError"}`
  ⇒ `verdict: "probe_failed"`
- **根因判定**：上游**推理层僵死**（非额度、非二进制 —— `--version` 第 13 轮已验 5.2.3 完好，
  非登录态 —— `logged_in=true` 且未报 403）
- **处置**：按收敛纪律（技能 §3.12-8）降级本地 Read/Grep 精读，**0 积分**，不再耗时间。
  这是**执行失败，不是知识失败** —— 本轮六项硬指标全部由本地精读达成。

### 8.2 白名单 `core_file` 字段失真（第 3 次出现）
- TASK_CARD 写 `binance_gateway.py`，仓库实际只有：
  `inverse_gateway.py`(1699) / `linear_gateway.py`(1770) / `portfolio_gateway.py`(2146) / `spot_gateway.py`(1523)
- 记忆第 10 轮记「白名单第 2 次勘误」，第 20 轮修了**第 5 位 404**，
  但 `run_nightly_learning.py:REPO_ROTATION` 的 `core_file` 字段**仍未改**
  ⇒ 每 12 天必空转一次。**下轮 P0：直接把该字段改成 `linear_gateway.py`。**

### 8.3 本轮**自己写错的三处判据**（比源码 bug 更值得记）
1. **断言手指数错**：`audit_gateway` 断言 `count == 11`，实际 **12**（11 类，`MAP_DIRECT_INDEX` 2 站点）
   ⇒ 已改为「**总数由 `by_code` 加总派生**，不手填」。
2. **判据锚错对象**：`audit_keepalive` 初版拿「隐含间隔 vs **我的建议值 1800s**」比，
   得出「差 30 分钟」；真相是 `6s×600=3600s` **正好等于 listenKey 寿命 = 零余量**。
   ⇒ 判据必须锚在**交易所硬事实**（3600s），不是我的建议值。
3. **测错了对象**：`ListenKeyKeeper` 时序测试未先 `mark_ok()`，`_last_ok=None` ⇒ `expired()` 恒真
   ⇒ 测到的是初始化分支，不是时钟推进分支。已拆成「未初始化 → rebuild」+「已初始化 → idle/refresh/rebuild」两条。
> **共性**：三处都是「**断言/判据本身是错的，代码是对的**」。
> 这正是铁律「断言 == 期望 永远是绿的」的反面 —— 我不敢让它绿，所以它红了三次。

### 8.4 ★ 本轮自己写出的**设计缺陷**（第八步自检抓到，已修）
`audit_order_params(has_reduce_flag: bool = False, ...)` —— 缺省值是 `False`，
而 `audit_gateway` 里又写 `bool(profile.get("has_reduce_only", False))`。
⇒ **空画像 `{}` 也会被判出 `NO_REDUCE_FLAG`**：「**没给证据**」被当成「**证据是坏的**」。
这是把 fail-open 反着写成了**假阳性**，比漏报更隐蔽（漏报会被发现，假阳性会被当成"一直有问题"）。

- **修法**：改三态 `True / False / None(=未提供证据，静默)`，**禁止 `bool()` 强转**。
- **验证**：`audit_gateway({})` → `{'count': 0, 'ok': True, 'worst': 'none'}`；补 3 条自测（72 → 75）。
- **共性**：与 §8.3 三处同源 —— **都是「判据本身错，代码对」**。
  区别是这次错在**接口契约**（默认值语义），不是错在断言写法。

### 8.5 自检脚本自身的第二个「判据找错对象」
首版把 `risk_wiring` / `fill_realism` 当 `core.*` 模块 import ⇒ `ModuleNotFoundError`，
看起来像「回归缺失」。真相是它们**是 `core/backtest.py` 里的函数**
（`selftest_risk_wiring()` / `selftest_fill_realism()`）。
⇒ **「导入失败」不等于「功能不存在」** —— 先确认它在哪个命名空间，再判红绿。

### 8.6 D109 初判被自己证伪
初判「订阅成功但未收到 tick 的合约在断线后永久丢订阅」。读 `subscribe()` 后发现
`ticks[symbol] = tick` 建在 `send_subscribe_packet` **之前** ⇒ 侥幸成立。
**缺陷真实存在，但只在「一次都没连上过就断线」时触发**。
已按「推翻自己写下的结论必须回溯改正」改写（见 §4 D109）。

### 8.7 B 站 30% 权重
实质 **0**（第 10 轮已结案）。本轮用跨网关对照替代，笔记 §6 已如实标注，**不计入完成度**。

### 8.8 未做（明确挂账）
- `core/backtest.py` 的 `exit_limit_premium` / `entry_limit_discount` 开关（P0，第 2 轮挂账）
- `core/risk.py` 接 `GateVerdict` + 两层闸（P0）
- 实盘逐笔导出（P0，挂账第 4 轮）
- `MEMORY.md` 已 13.2KB 接近注入上限 → 第九次整理（P2）

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：`ai_quant_lab/20261101_vnpy_vnpy_binance/gateway_consistency_guard.py`
      · selftest **75/75** · `lab_bridge` 零警告
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-043**（搁置）+ `hypothesis_runner.REGISTRY` 已注册

---

## 10. 成本与技能

- **本次花费积分估算**：**0**（AtomCode 推理层降级，全程本地 Read/Grep + 本地 Python）
- **用了哪些技能**：
  - `ai-quant-open-source-nightly-learning`（夜学协议 V3.6，本任务骨架）
  - `币安量化数据通路与黑马策略诊断`（本地数据/回测口径纪律）
- **没用哪个技能**：`云端四端归档通道` / `六端空间归位`（周日归档阶段才用，见收尾报告）
- **沉淀 / 迭代了什么**：
  - 新建模块 `gateway_consistency_guard.py`（75/75，lab_bridge 可加载）
  - `hypothesis_runner.py` 新增 `_joint_limit_study` + `verify_H043`（+13678 B，LF 行尾保持）
  - 本笔记（六项硬指标齐）
- **技能版本**：本轮**未改** SKILL.md（连续多轮已稳定，无非改不可的错）

---

*建立：2026-11-01 · 汤小龙 · 绑定 AI量化平台夜学任务第 21 轮*
