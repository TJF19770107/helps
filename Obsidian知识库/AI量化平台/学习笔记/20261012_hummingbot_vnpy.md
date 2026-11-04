---
日期: 2026-10-12
仓库: hummingbot
核心文件: hummingbot/strategy/pure_market_making/pure_market_making.pyx（c_apply_budget_constraint）· hummingbot/connector/budget_checker.py · hummingbot/core/clock.pyx · hummingbot/strategy/order_tracker.pyx
轮次: 第 6 轮
tags: [AI量化平台, 夜学, 代码拆解, 订单预算, 库存管理, 做市]
---

# 20261012 · hummingbot · 订单预算前置校验 + Clock 双模时钟

## 0. 一句话结论

> hummingbot 把**「余额与手续费」当成一等约束，在下单前逐单预扣**（`c_apply_budget_constraint` 40 行把「含费 + 顺序锁定 + 只缩不放」三件事一次做完）；
> 同时用「一个 `Clock` 两种模式 + 每个迭代器同一个 `c_tick` 接口」把**回测与实盘压成同一条代码路径**。
> → 前者正是我方风控层 **G3/G1** 明确缺失的答案；后者是我方 `core/events.py` **E1（timer 寄生在事件线程）** 的干净解。

---

## 1. 这个文件在系统里管什么（架构定位）

| 精读对象 | 所属层 | 在系统里管什么 |
|---|---|---|
| `strategy/pure_market_making/pure_market_making.pyx` | **策略层** | 纯做市：每 tick 生成报价方案（proposal）→ 施加限价/限价改价/改量/**预算约束** → 撤旧单 → 下新单 |
| `connector/budget_checker.py` | **风控层（前置）** | 订单抵押品校验器：把「本金 + 百分比手续费 + 固定手续费」算全，并按可用余额**缩小或归零** |
| `core/data_type/order_candidate.py` | **工具层/数据层** | 一张「订单意图全集」：本金占用 / 手续费占用 / 含费后所得 |
| `core/clock.pyx` + `core/time_iterator.pyx` | **事件层** | 全系统唯一的时钟：`REALTIME` 用 wall-clock 睡到下一个 tick，`BACKTEST` 用固定步长自增；两者调**同一个 `c_tick`** |
| `strategy/order_tracker.pyx` | **执行层/状态层** | 在途订单账本：活跃限价单 / 影子单（已撤但保留 3 分钟）/ 在途撤单（60s 过期） |

**上下游**
- 上游依赖 → `core/clock.pyx`（时间源）· `connector/*`（余额与费率查询 `c_get_fee` / `c_quantize_order_amount`）
- 下游被谁调用 → `cli/`（启动 clock 与策略）· 各 `strategy/*`（纯做市、Avellaneda、跨所套利…）· `connector/exchange/paper_trade/*`（模拟撮合里复用同一个 BudgetChecker）

---

## 2. 调用链（文字版时序图）

**A. 策略 tick（预算闸在「下单之前」，不是在「报错之后再补」）**
```
Clock.run_til / backtest_til
  → StrategyBase.c_tick(timestamp)                     strategy_base.pyx:286
    → PureMarketMakingStrategy.c_tick()                 pure_market_making.pyx:715
      ├ 1. c_create_base_proposal()                     :766   生成买卖报价草案
      ├ 2. c_apply_order_levels_modifiers()             :~880  限制单数
      ├ 3. c_apply_order_price_modifiers()              :~880  改价
      ├ 4. c_apply_order_size_modifiers()               :886   改量（订单金字塔/深度）
      ├ 5. ★ c_apply_budget_constraint()                :930   ★ 含费 + 顺序扣减 + 只缩不放
      ├ 6. c_filter_out_takers()                        :972   （可选）剔除会吃单的报价
      ├ 7. _hanging_orders_tracker.process_tick()       :756   挂单离价太远则撤 / 超龄则续
      ├ 8. c_cancel_active_orders_on_max_age_limit()    :1177
      ├ 9. c_cancel_active_orders(proposal)             :1188  撤掉不在新方案里的旧单
      └ 10. c_execute_orders_proposal(proposal)         :1247  真正下单
              → StrategyBase.c_buy_with_specific_market()  strategy_base.pyx:478
                  → market.c_buy()                        connector_base.pyx:239
                  → c_start_tracking_limit_order()        strategy_base.pyx:574 → OrderTracker
```

**B. 撤单（顺序锁 / 幂等的样本）**
```
StrategyBase.c_cancel_order()            strategy_base.pyx:554
  → OrderTracker.c_check_and_track_cancel(order_id)   order_tracker.pyx:154
       ├ 若该单「创建事件还没回来」→ 直接拒撤（return False）  ← 防幽灵撤单
       ├ 清理 60s 前的过期撤单记录（CANCEL_EXPIRY_DURATION :27）
       ├ 已在途撤单 → 拒（幂等）
       └ 否则登记在途撤单时间戳 → return True
```

**C. 成交/模拟撮合（含费口径在这里统一）**
```
PaperTradeExchange.c_execute_buy()         paper_trade_exchange.pyx:445
  → order_book.simulate_buy(amount)         :454  用订单簿**逐档吃**得均价
  → OrderCandidate(..., from_total_balances=True) :462
  → BudgetChecker.populate_collateral_entries()  :473  ★ 手续费进入 collateral 与 returns
  → paid_amount(含费支出) / acquired_amount(含费所得) :476-478
  → 余额不足 → 触发 MARKET_ORDER_FAILURE_EVENT   :481
  → 否则 扣 paid / 加 acquired                    :492-495
  → 逐档 OrderFilledEvent + BuyOrderCompletedEvent  :509-525
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 签名/位置 | 职责 | 备注 |
|---|---|---|---|---|
| `BudgetChecker` | 类 | `connector/budget_checker.py:13` | 订单抵押品校验；**顺序锁定** `_locked_collateral` | 单笔/批量两套入口 |
| `BudgetChecker.adjust_candidates` | 方法 | `:38-58` | 批量：开头 reset → 逐个过闸并预扣 → 结尾 reset | ★ D5 的核心 |
| `BudgetChecker.adjust_candidate_and_lock_available_collateral` | 方法 | `:60-80` | 单笔：调整后**立刻锁**，后续订单看不见这笔余额 | — |
| `BudgetChecker._get_available_balances` | 方法 | `:122-146` | `balance_fn(token) − locked[token]`，**每币种只读一次** | ★ 我方曾在此踩坑 |
| `BudgetChecker._lock_available_collateral` | 方法 | `:159-161` | 按 `collateral_dict` 累加锁定 | 同币种**需求金额**相加 |
| `OrderCandidate` | dataclass | `core/data_type/order_candidate.py:17` | 订单意图全集：`order_collateral` / `percent_fee_collateral` / `fixed_fee_collaterals` / `potential_returns` | 文件头明写「不要用本类做 sizing，用 BudgetChecker」 |
| `OrderCandidate.adjust_from_balances` | 方法 | `:82-91` | 依次对三类抵押品做「缩小/归零」 | — |
| `PureMarketMakingStrategy.c_apply_budget_constraint` | 方法 | `pure_market_making.pyx:930-970` | ★★ **策略层**：`quote_size = size*price*(1+fee.percent)`，从运行余额里**逐单扣**，不足则缩量并对齐最小步长 | 40 行做完 D5+D6+D7 |
| `PureMarketMakingStrategy.adjusted_available_balance_for_orders_budget_constrain` | 方法 | `:920` | 钩子：让策略在上述余额上**再扣一笔保留金** | 可被 override |
| `Clock` | cdef class | `core/clock.pyx:16` | 全系统唯一时钟；`ClockMode.REALTIME/BACKTEST` | — |
| `Clock.run_til` | 方法 | `:88-128` | 实盘：`await asyncio.sleep(next_tick − now)`，逐个 `child_iterator.c_tick(t)` | 每个迭代器**被推着走**，不是自己抢 |
| `Clock.backtest_til` | 方法 | `:130-155` | 回测：`_current_tick += _tick_size` 同步循环 | ★ 与 run_til 同 `c_tick` 接口 |
| `TimeIterator` | cdef class | `core/time_iterator.pyx:9` | 所有被时钟驱动的组件基类（`PubSub` 子类）；`_current_timestamp` / `_clock` | `tick()` 供单测手动驱动 |
| `TimeIterator.c_tick` | 方法 | `:22-23` | `self._current_timestamp = timestamp`（默认实现） | ★ 单一时间源 |
| `OrderTracker.c_check_and_track_cancel` | 方法 | `order_tracker.pyx:154-177` | 撤单幂等 + 在途撤单窗口（60s） | 防重复撤单 |
| `OrderTracker.SHADOW_MAKER_ORDER_KEEP_ALIVE_DURATION` | 常量 | `:25` | 影子单保留 `60*3` 秒（等链上确认，防重复补单） | — |
| `HangingOrdersTracker` | 类 | `strategy/hanging_orders_tracker.py:44` | 挂单账本：离价 >`cancel_pct` 撤、超 `max_order_age` 续、**部分成交配对**补对侧 | 库存回收的手工版 |

---

## 4. 可迁移设计点（逐条写「为什么好」）

### D5 · 顺序锁定：一批订单共用一个「递减余额」，而不是各自对「总余额」做判断
`c_apply_budget_constraint`（`pure_market_making.pyx:937-953`）持有 `quote_balance`，每处理一单就 `quote_balance -= quote_size`。
**为什么好**：朴素写法对每一单独立校验「余额够不够」，于是 N 单各自都「够」，合起来超配 —— 这是**批处理的经典漏洞**。
顺序锁定把「批」的语义变成一个**有状态的递减量**，代价是 O(N)、收益是「批内不可能超配」。
**这正是我方 G3「挂单不占持仓额度」的直接解**：挂单必须先扣掉额度，后到的申报才看得见真实剩余。

### D6 · 手续费进「抵押品」，不是进「备注」
`OrderCandidate` 把 `percent_fee_collateral` 与 `fixed_fee_collaterals` 与本金**并列**，并由 `collateral_dict` 聚合同币种。
策略层更直接：`quote_size = buy.size * buy.price * (Decimal(1) + buy_fee.percent)`（`:942`）。
**为什么好**：手续费是**确定要占用的资金**，把它排除在预算之外，等价于「预算里藏着一笔一定会发生的支出」——
止损越近、费率越高，超配越狠（我方 H-005 实测：止损 100 点超配 50%）。**把费当抵押品，问题在源头消失。**

### D7 · 预算闸只做「缩小/归零」，从不放大
`adjust_candidate`（`budget_checker.py:82-105`）只有两条出路：`all_or_none → set_to_zero()` 或 `_quantize_adjusted_order()`（缩量）。
**为什么好**：闸门**天然不可用于「加仓」**，因此不存在「风控闸把仓位放大」的反向风险。与我方风控层血泪规则 #1 同向：
**风险闸只能作用于「增大敞口」方向，减仓/平仓必须无条件放行** —— 否则停机后平不掉自己的仓 = 爆仓加速器。

### D8 · 一个 Clock，两种模式，同一个 `c_tick`
`Clock.run_til`（`:88`）与 `Clock.backtest_til`（`:130`）实现完全不同（一个 `await asyncio.sleep`，一个 `+= tick_size`），
但**调用的是同一个 `child_iterator.c_tick(timestamp)`**；所有组件从 `TimeIterator` 继承，时间只从 `_current_timestamp` 读。
**为什么好**：这是「回测与实盘同源」最省成本的实现方式 —— 不需要抽象出「接口层」，只需要**把时间源收敛到一个对象**。
**同时它解决我方 E1**：timer 不寄生在任何事件消费线程里，而是被 Clock **推着**按 `tick_size` 精确调用 → 事件再忙也不会让定时任务迟。

### D9 · 「在途态」是显式的一等状态，不是靠重试兜
`OrderTracker` 分别维护 `_in_flight_pending_created`（已发单、创建事件未回）、`_in_flight_cancels`（撤单在途，60s 窗口）、影子单（撤后保留 3 分钟）。
撤单前先查「创建事件是否已回」，没回就**拒撤**（`:162-163`）。
**为什么好**：网络世界「下单」不是一个原子动作，而是「已发 → 已回执 → 已生效」三段。
不建在途态，就会写出一串重试逻辑来兜边界，且必然兜不干净（重复下单 / 幽灵撤单）。**把不确定性变成状态，而不是变成分支。**

---

## 5. 可复用代码片段

**片段 1 —— 顺序锁定 + 含费 + 只缩不放（40 行原文精华，`pure_market_making.pyx:937-953`）**
```python
# 来源：hummingbot/strategy/pure_market_making/pure_market_making.pyx:937-953
# 用途：一批买单共用一个递减余额，且余额里已含手续费
base_balance, quote_balance = self.adjusted_available_balance_for_orders_budget_constrain()
for buy in proposal.buys:
    buy_fee = market.c_get_fee(self.base_asset, self.quote_asset,
                               OrderType.LIMIT, TradeType.BUY, buy.size, buy.price)
    quote_size = buy.size * buy.price * (Decimal(1) + buy_fee.percent)   # ★ 含费
    if quote_balance < quote_size:
        adjusted_amount = quote_balance / (buy.price * (Decimal("1") + buy_fee.percent))
        adjusted_amount = market.c_quantize_order_amount(self.trading_pair, adjusted_amount)
        buy.size = adjusted_amount      # 缩到余额上限
        quote_balance = s_decimal_zero
    elif quote_balance == s_decimal_zero:
        buy.size = s_decimal_zero       # 没钱了 → 归零（只缩不放）
    else:
        quote_balance -= quote_size     # ★ 顺序扣减：后面的单看到扣完的余额
proposal.buys = [o for o in proposal.buys if o.size > 0]
```

**片段 2 —— 可用余额「每币种只读一次、同币种需求累加」（`budget_checker.py:122-146` + `order_candidate.py:41-50`）**
```python
# 来源：hummingbot/connector/budget_checker.py:122-146
# 用途：多类抵押品归集到同一币种时的正确读法
def _get_available_balances(self, order_candidate):
    available_balances = {}
    balance_fn = (self._exchange.get_available_balance
                  if not order_candidate.from_total_balances
                  else self._exchange.get_balance)
    if order_candidate.order_collateral is not None:
        token, _ = order_candidate.order_collateral
        available_balances[token] = balance_fn(token) - self._locked_collateral[token]
    if order_candidate.percent_fee_collateral is not None:
        token, _ = order_candidate.percent_fee_collateral
        available_balances[token] = balance_fn(token) - self._locked_collateral[token]  # 只读一次
    for entry in order_candidate.fixed_fee_collaterals:
        token, _ = entry
        available_balances[token] = balance_fn(token) - self._locked_collateral[token]
    return available_balances
```

**片段 3 —— 双模时钟：同接口、两个实现（`core/clock.pyx:104-128` vs `:139-149`）**
```python
# 来源：hummingbot/core/clock.pyx:104-128（实盘）与 :139-155（回测）
# 用途：把「时间源」收敛到一个对象，回测/实盘共用同一套组件
# 实盘
while True:
    now = time.time()
    if now >= timestamp: return
    next_tick_time = ((now // self._tick_size) + 1) * self._tick_size
    await asyncio.sleep(next_tick_time - now)
    self._current_tick = next_tick_time
    for ci in self._current_context:
        ci.c_tick(self._current_tick)          # ★ 同一个接口
# 回测
while not (self._current_tick >= timestamp):
    self._current_tick += self._tick_size
    for ci in self._child_iterators:
        ci.c_tick(self._current_tick)          # ★ 同一个接口
```

**我方落地版本** → `ai_quant_lab/20261012_hummingbot_vnpy/order_budget_guard.py`（自测 **21/21**，`lab_bridge` 零警告加载）

---

## 6. B站学习（本日 30% 权重）

| 项 | 内容 |
|---|---|
| **视频** | ❌ **仍拿不到带 CC 字幕的量化课程**（B站字幕接口需登录态）→ 本轮**降级** |
| **降级替代**（等权补足 30%，来源可核验） | ① hummingbot 官方文档中文镜像（`wuzao.com/p/hummingbot/document/blog/...`）② Avellaneda-Stoikov 策略指南 ③ 库存风险/逆向选择工程文章（`quantrading.space`、`quantmemo.com`） |
| **蒸馏要点** | 见下 |

**要点 1 · 做市的真正风险不是价差，是「库存 + 逆向选择」**
P&L 分解：`P&L = spread_capture + inventory_pnl + fees_rebates − adverse_selection_cost`。
失败模式极清晰：价差端稳定 +$500/天，库存端趋势日 −$2000/天 → 净亏。
**逆向选择检测量**：`picked_off = mean(fill_side × ret_1m)`，持续为正 = 你的报价被「知道方向的人」吃。

**要点 2 · Avellaneda-Stoikov 的两个公式（本轮的「跨领域」增量）**
- 保留价（库存偏移）：`r = s − q·γ·σ²·(T−t)` —— 持多则把整个报价带**下移**，让卖单更容易成交
- 最优价差：`δ = γ·σ²·(T−t) + (2/γ)·ln(1 + γ/κ)`
→ 核心思想一句话：**做市商报的不是「公允价」，是「偏向清库存的保留价」**。

**要点 3 · 落地控制阶梯（生产级做法，从小到大）**
`硬限仓` → `线性软偏移（bid -= k·inventory）` → `临近收盘加 γ` → `波动率自适应价差` → `毒性检测（OFI 为负就撤买盘）`。

**存疑处（待代码验证）**
- 上述 AS 公式全部来自二手科普，**未读原始论文**，也未核实 hummingbot 的 `avellaneda_market_making.pyx` 实现细节（本轮未精读该文件，属未完成项）。
- 「OFI 预测力」文章自报：同期 R²≈0.17 而预测 R²≈0.0003（≈540× 落差）→ 说明**订单流失衡几乎只解释当期**。这条若成立，对我方「拿 taker_buy_volume 做预测因子」（H-002/H-004 结论：不可交易）是**独立侧证**。

---

## 7. 对黑马策略的启发（必须落到具体动作）

| # | 假设 | 怎么验 | 若成立，改哪 |
|---|---|---|---|
| **H-012** | 入场附加「当根量 ≥ 48 根均量」流动性门槛（`vol_ratio ≥ 1.0`）后含成本单笔均值不下降 | `hypothesis_runner.py --only H-012` | 在 `core/strategy.py:201` 的 `entry_signal` 加一项 `& (vol_ratio >= 1.0)` |
| **H-013** | 入场限定 `signal_score == 2`（上一轮归因观察的最优层）后含成本单笔均值不下降 | `hypothesis_runner.py --only H-013` | 在 `core/strategy.py:197` 把 `>= p.min_signal_score` 改为 `== 2` |

**本轮实测结果（两条都证伪，见 §8 与台账）**
- **H-012 → 已证伪（2/4 不下降）**：BTC +0.054 · ETH −0.107 · BNB +0.315 · DOGE −0.066（单位 pp）。
  → 「突破必须带量」是**直觉，不是统计**。门槛只减样本、不提纯。
- **H-013 → 已证伪（1/4，且降幅大）**：BTC −0.312 · ETH −0.485 · BNB +0.046 · DOGE −0.329（pp）。
  → ★ **这是本轮最有价值的一条**：第 4 轮「score=2 层最优」是**同批样本内的归因观察**，
    一旦把它当规则去做独立 A/B 回测就**崩掉** → **典型过拟合**。今后引用归因结论必须附「已过独立回测」标记。

**平台侧动作（下一轮 P0）**：把 D5（顺序锁定）+ D6（含费抵押品）落进 `core/risk.py` 的 R1/R7，
并新增 R8「报单限流」。落点与验收见《AI量化平台_订单预算前置层对标hummingbot设计_20261012》。

---

## 8. 未完成 / 失败区（诚实留痕）

1. **B站 CC 字幕仍未打通**（需登录 cookie）。本轮已用可核验的官方文档中文镜像 + AS 科普补齐权重，但**不是视频学习**，如实标注。
2. **AtomCode 通道本轮正常**：`verdict=healthy`，实测推理 HTTP 200 / 13.8s / `glm5.3-flash` 正常回字；本轮用于**交叉复核**（回复存 `atomcode_reply.md`）。逐条采纳见 §11。
3. **`avellaneda_market_making.pyx` 未精读**（仅读科普），AS 公式未经源码核实。
4. **无 OMS / 无订单簿快照**：`order_budget_guard` 的「净额扣减」只做到「同向未成交挂单」这一层，
   真实占用源（反向挂单 / 部分成交残单 / 在途划转 / 资金费）**尚未纳入** → 见 §11 Q3 清单。
5. **D1~D4（freqtrade 四条）+ G1~G4（nautilus 四条）仍未回填 `core/` 本体** —— 已连续 3 轮挂账，本轮新增 D5~D7，
   下一轮必须真的动手改本体，不能再只出设计。
6. **DOGE 系统性亏损仍未归因**（H-012 的成交量门槛没有救它：DOGE 仍 −0.066pp）。
7. **C 盘剩余仅 0.90GB**（自检告警）—— 会影响 WorkBuddy 文件工具与备份机制。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘路径：`ai_quant_lab/20261012_hummingbot_vnpy/order_budget_guard.py`（自测 **21/21**；`lab_bridge.get("order_budget_guard")` → `loaded=True`，`warnings=[]`）
- [x] ③ 策略假设已追加进 [[策略假设台账]]（H-012 / H-013，跑完后状态已回写为**已证伪**）
- [x] 附：AtomCode 交叉复核 `atomcode_reply.md` · 回测结果 `策略假设/回测结果/回测结果_20261012.json`

## 10. 成本与技能

- **本次花费积分估算：0**（全程本地运算 + AtomCode 免费档 `glm5.3-flash`，未触发 0.01 折）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程）· `币安量化数据通路与黑马策略诊断`（数据口径与回测纪律）
- **没用哪个技能**：`tencent-pptx` / `tencent-docx`（本轮无文档/演示产出需求）；`推荐市场`类技能（无新装需求）
- **沉淀 / 迭代**：`ai-quant-open-source-nightly-learning` v1.1.3 → **v1.1.4**（新增「顺序锁定两坑」与「归因观察须过独立回测」两条纪律）

## 11. AtomCode 交叉复核（本轮新增 · 4 问 4 答摘要）

> 原始回复：`ai_quant_lab/20261012_hummingbot_vnpy/atomcode_reply.md`（HTTP 200 / 13.8s / glm5.3-flash）

| 问 | 它的回答 | 我方采纳 |
|---|---|---|
| **Q1 实盘还缺什么前置条件？** | ① 实时余额源（须有成交回报/PnL 对账钩子，否则锁的是**幻影余额**）② 本地↔交易所状态同步（撤单失败/部分成交/强平都会**预算泄漏**）③ 费率动态性（maker/taker、券扣、滑点，不能取常数） | ✅ 全部采纳，升级为设计文档的 P0 前置 |
| **Q2 顺序锁定在回测里的偏差？** | 回测锁的是「本地名义余额+估算费」，无撮合队列；部分成交/延迟成交/撤单竞争全缺 → **高估预算可用性、低估占用时长**；且锁定顺序=候选列表顺序，实盘由价格竞争决定 → **回测系统性乐观** | ✅ 采纳。这条把我方「回测乐观偏差」的清单又加了一项（第 5 项） |
| **Q3 还有哪些容易漏算的占用源？** | ① 反向挂单（对锁单占用双向额度）② 部分成交残单 ③ 手续费已扣但未成交的资金沉淀 ④ 资金费率/隔夜利息 ⑤ 预估滑点 ⑥ 跨市场/子账户在途划转 | ✅ 采纳为 R7 的扩展清单（按风险排序，反向挂单第一） |
| **Q4 下一轮只做一件事？** | **实时对账 reconcile**：每 tick 比对内存余额 vs 交易所可用余额，偏差超阈值即 Halt 并告警。**验收标准：注入人为余额偏差的故障演练，系统在 1 个轮询周期内自动停机并发出事件** | ⚠️ 采纳但**降优先级**：我方尚无实盘接单通道（无交易所 API 对接），reconcile 无对象 → 登记为「实盘前置」，先做 R7/R8 |

**★ 复核带来的最重要认知**：D5 的顺序锁定**在回测里是「结构上做不到」的**（没有真实挂单簿与撤单竞争），
所以它必须被标注为**实盘增强项**，而不是回测可验证项 —— 这正好解释了为什么我们要把它写进风控层本体而不是回测引擎。

---

*建立：2026-10-12 · 汤小龙 · 第 6 轮夜学（hummingbot #9/12）*
