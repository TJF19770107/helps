---
日期: 2026-11-02
仓库: nautilus_trader
核心文件: crates/execution/src/matching_core.rs（2056 行）+ matching_engine/mod.rs（12889 行）
轮次: 第 22 轮
tags: [AI量化平台, 夜学, 代码拆解, 撮合内核, 成交判据]
---

# 20261102 · nautilus_trader · `matching_core.rs` + `matching_engine/mod.rs`

## 0. 一句话结论

> **「限价单成交了没有」不是事实，是一个档位。** nautilus 把它显式做成两档开关
> （跨价 / 价差内）且**默认严格**；我方回测一直用的 `low ≤ px ≤ high` 是宽松档。
> 把 H-042 的出场挂限价换到严格档一测：**中位 +0.4039pp → −0.0713pp，7/12 格转负**
> ⇒ H-042 的增益有 **20.6~34.4%** 是靠插针凑出来的成交率。这条口径今天第一次被量化。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：撮合回测层（matching / fill simulation）。
  - `matching_core.rs` = **撮合内核**：纯函数式「给定一个市场快照 + 一堆挂单，返回谁该成交/谁该触发」，
    **不动订单簿、不下单、不记账**（模块注释 `:16-19` 明确「without removing orders from the books」）。
  - `matching_engine/mod.rs` = **撮合引擎**：拿内核的 `MatchAction` 去真正改订单状态、算成交价量、
    记账、发事件。
- **上下游**：
  - 上游 → `nautilus_model::orders`（`PassiveOrderAny` / `StopOrderAny` / `TriggerType`）、
    `nautilus_common::clock`、`FillModelHandle` / `FeeModelHandle`（可插拔的成交/费用模型）、
    `OrderBook`（L1/L2/L3 深度）。
  - 下游被谁调用 → `ExecutionEngine` 的 `process` / `on_quote` / `on_trade`；
    `OrderEmulator`（本地模拟撮合，`order_emulator/emulator.rs` 4371 行）复用同一内核。
- **它在我方平台的对应物**：`quant_app/core/backtest.py` 的撮合段（第 556~623 行）
  —— 那里没有独立内核，成交判定直接内联在策略循环里。**这就是今天的结构性差距**。

---

## 2. 调用链（文字版时序图）

```
交易所报价/成交 tick 到达
  → OrderMatchingEngine::on_quote / on_trade
      → 更新 core.bid / core.ask / core.last（或 L2/L3 用 book.best_*，mod.rs:4185-4186）
      → 【路径：快照 → 动作】
        core.iterate()
          → iterate_bids()   （先买方：limits 高价优先，再 stops 低价触发优先）
              → iter_bid_book_orders()  BTreeMap.rev() 遍历 limit 桶，再接 stop 桶
                  → match_order(order)
                        ├ is_stop()  → match_stop_order  → is_stop_matched / is_touch_triggered
                        └ is_limit() → match_limit_order → is_limit_fillable
                                                            ├ is_limit_matched（跨价，严格）
                                                            └ fill_limit_inside_spread（价差内，宽松）
              → 返回 Vec<MatchAction>{ FillLimit(id) | TriggerStop(id) }
          → iterate_asks()   （后卖方，镜像）
      → 【路径：动作 → 撮合】（mod.rs:4195-4219）
        for action in actions:
            should_process_match_action()      ← ○ 市场状态/撮合模式过滤
            FillLimit    → fill_resting_limit_order → fill_limit_order_with_snapshot
            TriggerStop  → trigger_stop_order
      → 【路径：撮合 → 定价定量】（mod.rs:4907-5040）
        cache 取订单快照 → 已平仓则清残留 → 报价数量转基础数量
        → maker 则在 limit 上查 fill_model.is_limit_filled()（概率闸，**只许查一次**）
        → config.queue_position 则 determine_trade_fill_qty（队列允许量）
        → reduce_only 无持仓则 cancel（不是 reject）
        → determine_limit_fill_model_price_and_volume
              ├ 有深度：fill_model.get_orderbook_for_fill_simulation → book.simulate_fills
              └ 无深度：determine_limit_price_and_volume → book.simulate_fills / 单笔 trade 预算
        → 应用 fills → 发 OrderFilled 事件
      → 【路径：撮合后维护】post_match_order_action → RemoveClosed / 保留在途
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `OrderMatchingCore` | struct | 撮合内核：四个 `BTreeMap`（bid/ask × limit/stop）+ 两列 pending + 一个 `AHashMap` 索引 | `matching_core.rs:131`；无 I/O、无状态机 |
| `MatchAction` | enum | `FillLimit(ClientOrderId)` / `TriggerStop(ClientOrderId)` | `:123`；**只报「该干」，不报「干成了」** |
| `RestingOrder` | struct | 撮合用的轻量订单视图（7 字段） | `:600`；与完整 `OrderAny` 解耦 |
| `OrderMatchingCore::iterate()` | fn | 买方全部 → 卖方全部 | `:362`；**顺序是硬编码契约，不是实现细节** |
| `::match_order()` | fn | 按「有 trigger → 走 stop；否则有 limit → 走 limit；都不是 → None」分派 | `:386-394` |
| `::is_limit_matched()` | fn | 跨价判定：BUY `ask ≤ px` / SELL `bid ≥ px` | `:396-404`；**严格档** |
| `::is_limit_fillable()` | fn | 先跨价；`fill_limit_inside_spread` 开时再加「价差内」：BUY `px ≥ bid` / SELL `px ≤ ask`，**要求双边都初始化** | `:459-476`；**宽松档** |
| `::set_fill_limit_inside_spread()` | fn | 切换上面那一档 | `:448`；由 fill model 注入 |
| `::is_stop_matched_with_trigger_type()` | fn | 止损触发：BUY `ask ≥ px` / SELL `bid ≤ px`，价格源随 `TriggerType` | `:414-425` |
| `::is_touch_triggered_with_trigger_type()` | fn | MIT/LIT 触发：**方向与止损相反**（BUY `ask ≤ px`） | `:435-446` |
| `::market_price_for_trigger()` | fn | `LastPrice`→last；`LastOrBidAsk`→`last.or(quote)`；其余→quote | `:580-595` |
| `::add_order()` | fn | 按 `locate()` 路由到 limit book / stop book / pending | `:300`；`debug_assert` 挡重复 ID |
| `::delete_order()` | fn | 删索引 + 桶内线性定位删除 + 空桶回收 | `:330-358` |
| `::locate()` | fn | 有 trigger_price → Stop 书；否则有 limit_price → Limit 书 | `:534-540` |
| `OrderMatchingEngine::fill_limit_order_with_snapshot()` | fn | **限价成交的总入口**：幂等判重 → maker 概率闸 → 队列许可 → reduce_only → 定价定量 → 应用 | `mod.rs:4907`；~130 行 |
| `::determine_limit_fill_model_price_and_volume()` | fn | 优先「fill model 给深度」→ `simulate_fills`；否则落回报价路径 | `:4716-4732` |
| `::determine_limit_price_and_volume()` | fn | 无深度时的成交价量；含 L1 trade 预算分支 | `:4478-4532` |
| `::fill_limit_inside_spread_or_false()` | fn | 从 fill model 读宽松档开关，**读失败 → false（严格）** | `:563-568` |
| `::should_process_match_action()` | fn | 撮合模式过滤（`All` / `LastPriceStopTriggers`） | `:4348-4367` |

---

## 4. 可迁移设计点（本次 10 条，每条写「为什么好」）

### D113 成交判据必须**显式成档**，且默认取严格档

`is_limit_matched`（跨价）与 `fill_limit_inside_spread`（价差内）是两个函数，
后者由开关控制，**默认 `false`**（`matching_core.rs:162` 初始化 + `mod.rs:563-568` 读失败也落 `false`）。

**为什么好**：宽松档在物理上不成立——买单挂在卖一之下、买一之上（价差内），
你在那个价位上**没有对手方**，凭什么成交？它存在的唯一理由是「给某些数据源做兼容」，
所以必须是**显式、可选、默认关**。

**我方差距**：`core/backtest.py` 的出场判定用 `low ≤ trail_prev`（触及即成交），
**从来没有把「档位」这个维度暴露出来**。今天补上了：`exit_confirm ∈ {none, close}`。

### D114 maker 的成交判据是「价格**精确等于**挂单价」，不是「穿越」

`mod.rs:4948-4954`：

```rust
let at_limit = if self.last_trade_size.is_some() && self.core.last.is_some() {
    self.core.last.is_some_and(|last| last == order_price)      // 成交驱动
} else if order.order_side() == OrderSide::Buy {
    self.core.bid.is_some_and(|bid| bid == order_price)         // 报价驱动，买方看 bid
} else {
    self.core.ask.is_some_and(|ask| ask == order_price)         // 报价驱动，卖方看 ask
};
```

**为什么好**：`==` 而不是 `<=`/`>=`。原因是**观测的粒度**：nautilus 消费的是离散的
tick/trade 流，价格路径**没有被观测到**。当一根 bar 直接跳空越过你的挂单价时，
「成交价序列里从未出现过你的价」⇒ 保守判「没成交」。这是**宁可少算成交**的取向。

**★ 但这条不能直接搬到 bar 级回测**：bar 的 `low/high` 是**路径的极值摘要**，
在连续价格假设下 `low ≤ px ≤ high` 恰恰**是**「路径经过该价」的合理解。
今天笔记里我特意把 `exact` 档实现成「只认 `open == limit`」并标为**最保守下界**，
而不是假装它就是 nautilus 的 `==`——**语义可以借，粒度不能借**。

### D115 撮合分两级：有深度用深度，无深度用报价；且**降级路径自己再判一次跨价**

`determine_limit_fill_model_price_and_volume`（`mod.rs:4716`）先问 fill model 要深度，
要不到才落回 `determine_limit_price_and_volume`；而后者内部
（`:4506`）**又独立调一次** `self.core.is_limit_matched(...)`。

**为什么好**：降级不是「信任上层的结论」，而是**在降级路径上重新验一次前置条件**。
这一条直接对应本项目第 20 轮 `_lfp` 两份实现漂移的教训 —— 单一真源不是抄一份代码，是**一处判、处处引用**。

### D116 「算不出来」与「确实是零」必须分态（**但两者都 fail-closed**）

`mod.rs:4976-4982`：

```rust
match self.determine_trade_fill_qty(&order) {
    None | Some(0) => { if IOC/FOK { cancel } return; }   // ← 两者合并
    Some(allowed) => Some(allowed),
}
```

**行为对**（都不成交，fail-closed 正确），但**丢掉了可诊断性**：事后分不清
「队列算不出来」和「容量真的是 0」。这正是第 19 轮 `glob` 返回 `None` 那次坑的同族。

**我方做法**：`limit_fill_semantics.FillStats` 里 `misses` 与 `unknown` **分开计**，
且 `rate` 的分母**不含 unknown**（把算不出来的算成「没成交」= 用执行失败污染统计）。

### D117 成交幂等用「已落库成交量 ≥ 委托量」判重，不用事件 ID

`mod.rs:4927-4939` + `:4762-4773`：两处都用 `cached_filled_qty >= order.quantity()` 提前返回。

**为什么好**：事件可能被重放而 ID 不同（重连、快照重放），
**但「这单已经成交完了」是业务事实**。用业务事实做幂等键，比用传输层标识鲁棒。

### D118 `reduce_only` 在无持仓时「取消」，不是「拒单」

`mod.rs:4991-4998` / `:4777-4784`：`reduce_only_position_missing` ⇒ `cancel_order`。

**为什么好也为什么要注意**：取消会**释放额度、进「撤单」计数、允许策略重发**；
拒单则完全不进撮合。两者在回测的统计报表上是完全不同的事件。
我方 `core/risk.py` 的 `reduce_only` 已有，但**「无持仓时的终态」没显式声明**，
在 `risk.py` 里是归入拒单还是取消，下轮要核（挂账）。

### D119 概率型约束必须有**单次调用不变量**，否则概率被平方

`mod.rs:4508-4509` 的注释（原话）：

> Fill model check for MAKER at limit is already handled in fill_limit_order,
> don't re-check here to avoid calling `is_limit_filled()` twice (**p² probability**).

**为什么好**：这是「同一个概率被两处各乘一次 → 实际成交概率 = p²，而结果里看不出来」的
真实防线。我方同时有 `participation`（参与率）与 `queue`（队列位）两个概率型开关，
**没人保证它们不会在多处各乘一次**。

**落地**：`ProbGuard` —— 同一 scope 内第二次 `claim` 直接抛错，不静默乘第二次。

### D120 快照式撮合**无法恢复路径顺序**，源码自己承认并写进文档

`matching_core.rs:61-74`（"Snapshot Ordering Limitation"）原话要点：

> `iterate_bids` / `iterate_asks` emit all matchable limits before triggered stops…
> **A stop can trigger during a price move and then aggress against the limit book;
> a snapshot alone cannot recover that sequence** when both limits and stops are matchable.
> Callers must not interpret the limits-then-stops sequence as price-path order.

**为什么这是今天最有价值的一条**：一流平台**主动承认**自己的撮合有结构缺陷，
并且明确给出「要么补价格路径信息、要么改引擎按穿越顺序发成交」的出口，
而不是含糊过去。我方 `exit_trigger="intrabar"` 面临**完全同构**的问题：
同一根 15m bar 内既触及止损又触及止盈时，**谁先？** 我方当前是「止损优先」——
这**是假设，不是事实**，而且源码级对标告诉我：**不可能从 bar 恢复**。

**落地**：`same_bar_barriers(...)` 把路径做成显式枚举
（`olhc` 保守 / `ohlc` 乐观），`selftest` 里用「两档结论必须相反」证明它真的起作用。

### D121 改单 = delete + add ⇒ 队列位**必丢**，即使只改数量

`matching_core.rs:52-59`：

> The order joins the back of its price level, **even if the price is unchanged**.
> This models loss of queue position on price changes, but **also loses position for
> quantity-only changes**. Preserving position for quantity-only changes would require
> an in-place update API.

**为什么好**：它承认这是**取舍**而不是 bug，并指出「量改保队列位」需要额外信息。
⇒ 回测里给「改量保队列位」是**额外奖励**，默认不该给。

### D122 幂等键唯一性必须由**索引**保证，不能靠调用方自觉

`matching_core.rs:76-82`：

> `add_order` panics on duplicate IDs **when debug assertions are enabled**.
> **Without debug assertions**, adding the same ID twice … leaves duplicate entries
> that **can both match**.

**为什么这是反面教材**：约束只在 debug 生效 ⇒ release 下静默双成交。
**我方做法**：`MatchingIndex.add()` 重复即抛 `KeyError`，且**不污染索引**
（先判后写），并在 `duplicate_attempts` 留痕。

### D123 证据/日志类字段的**更新语义**：路径可过期，注释不可丢

（本轮修 `hypothesis_runner.update_ledger` 时提炼，与 nautilus「同一字段两条通道两套定义」同族。）

旧实现：`parts[10] = v.evidence` —— 新证据直接把整列覆盖。
本轮实证：`回测结果_20261027.json` → `回测结果_20261102.json` 这一**看似无害的换路径**，
把 H-042 / H-044 手写的「关键数：+0.4039 → −0.0713pp」整段冲掉，台账 **−2390 B**，
而终端只打印「证据 `…json` → `…json`」——**数字死了，报表还在笑**。

**为什么好（修法）**：把一列拆成两类 token ——
「纯路径」是**会过期的指针**，以新为准；「注释（关键数 / ★）」是**知识**，一律保留。
`_merge_evidence` 7/7 自检（含变更测试 + 幂等），实测第二次回写 `bytes_delta = 0`。

**更普适的一条**：**任何"更新"操作都要先问「这一列里是不是混着两种东西」**。
混着就必须分类处理，否则「换指针」会顺手删掉「指针指向的意义」。

---

## 5. 可复用代码片段

> 完整实现见 `ai_quant_lab/20261102_nautilus_trader_vnpy/limit_fill_semantics.py`（selftest **26/26**）。
> 下面只摘核心 25 行，不贴整段源码。

```python
# 来源：nautilus_trader/crates/execution/src/matching_core.rs:459-476 + matching_engine/mod.rs:4948-4954
# 用途：把「限价单成交判据」做成三级阶梯，按需取档，默认严格

def sell_limit_fill_px(limit, bar_open, bar_high, bar_low, bar_close, mode="touch"):
    """卖出限价在单根 bar 内的成交价；0.0 = 不成交。"""
    _validate_mode(mode)
    # 跳空高开：价格从未回落到挂单价以下 ⇒ 确定成交（两档都不能否掉它，
    # 否则等于假设「开盘成交也要等收盘确认」，把确定当不确定）
    if bar_open >= limit:
        return float(bar_open)
    if bar_high < limit:                       # 根本没触及
        return 0.0
    if mode == "touch":                        # 宽松档：区间触及即成交（= H-042 口径）
        return float(limit)
    if mode == "close_confirm":                # 严格档：收盘仍在对侧才算，剔除插针
        return float(limit) if bar_close >= limit else 0.0
    return 0.0                                 # exact：bar 级不可观测 ⇒ 最保守
```

**结构不变量（selftest 里真的反测过，不是只断言一次）**：
`exact ⊆ close_confirm ⊆ touch` —— 三级阶梯必须单调包含。
`T2` 是**变更测试**：把收盘从 103 抬到 106，`close_confirm` 必须从「不成交」翻成「成交」；
不改输入就永远为真的断言，等于没断言。

---

## 6. B站学习（本日 30% 权重）

- **实质产出：0**。第 10 轮已结案（该 UP 主所有视频字幕接口恒返回空），**不再记入「未完成」**。
- 本日 30% 权重改用**跨层交叉阅读**替代：`matching_core.rs`（内核）+ `matching_engine/mod.rs`（引擎）
  + `order_emulator/`（本地模拟）三处对读同一语义，等价于「同一概念在不同抽象层怎么落地」的训练。
- 交叉阅读的直接产物：发现 D115「降级路径自己再判一次跨价」——
  只看内核**根本看不出**这条，因为判定发生在引擎侧。
  这是「交叉学习」有效性的证据，也说明**单文件精读必然漏设计**。

---

## 7. 对黑马策略的启发（必须落到具体动作）

- **假设 H-044**：把出场挂限价的成交判据从「触及即成交」换成「触及且收盘确认」，
  H-042 的 +0.4039pp 增益还剩多少？→ **已证伪**：严格档中位 **−0.0713pp**，7/12 格转负。
- **怎么验**：`ai_quant_lab/hypothesis_runner.py::verify_H044`（四标的 × 3 档 × 2 判据 = 24 格）。
- **若成立，改哪**：
  1. `core/backtest.py` 已加 `exit_confirm ∈ {none, close}` 开关（默认 `none` = 零退化），
     并加了「`exit_confirm` 只允许与 `exit_trigger='intrabar'` 组合，否则**直接报错**」
     —— 防「参数给了但变成静默空操作」。
  2. **BNB / DOGE 两项不许再用 H-042 的结论**（严格档 3/3 全负）；
     BTC / ETH 两档都正，可继续用但**结论要标上下界**。
  3. 引擎侧新计数器 `exit_confirm_rejected`（插针剔除数），
     `selftest_exit_confirm` **8/8**：默认零退化、咬合力自证、变更测试、非法组合抛错。
- **实测数字（顺带发现）**：`intrabar` 宽松档总收益 172.495%，严格档 **179.0%**，
  基线 179.347%。即**插针出场在 BTC 上是坏出场**（错杀了一批还会回来的仓位），
  这与 H-044 在 BTC 上 3/3 全正互相印证。

---

## 8. 未完成 / 失败区（诚实留痕）

1. **AtomCode 第零步：连续第 12 轮失败。**
   `proxy_down` → 后台拉起 `atomcode_proxy.py 13460` → 复测 `proxy_listening=true` /
   `health_http=200` / `health_reports_ok=true` / `logged_in=true`（`gcw_1D1KA17b`），
   但**最小推理 240s 超时 `HTTP=0`** ⇒ 上游推理层僵死（非额度、非二进制）。
   按收敛纪律不耗时间，降级本地 Read/Grep，**0 积分**。已如实记，未伪装成「已用 AtomCode」。
2. **`exit_limit_premium` 开关没做，改做 `exit_confirm`。**
   理由写清：**不该在一个未校准的成交判据上做参数寻优**（加价档位的结论完全依赖成交判据），
   所以先补判据、后补档位。这是**主动重排**，不是漏做 —— 下轮 P0 接 `exit_limit_premium` 时
   必须带着今天的严格档一起测。
3. **`core/risk.py` 的 `reduce_only` 无持仓终态未核**（D118）：取消 vs 拒单在报表上不同事件，
   今天只看出 nautilus 的做法，没核我方。
4. **H-043（联合挂单）仍是「搁置」，未解锁**：样本外 + `min_trades ≥ 100` + 资金闲置成本
   三项都还没做；今天也没做（优先级让给 H-044）。
5. **实盘 4543 笔 vs 回测 129 笔（差 35 倍）挂账第 6 轮**，今天**没动**。
   没有实盘逐笔导出，任何解释都是猜测。
6. **`order_emulator/emulator.rs`（4371 行）只扫了函数名，没精读**——
   它是「本地模拟撮合」的完整实现，与今天的主题强相关，但一天读不完，
   下轮若再轮到 nautilus 应优先它。
7. **`exact` 档在 bar 级数据上几乎退化**（只认开盘等值），
   所以严格的「真值」仍然**不可得**：宽松档是**上界**、严格档是**下界**，
   两者之差才是口径风险敞口。**不许把单档数字当结论**——这句要写进台账。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘：本文件
- [x] ② 可复用代码落盘：
  - `ai_quant_lab/20261102_nautilus_trader_vnpy/limit_fill_semantics.py`（selftest **26/26**，lab_bridge 零警告）
  - `quant_app/core/backtest.py` → `selftest_exit_confirm()`（**8/8**）+ 新开关 `exit_confirm`
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-044**（已证伪），并**回溯修正 H-042 结论**为上下界表述

---

## 10. 成本与技能

- **本次花费积分估算：0**（AtomCode 全程未得可用推理，纯本地 Read/Grep + 本地 Python 计算）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程）。
  未加载 `币安量化数据通路与黑马策略诊断`（本地 CSV 已在位，不需要下载通路）；
  未加载 `云端四端归档通道`（今日周一，周中不归档）。
- **沉淀 / 迭代**：
  - 新模块 `limit_fill_semantics.py`（可进 lab_bridge，供后续假设复用）
  - `core/backtest.py` 新增 `exit_confirm` 开关 + `selftest_exit_confirm` 8/8
  - `run_nightly_learning.py:REPO_ROTATION` 白名单 `core_file` 第 3 次失真已修
    （`binance_gateway.py` → `linear_gateway.py`）
  - **修 `hypothesis_runner.update_ledger` 的第二次证据覆盖 bug**（D123）：
    新增 `_merge_evidence`（**路径以新为准 / 注释不可丢**）+ `selftest_merge_evidence` **7/7**；
    实测重跑 `--only H-044` 得 `bytes_delta = 0`、`changed = []`、注释 3 条全留。
    ★ 这是**同一个字段第二次咬人**：2026-10-23 只修了「空证据清空」，没修「非空证据冲掉注释」。
  - 方法论沉淀见 [[AI量化平台]] 主索引的本轮更新
- **本轮自己踩的坑（3 条，全记在案）**：
  1. 回归脚本用 `.get("all_ok")` 而真键是 `_all_ok` ⇒ 三模块报 `None` 却仍打印 **"ALL GREEN"（假绿）**
     → 改成「模块未自报结果即判 FAIL」。
  2. 自检里把计数（`0`）塞进断言字典 ⇒ `0 is not True` 造出**假 FAIL**（同类自伤第 3 次）。
  3. 预测 E4/E5 的**方向**（严格档笔数 ≥ 宽松档）——但严格档会改变冷却期，笔数可升可降，
     **方向不是结构保证** → 改成变更测试 + 咬合力自证。**把猜测写成断言，会在真需要它的那天给假红或假绿。**

## 关联

- [[策略假设台账]] · [[AI量化平台]] · [[20261101_vnpy_vnpy_binance]] · [[20261031_vnpy_vnpy_riskmanager]]
