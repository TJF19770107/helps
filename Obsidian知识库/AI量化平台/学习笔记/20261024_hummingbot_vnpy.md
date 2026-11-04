---
日期: 2026-10-24
仓库: hummingbot（主）+ backtrader（副）
核心文件: hummingbot/connector/exchange/paper_trade/paper_trade_exchange.pyx（1139 行）+ core/data_type/order_book.pyx（483）+ connector/budget_checker.py（161）/ backtrader/brokers/bbroker.py:994-1036
轮次: 第 14 轮（周六 · 周中）
tags: [AI量化平台, 夜学, 代码拆解, 撮合仿真, 滑点, 手续费归因]
---

# 20261024 · hummingbot · paper_trade_exchange.pyx + bbroker 滑点夹断

## 0. 一句话结论

> **滑点这条「最后一个没被动过的乐观源」，实测只有 0.0014~0.0038pp/笔 —— 是手续费的 1/50。
> 撮合模型这条线边际收益已经耗尽；乐观偏差 98% 的账都在「双边 0.1% taker 手续费」上。
> 下一步不是把回测做得更真，是把真实成本做得更低。**

而且今天有一条**先验被 4/4 打死**的证伪：我以为突破型入场 close 贴近最高价，
所以入场端滑点越界一定更严重 —— 实测**全面相反**（BTC 8.53% vs 全样本 22.43%，低 13.91pp）。

---

## 1. 架构定位

**主文件 `paper_trade_exchange.pyx` 属于「撮合回测层」**——它是 hummingbot 的**纸面交易所**：
把真实的 order book 数据回放，用真实的簿级深度撮合你的委托，账户余额/持仓按真实规则变动。
它不是"回测器"，是**一个假的交易所**（同构于 vnpy 的 `BacktestingGateway`、nautilus 的
`SimulatedExchange`），所以它必须实现 `ExchangeBase` 的全套接口（`c_buy`/`c_sell`/`c_cancel`/
`c_tick`/`c_get_balance`…）。

- 上游依赖 →
  - `core/data_type/composite_order_book.py`（多交易所合成盘口，喂 `simulate_buy/sell`）
  - `core/clock`（`c_tick` 由统一时钟驱动，`_current_timestamp` 是撮合唯一时间基准）
  - `connector/budget_checker.py`（**费用与余额参与"能不能下单"判定**，不是事后扣）
  - `core/utils/estimate_fee.py:build_trade_fee`（费率按 maker/taker 分支）
- 下游被谁调用 →
  - `hummingbot/strategy/*`（所有做市/套利策略通过 `ExchangeBase` 接口下撤单）
  - `connector/client_order_tracker.py`（把 `OrderFilledEvent` 汇总成订单状态机）
  - 事件总线 `core/pubsub`（`OrderFilledEvent` / `BuyOrderCompletedEvent` 向外广播）

**副文件 `bbroker.py` 属于「撮合价格层」**——backtrader 的 broker 只管三件事：
何时成交（`_try_exec_*`）、按什么价成交（`_slip_up/_slip_down`）、佣金与保证金（`comminfo`）。
它比 hummingbot 粗（无盘口、只有 OHLC），但**在"滑点必须落在当根区间内"这一点上比我们严谨**。

---

## 2. 调用链（文字版时序图）

### 2.1 市价单（hummingbot · 延迟是一等参数）

```
strategy.buy(pair, amount, MARKET)
  → ExchangeBase.c_buy                       (:324)
      quantize price/amount                  (:345-348)
      _queued_orders.append(QueuedOrder(ts))  (:350)  ← 不立即成交！
  …
  core/clock 每 tick 推进 _current_timestamp
  → PaperTradeExchange.c_tick                (:319)
      → c_process_market_orders              (:609)
          if front.create_timestamp <= now - TRADE_EXECUTION_DELAY(=5.0s):   (:614)
            → c_execute_buy                  (:445)
                entries = order_book.simulate_buy(amount)     (:454)  ← 逐档吃量
                avg_price = Σ(price×amount)/amount            (:457-460)
                BudgetChecker.populate_collateral_entries     (:473)  ← 费进抵押品
                if paid > quote_balance → MarketOrderFailure  (:481-489)
                set_balance(扣款/加仓)  → OrderFilledEvent×N → BuyOrderCompleted  (:492-525)
```

> **5 秒延迟不是随手写的常数**：`TRADE_EXECUTION_DELAY = 5.0`（:144）意味着**下单与成交之间
> 一定隔着一个时间窗**，窗内价格可以变。要做延迟建模，最低配就是"排队 + 到点按当时盘口撮"。

### 2.2 限价单（双通道，OR 关系）

```
通道 A（主动成交 / 有真实 trade 打穿我的价）
  order_book.record_filled_order → OrderBookEvent.TradeEvent
    → OrderBookTradeListener.c_call           (:121-125)
        → c_match_trade_to_limit_orders       (:895)
            maker_buy = (trade.type is SELL)  (:903)     ← 方向是反的！
            从 rbegin() 起，凡 price <= trade_price 的买单全部成交  (:920-928)

通道 B（对手盘最优价穿越我的挂单价）
  PaperTradeExchange.c_tick
    → c_process_crossed_limit_orders          (:876)
        opposite_price = c_get_price(pair, is_buy)          (:850)
        买单：opposite_price > my_price → 跳出；否则成交   (:857-864)
```

> 两条通道**都成立才成交**是错的，正确语义是 `A or B`：真实成交流打穿（A）比"最优价穿越"（B）
> 更硬，但 hummingbot 不做优先级 —— 两者都会直接触发 `c_process_limit_order`。

### 2.3 滑点夹断（backtrader）

```
_try_exec_market(order, popen, phigh, plow)                    (:854)
  exprice = popen  (或 coc 模式下的 pclose)
  buy : p = _slip_up(phigh, exprice, doslip=slip_open)          (:866)
  sell: p = _slip_down(plow, exprice, doslip=slip_open)         (:868)
  → _execute(order, price=p)

_slip_up(pmax, price, doslip, lim):                            (:994)
  pslip = price × (1 + slip_perc)
  if pslip <= pmax        : return pslip        ← 不越界，用滑点价
  elif slip_match or ...  : return pmax         ← **越界，夹到当根 high**
  else                    : return None         ← slip_out=False：宁可不成交
```

---

## 3. 关键类 / 函数

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `PaperTradeExchange.c_execute_buy` | cdef 方法 | 市价买入：簿级 VWAP → 抵押品校验 → 改余额 → 发事件 | `:445-525` |
| `OrderBook.simulate_buy` | 方法 | 逐档吃量，返回 `List[OrderBookRow]` | `order_book.pyx:283-295`；深度不足时**用最后一档价硬吃** |
| `QueuedOrder` | cdef class | 待撮合市价单（时间戳+ID+方向+量） | `:73-110` |
| `TRADE_EXECUTION_DELAY` | 类常量 | 市价单延迟撮合窗口 = 5.0s | `:144`，延迟是一等参数 |
| `c_quantize_order_amount` | cdef 方法 | `(amount//quantum)*quantum` + `<1e-7 → 0` | `:1078-1086`，量化在**报单前** |
| `BudgetChecker.populate_collateral_entries` | 方法 | 把手续费算进"买得起吗" | `budget_checker.py`，费进抵押品 |
| `c_match_trade_to_limit_orders` | cdef 方法 | 通道 A：真实成交打穿挂单价 | `:895-939`，maker 方向取反 |
| `c_process_crossed_limit_orders` | cdef 方法 | 通道 B：对手盘最优价穿越 | `:836-892` |
| `BBroker._slip_up / _slip_down` | 方法 | 滑点后夹回 `[low, high]`，或拒绝给价 | `bbroker.py:994-1036` |
| `BBroker._try_exec_stop` | 方法 | 止损：`open` 已穿越则按 open，否则按触发价 | `:917-946`，与我们 `gap_stop_price` 同构 |

---

## 4. 可迁移设计点（D51~D59）

### D51 成交价必须来自**簿级 VWAP**，不是「收盘价 + 常数」
`simulate_buy` 逐档吃量再算加权均价（:454-460）。我们的 `core/backtest.py` 到今天还是
`px = close × (1±slip)` —— 一个**与当根深度无关**的价。
- **为什么更好**：滑点的物理成因是"吃掉薄档"，所以它**必然随下单量/深度变化**。
  同一笔 $10k 在 DOGE 上吃掉 3 档、在 BTC 上吃 0.3 档，用一个常数把这两件事抹平了。
- 落地限制（诚实说）：我们只有 15m OHLCV，**没有历史盘口快照**，做不了真簿级 VWAP。
  能做的是"用当根成交量与振幅反推档位模型"—— 见 H-026 结论：V/Q 中位 12155×，
  **15m 粒度下我们的单子小到看不见**，所以这一步**当前不必要**（这也是 D51 对我们降级为 P2 的原因）。

### D52 延迟必须是**参数**，不是 0
`TRADE_EXECUTION_DELAY = 5.0`（:144）：下单进队列，T+5s 才按**当时**盘口撮。
- **为什么更好**：0 延迟 = 宣称「我看见的价格就是我的成交价」，这是所有回测乐观的源头之一。
  延迟的成本不是固定的，它 ∝ 波动率，所以**在高波动时段延迟最贵**。
- 我们的现状：`entry_on="close"` 与 `"next_open"` 两档，等价于 0 延迟 / 1 根延迟。
  15m 一根 = 900s，比 hummingbot 的 5s 粗 180 倍 —— 但方向是对的，且 `next_open` 已经更保守。

### D53 限价成交是**双通道 OR**，不是单通道
通道 A（真实 trade 打穿，:895）+ 通道 B（对手盘最优价穿越，:836），任一即成交。
- **为什么更好**：只用 A 会漏掉"我的挂单在队列前面、被一笔同价大单成交"的情况；
  只用 B 会漏掉"价格只是插针到我这一档"。两条 OR 是**上界估计**（偏乐观），
  但对做市策略是合适的近似 —— 因为做市本来就假设自己是队列前排。
- 反例提醒：这正是 H-026 检验的东西（真实队列位置）。结论是 15m 粒度下排队**不紧**
  （V/Q 中位 12155×），所以 OR 的乐观性在我们这个周期上**兑不出来**。

### D54 同一个「资金不足」，限价单是 **Cancel**、市价单是 **Failure**
`:680`（限价买入余额不足 → `OrderCancelledEvent`）vs `:485`（市价买入余额不足 →
`MarketOrderFailureEvent`）。**两种不同终态，走的是同一个原因**。
- **为什么这是对的**：限价单本来就在挂，撤掉它是正常生命周期；市价单是"我要立刻成交"，
  资金不够就是**失败**，必须让上层重试/降量。混用会让上层状态机分不清"我该重试还是该放弃"。
- 这条直接对应我们 `core/order_lifecycle.py` 的 7 态：`CANCELLED` 与 `REJECTED` 必须分开，
  且 `REJECTED` 要可重试、`CANCELLED` 不可重试。

### D55 量化必须在**报单前**完成，且不足一个最小单位就**归零**
`c_quantize_order_amount`（:1078-1086）：`(amount // quantum) * quantum`，`< 1e-7 → 0`。
- **为什么必须归零**：不归零会出现"下单 0 但记为成交一笔"的**幽灵成交**；实盘会直接拒单。
  这是回测比实盘乐观的**结构性**来源之一（不是参数问题）。
- 本轮已落地：`quantize_qty()` + `run_backtest(lot_size=...)`。实测 `qty_zeroed = 0`
  ⇒ 当前 $10k 规模下**从未触发**（归属"未观测"，不是"无影响"，见 §8）。

### D56 手续费参与「能不能下单」判定（费进抵押品）
`BudgetChecker.populate_collateral_entries` 把估算手续费算进 `paid_amount`（:473-484），
所以"我买得起"指的是**含费买得起**。
- **为什么更好**：先扣费再看余额，和"先买再扣费"在边界上差一整笔 —— 满仓策略会系统性
  在最后一格超配。这是我们 `risk.py` `R7 顺序锁定` 的同一条纪律（第 6 轮 D6 的第二次独立实现证据）。

### D57 ★ 反例：hummingbot 的 VWAP 分母用**请求量**，把"深度不足"吃掉了
`:460` `avg_price = avg_price / amount`（amount = **请求量**）。若盘口深度不够，
`simulate_buy` 会在 `order_book.pyx:286-294` 用**最后一档价硬吃剩余量**，于是：
- 返回的 entries 总量 < 请求量，但分母仍用请求量 → VWAP 被**拉向最后一档价**；
- 更糟的是**看不出来**：没有任何标志位告诉你"这单没吃完"。
- 我们的修法：`vwap_from_levels()` 分母用 `Σ entry.amount`，并返回 `depth_short: bool`。
  **宁可报"只吃到 60%"，不报一个假均价。** 这条已写进 `fill_price_model.py` 并在自测 V2/V3 断言。

### D58 ★★ 滑点必须被当根 `[low, high]` 夹断（**今天真正的落地件**）
`_slip_up(pmax=phigh, ...)`：滑点价超过当根 high 就返回 high（`slip_match=True` 默认）。
- **为什么这不是"放宽优化"而是物理修正**：当根最高只到 high，你**不可能**买在它之上。
  旧口径 `close×(1+0.05%)` 在越界的 bar 上收了一个**不存在的价**。
- **实证（本轮标定 `slip_bounds_table.json`）**：0.05% 单边滑点越界占比
  BTC **22.43%** / ETH **15.94%** / BNB **20.39%** / DOGE **12.63%** —— 五分之一到四分之一的成交
  被记了不可能的价格。
- **但成本影响只有 +0.0014~+0.0038pp/笔**（H-028）—— 因为越界量通常只差一点点
  （振幅 p10 就有 0.06~0.11%，0.05% 只是偶尔溢出）。
- **方法论教训**：夹断让成本只降不升，所以"Δ>0"**注定成立、不构成证据**。
  证据只能是 `slip_clamped` 非零（咬合力）。这条纪律已写进 `bite_v2`。

### D59 `slip_out=False`：**宁可不成交，也不给不存在的价**
`_slip_up` 末尾 `return None`（:1015）：滑点价越界且 `slip_match=False` →
该 order 本轮**不执行**（继续挂着等）。
- **为什么更好**：这是"无价可给 → 挂单继续等"的语义，比"硬塞一个价"诚实得多。
  回测里"没成交"是一个**合法结果**，不是异常。
- 对我们的动作：`gap_stop` + `clamp_slip` 组合已经能表达"止损穿越后按真实价成交"；
  再往下的"部分成交后剩余继续挂"我们**没做**（回测不排队，剩余直接撤）——
  这条留作 P2，理由是：H-026 已证 15m 排队不紧，做了也没有咬合力。

---

## 5. 可复用代码片段

**① 滑点夹断（落地到 `core/backtest.py:slip_price`）**

```python
# 来源：backtrader/backtrader/brokers/bbroker.py:994-1015（_slip_up/_slip_down）
# 用途：滑点价越出当根区间时夹回边界；关掉开关时逐点等价旧公式（零退化）
def slip_price(px, high, low, is_buy, slip, clamp=False):
    raw = px * (1.0 + slip) if is_buy else px * (1.0 - slip)
    if not clamp or high is None or low is None:
        return raw
    hi, lo = float(high), float(low)
    if not (np.isfinite(hi) and np.isfinite(lo)) or hi < lo:
        return raw
    return min(raw, hi) if is_buy else max(raw, lo)
```

**② 数量量化（落地到 `core/backtest.py:quantize_qty`）**

```python
# 来源：hummingbot/connector/exchange/paper_trade/paper_trade_exchange.pyx:1078-1086
# 用途：按 lot_size 向下取整；不足一个最小单位直接归零（不下 0 量单）
def quantize_qty(qty, lot_size, min_qty=0.0, eps=1e-12):
    q = max(0.0, float(qty)); lot = float(lot_size or 0.0)
    if lot <= 0:
        return q, q <= eps
    steps = max(0, int((q + eps) // lot))
    qq = round(steps * lot, max(0, int(round(-np.log10(lot))) + 2))
    floor_q = float(min_qty if min_qty and min_qty > 0 else lot)
    if qq < floor_q - eps:
        return 0.0, True
    return qq, False
```

**③ 簿级 VWAP（修正版，落地到 `ai_quant_lab/20261024_hummingbot_vnpy/fill_price_model.py`）**

```python
# 来源：hummingbot paper_trade_exchange.pyx:454-460 + order_book.pyx:283-295（含其缺陷修正）
# 用途：分母改用真实成交量，深度不足显式上报，不静默给假均价
def vwap_from_levels(levels, qty):
    want = max(0.0, float(qty)); left, cost, got, used = want, 0.0, 0.0, 0
    for price, amount in levels:
        if left <= 0: break
        p, a = float(price), float(amount)
        if not (math.isfinite(p) and math.isfinite(a)) or p <= 0 or a <= 0: continue
        take = min(a, left); cost += p * take; got += take; left -= take; used += 1
    if got <= 0:
        return {"vwap": None, "filled": 0.0, "depth_short": want > 0, "levels_used": 0}
    return {"vwap": cost / got, "filled": got, "depth_short": left > 1e-12, "levels_used": used}
```

---

## 6. B站学习（本日 30% 权重）

- **状态**：**已于 2026-10-20 永久降级为「标题级」（W3 结案）** —— 实测字幕接口恒返回空，
  不再每轮重复记「未完成」。零成本底线不允许做音频转录。
- 本轮交叉学习改为：**hummingbot 官方文档口径 vs 代码口径** 的自查（不花积分）——
  hummingbot 文档说 `paper_trade` 是「模拟撮合」，但代码里 `simulate_buy` 在深度不足时会
  **用最后一档价硬吃**，文档没写这件事。**文档说"模拟"，代码说"模拟 + 兜底"，两者不等价。**
- 存疑处（待代码验证）：`OrderBookMarketOrderFillListener`（:127-140）把市价单的成交也
  `record_filled_order` 回盘口 —— 这会**污染后续的 VWAP**（自己吃掉的量被记成市场成交）。
  本轮没时间深挖，列入 §10 待跟进。

---

## 7. 对黑马策略的启发（落到具体动作）

### 已落地（本轮真做了）
| 动作 | 文件:位置 | 验收 |
|---|---|---|
| 滑点价夹回当根 `[low, high]` | `quant_app/core/backtest.py:slip_price()` + 6 处调用 | `selftest_slip_lot_wiring` **13/13** |
| 委托量按 lot_size 向下取整 + 归零 | `core/backtest.py:quantize_qty()` + 入场段 ③ | 同上 R4 |
| 新增咬合力计数 `bite_v2`（旧 `bite` 不变） | `core/backtest.py:_fs` | R3 / R3b |
| 滑点物理上界标定表 | `ai_quant_lab/20261024_hummingbot_vnpy/slip_bounds_table.json` | 4 标的 × 6 分位 |
| 簿级 VWAP 修正版 | `ai_quant_lab/20261024_hummingbot_vnpy/fill_price_model.py` | 自测 **26/26** |
| 接进平台 | `core/lab_bridge.get("fill_price_model")` → module | 加载成功、`selftest ok=True` |

### 下一步（按 ROI 排序，本轮结论驱动）
1. **P0 · 换赛道：手续费档位**。本轮把撮合模型的乐观量压到 `<0.004pp/笔`，
   而手续费是 **0.2041pp/笔**（双边 0.1% taker）。**50 倍的差距。**
   具体动作：把 `StrategyParams.fee_rate` 从 `0.001`（taker）改成 `0.0002`（BNB 抵扣后 taker）
   或 `0.0002~0.0004`（maker），看净额单笔均值怎么变 —— 这比再修撮合模型值钱 50 倍。
   ⚠️ 但**不许把它当结论**：手续费档位取决于实盘能否真拿到 maker 成交/BNB 抵扣，
   这是**执行能力问题**，不是回测参数问题。
2. **P1 · `H-023` 分标的给结论**（已挂账 2 轮）：停止盲目外推 `tp_tiers` 端点。
3. **P1 · `core/live.py` 接 `reconcile_position()`**（挂账）。
4. **P2 · 延迟参数化**（D52）：`entry_on` 已经是 0/1 根两档，加第三档"半根"意义不大。

### 若假设成立，**不改策略** —— 改的是我们对"回测可信度"的账
H-027/H-028 都不是交易信号假设，它们是**口径假设**。它们成立的含义是：
**以后报收益时，可以放心说"撮合侧我们已经修到误差 <0.004pp"**，
剩下的误差项只在手续费档位与资金费（funding）上。**这本身就是一个可交付的结论。**

---

## 8. 未完成 / 失败区（诚实留痕）

1. **AtomCode 通路：连续第 4 轮失败**（`proxy_down` → 后台拉起 → `/health` 200 +
   `logged_in=true` + `/v1/models` 3 个免费模型，但最小推理 **240s 超时 HTTP=0**）。
   `atomcode.exe --version` 在第 13 轮已验 5.2.3 完好 → **上游推理层挂死，非额度、非二进制**。
   全程降级本地 Read/Grep，**0 积分**。按第 13 轮收敛纪律，第 3 轮起不再在这上面耗时间。
2. **`qty_zeroed = 0`（4 只全为 0）⇒ lot 粒度约束「未观测」，不是「无影响」。**
   这是本轮必须点破的：`lot_applied` 129/211/203/472 证明开关执行了，但**一次归零都没触发**，
   因为 $10k × 100% 仓位在 BTC 上是 0.05~0.2 个币，远高于 0.001 的 lot。
   要真测粒度，必须把本金降到"仓位量级 = lot 量级"（如 BTC 本金 $100），否则永远是未观测。
   **台账状态只按主命题（夹断不劣化）判已验证，粒度半边在这里显式降级。**
3. **H-027 先验被证伪**：我预期"入场 bar 越界更严重"，实测 4/4 全部更低
   （BTC −13.91pp / ETH −4.09pp / BNB −1.18pp / DOGE −4.37pp）。
   原假设的机理（突破型入场 close 贴最高价）**不成立** —— 黑马策略的入场 bar 落在相对温和的中段。
   如实记：**这条先验是错的**，不改写成"我早就料到"。
4. **P1 三项未动**：`core/live.py` 接 `reconcile_position()` / H-023 分标的 / 滑点参数的
   "半根延迟"档。本轮时间全投在 P0 的两项标定与接线，P1 挂到下一轮。
5. **`core/backtest.py` 仍是 OHLCV 粒度，做不了真簿级撮合**（D51）。
   不是不想做，是**没有历史盘口快照**。诚实边界：本轮所有滑点结论都建立在
   "当根振幅可容纳滑点"的近似上，不是真实档位穿越。
6. **B站 30% 权重未产出新内容**（2026-10-20 已永久降级，W3 结案，不再记为未完成，
   但今天确实没有新增视频蒸馏 —— 如实列在此）。
7. **`paper_trade_exchange.pyx:127-140` 的盘口污染疑点未深挖**：市价单成交被
   `record_filled_order` 写回盘口，可能让后续 VWAP 吃到自己的量。列入下一轮 P2。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：
  - `ai_quant_lab/20261024_hummingbot_vnpy/fill_price_model.py`（自测 **26/26**）
  - `ai_quant_lab/20261024_hummingbot_vnpy/slip_bounds_table.json`（4 标的标定表）
  - `quant_app/core/backtest.py`：`slip_price` / `quantize_qty` / `selftest_slip_lot_wiring`（**13/13**）
  - `lab_bridge.get("fill_price_model")` → **module，加载成功**
- [x] ③ 策略假设已追加：**H-027 已证伪** / **H-028 已验证**，证据
  `策略假设/回测结果/回测结果_20261024.json`（两条同一文件，避免互相覆盖）

### 回归（旧路径零退化）
| 自检 | 结果 |
|---|---|
| `selftest_slip_lot_wiring`（本轮新增） | **13/13** |
| `selftest_fill_realism` | **10/10** |
| `selftest_participation_wiring` | **6/6** |
| `selftest_risk_wiring` | **10/10** |
| `fill_price_model.selftest` | **26/26** |

---

## 10. 成本与技能

- **本次花费积分估算：0**（AtomCode 推理不通 → 全程本地 Read/Grep + 本地 python 计算）
- **用了哪个技能**：`ai-quant-open-source-nightly-learning`（夜学主流程 v1.1.11）
- **没用哪个技能**：`币安量化数据通路与黑马策略诊断`（本轮不下载数据、不做全市场扫描，
  本地 15m 全历史已够）；`六端空间归位`（周中不归档，周日 2026-10-25 统一走）
- **沉淀/迭代**：技能 `ai-quant-open-source-nightly-learning` v1.1.11 → **v1.1.12**（§3.14 六条）
- **归档状态**：周六（周中）→ 仅 Obsidian + 工作区日志；**六端归档 2026-10-25（周日）**
- **下一轮待跟进**：
  1. **P0** 手续费档位敏感性（换赛道，ROI 最高）
  2. **P0** H-023 分标的结论（挂账 3 轮）
  3. **P1** `core/live.py` 接 `reconcile_position()`
  4. **P1** 粒度观测的正确做法：降本金到 lot 量级再测（否则永远 qty_zeroed=0）
  5. **P2** `paper_trade_exchange.pyx:127-140` 盘口污染疑点
