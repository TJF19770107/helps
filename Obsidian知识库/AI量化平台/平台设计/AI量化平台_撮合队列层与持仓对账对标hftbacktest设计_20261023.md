---
标题: AI量化平台 · 撮合队列层 + 持仓对账 · 对标 hftbacktest / nautilus_trader 设计
日期: 2026-10-23
层: 撮合回测层（队列位置）· 执行层（持仓对账）
来源仓库: hftbacktest（`backtest/models/queue.rs` 1366 行 · `backtest/proc/nopartialfillexchange.rs` 649 行）／ nautilus_trader（`crates/execution/src/reconciliation/positions.rs` 1038 行）
设计编号: D41 ~ D50
状态: 部分已回填（`core/backtest.py` 参与率标定 · `core/order_lifecycle.py` 持仓三态对账）
tags: [AI量化平台, 平台设计, 撮合回测, 队列位置, 持仓对账, 对标]
---

# 撮合队列层 + 持仓对账 · 对标 hftbacktest / nautilus（D41~D50）

> **一句话**：前 12 轮我们把「价格怎么成交」修到差不多了（跳空、部分成交开关、拒单），
> 但**成交判据**一直停在「价格触及即成交」—— 这等于假设自己**永远排在队列最前面**。
> 本轮把 hftbacktest 的队列位置模型搬进来，并顺带补齐 nautilus 的**持仓**对账（我们只有订单对账）。
> 结果出乎意料地干脆：**两条假设双双判「不咬」** —— 容量不咬、排队不咬。
> 这意味着继续在"成交现实度"上加码的边际收益已接近 0，**唯一还没动的乐观源是滑点系数**。

## 一、现状 vs 对标（逐条对账）

| 能力 | hftbacktest / nautilus 的做法 | 我们改造前 | 判定 |
|---|---|---|---|
| 限价单成交判据 | 价格穿越→成交；同价→**必须队列前方量被吃完**（`queue.rs:114-137`） | `bar_fills_limit`：`low ≤ rate ≤ high` | **我们最乐观：等于永远排第一** |
| 队列前进 | `trade`/`depth` 双通道 + `cum_trade_qty` **去重** | 无队列概念 | 需自建（本轮已建） |
| 数量减少 | 直接 `min(front, new_qty)` 夹断，**不做概率分摊** | — | 需自建 |
| 部分成交粒度 | 按 `lot_size` 取整（`L209`） | 连续浮点（`volume_capped_qty`） | 我们天生乐观一点点 |
| 容量约束 | 文档**自己承认不建模**，并警告大单会失真 | `participation` 开关，但值是 **1e-7 演示值** | **假开关**（本轮已换成标定值） |
| 持仓对账 | 三态 + 容差绑 `size_precision`（`positions.rs:431-466`） | 只有订单对账；容差魔法数 `1e-9` | **缺半层**（本轮已补工具） |
| 生命周期切分 | 按「归零」切，翻转不算边界 | 无 | 本轮已建 |
| 合成价 | 只封上侧 + 按价格精度向下取整 | 无 | 本轮已建 |

## 二、十条可落地设计

### D41 · 成交判据是「队列位置」而不是「价格触及」
价格触及只说明「这个价位有成交」，不说明「其中有我的份」。限价挂单必须走
`front_q_qty < 0` 才判成交。落法：`queue_position_model.RiskAdverseQueueModel / ProbQueueModel`。

### D42 · `trade` 与 `depth` 两条通道必须去重
同一笔成交会**两次**到达撮合器（trade 事件 + depth 减少）。不去重就前进两次 →
**成交量算两遍** → 成交系统性高估。落法：`QueuePos.cum_trade_qty`（`queue.rs:182-188`）。
这条靠肉眼审不出来，只能靠测试（B1 用例）。

### D43 · 数量减少直接夹断，不做概率分摊
减少可能来自"我后面的人撤了"。概率分摊是**最乐观**的解释。落法：`depth()` 里 `chg<0` 分支。

### D44 · 部分成交按 `lot_size` 取整
交易所最小成交单位是步长，「差 0.4 个步长」永不成交。落法：`lot_size_round()` + `is_filled(lot_size)`。
**待回填**：`core/backtest.py` 的 `volume_capped_qty` 仍是连续量（下一步）。

### D45 · 队列概率没有唯一解，只能标定
`queue.rs` 里 5 种概率函数、2 套分母并存 —— 作者自己没选出一个"正确的"。
落法：把概率族做成参数（`power_prob(n)` / `log_prob()`），**结论必须附标定数据与区间**。

### D46 · taker 单不受队列约束 → 容量必须单独建模
`nopartialfillexistence.rs:58-62` 文档原文承认：大额 taker 会给出不现实成交。
落法：`participation_calibration.py` + `core/backtest.py:participation_for(symbol)`。

### D47 · 对账容差必须绑 `size_precision`，`precision=0` 零容差
魔法数 `1e-9` 在 BTC（步长 0.001）上等于要求绝对精确 → 假告警刷屏；在整数张合约上又"碰巧对"。
落法：`order_lifecycle.tolerance_for_precision()`（**已回填**，自测 10/10）。

### D48 · 生命周期按「归零」切，不按「翻转」切
翻转当边界会把一条持仓劈两半，让"缺的开仓"与"多的平仓"**自我抵消**，bug 永远测不出。
落法：`position_reconciliation.split_last_lifecycle()`。

### D49 · 合成价只封上侧，且封顶按价格精度**向下**取整
爆炸只往高处炸；`round` 会把 0.999 重新顶到 1.00（2 位精度）。
落法：`cap_price_at_instrument_max()` / `synthetic_opening_price()`。

### D50 · 合成回报前先判「这笔成交是否已被快照包含」
成交时间早于某持仓开仓、且该持仓 `trade_ids` 没它 → 快照已含 → 再 app 就是**重复计入**。
落法：`fill_precedes_snapshot()`。

## 三、本轮接线状态（诚实二分）

| 设计 | 落点 | 状态 |
|---|---|---|
| D41~D45 | `ai_quant_lab/20261023_hftbacktest_vnpy/queue_position_model.py` | ✅ 模块级（自测 **20/20**），**未进 `core/`** |
| D46 | `core/backtest.py:participation_for()` + 标定表 | ✅ **已回填**（自测 6/6） |
| D47 | `core/order_lifecycle.py:reconcile_position()` | ✅ **已回填**（自测 9/10→**10/10**） |
| D48~D50 | `ai_quant_lab/.../position_reconciliation.py` | ✅ 模块级（自测 **25/25**），**`core/live.py` 未调用** |

> ★ 为什么 D41~D45 不急着进 `core/`：我们没有 L2/L3 盘口数据，队列模型只能给**上界**。
> 把"只给上界"的东西塞进主回测路径，会把「未观测」伪装成「已建模」——那比不做更糟。

## 四、实证：两条假设的判定（这才是本轮的真产出）

| 假设 | 判定 | 关键数字 |
|---|---|---|
| **H-025 容量咬不咬** | **已验证：不咬** | 逐标的 P99 参与率下 Δ净额单笔均值全为 **+0.0000pp**，部分成交合计 2 笔，未成交 0；**对照组 1e-7 下 100% 委托被截断**（140/140·211/211·202/202·472/472） |
| **H-026 排队紧不紧** | **已证伪：不紧** | V/Q 中位 BTC **12155×**／ETH **1938×**／BNB **195×**／DOGE **738×**；k=1 与 k=10 上界成交率 **100%**（DOGE k=10 才 97.46%） |

**战略含义**：$10k 单 + 15m 粒度下，「容量」与「排队」都不是约束。
**剩下的乐观来源只有一个：滑点与费率**（挂账第 5 轮）→ 本轮之后**上调为 P0**。

## 五、下一步（按优先级）

1. **P0** 滑点系数实盘标定（用真实成交回报的滑点分布，而不是 `slippage=0.05%` 常数）。
2. **P0** `volume_capped_qty` 改成按 `lot_size` 取整（D44），让"差一点没成交"能重现。
3. **P1** `core/live.py` 接 `reconcile_position()`，把持仓快照对账接进实盘路径。
4. **P1** `manifest_min` 接进 `core/backtest.py` 主链（本轮只接了假设回测链）。
5. **P2** 若有 L2 数据，再把 `ProbQueueModel` 进主回测路径（现在只能给上界，不进）。
