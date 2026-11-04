---
标题: AI量化平台 · 撮合现实化层 · 对标 freqtrade 设计
日期: 2026-10-22
层: 撮合回测层
来源仓库: freqtrade（optimize/backtesting.py · exchange/exchange.py）
设计编号: D36 ~ D40
状态: 已回填（core/backtest.py）
tags: [AI量化平台, 平台设计, 撮合回测, 对标]
---

# 撮合现实化层 · 对标 freqtrade（D36~D40）

> **一句话**：我们回测的撮合是「信号→按收盘价全额成交→止损价精确成交」，
> freqtrade 的撮合也只有一行 `low ≤ rate ≤ high`，但它在**止损定价**与**撤单语义**上比我们诚实。
> 本轮把这三件事拆成 5 条设计，并把其中 3 条**直接回填进 `core/backtest.py`**。

## 一、现状 vs 对标（逐条对账）

| 能力 | freqtrade 的做法 | 我们改造前 | 判定 |
|---|---|---|---|
| 限价单成交判定 | `_get_order_filled`：`low ≤ rate ≤ high`（二元） | 信号即按 `close` 全额成交 | **同样二元，但 freqtrade 至少承认它** |
| 部分成交 | **不建模**（回测里 `PARTIALLY_FILLED` 永不出现） | 只在 `fill_ratio` 常数注入时出现 | 两者都缺，需自建 |
| 排队/量能约束 | **不建模** | 无 | 需自建（用 `participation`） |
| 止损成交价 | 先判「开盘是否已穿越」，是则按 `open`，再夹回 `[low, high]` | `sl_price × (1−slip)` 一刀切 | **freqtrade 更诚实** |
| 限价报价合法性 | `min(propose, high)`（买单不许高于当根 high） | 无约束 | **freqtrade 更诚实** |
| 挂单超时处置 | `check_order_cancel` 返回 True/False/None 三态 | 布尔 | **freqtrade 更诚实** |
| 滑点 | **无模型**，官方口径是「用 fee 顺带模拟」 | 固定 `slippage=0.05%` | 都属未标定 |

## 二、五条可落地设计

### D36 · 二元成交必须被显式承认为「上限」，而不是默认正确
freqtrade 不建模部分成交这件事本身就是证据：**撮合保真度不是任何框架的招牌能力，而是每个平台必须自己交代的缺口**。
- 落法：`run_backtest(..., participation=0.0)` —— `>0` 时委托量被截到 `当根 volume × participation`，产出 `PARTIALLY_FILLED`。
- 为什么更好：缺口变成**可开关的量**，才能回答「这个缺口值多少钱」。默认 0 = 旧行为逐字节一致。

### D37 · 止损成交价必须走「开盘穿越优先」，而不是止损价
`_get_close_rate_for_stoploss` 的逻辑：止损触发后先问「开盘是不是已经在 stop 之外」，是则按 `open`，最后夹回当根区间。
- 落法：`run_backtest(..., gap_stop=True)` → `gap_stop_price(open, high, low, stop)`。
- 为什么更好：`sl×(1−slip)` 等于宣称「止损永远精确成交」，等于把**尾部风险**从回测里删掉 —— 而尾部风险是唯一能打穿账户的东西。
- ⚠️ 诚实边界：本轮实测 4 只标的 6 年 **835 笔止损 / 0 笔跳空穿损**（H-024 已证伪）→ 这条设计在我们当前的 15m + 5% 参数下**价值为 0**，但它是**防空**，
  换 1m 或 2% 止损必须重测，不可外推。

### D38 · 限价报价必须夹在当根区间内
买了挂在 `high` 之上 → 实盘上它是 stop-limit，语义与行为都变了。**回测允许、实盘不支持的参数，就是回测幻觉的源头。**
- 落法：`clamp_limit_price(propose, high, low, side)`；挂单价在进引擎前先夹取。
- 为什么更好：H-022 那种「挂单价下移 0.05%」的策略，一旦挂单价落到区间外，实盘直接不成交，回测却照常算单 —— 夹取能把这类伪信号挡在门外。

### D39 · 撤单三态不能压成布尔
freqtrade `check_order_cancel` 返回 `True`（删整笔交易）/ `False`（只撤这张）/ `None`（继续挂）。
- 落法：`CancelDecision` 枚举（`DELETE_ORDER` / `CANCEL_ORDER` / `KEEP`）+ `timeout_decision(timed_out, is_entry, filled_qty)`。
- 为什么更好：入场单超时且**一笔未成** → 整笔交易作废；**已部分成交** → 只能撤剩余。压成布尔后，
  调用方必然把「撤剩余」写成「整笔作废」，账上凭空多出一段没被记录的持仓。

### D40 · 撮合约束必须自带「咬合力计数」
- 落法：`core/backtest.py` 的 `LAST_FILL_STATS`（`rejected_entries` / `partial_fills` / `gap_stop_events` / `bite` 合计）。
- 为什么更好：第 11 轮的教训是「假设没被观测到」比「假设被证伪」更危险 —— 咬合力 0 时任何收益对比都没意义。
  现在自检 `selftest_fill_realism()` 的 F1~F10 里，**F2/F3 就是先证明「咬到了」再谈结论**。
- ★ 配套判据纪律（本轮新增）：
  - **模型参数类**假设（放行率/成交率）咬合力为 0 ⇒ 判**搁置**（参数没生效，未观测）
  - **市场属性类**假设（事件发生率）数出 0 次 ⇒ 判**已证伪**（市场没发生，这就是观测结果）

## 三、回填与验收

| 项 | 落点 | 验收 |
|---|---|---|
| 三个撮合开关 | `quant_app/core/backtest.py::run_backtest(gap_stop, participation, reject_prob, reject_seed)` | `selftest_fill_realism()` **10/10**；默认全关时 `bite=0`、笔数与总收益与基线一致 |
| 纯函数族 | `gap_stop_price` / `volume_capped_qty` / `deterministic_reject` / `bar_fills_limit` | 与 `ai_quant_lab/20261022_freqtrade_vnpy/fill_realism.py` **逐点等价 diff=0**（500 组随机样本） |
| 三态撤单 + 撮合组合 | `fill_realism.py::CancelDecision / simulate_bar_fill` | 自测 **24/24**；`lab_bridge.get("fill_realism")` 装载成功 |
| 订单簿三态覆盖 | `OrderBook` 回放：`PARTIALLY_FILLED` / `UNKNOWN` / `CLOSED(REJECTED)` | 自检项 F8 |
| 台账回写器 CRLF bug | `hypothesis_runner.update_ledger` 改为按原行尾字节写回 | 两次回写 `bytes_delta=0`、`eol=CRLF` |

## 四、仍挂账
- **D41 排队位置建模**（同价位前方挂单量 → 成交概率）：freqtrade 不做，我们也没有 L2 数据，只能走概率近似。
- **D42 滑点系数实盘标定**：`slippage=0.05%` 仍是拍的（挂账第 4 轮）。freqtrade 干脆没有滑点模型 → 无人可对标，必须自建。
- **D43 部分成交的「成交价劣化」**：现在部分成交只缩量不改价；真实世界里部分成交往往伴随更差的均价。

## 五、关联
- 学习笔记：[[20261022_freqtrade_vnpy]]
- 假设：[[策略假设台账]] · H-023（补档 6 档）· **H-024（已证伪）**
- 上游设计：[[AI量化平台_成交现实化层对标hftbacktest设计_20261011]]（延迟/拒单/费用模型）· [[AI量化平台_组合回测层对标vnpy_portfoliostrategy设计_20261019]]（额度在报单唯一入口）
- 索引：[[README]]
