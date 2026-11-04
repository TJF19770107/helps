---
日期: 2026-10-28
仓库: vnpy/vnpy_ctastrategy
核心文件: cta_strategy/template.py（507）+ backtesting.py（1294）+ engine.py（986）+ base.py（62）
轮次: 第 17 轮
tags: [AI量化平台, 夜学, 代码拆解, 出场端, 停止单, 统计口径]
---

# 20261028 · vnpy/vnpy_ctastrategy · CtaTemplate / cross_stop_order / DailyResult

## 0. 一句话结论

> **vnpy 的停止单层教会我一件事：出场触发有一个「时刻」，而我方引擎一直在用「收盘」这个时刻冒充它。**
> 把触发判据从 `close<=trail` 换成「bar 内 `low<=trail_prev`」后，4 只标的净额单笔均值**全部下降**
> **0.0439 ~ 0.8277pp**（ETH 最狠 −0.83pp）—— 这是继手续费（0.1006~0.1023pp）之后
> **第二条被量化的乐观源**，且量级比手续费更大。
> 同时，我上轮笔记里「空仓 bar 压低 std → bar 频夏普虚高」的推断**被自己的实验打死**（H-036 已证伪，
> 比值只有 0.771~1.031），方向还反了：空仓 bar 是**拉低**夏普，不是抬高。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：策略层（`template.py`）+ 撮合回测层（`backtesting.py`）+ 执行层（`engine.py`），三层同一个包 ——
  这正是 vnpy 最值得学的地方：**回测与实盘共用同一份策略模板与同一套停止单语义**。
- **上下游**：
  - 上游依赖 → `vnpy.trader.constant`（Direction/Offset/Interval）、`vnpy.trader.object`
    （BarData/TickData/OrderData/TradeData）、`vnpy.trader.database`（`load_bar_data`）。
  - 下游被谁调用 → `vnpy_ctabacktester`（图形化回测 UI）、`vnpy_ctastrategy.ui.widget`（策略实例管理面板）、
    各策略 `strategies/*.py`（10 个样例策略全部继承 `CtaTemplate`）。
- **与本项目的关系**：`quant_app/core/events.py`（事件层）、`core/backtest.py`（撮合层）、
  `core/order_lifecycle.py`（7 态状态机）三块分别是这三个层的对标位。本轮只动**出场触发判据**这一处。

---

## 2. 调用链（文字版时序图）

**回测路径**（`backtesting.py`）

```
run_backtesting 219
  → strategy.on_init / on_start
  → for data in batch: new_bar 666
        ├→ cross_limit_order 688   （挂单先撮合：long 用 low，short 用 high，成交价 = min/max(order, open)）
        ├→ cross_stop_order  762   （停止单后撮合：long 用 high，short 用 low，成交价 = max/min(stop, open)）
        ├→ strategy.on_bar(bar)    ★ 策略在这一步才看到这根 bar —— 当根信号不可能当根成交
        └→ update_daily_close 656
  → strategy.on_stop
  → calculate_result 257   （成交按日归集 → DailyResult.calculate_pnl 1110 逐日盯市）
  → calculate_statistics 305（balance → return → sharpe/回撤/…）
```

**实盘路径**（`engine.py`）

```
process_tick_event 149
  → check_stop_order 223       （tick.last_price 穿越 → 立刻发**限价单**，价 = limit_up 或 ask_price_5）
  → strategy.on_tick
process_order_event 164
  → STOP_STATUS_MAP 61 映射停止单态 → strategy.on_stop_order
```

★ 两条路径的**分叉点**：回测在 `new_bar` 里用 OHLC 撮合，实盘用 tick 逐笔；
**回测的停止单成交价是 `stop` 价，实盘的停止单成交价是 `ask5/bid5` 追价** —— 见 D81。

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `CtaTemplate.__init__` | 方法 `21-44` | 绑引擎/策略名/vt_symbol，`variables` 做 `copy()` 防多实例串写 | ★ `copy(self.variables)` 是**类属性当可变默认值**的正确解法 |
| `CtaTemplate.send_order` | 方法 `233-252` | `trading=False` 时**返回空列表**而不是抛错 | 静默语义：回测未启动时下单无声消失 |
| `CtaTemplate.on_stop_order` | 回调 `143-147` | 停止单状态变化回调（默认空实现） | 策略可据此重挂/放弃 |
| `TargetPosTemplate.send_new_order` | 方法 `455-507` | 按 `target_pos - pos` 差额发单；**回测用开仓、实盘先平后开** | ★ 同一函数两套语义（`EngineType` 分支） |
| `StopOrder` | dataclass `base.py:35-49` | 本地停止单：三态 WAITING/CANCELLED/TRIGGERED | **没有 REJECTED**，见 D80 |
| `BacktestingEngine.new_bar` | 方法 `666-675` | 撮合旧单 → 回调策略 → 更新日收盘 | ★ 顺序本身就是防未来函数的机制 |
| `cross_limit_order` | 方法 `688-760` | long 用 `bar.low` 判穿越，成交价 `min(order, open)` | 二元全成，无部分成交 |
| `cross_stop_order` | 方法 `762-849` | long 用 `bar.high` 判穿越，成交价 `max(stop, open)` | ★ **跳空按 open** —— 我方 D37 同构 |
| `DailyResult.calculate_pnl` | 方法 `1110-1154` | 逐日盯市：`holding_pnl` + `trading_pnl − commission − slippage` | 首日 `pre_close=1` 兜底 = 坑（D76） |
| `calculate_statistics` | 方法 `305-538` | balance → return → sharpe/回撤/卡玛/EWM/GRR | 三套口径混用（D77） |
| `CtaEngine.check_stop_order` | 方法 `223-285` | 实盘本地停止单：tick 触发 → 发限价单到 `ask5/bid5` | ★ 出场滑点口径缺口（D81） |
| `STOP_STATUS_MAP` | 常量 `61-67` | 交易所委托态 → 停止单态 | ★ REJECTED→CANCELLED（D80） |

---

## 4. 可迁移设计点（9 条，逐条写「为什么好/为什么是坑」）

### D73 ★ 停止单触发必须**显式排序**，不能靠容器遍历序
`backtesting.py:778` 是 `for stop_order in list(self.active_stop_orders.values())` —— 遍历序 = **dict 插入序**
= 「谁先挂谁先触发」。而同一根 bar 里两张止损单可能同时被穿越，**谁先成交决定这笔是赚是亏**。
插入序是一个**没人声明过、且会随重构静默改变**的假设。
→ 落地：`StopOrderBook` 用「价格走到触发价的**进度比例** `(open−price)/(open−low)`」排序，
只看 bar 的 OHLC 与挂单价，**与插入顺序完全无关**。自测里配了 A/B 反测：`order_policy="insertion"`
时打乱挂单顺序**必须**改变成交顺序，否则「顺序不变」这条断言是恒真的假绿。

### D74 ★★ 先撮合旧单、后回调策略 —— 顺序本身就是防未来函数
`new_bar` 是 `cross_limit_order → cross_stop_order → strategy.on_bar`。
策略在 `on_bar` 里发的单，**当根 bar 不会被撮合**（下一根才进 `active_*` 名单遍历）。
→ 我方 `core/backtest.py` 用「信号在 `i` 收盘产生、`entry_on="next_open"` 在 `i+1` 开盘成交」实现同一效果，
且更显式。**这条是对标确认，不是缺口**。
→ 但反过来暴露一件事：我方「止盈回撤」用 `close[i] <= trail` 判、又用 `close[i]` 成交 ——
**判定与成交在同一时刻**，看起来自洽，其实是**把 bar 内路径压成了一个点**（D75/H-035 的根）。

### D75 跳空穿越按开盘价 —— vnpy 这一处是对的，与我方 D37 交叉验证通过
`backtesting.py:813-818`：多头停止单 `trade_price = max(stop, open)`；空头 `min(stop, open)`。
→ 我方 `gap_stop_price(..., is_short=False)` 给 `min(stop, open)`，**语义等价但参数名相反**：
vnpy 的 `direction` 是**报单方向**，我方的 `is_short` 是**持仓方向**。
→ 本轮在 lab 模块里加了 `漂移守卫` 断言：两套实现在 4 组手算样例上必须给出同一答案，
且**显式写了语义映射**（`is_short=False ↔ order_side="short"`）。同名反义是缝合时最经典的事故源。

### D76 ★ 兜底值必须量纲正确 —— `pre_close=1` 是反例
`backtesting.py:1121-1124`：首日 `pre_close` 为 0 时用 `1` 兜底「避免除零」。
于是 `holding_pnl = start_pos × (close − 1) × size` —— 若首日已有持仓、标的价格 6 万，
这一项直接爆出**六万倍级别的假盈亏**。
→ 正确做法：用**首日 close**（当日无隔夜仓时 `holding_pnl ≡ 0`）。
→ 自测里把这条量化了：手算样例 `1×(110−1)×1 = 109` vs 正确值 `0`。
→ 普适规则：**「避免除零」不能随手填 1/0.5/eps，兜底值必须与被兜底量同量纲。**

### D77 ★★ 一个函数里三套收益口径 + 两个年化因子（vnpy 自己的口径污染）
`calculate_statistics` 内同时存在：
- `total_return = end/capital − 1` → **简单收益**
- `annual_return = total_return / total_days × annual_days` → **线性年化**（`409-410`）
- `daily_return = df["return"].mean()`，其中 `return = log(balance/pre_balance)` → **log 收益**（`360-362, 411`）
- `sharpe = (daily_return − rf/√annual_days)/std × √annual_days` → 用 log 收益算（`415-416`）
- `annual_downside_risk = downside_std × √252` → **换成 252**（`443`）

⇒ 同一个统计表里 简单/log 两种收益 + 240/252 两个年化因子。`√252/√240 − 1 = 2.4721%`（自测断言过）。
→ 我方 `compute_performance` 用的是「简单收益 + 复利 CAGR + bar 频」，**比 vnpy 自洽**，
  但同样必须**一句话说清每个数字的定义**。→ 落地 `return_bases()`，把四种口径摊在同一张表上。

### D78 ★★ 爆仓日 `fillna(0)` = 时间维度的幸存者偏差
`backtesting.py:358-362`：
```python
x = df["balance"] / pre_balance
x[x <= 0] = np.nan
df["return"] = np.log(x).fillna(0)
```
权益跌破 0 的那天，收益被**替换成 0**，等于「那天什么都没发生」。
最极端的亏损日被从收益序列里静默删掉 ⇒ 波动率低估、夏普虚高。
→ 与 D65 / H-032「单笔均值是幸存者偏差放大器」**同源**，只是发生在**时间维度**上而不是交易维度上。
→ 落地 `settle_daily(blown_basis="fixed")`：爆仓日记 `−1.0`（−100%）并计入 `blown_days`；
  `blown_basis="vnpy"` 保留原行为供 A/B。自测断言两口径在该日**必须不同**（差 1.0）。

### D79 ★ 吞异常并静默 return ⇒ 半程回测被当完整回测
`run_backtesting 243-248`：`except Exception: output("触发异常，回测终止"); return`
—— **不 raise**。调用方拿到的是**跑了一半的 `daily_results`**，`calculate_statistics` 照常出数。
→ 这正是我方「执行失败 ≠ 结论」铁律的对标位。我方已有 `manifest_min` 的 `scope` 字段
（`full` / `reuse` / `first-run`）来标注「这次结果覆盖了多少范围」，比 vnpy 强；
但 **`core/backtest.py` 自身仍是 try/except 吞异常**（`risk.on_equity` 那段 `pass`），
一旦风控喂数失败会静默降级 —— 记为 P2 跟进（见 §8）。

### D80 把 REJECTED 并进 CANCELLED ⇒ 拒单与撤单不可区分
`engine.py:61-67` `STOP_STATUS_MAP`：`Status.REJECTED → StopOrderStatus.CANCELLED`。
而四种真实场景的运维动作完全相反：撤单（该重挂）/ 拒单-资金不足（**不能重挂**，会连拒）/
拒单-价格越界（改价再挂）/ 拒单-合约不可交易（告警下线）。
合并成同一终态 = 放弃分诊能力。
→ 我方 `core/risk.py` G2（2026-10-20 落地，**24/24**）已经是四态分开的 ⇒ **这一条是对标确认「我们已反超」**。
→ 落地 `stop_order_terminal_map(merge_rejected=False/True)` 做 A/B：两版**只在 REJECTED 上不同**，
  `ALLTRADED` 必须相同（否则说明我改多了）。

### D81 ★★★ 实盘停止单触发后按 `ask5/bid5` 追价 —— 回测用 `stop` 价 = 出场滑点口径缺口
`engine.py:240-252`：
```python
# To get excuted immediately after stop order is triggered,
# use limit price if available, otherwise use ask_price_5 or bid_price_5
if stop_order.direction == Direction.LONG:
    price = tick.limit_up or tick.ask_price_5
else:
    price = tick.limit_down or tick.bid_price_5
```
⇒ 实盘为了让停止单「触发即成交」，把限价直接挂到**对手五档**。
回测里同一次触发成交在 `stop` 价（最多再吃 0.05% 滑点）。
对高频剥头皮（实盘 4543 笔）这个差额会逐笔累积 ⇒ **给「实盘 4543 笔 vs 回测 129 笔」的差异
增加了一个新候选解释（出场端追价成本），与既有四候选（标的池/时段/记账口径/未来函数）并列**。
→ 但按纪律：**「成本变大导致收益变差」方向注定，不能当结论**，只能当**量级估计**。
  P0 跟进项已登记（§8）。

---

## 5. 可复用代码片段

本轮落地模块：`ai_quant_lab/20261028_vnpy_vnpy_ctastrategy/vnpy_cta_exit_patterns.py`
（**44/44 自测通过**，`lab_bridge.get("vnpy_cta_exit_patterns")` 零警告）

六件套：`StopOrderStatus`（四态）/ `StopOrderBook`（确定性触发排序）/ `stop_order_terminal_map`
（拒单撤单分离）/ `settle_daily`（逐日盯市 + 爆仓日修正）/ `sharpe_basis`（三口径）/
`return_bases`（四口径）。节选核心 30 行：

```python
# 来源：vnpy/vnpy_ctastrategy/vnpy_ctastrategy/backtesting.py:762-850（cross_stop_order）
#       + base.py:35-49（StopOrder）+ engine.py:61-67（STOP_STATUS_MAP 反例）
# 用途：让「同根 bar 内多张停止单谁先成交」变成**可声明、可复现**的规则，
#       而不是依赖 dict 插入序这个没人声明过的隐含假设。
def cross(self, i, open_px, high, low):
    o_px, hi, lo = float(open_px), float(high), float(low)
    hit = []
    for oid, so in self._active.items():
        sell_side = (so.direction == "short")      # 多头持仓的止损 = 卖出方向
        if sell_side:
            trig = (lo - 1e-12) <= so.price
            # 「走到该价」的进度比例 ∈[0,1]：越小表示越早被扫到
            prog = (o_px - so.price) / max(o_px - lo, 1e-12) if o_px > so.price else 0.0
        else:
            trig = (hi + 1e-12) >= so.price
            prog = (so.price - o_px) / max(hi - o_px, 1e-12) if so.price > o_px else 0.0
        if not trig:
            continue
        hit.append((max(0.0, min(1.0, prog)), oid, so))
    # 排序键只依赖 OHLC 与挂单价 → 与插入顺序无关 → 可复现
    hit.sort(key=lambda t: (t[0], t[1]))
    ...
```

★ 自测纪律：**每条「正测」都配一条「反测」**（改输入必须改输出）。
本轮反测抓到 4 个真 bug：① `gap_fill_price` 方向算反（卖出止损跳空时被夹到 high）；
② 断言比 `stop_orderid` 而非价格 → 假失败；③ 爆仓样例仓位太小（−500 才真爆，10 手只到 500）；
④ `cagr` 在 3 根 bar 上 overflow（数学事实，应给 `None` 而非 `inf`）。

---

## 6. B站学习（本日 30% 权重）

- **状态**：**永久降级为「标题 + 目录级」笔记，不再记入「未完成」区**（第 10 轮已结案 W3）。
- 原因：该课程组字幕接口恒返回空（多次实测），按零成本底线**不做音频转录**。
- 本日耗时为 0，权重让渡给代码精读与假设回测。**如实记录，不假装做了。**

---

## 7. 对黑马策略的启发（全部落到具体动作）

### 7.1 H-035 出场触发口径 —— **已验证 4/4**

可回测动词句：15m 周期、3 档追踪止盈(10/8/5)、5% 硬止损、`entry_on=close`，
把追踪止盈触发判据由 `close <= trail` 改为 `low <= trail_prev`（`trail_prev` 用**前一根**已知峰值算），
4 只标的净额单笔均值的相对变化。

| 标的 | 笔数 | 净单笔%（baseline→intrabar） | Δpp | 总收益% | 最大回撤% | `intrabar_exits` |
|---|---|---|---|---|---|---|
| BTCUSDT | 129→125 | 2.1521→2.1082 | **−0.0439** | 321.7→331.3 | 78.1→80.2 | 28 |
| ETHUSDT | 211→235 | 2.1683→1.3406 | **−0.8277** | 863.2→210.1 | 77.0→73.8 | 47 |
| BNBUSDT | 203→216 | 2.1128→1.7399 | **−0.3729** | 708.5→537.6 | 79.7→76.1 | 47 |
| DOGEUSDT | 472→498 | 0.4726→0.0512 | **−0.4214** | −79.8→−94.0 | 99.5→99.6 | 85 |

**结论（只讲量级，不讲优劣 —— 方向注定）**：
- 旧口径（收盘判定 + 收盘成交）**系统性高估** 净单笔 **0.0439 ~ 0.8277pp**。
- 咬合力 `intrabar_exits` = 28/47/47/85，占入场笔数 18.0%~23.2%，**不是「没咬到」**。
- ★ 与第 14 轮「乐观偏差收口到手续费一项（0.2041pp）」的关系：
  **不是推翻，是补充了一条被漏掉的维度** —— 那五条（成交价/容量/排队/止损穿价/手续费）全在
  「**已知触发时刻之后**」的定价上，从未问过「**触发时刻本身**对不对」。
  修正后的完整口径：**手续费 0.1006~0.1023pp（第 16 轮修正后）+ 出场触发口径 0.0439~0.8277pp**。
- ★ 又一次印证 H-032：BTC 净单笔 **下降** 0.0439pp 而总收益 **上升** 9.6pp —— **单笔均值与总收益可反向**。
  A/B 表必须四列齐（笔数/净单笔/总收益/最大回撤），缺列即未完成。

### 7.2 H-036 统计频度口径 —— **已证伪（且证伪得有价值：自我纠错）**

| 标的 | bar 夏普 | 日 夏普 | bar/day | 空仓 bar 占比 | 零收益 bar 占比 | 持仓期夏普 | 回撤 bar→日 | bar 数 |
|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 0.6652 | 0.6628 | **1.004** | 4.08% | 4.15% | 0.7309 | 78.11→77.91 | 238,737 |
| ETHUSDT | 0.8382 | 0.8362 | **1.002** | 6.77% | 6.95% | 0.9377 | 77.01→76.74 | 237,417 |
| BNBUSDT | 0.8083 | 0.7841 | **1.031** | 5.95% | 6.49% | 0.9013 | 79.75→77.28 | 234,870 |
| DOGEUSDT | 0.2051 | 0.2662 | **0.771** | 12.91% | 14.46% | 0.3278 | 99.46→99.32 | 215,726 |

**被证伪的两条机制猜测（都是我自己的推断，必须自己改口）**：
1. ❌ 「空仓 bar 占比 ≥50%」—— 实测只有 **4.08%~12.91%**。
   因为 129 笔 × 均持仓 ~1777 根 ≈ 覆盖 96% 的 bar：**黑马策略几乎全程在仓**。
2. ❌ 「空仓 bar 收益恒 0 → 压缩 std → 夏普虚高」—— **方向反了**。
   零收益 bar 会同时压低均值与标准差，实测结果是**拉低**夏普：
   持仓期夏普（0.7309/0.9377/0.9013/0.3278）**高于** bar 频夏普。
   ⇒ 我方 bar 频夏普是**保守的（低估 ~9.9%）**，不是虚高。

**留下来的真结论**：
- bar 频与日频年化夏普**基本等价**（比值 0.771~1.031）⇒ **第 9~16 轮所有引用 sharpe 的结论口径是稳的，不需要回溯降级。**
- 日频最大回撤比 bar 频**低 0.14~2.47pp**（BNB 最明显 79.75→77.28）⇒ 若改用日频结算，**回撤会被轻微低估**。
  结论：**继续用 bar 频**（更保守），但报告里要标 `basis=bar`。
- 后续纪律：**不许再用「bar 频夏普虚高」当理由质疑历史结论** —— 这条已被数据打掉。

### 7.3 H-023 分标的结论（挂账 5 轮，本轮结清）

训练段（前 70%）8 档 `tp_tiers` 净额单笔均值：

| 标的 | 8/6/4 | 10/8/5(基线) | 15/12/8 | 20/15/10 | 25/20/12 | 30/25/15 | 40/32/20 |
|---|---|---|---|---|---|---|---|
| BTCUSDT | 1.2358 | 1.8270 | 2.8438 | 4.2079 | 6.8157 | 9.7087 | **17.9424** |
| ETHUSDT | 1.3719 | 1.8752 | 3.5710 | 4.5401 | 6.1410 | 8.7205 | **13.4416** |
| BNBUSDT | 1.3812 | 2.0550 | 3.6290 | 5.2807 | 6.4507 | 11.8206 | **16.5954** |
| DOGEUSDT | 0.1967 | 0.6691 | 2.2662 | 2.5836 | 3.2346 | 5.2195 | **10.1555** |

样本外（后 30%）基线档 → 训练最优档：

| 标的 | 基线 10/8/5 | 最优档 40/32/20 | Δ | 判定 |
|---|---|---|---|---|
| BTCUSDT | 1.0817 | 14.3914 | **+13.3097** | 通过 |
| ETHUSDT | 0.8263 | 2.5311 | **+1.7048** | 通过 |
| BNBUSDT | 0.8147 | 0.8343 | **+0.0196** | 勉强通过（几乎无差异） |
| DOGEUSDT | −0.9418 | −1.9930 | **−1.0512** | **恶化** |

**分标的结论（这就是挂账 5 轮要的答案）**：
- **4/4 训练段 8 档单调递增，最优档第 4 次落在网格端点** ⇒ `tp_tiers` 这族参数**在网格内不收敛**，
  「存在内部最优档」这个说法**在本网格上不成立**，必须停止在此网格上继续外推
  （从 20/15/10 → 25/20/12 → 30/25/15 → 40/32/20 已外推 3 次，每次端点都外移）。
- **BTC / ETH**：放宽到 `40/32/20` 样本外大幅改善（+13.31 / +1.70）⇒ **可以放宽**。
- **BNB**：样本外几乎无差异（+0.0196）⇒ **放宽无害但也无用**，按「不做无收益改动」原则**维持基线**。
- **DOGE**：放宽后样本外**恶化 −1.0512** ⇒ **不许放宽，回基线 10/8/5**（与第 16 轮「降费对 DOGE 无效」同向：
  DOGE 的问题不在任何单一参数上）。
- ★ 与 H-020（`let_run` 0/4 全翻负）不矛盾也不一致：`let_run` 换的是**离场机制**（跌破 MA30），
  不是同一族参数的极限。**「参数族内的极限」≠「换一种机制」** —— 这条以后别再混着说。

### 7.4 怎么验 / 若成立改哪

| 假设 | 验证器 | 平台改动 | 状态 |
|---|---|---|---|
| H-035 | `hypothesis_runner.verify_H035` | `core/backtest.py` 新开关 `exit_trigger="intrabar"`（默认 `"close"` 零退化） | 已验证 4/4 |
| H-036 | `verify_H036` | 无（纯统计口径，只要求报告标 `basis`） | 已证伪 |
| H-023 | `verify_H023`（补分标的结论入笔记） | 无（参数选择属研究结论，不硬编码进引擎） | 已验证 3/4 |

---

## 8. 未完成 / 失败区（诚实留痕）

1. **AtomCode 13460 推理通道：连续第 7 轮失败**（10-21/22/23/24/26/27/28）。
   本轮 `proxy_down` → 后台拉起 → `/health` 200 + `logged_in=true` + 3 个免费模型，
   但最小推理 **240s 超时 HTTP=0** ⇒ 上游推理层挂死（**非额度、非二进制**，`--version` 第 13 轮已验）。
   → 全程降级本地 Read/Grep，**0 积分**。按收敛纪律（第 3 轮起）不再在此耗时间。
2. **B 站（30% 权重）今日实质产出 0** —— 第 10 轮已结案降级为标题级，本条不计入失败，但**如实记录**。
3. **【P1 新发现】`write_results` 按日单文件、后跑覆盖前跑** ⇒ 分次运行会互相抹掉证据。
   本轮实测：先跑 `H-035,H-036` 再跑 `H-023`，`回测结果_20261028.json` 里的 H-035/H-036 明细被 H-023 覆盖。
   → 临时解法：三条合成一次跑（`--only H-023,H-035,H-036`，2m54s）。
   → 根治：文件名加 `run_id` 或改为 append；**下一轮 P1 修**。
4. **【P2】`core/backtest.py` 风控喂数仍 try/except `pass`**（`risk.on_equity` 那段）
   ⇒ 风控喂数失败会静默降级（D79 同类）。本轮未动，记为 P2。
5. **H-035 未做参数交互**：只测了默认档 `10/8/5`。`intrabar` 与更宽档位（如 `40/32/20`）的交互未测，
   `40/32/20 + intrabar` 可能把「放宽」的收益吃掉一部分 —— **这是下一轮最高优先级**。
6. **D81（实盘 ask5/bid5 追价）只到「量级估计」层面，未做回测量化**：
   需要 tick 级盘口数据才能标定 ask5 相对 last 的真实偏离，当前数据只有 15m OHLC，
   **做不出来就是做不出来**，不许用 15m 数据硬凑。
7. **`_position_from_trades` 用 `entry_idx + holding_bars` 还原持仓**，
   对「出场当根即再入场」的情形会少算 1 根 —— 对空仓占比影响 <0.1pp，**未修，登记备查**。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：
  - `ai_quant_lab/20261028_vnpy_vnpy_ctastrategy/vnpy_cta_exit_patterns.py`（**44/44** 自测，lab_bridge 零警告）
  - 平台侧改动：`quant_app/core/backtest.py` 新增 `exit_trigger`（默认 `"close"` 零退化，+3347 bytes）
  - 回归：risk **24/24** · events ok · router **8/8** · lifecycle **10/10** · fill_realism **10/10**
    · slip_lot **13/13** · participation **6/6** · risk_wiring **10/10**（全绿）
- [x] ③ 策略假设已追加进 [[策略假设台账]]：H-035（已验证）/ H-036（已证伪），台账回读确认 36 条全部有状态

---

## 10. 成本与技能

- **花费积分**：**0**（AtomCode 推理不可用 → 全程本地 Read/Grep/回测，无任何外部 API）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程 v1.1.14）
- **没用哪些技能**：`云端四端归档通道`（今日周三=周中，按第九步只落 Obsidian + 日志）；
  `番茄小说写作与发布` / `拼豆图纸变现物料包`（与主题无关）
- **沉淀 / 迭代**：
  - 新模块 `vnpy_cta_exit_patterns.py`（6 件套 + 44 条断言 + 4 条 A/B 反测）
  - 引擎新开关 `exit_trigger`（第 6 个撮合类开关，同样默认关闭零退化）
  - 技能 `ai-quant-open-source-nightly-learning` v1.1.14 → **v1.1.15**（§3.17 见技能文件）
- **六端归档**：今日周三（周中）→ 仅 Obsidian + `.workbuddy/memory/2026-10-28.md`；
  **周日（2026-11-01）补六端，含 10-18 / 10-25 两轮顺延**
