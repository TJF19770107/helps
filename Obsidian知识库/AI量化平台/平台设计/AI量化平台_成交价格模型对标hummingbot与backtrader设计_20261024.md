---
标题: AI量化平台 · 成交价格模型 · 对标 hummingbot / backtrader 设计
日期: 2026-10-24
层: 撮合回测层（成交价格与数量粒度）
来源仓库: hummingbot（`connector/exchange/paper_trade/paper_trade_exchange.pyx` 1139 行 · `core/data_type/order_book.pyx` 483 行 · `connector/budget_checker.py` 161 行）／ backtrader（`brokers/bbroker.py:994-1036`）
设计编号: D51 ~ D59
状态: 已回填（`core/backtest.py` 新增 `slip_price` / `quantize_qty` / `clamp_slip` / `lot_size` + `selftest_slip_lot_wiring` 13/13）
tags: [AI量化平台, 平台设计, 撮合回测, 滑点, 手续费归因, 对标]
---

# 成交价格模型 · 对标 hummingbot / backtrader（D51~D59）

> **一句话**：前 13 轮把「成交率」「队列位置」「容量」都修到不咬了，只剩**滑点系数**
> 这一个没标定的乐观源。本轮把它标定掉了，结果是**好消息也是坏消息** ——
> 滑点夹断的真实影响只有 **+0.0014~+0.0038pp/笔**，而手续费是 **0.2041pp/笔**。
> ⇒ **乐观偏差 98% 的账都在手续费档位上，不在撮合模型里。**
> 这条结论的价值是：它把「继续修回测」这条路**正式关掉**了，资源必须转到「真实成本」。

## 一、现状 vs 对标（逐条对账）

| 能力 | 对标做法 | 我们改造前（第 13 轮末） | 判定 |
|---|---|---|---|
| 成交价来源 | hummingbot `simulate_buy` 逐档吃量算 VWAP（`:454-460`） | `close × (1±slip)`，与深度无关 | 降级为 P2（无历史盘口快照） |
| 滑点区间约束 | backtrader 越界则 `return pmax`（`:1007-1015`） | **无任何约束**，可产出比 high 更高的买价 | **真缺口，本轮已修** |
| 数量粒度 | hummingbot `(amount//quantum)*quantum` + `<1e-7→0`（`:1078-1086`） | 连续浮点，无归零 | **真缺口，本轮已修** |
| 延迟 | hummingbot `TRADE_EXECUTION_DELAY=5.0s`（`:144`） | `close` / `next_open` 两档 | 已够（15m 一根 900s） |
| 限价成交通道 | hummingbot A(trade 打穿) OR B(最优价穿越) | `bar_fills_limit`（当根区间） | 等价于 B，缺 A |
| 资金不足终态 | 限价→Cancel（`:680`）／市价→Failure（`:485`） | `risk.py` 预占 + `order_lifecycle` 7 态 | 我们更严（前置而非事后） |
| 手续费位置 | `BudgetChecker` 费进抵押品（`:473-484`） | `R7` 顺序锁定 | 已对齐 |
| 深度不足 | **被算法吃掉**（`order_book.pyx:286-294` 用最后一档价硬吃） | — | **学它 + 反它**：我们显式返回 `depth_short` |

## 二、九条可落地设计

### D51 · 成交价应来自簿级 VWAP，不是「收盘价 + 常数」
滑点的物理成因是「吃掉薄档」，所以它必然随下单量与深度变化。
**但当前不该做**：H-026 已证 15m 下 V/Q 中位 BTC 12155×，我们的单子小到看不见档位差异。
⇒ 降级 P2，等有盘口快照数据再说。**知道该做但知道现在不该做，同样是一条设计。**

### D52 · 延迟必须是参数，不是 0
hummingbot 的 5s 延迟意味着「下单与成交之间一定隔一个时间窗，窗内价格会变」。
延迟成本 ∝ 波动率 → **高波动时段延迟最贵**。
我们已有 `entry_on ∈ {close, next_open}`（0 延迟 / 1 根延迟），方向正确。

### D53 · 限价成交是双通道 OR
A = 真实 `TradeEvent` 打穿我的价（`:895-939`，maker 方向要**取反**：`trade.type is SELL` ⇒ maker 是买）；
B = 对手盘最优价穿越我的价（`:836-892`）。任一即成交。
- 为什么 OR 是合理的：做市策略本来就假设自己在队列前排。
- 为什么对我们不构成问题：H-026 已证排队不紧。

### D54 · 同一个「资金不足」，限价 Cancel、市价 Failure
`:680` vs `:485`。限价单本就在挂，撤掉是正常生命周期；市价单资金不够是**失败**，须重试/降量。
⇒ 直接对应 `core/order_lifecycle.py` 的 `CANCELLED`（不可重试）与 `REJECTED`（可重试）**必须分开**。

### D55 · 量化在报单前完成，不足一个最小单位就归零
`(amount // quantum) * quantum` + `< 1e-7 → 0`。不归零会出现「下单 0 却记一笔成交」的**幽灵成交**，
实盘直接拒单 ⇒ **回测比实盘乐观的结构性来源**。
落法：`core/backtest.py:quantize_qty()` + `run_backtest(lot_size=...)`。

### D56 · 手续费参与「能不能下单」判定（费进抵押品）
`populate_collateral_entries` 让「买得起」= **含费买得起**。差一整笔的位置，满仓策略会系统性超配。
这是我们 `risk.py R7` 的同一条纪律的第二次独立实现证据。

### D57 · ★ 反例：hummingbot 的 VWAP 分母用请求量，把「深度不足」吃掉了
`:460` 分母是 `amount`（请求量）。深度不够时 `simulate_buy` 用最后一档价硬吃剩余量
⇒ VWAP 被拉向最后一档，且**没有任何标志位**告诉你「这单没吃完」。
我们的修法：`vwap_from_levels()` 分母用 `Σ entry.amount` + 返回 `depth_short: bool`。
**宁可报「只吃到 60%」，不报一个假均价。**

### D58 · ★★ 滑点必须被当根 `[low, high]` 夹断
`_slip_up(pmax=phigh, ...)`：超过当根 high 就返回 high（`slip_match=True` 默认）。
- 这不是「放宽优化」，是**物理修正**：当根最高只到 high，你不可能买在它之上。
- 实证越界占比：BTC **22.43%** / ETH **15.94%** / BNB **20.39%** / DOGE **12.63%**。
- 但成本影响只有 **+0.0014~+0.0038pp/笔** —— 越界量通常只差一点点。
- **方法论**：夹断让成本只降不升 ⇒ 「Δ>0」**注定成立，不构成证据**；
  证据只能是 `slip_clamped` 非零。已写进 `bite_v2`。

### D59 · `slip_out=False`：宁可不成交，也不给不存在的价
`_slip_up` 末尾 `return None`（`:1015`）⇒ 该 order 本轮**不执行**，继续挂着等。
**「没成交」是合法结果，不是异常。** 我们的 `gap_stop + clamp_slip` 组合已能表达主路径；
「部分成交后剩余继续挂」没做（回测不排队，剩余直接撤），列 P2 —— 理由同样是 H-026 已证排队不咬。

## 三、已回填清单

| 落点 | 内容 | 验收 |
|---|---|---|
| `quant_app/core/backtest.py:slip_price()` | 滑点价夹回当根 `[low, high]`，关开关等价旧公式 | `selftest_slip_lot_wiring` S1~S4 |
| `quant_app/core/backtest.py:quantize_qty()` | 按 lot_size 向下取整 + 不足一 lot 归零 | S5~S7 |
| `run_backtest(clamp_slip=, lot_size=)` | 两开关默认关 = **逐点零退化** | R1 权益 `allclose(atol=0)` |
| `LAST_FILL_STATS['bite_v2']` | 新咬合计数（旧 `bite` 口径不动） | R3 / R3b |
| `ai_quant_lab/20261024_hummingbot_vnpy/fill_price_model.py` | 夹断 + 量化 + 簿级 VWAP（修正版）+ 标定 | 自测 **26/26** |
| `…/slip_bounds_table.json` | 4 标的 × 6 分位半振幅 + 越界占比 | T1~T4 |

## 四、结论：撮合模型这条线到此为止

| 成本项 | 实测乐观量（每笔） | 来源 |
|---|---|---|
| 成交价模型（滑点夹断，含越界修正） | **+0.0014 ~ +0.0038pp** | H-028（本轮） |
| 成交量/容量约束 | ≈ 0（Δ 全 +0.0000pp） | H-025（第 13 轮） |
| 排队位置 | 不紧（V/Q 中位 12155×） | H-026（第 13 轮） |
| 止损成交价（跳空穿损） | 0 次 / 835 笔止损 | H-024（第 12 轮） |
| **手续费（双边 0.1% taker）** | **0.2041pp** | 第 9 轮口径纠偏 |

⇒ **换赛道**：从「让回测更真实」转到「让真实成本更低」（maker 挂单 / BNB 抵扣 / VIP 阶梯 / 返佣）。
⚠️ 但不许把「费率降到 0.02% 后收益很好」当结论 —— 那是**执行能力问题**，不是回测参数问题。

---

*建立：2026-10-24 · 汤小龙 · 第 14 轮夜学 · 详细拆解见 [[20261024_hummingbot_vnpy]]*
