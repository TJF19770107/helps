---
日期: 2026-10-23
仓库: hftbacktest（#5 轮 · 二刷，改读**队列层**）+ nautilus_trader（#6 · 三刷，改读**持仓对账层**）
核心文件: hftbacktest/hftbacktest/src/backtest/models/queue.rs（1366 行）／ proc/nopartialfillexchange.rs（649 行）
副文件: nautilus_trader/crates/execution/src/reconciliation/positions.rs（1038 行）
轮次: 第 13 轮
tags: [AI量化平台, 夜学, 代码拆解, 队列位置, 撮合回测, 部分成交, 持仓对账]
---

# 20261023 · hftbacktest · queue.rs ／ nopartialfillexchange.rs

## 0. 一句话结论
> 限价单成交的判据**不是「价格触及」而是「队列前方量被吃完」** —— hftbacktest 把
> `front_q_qty` 当一等公民，价格只是两个分支之一（价格穿越=taker，同价=必须排队）。
> 顺着这条线，本轮把我们自己两个长期"看着有、其实没接线"的东西一次做实：
> ① `participation` 从 **1e-7 演示值**换成**逐标的真实成交量 P99 标定值**（BTC 4.2e-3 ↔ DOGE 1.22，差 3 个量级）；
> ② 订单簿的**持仓对账**从「魔法容差 1e-9」换成「**绑 size_precision 的步长容差**」，并当场抓出
> 「precision=0 时容差=1.0 会把一整张合约的错账判成正常」这个真 bug（自测 9/10 → 10/10）。
> 两条新假设都判出来了：**H-025 已验证（容量不咬）**、**H-026 已证伪（排队不咬）** ——
> 也就是说，在 $10k 单 + 15m 粒度下，我们的成交假设**既不受容量约束、也不受排队约束**，
> 真正的约束只剩**价格与成本**。

## 1. 这个文件在系统里管什么（架构定位）
- 所属层：**撮合回测层**（`queue.rs` 是「我的单在队列第几位」的唯一实现；
  `nopartialfillexchange.rs` 是「什么样的行情事件能让它成交」的唯一实现）
- 上下游：
  - 上游依赖 → `depth.rs`（`MarketDepth`：tick 级买卖盘，提供 `bid_qty_at_tick` / `ask_qty_at_tick` / `lot_size`）、
    `types.rs`（`Order`，`order.q` 是一个 `Box<dyn Any>` 用来塞模型私有状态）、
    `models/{latency,fee}.rs`（延迟与费率，与服务层解耦）
  - 下游被谁调用 → `backtest/mod.rs`（回测主循环，按事件类型分发）、
    `proc/{partialfillexchange,l3_*}.rs`（同族撮合器，**共用同一套 QueueModel 接口**）、
    `hftbacktest/examples/*.rs`（用户侧只换 `QueueModel` 就能换一套成交现实度）
  - 平行对照 → `crates/execution/src/reconciliation/positions.rs`（nautilus 的**持仓**对账，
    与我们的 `core/order_lifecycle.py`（**订单**对账）是同一层缺的另一半）

## 2. 调用链（文字版时序图）
```
回测主循环 backtest/mod.rs
 └─ process(event)                                    # nopartialfillexchange.rs:529-607
     ├─ EXCH_BID/ASK_DEPTH_EVENT                      # 536-551
     │   ├─ depth.update_bid_depth(px, qty, ts)       #   → (price_tick, prev_best, best, prev_qty, new_qty)
     │   ├─ on_bid_qty_chg(price_tick, prev_qty, new_qty)   # 218-228
     │   │   └─ queue_model.depth(order, prev_qty, new_qty) # ★ 只有「同价位」的挂单收到
     │   └─ best 变好 → on_best_bid_update()           # 242 价格穿越 → 对手方单成交
     ├─ EXCH_BUY_TRADE_EVENT                          # 552-577
     │   ├─ 遍历 (best_bid+1 ..= 成交价] 的卖单（价格已穿越 → 直接成交）
     │   └─ 同价 → queue_model.trade(order, qty) → queue_model.is_filled(order)  # 129-133
     │       └─ front_q_qty < 0 → 成交（且按 lot_size 取整）
     └─ remove_filled_orders()                         # 198-216 成交后从 buy/sell_orders 索引里剔除
```
> 关键在 `L121-135` 的 `match order.price_tick.cmp(&price_tick)`：
> **Greater/Less 两分支直接成交（价格已经穿过我）**，**Equal 分支才走队列**。
> 我们旧撮合只有「价格是否落在 [low, high]」这一条，等于把 Equal 分支也当成 Greater 处理。

## 3. 关键类 / 函数（签名 + 职责）
| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `trait QueueModel<MD>` | trait | `new_order / trade / depth / is_filled` 四件套 | `queue.rs:24-38`；**把「队列怎么变」与「怎么算成交」分离** |
| `RiskAdverseQueueModel` | struct | 只有同价成交才前进；盘口撤单**不让**我前进 | `L44-96`；最保守，`depth()` 是空实现 |
| `QueuePos { front_q_qty, cum_trade_qty }` | struct | 队列状态 + **去重计数器** | `L100-103`；`cum_trade_qty` 是去重的关键 |
| `trait Probability` | trait | `prob(front, back) -> f64` | `L125-128`；把「概率形状」变成可插拔参数 |
| `ProbQueueModel<P, MD>` | struct | 数量减少时按概率分摊前进 | `L139-217`；三处易抄错点在 §4 |
| `PowerProbQueueFunc(n)` / `LogProbQueueFunc` / `…Func2/3` | struct | 5 种概率函数、**两套分母约定** | `L219-330`；作者自己保留多套 = 没有唯一正确解 |
| `L3FIFOQueueModel` | struct | 用 L3 逐笔订单做真 FIFO 队列 | `L481-...`；有 L3 数据时的上策 |
| `is_filled(lot_size)` | fn | `exec = round(-front_q / lot_size) * lot_size` | `L207-216`；**部分成交粒度=步长** |
| `check_position_reconciliation` | fn | 三态：match / within_tolerance / discrepancy | nautilus `positions.rs:431-466` |
| `is_within_single_unit_tolerance` | fn | 容差 = `10^-precision`，**precision=0 必须精确相等** | `positions.rs:1026-1038` |
| `adjust_fills_for_partial_window` | fn | 对账窗口不全时按**归零**切生命周期再补差 | `positions.rs:218-...` |
| `cap_price_at_instrument_max` | fn | 合成价只封上侧 + 按价格精度向下取整 | `positions.rs:510-517` |

## 4. 可迁移设计点（本轮 10 条，逐条写「为什么好」）

**D41 · 成交判据是「队列位置」而不是「价格触及」。**
`L114-137` 把成交拆成两分支：价格穿越（我成了 taker，直接成交）／同价（我还排在队里，
必须 `front_q_qty < 0`）。**为什么好**：价格触及只说明「市场在这个价位有成交」，
不说明「这些成交量里有我的份」。我们旧撮合 `bar_fills_limit` 用的是 `low ≤ rate ≤ high`，
在限价挂单场景等于假设自己**永远排在最前面** —— 这是回测里最隐蔽的一类乐观。

**D42 · `trade` 与 `depth` 两条通道必须去重（`cum_trade_qty`）。**
`L175-188`：`trade()` 里 `front -= qty; cum_trade += qty`；`depth()` 里先把
`chg -= cum_trade_qty` 再归零。**为什么好**：同一笔成交会**两次**到达撮合器 ——
一次作为 trade 事件，一次体现为 depth 减少。不去重就前进两次，
**成交量被算了两遍**，队列虚快 → 成交被系统性高估。这条几乎不可能靠肉眼审查发现，
必须靠测试（本模块 B1 用例就是钉这个）。

**D43 · 数量「减少」直接夹断，不做概率分摊。**
`L190-193`：`if chg < 0 { front = min(front, new_qty); return; }`。
**为什么好**：挂单量减少可能是**我后面的人**撤了，可能是我前面撤了，也可能同时既撤又挂。
在这些可能里，「前方按比例减少」是**最乐观**的解释；直接夹到 `new_qty`
是唯一不引入乐观假设的处理。而数量「增加」时 `L195-204` 才用概率分摊 ——
因为新增挂单必然排在我后面，**我方前方量不该因此变多**。

**D44 · 部分成交按 `lot_size` 取整（不是连续量）。**
`L209`：`exec = (-front_q / lot_size).round() as i64`，再乘回 `lot_size`。
**为什么好**：交易所的最小成交单位是步长，「差 0.4 个步长」永远不会成交。
我们的 `volume_capped_qty` 返回的是连续浮点数，**天生不可能重现「差一点没成交」**，
这会让「部分成交」永远比实盘乐观一点点 —— 小，但方向一致地偏乐观。

**D45 · 概率函数有 5 种实现、2 套分母 —— 这本身就是结论。**
`PowerProbQueueFunc`（`f(back)/(f(back)+f(front))`）与 `PowerProbQueueFunc2`
（`f(back)/f(back+front)`）并存，`Func3` 又是 `1 - f(front/(front+back))`。
**为什么好（对我们的启示）**：队列位置估计**没有唯一正确解**，
它是**必须用实盘数据标定的参数**，不是可以从教科书推出来的公式。
任何「我们算出了队列位置」的说法，都必须附带「用什么数据标定、标定区间多长」。

**D46 · taker 单不受队列约束 —— 这正是容量必须单独建模的原因。**
`L58-62` 文档原文：*"liquidity-taking orders will be fully executed at the best.
Be aware that this may cause unrealistic fill simulations if you attempt to execute
a large quantity."* **为什么好**：作者在自己文档里承认了这个缺口。
我们正好一直用 1e-7 演示值假装有容量约束（见 §7 H-025 的对照组：**每一笔都被截断**）。

**D47 · 对账容差必须绑 `size_precision`，`precision=0` 必须精确相等。**
`positions.rs:1026-1038`：`if precision == 0 { return v1 == v2 }` 单独一个分支。
**为什么好**：整数张合约上「差 1 张」是**真实错账**，不是精度噪声。
我们 `core/order_lifecycle.py:117` 原用魔法数字 `tol=1e-9`：
BTC（步长 0.001）等于要求绝对精确 → 天天刷假告警；整数张又"碰巧"对。
**「碰巧对」比明着错更危险：换品种就错，而且错得没有声音。**

**D48 · 生命周期按「归零」切，不按「翻转」切。**
`positions.rs:245-250`（`prev_qty != 0 && running_qty == 0` 才算边界），
注释明写 "flips within a lifecycle don't count"。
**为什么好**：多→空→多 的**翻转不是新生命周期**。拿翻转当边界会把一条持仓劈两半，
对账时「缺的开仓成交」与「多出来的平仓成交」互相抵消 —— **错误会自己抵消成 0**，
于是 bug 永远测不出来。

**D49 · 合成价只封上侧，且封顶要按价格精度**向下**取整。**
`positions.rs:498-517`：合成价 = notional / qty，qty 是粉尘残量时结果会爆表。
**为什么好**：两个细节都对 —— ① 爆炸只往高处炸（分母趋 0+），负价与零成本单要原样放过；
② 封顶后用 `round` 重建 Price 会**重新顶回上限之上**（`max=0.999` 在 2 位精度下 round 成 1.00），
所以必须先向下取整。

**D50 · 合成回报前先判「这笔成交是否已被快照包含」。**
`positions.rs:474-496`：若成交时间**早于**某持仓的开仓时间，且该持仓 `trade_ids` 里**没有**这笔成交，
说明交易所快照**已经包含**它，再 app 一次就是**重复计入**（持仓凭空翻倍）。
**为什么好**：对账的敌人不是"差"，而是"重复算"与"漏算"混在一起分不清。

## 5. 可复用代码片段

**片段 1：`ProbQueueModel.depth()` 的三行去重 + 夹断**（我们最该抄的一段）
```python
# 来源：hftbacktest/src/backtest/models/queue.rs:181-205
# 用途：盘口数量变化时，正确推进「我方队列前方量」。缺任何一行都会系统性高估成交。
def depth(self, prev_qty: float, new_qty: float) -> None:
    chg = prev_qty - new_qty
    chg -= self.pos.cum_trade_qty        # ★ L186 去重：trade 事件已经消化过的量不再算
    self.pos.cum_trade_qty = 0.0         # ★ L188 重置
    if chg < 0.0:                        # ★ L190-193 数量减少 → 直接夹断，不分摊
        self.pos.front_q_qty = min(self.pos.front_q_qty, new_qty)
        return
    front = self.pos.front_q_qty
    back = prev_qty - front
    prob = self.prob_fn(front, back)
    if math.isinf(prob):
        prob = 1.0
    est = front - (1.0 - prob) * chg + min(back - prob * chg, 0.0)   # ★ L203 反向补正
    self.pos.front_q_qty = min(est, new_qty)
```
落地：`ai_quant_lab/20261023_hftbacktest_vnpy/queue_position_model.py:ProbQueueModel.depth`

**片段 2：容差的正确形态**
```python
# 来源：nautilus_trader crates/execution/src/reconciliation/positions.rs:1026-1038
# 用途：任何「数量对不上」的判定都该这么写，别用魔法数字
def tolerance_for_precision(precision: int) -> float:
    p = int(precision)
    return 0.0 if p == 0 else float(10.0 ** (-p))   # precision=0 → 零容差，差 1 张就是错
```
落地：`quant_app/core/order_lifecycle.py:tolerance_for_precision`（已接，自测 10/10）

**片段 3：按归零切生命周期**
```python
# 来源：nautilus_trader .../positions.rs:245-250（adjust_fills_for_partial_window 内）
# 用途：对账窗口只覆盖半条持仓时，先切出「最后一条生命周期」再比，否则错账会自我抵消
running = Decimal(0); boundary = None
for f in fills:
    prev, running = running, running + Decimal(str(f.qty))
    if prev != 0 and running == 0:      # ← 只有真正回到 FLAT 才算边界
        boundary = f.ts
```
落地：`ai_quant_lab/20261023_hftbacktest_vnpy/position_reconciliation.py:split_last_lifecycle`

## 6. 对黑马策略的启发（必须落到具体动作）

### 6.1 本轮已经落地的两个平台动作

| 动作 | 改哪 | 验证 |
|---|---|---|
| **参与率标定**：`volume_capped_qty` 的 `participation` 不再用 1e-7 演示值 | `quant_app/core/backtest.py` 新增 `PARTICIPATION_TABLE_PATH` / `load_participation_table()` / `participation_for(symbol)`；数据来自 `ai_quant_lab/20261023_hftbacktest_vnpy/participation_table.json` | `selftest_participation_wiring()` **6/6**；BTC p99=4.25e-3、DOGE p99=1.22e0 |
| **持仓对账三态**：容差绑步长，禁止静默改本地持仓 | `quant_app/core/order_lifecycle.py` 新增 `tolerance_for_precision()` + `reconcile_position()` | `selftest_lifecycle()` **9/10 → 10/10**（新抓 1 个真 bug，见 §8） |

### 6.2 两条新假设（均已在台账）

- **H-025（容量到底咬不咬）** —— 已验证：**不咬**。
  逐标的 P99 参与率下，4 只标的 Δ净额单笔均值 = **全部 +0.0000pp**，部分成交合计 **2 笔**（BTC 1 / ETH 1），
  整单未成交 **0**。**对照组**（1e-7）：partial = **140/140、211/211、202/202、472/472 = 100% 全部被截断**
  —— 这坐实了 H-021 那句「咬合力≈0」是**假观测**：1e-7 下每一笔都被截成 0，
  所谓"约束"从没被真测过。**这就是「咬合力 100% ⇒ 判没被测到」纪律的又一次实证。**
- **H-026（排队到底紧不紧）** —— 已证伪：**不紧**。
  V/Q 中位：BTC **12155×**、ETH **1938×**、BNB **195×**、DOGE **738×**
  → 我们的委托量比 15m 成交量小 2~4 个量级，k=1 与 k=10 的成交率上界都是 **100%**
  （DOGE 在 k=10 才降到 97.46%）。**结论：15m + $10k 规模下，排队不是约束，
  H-022 的 maker 结论没有被排队这一层否定；真正的约束是价格与成本。**

> ★ 两条合起来的战略含义：**我们不必再花时间在"成交现实度"上继续加码**
> （容量与排队都已证伪为"不咬"）。剩下的乐观来源只有一个：**滑点与费率**（挂账第 5 轮）。

### 6.3 结掉前日悬空的旧假设：H-023 补档第三次外推（P0-2）

`_TP_CANDIDATES` 加第 7 档 **`40/32/20`**（前两轮最优连续两次落在网格端点，按纪律必须继续外推）：

| 标的 | 训练段最优档（7 档中） | 训练段净额单笔% | 样本外基线 10/8/5 | 样本外最优档 | Δpp |
|---|---|---|---|---|---|
| BTCUSDT | **40/32/20** | 15.7198 | 0.6028 | 3.2842 | **+2.6814** |
| ETHUSDT | **40/32/20** | 13.4416 | 0.8263 | 2.5311 | **+1.7048** |
| BNBUSDT | **40/32/20** | 16.3877 | 1.1740 | 1.5521 | **+0.3781** |
| DOGEUSDT | **40/32/20** | 10.1555 | −0.9418 | −1.9930 | **−1.0512（恶化）** |

判定 **已验证 3/4**（≥3 只不下降），但两个必须写进结论的限定：
1. **端点第三次外移**（`20/15/10` → `30/25/15` → `40/32/20`）：训练段净额随档位**单调上升**
   （BTC 1.12 → 1.70 → 2.57 → 4.02 → 6.10 → 7.82 → **15.72**），说明在网格内**根本没测到内部最优**。
   「存在内部最优」这个说法**只能靠 `let_run` 已知 0/4 全负来支撑**（即最优点在 `40/32/20` 与 `let_run` 之间），
   **不能**说 40/32/20 是拐点。
2. **DOGE 样本外恶化 −1.0512pp**：低波动标的上单调性断裂 —— 与 H-014（DOGE 在低波动门槛下更差）同向。
   ⇒ **下一个动作不是再外推一档，而是分标的给结论**：高波动标的可继续放宽，低波动标的必须留在基线档。


## 7. B站学习（本日 30% 权重）
- 视频：`面向个人交易员的量化投资课程` 第三讲 vn.py 基础操作（1-2）CTA 策略编写 ·
  <https://www.bilibili.com/video/BV1ov4y1q7Ms/> · 课程目录含「第六章 高频交易」
- 有无字幕：**无可用 CC 字幕**（与前几轮一致）。按纪律**降级为标题/目录级**笔记，不做音频转录（零成本底线）。
- 目录级蒸馏（仅结构，不含未验证的结论）：
  - 第 1~3 章 工具层：python / backtrader / vn.py（与我们 `quant_app` 的定位对照）
  - 第 4 章 策略开发方法 ｜ 第 5 章 实盘操作 ｜ **第 6 章 高频交易** ← 与今天 `queue.rs` 主题直接同域
- 存疑处（待代码验证）：口播里任何「移动止损优于固定止损」之类的断言，我们先当假设。
  本仓库已有 H-006（时间止损）/ H-018/H-023（止盈档）的实测，**结论以台账为准，不以视频为准**。

## 8. 未完成 / 失败区（诚实留痕）

1. **AtomCode 推理连续第 3 轮不可用 → 全程本地 Read/Grep，0 积分。**
   本轮新证据（比前两轮更具体）：`/health` 200、`logged_in=true`（账号 gcw_1D1KA17b，到期 2026-10-26）、
   `/v1/models` 正常返回 3 个免费模型；但 `POST /v1/chat/completions`：
   - 第 1 次 240s 超时（HTTP 0）
   - 第 2 次 60s → **HTTP 500 `AtomCode serial lock timed out after 30s`**
   - 杀掉僵死子进程 + **重启代理**后仍 120s 超时（HTTP 0）
   - `atomcode.exe --version` = **5.2.3 (d8918f0)，二进制完好**（排除二进制损坏，P2 待办结掉）
   ⇒ 定位：**上游推理通道挂死**（代理本地层正常、模型列表正常、仅推理阻塞），非额度、非二进制。
   ⇒ 按纪律第 3 轮起**不再耗时间**，本轮到此为止。
2. **B站无可抓字幕** → 第 5 轮起已永久降级为标题级，本轮照此执行，不再记「未完成」欠账（此处仅备注）。
3. **`reconcile_position` 只接进了 `order_lifecycle` 的工具层，`core/live.py` 实盘路径还没调用它。**
   下一轮要么在 `live.py` 的持仓快照回调里调，要么明确写下「实盘持仓对账仍未接线」。
4. **`manifest_min` 已接进 `hypothesis_runner`（跑完自动落清单 + 与上一份 diff），
   但 `core/backtest.py` / `core/live.py` 主链仍未接。** 本轮只解决了"假设回测能追溯"。
5. **持仓对账的差额来源无法拆分**：目前只有订单级回报，手续费扣币 / 资金费 / 强平
   三种"非成交"变动造成的持仓差，无法从成交推算里区分。需要交易所账单接口。
6. **滑点系数仍未实盘标定**（挂账第 5 轮）。H-025/H-026 双双证伪"不咬"之后，
   它是唯一还没被动过的乐观来源 —— 优先级应上调为 P0。
7. **15m 数据无法识别队列深度**（诚实边界）：`queue_position_model` 的层 B 只给**上界**，
   不给点估计。任何"我们算出了队列位置"的说法在 15m 数据上都是假的。

### 8.1 本轮自测抓到的三个真 bug（都已修 + 都有断言）

| # | bug | 后果 | 修法 | 断言 |
|---|---|---|---|---|
| ① | `tolerance_for_precision(0)` 返回 `10^0 = 1.0` | 整数张合约上「差 1 张」被判成精度噪声 → **错账永久合法化** | `precision==0 → 0.0`（照 nautilus 那个独立分支） | `selftest_lifecycle` 9/10 → **10/10** |
| ② | `breakeven_front_multiple` 搜索区间硬编码 `[0,1]` | 「k=1 仍 100%」返回假的 `1.0` = **把区间端点伪装成科学边界** | 区间倍增到 `k_max`，越过则返回 `None`（右删失） | `queue_position_model` 20/20（含 D2/D2b 两向对照） |
| ③ | `update_ledger` 无条件 `parts[10] = v.evidence` | **证据为空就把已有证据清空**（实证：H-024 的 `回测结果_20261022.json` 被抹掉，进度打印只显示"状态未变"→ 完全无声） | 空证据**只允许不写**，并把"保留原证据"记进 `warnings` | 临时副本回放：证据仍在 + warnings 有记录；H-024 证据已复原 |

> ★ ③ 是**数据丢失**级 bug，比任何策略结论都重要：台账是"唯一入口"，
> 入口被静默改写比写错更严重 —— 写错还能被下轮纠正，被抹掉的证据没有任何人会发现。


## 9. 三件套自检
- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：
  - `ai_quant_lab/20261023_hftbacktest_vnpy/queue_position_model.py`（自测 **20/20**）
  - `ai_quant_lab/20261023_hftbacktest_vnpy/position_reconciliation.py`（自测 **25/25**）
  - `ai_quant_lab/20261023_hftbacktest_vnpy/participation_calibration.py`（自测 **11/11** + `participation_table.json` 真实标定）
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-025（已验证）／ H-026（已证伪）**

## 10. 成本与技能
- 本次花费积分估算：**0**（AtomCode 全程不可用 → 本地 Read/Grep；回测纯本地 pandas/numpy，无外部 API）
- 技能：`ai-quant-open-source-nightly-learning`（本轮按 §3.12 执行，见收尾报告）
- 六端归档：周五（周中）→ **只落 Obsidian + 工作区日志**；下一次六端归档 **2026-10-25（周日）**
