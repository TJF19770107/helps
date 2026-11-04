---
日期: 2026-10-31
仓库: vnpy/vnpy_riskmanager（主） + vnpy/vnpy_paperaccount（副）
核心文件: vnpy_riskmanager/engine.py (268) + template.py (105) + rules/*.py (298) + tests/test_rules.py (99) · vnpy_paperaccount/engine.py (673) + tests/test_matching.py (188)
轮次: 第 20 轮
tags: [AI量化平台, 夜学, 代码拆解, 风控闸, 拒单语义, 模拟撮合, 限价挂单, 逆向选择]
---

# 20261031 · vnpy_riskmanager + vnpy_paperaccount · 风控闸网关化 / 模拟撮合语义

## 0. 一句话结论
> **风控闸的正确形态是「唯一入口 + 可区分原因码 + 两层闸 + 纯检查」**，vnpy 这四条**一条都没做到**：
> 拦截后 `return ""`（拒因不可区分）、靠 `dict` 插入序 + `glob` 文件序决定规则顺序（同套规则换台机器就换执行序）、
> 全闸统一拦（**日委托上限到顶后连平仓都平不掉**）、`DuplicateOrderRule` **在检查函数里自增计数**（被拒也计、永不衰减 ⇒ 正常策略被永久锁死）。
> 我方 `core/risk.py` 在「减仓豁免」上**已反超**，但在**拒因码 / 逐闸归因计数 / 检查纯度**三项上仍是缺口，本轮做成 `paper_risk_gateway.py`（自测 50/50）。
>
> **撮合侧**：vnpy `cross_order` 用 `if trade_price:` 把「成交价非零」当「成交」判据，用 `if req.price:` 把「字段真值」当「限价单」类型判据（市价单直接绕过市值闸），**恒 `traded = volume` 全量成交**（不看盘口可用量）。
> 顺着这条线做了两条此前从没量化过的假设：**入场挂单折价 = 已证伪（逆向选择）**、**出场挂限价 = 已验证但只是执行改进（+0.20~+0.48pp/笔）**。

## 1. 这个文件在系统里管什么（架构定位）

| 文件 | 所属层 | 职责 |
|---|---|---|
| `vnpy_riskmanager/engine.py` | **风控层**（前置闸） | 动态发现规则类 → 实例化 → **monkey-patch `MainEngine.send_order`**，把风控塞进报单唯一入口 |
| `vnpy_riskmanager/template.py` | 风控层基类 | `active / parameters / variables / check_allowed / on_tick/on_order/on_trade/on_timer` |
| `vnpy_riskmanager/rules/*.py` | 风控层实现 | 5 条规则：日上限 / 活动委托 / 重复报单 / 委托合法性 / 委托规模 |
| `vnpy_paperaccount/engine.py` | **撮合回测层（影子账户）** | patch `subscribe/query_history/send_order/cancel_order/send_quote`，本地撮合 + 持仓记账 |

- **上游依赖** → `vnpy.event.EventEngine`、`vnpy.trader.engine.MainEngine/BaseEngine`、`vnpy.trader.object.*`、`vnpy.trader.constant.Status/Direction/Offset`
- **下游被谁调用** → 策略层（CTA / 组合）**完全不知道风控存在**（这正是 patch 唯一入口的价值）；UI `ui/widget.py` 只读事件
- **一句话分工**：`RiskEngine` 管「**这单能不能发**」，`PaperEngine` 管「**发了之后怎么成交**」。**两者都是通过替换 `MainEngine` 的方法接进去的**——同一个手法，两种命运（见 D91 / D100）。

## 2. 调用链（文字版时序图）

**报单链（风控在前、撮合在后，串成一条）**
```
strategy.buy()
└─ MainEngine.send_order            # ← 已被 patch
     ├─ RiskEngine.send_order        # engine.py:199
     │    ├─ check_allowed(req, gw)  # :207  遍历 self.rules.values()（★ dict 插入序）
     │    │    └─ 任一 rule.check_allowed() 为 False → return False
     │    └─ 拒绝 → return ""        # ★★ 拒因丢失，只剩一条日志 + winsound 蜂鸣
     └─ PaperEngine.send_order       # paperaccount/engine.py:201
          ├─ ORDER_COUNT+1 / 生成 orderid
          ├─ put(EVENT_ORDER)          # 未成交快照
          └─ put(EVENT_PAPER_NEW_ORDER)
               └─ process_new_order_event   # :228
                    ├─ check_order_valid     # :349  类型/数量/可平量 → REJECTED?
                    ├─ status = NOTTRADED → active_orders[sym][oid] = order
                    └─ instant_trade? → cross_order(order, tick)   # :387
                         ├─ LIMIT: price 穿越 → trade_price = 对手价
                         ├─ order.traded = order.volume              # ★ 恒全量
                         ├─ put(EVENT_ORDER) + put(EVENT_TRADE)
                         └─ update_position(trade, contract)         # :484 五情形
                              └─ save_data()                         # ★ 漏存 frozen
```

**事件回流链（风控规则靠它记账）**
```
EVENT_ORDER → RiskEngine.process_order_event → [DailyLimitRule.on_order, ActiveOrderRule.on_order]
EVENT_TRADE → process_trade_event → [DailyLimitRule.on_trade]
EVENT_TICK  → process_tick_event  → [仅在规则**重写**了 on_tick 时才订阅]   # needs_callback :166
```

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `RiskEngine.patch_functions()` | 方法 `engine.py:137-140` | `self._send_order = main_engine.send_order` + `object.__setattr__(...)` | ★ **二次 init 会把已 patch 的 bound method 存成「原始函数」⇒ 无限递归** |
| `RiskEngine.check_allowed(req, gw) -> bool` | 方法 `:207-216` | 遍历 `self.rules.values()`，`active and not check_allowed` 即拒 | ★ 顺序 = dict 插入序 = `glob` 顺序（不稳定） |
| `RiskEngine.send_order(req, gw) -> str` | 方法 `:199-205` | 过闸 → 原函数；不过闸 → **`return ""`** | ★ 空串与「网关异常」不可区分 |
| `RiskEngine.needs_callback(rule, name) -> bool` | 方法 `:166-170` | `getattr(rule,name).__func__ is not getattr(RuleTemplate,name)` | ✅ **正向设计**：没重写就不订阅，省 CPU（见 D92） |
| `RuleTemplate.update_setting(setting)` | 方法 `template.py:46-53` | 仅 `setattr` 命中键，**无范围校验、无重算钩子** | UI 填 0/负数直接生效 |
| `DailyLimitRule.on_order(order)` | 方法 `daily_limit_rule.py:90-108` | 首见记委托；`elif CANCELLED` 记撤单 | ★ **首见即终态**（重启/一次性推终态）⇒ 撤单永久漏记 |
| `DuplicateOrderRule.check_allowed(...)` | 方法 `duplicate_order_rule.py:30-41` | **检查里 `+=1`**，超 `limit` 拒 | ★★ 检查器自污染 + 全历史累计永不衰减 |
| `OrderSizeRule.check_allowed(...)` | 方法 `order_size_rule.py:22-35` | `req.volume > limit` 拒；`if contract and req.price` 才查市值 | ★★ 市价单 `price=0` ⇒ **整条市值闸被绕过** |
| `OrderValidityRule.check_allowed(...)` | 方法 `order_validity_rule.py:12-42` | 合约存在 / pricetick 整数倍 / 数量上下限 | ★ 容差**固定 1e-6**（不与 pricetick 关联） |
| `PaperEngine.cross_order(order, tick)` | 方法 `paperaccount/engine.py:387-435` | 市价/限价/停止价撮合 | ★ `if trade_price:` 判成交；`traded = volume` 全量 |
| `PaperEngine.check_order_valid(order, contract) -> PositionData\|None` | 方法 `:349-385` | FAK/FOK/RFQ/不支持的 STOP → REJECTED；平仓超可平量 → REJECTED | ★ 三种拒因共用一条「不支持的委托类型」日志 |
| `PaperEngine.update_position(trade, contract)` | 方法 `:484-560` | 净持仓/双向持仓记账 | ✅ 净持仓**五情形**显式列举（可迁移，见 §5） |
| `PaperEngine.save_data() / load_data()` | 方法 `:587-617` | 只存 `vt_symbol/volume/price/direction` | ★★ **漏 `frozen`** ⇒ 重启后可平量虚高 |

## 4. 可迁移设计点（10 条 · 逐条写「为什么这么设计更好」）

**D91 拒单必须带可区分原因码。**
vnpy 拦截后 `return ""`（`engine.py:203`）。空串同时意味着「被风控拒」「网关连不上」「参数非法」，策略层**无法归因、无法重试策略、无法统计哪道闸在咬**。
→ 本方 `GateVerdict(ok, code, detail, gate)`：`code` 给机器（`MAX_ORDERS` / `DUPLICATE` / `VALUE_LIMIT`…），`gate` 给归因统计，`detail` 给人。**「False」不是拒单，是失忆。**

**D92 事件订阅按「是否真的重写」决定。**（✅ 正向，直接抄）
`needs_callback` 用 `rule_method.__func__ is not base_method` 判断——没重写 `on_tick` 的规则**一个 tick 都不收**。5 条规则里只有 2 条真需要 `on_order`，其余全程静默。我方 `events.py` 现在是「谁注册谁全收」，可以照此改成**按重写探测订阅**，高频 tick 下省下的就是真金白银。

**D93 闸口顺序必须显式。**
`load_rules_from_folder` 用 `glob("*.py")`（`engine.py:99`）→ **文件系统序不保证稳定**；`self.rules` 是 dict → 顺序 = 插入序。同一套规则换台机器、换个文件系统，执行顺序就可能变。
→ 本方 `self.gates` 是 `(priority, gate, tier, fn)` 列表并 `sort(key=priority)`。**顺序是风控语义的一部分，不能交给 OS。**

**D94 两层闸：结构合法性 vs 敞口限额，**减仓只过前者**。**
vnpy `check_allowed` **不区分开仓/平仓**：`DailyLimitRule` 日委托上限到顶后，**平仓单也一起被拦死**——持仓平不掉的后果比多开一单严重一个量级。
→ 本方：`structural`（合约存在 / pricetick / qty>0 / 市价单参考价）**减仓也必须过**；`exposure`（单笔量、名义价值、日笔数、活动委托、重复）**减仓无条件放行**。
→ 这是本项目铁律 #1「风控只约束增大敞口」在**架构层**的落地。`core/risk.py` 已有 `increases_exposure`，本轮把它从「一个布尔判断」升级为「两层闸编排」。

**D95 检查函数必须是纯的。**（★★ 本轮最狠的反例）
`DuplicateOrderRule.check_allowed` 第一行就 `self.duplicate_order_count[req_str] += 1`（`duplicate_order_rule.py:33`）。
两个后果，都致命：
① **计数与实际发单脱钩**——被前面闸先拒的单因短路**不计**，被自己拒的单**照计**；
② `duplicate_order_limit=10` 是**全历史累计、无 TTL、无衰减**——一个连下 10 次同价同量单的策略（网格 / 追踪止损极常见）**永久锁死**，且它的键里带 `price`，追踪止损每次重定基准价 ⇒ **换个价就绕过**，「该拦的拦不住、不该拦的永久拦死」。
→ 本方 `DuplicateGuard.peek()` 纯查、`commit()` 才记、**时间窗内衰减**、被拒不记。
→ 更普适：**凡「检查」函数有副作用，这个检查就不可信**——它会把「谁先被问到」编码进结果。

**D96 「结果非零」不是「成交」判据。**
`cross_order` 用 `if trade_price:` 判成交（`:416`）。`tick.ask_price_1 == 0`（无盘口 / 涨跌停 / 未初始化）时，市价买成交价退化成 `slippage * pricetick`：slippage=0 则 **trade_price=0 ⇒ 静默不成交**；slippage>0 则**在 0 附近成交**。两条都是灾难且都无声。
→ 判据必须是「**条件是否满足**」（`low <= limit`），成交价单独返回。

**D97 类型判据不能用字段真值。**
`order_size_rule.py:29`：`if contract and req.price:` —— 用「`price` 有值」当「这是限价单」的类型判据。市价单 `price=0` ⇒ **整条名义价值闸被静默跳过**，而这恰恰是最需要限额的那类单。
→ 本方按 `order_type` 分流；市价单用 `ref_price` 估值，**缺参考价一律 fail-closed 拒绝**（`MISSING_REF`）。
→ 普适：`if x:` 是「真值判断」，**永远不要拿它当类型/枚举判断**。

**D98 容差必须随粒度缩放，且粒度=0 时容差=0。**
`order_validity_rule.py:28` 固定 `1e-6`。pricetick=0.01 时相对误差 1e-4，勉强能看；**pricetick=1e-8（山寨币常见）时 1e-6 = 100 倍 pricetick ⇒ 形同不校验**。
→ 本方 `tick_tolerance(pricetick) = pricetick × 1e-3`，`pricetick <= 0 ⇒ 0`（**不做伪校验**）。
→ 与第 13 轮 `tolerance_for_precision` 同族：**绝对容差是伪安全，容差必须绑粒度**。

**D99 撮合器必须知道「可用量」。**
`cross_order` 恒 `order.traded = order.volume`（`:418`），**完全不看 `tick.ask_volume_1`** ⇒ 深度不足时 100% 成交。
→ 本方 `tradable_capacity(order_qty, avail_qty) -> (可成交量, 是否部分)`；`avail <= 0 ⇒ 0`（**不是**「按全量成交」）。
→ 这与第 12 轮 freqtrade「二元成交是行业上限」互补：**二元成交可以接受，但「无深度概念」不行**。

**D100 模拟层不得原地改上游对象；持久化必须覆盖状态机用到的全部字段。**
`process_tick_event` 直接 `tick.gateway_name = GATEWAY_NAME`、`process_contract_event` 直接改 `contract.gateway_name`（`:129` / `:117`）—— **污染上游对象**，同一个 tick 后续被别的组件读到，「CTP」已被洗成「PAPER」。这与第 14 轮挂账的 `hummingbot paper_trade_exchange.pyx:127-140` 盘口污染**同形**，两处独立出现 ⇒ 是**通用反模式**，不是个例。
`save_data` 只存 4 个字段、**漏 `frozen`**（`:596-601`），而 `check_order_valid` 用 `volume - frozen` 判可平量 ⇒ **重启后可平量虚高**，平仓单会被错误放行。
→ 本方：模拟层一切写入前先 `copy`；持久化字段清单 `_LIVE_STATE_FIELDS` 与状态机同源，`missing_persisted()` 直接比对。

## 5. 可复用代码片段

**① 净持仓成本账的五情形（`paperaccount/engine.py:489-521` 的可复用提炼）**

vnpy 这段**是对的**，而且它的分支覆盖比大多数实现都全 —— 值得抄的是「**显式列举五种情形**」这个写法：
部分减仓**不改均价**、翻向**重置**而不是加权、归零**清价**（否则下次建仓会用旧成本）。
本项目 `core/backtest.py:_position_from_trades` 有「出场当根再入场 1 根误差」（P2 挂账），可直接用这套情形表对照自查。

```python
# 来源：vnpy/vnpy_paperaccount/vnpy_paperaccount/engine.py:489-521（净持仓分支）
# 提炼：ai_quant_lab/20261031_vnpy_vnpy_riskmanager/paper_risk_gateway.py:PositionCostBook
def apply(self, qty_delta: float, price: float) -> dict:
    old_v, old_p = self.volume, self.price
    new_v = old_v + qty_delta
    if new_v == 0:                                   # 1) 归零 → 清价
        self.volume, self.price = 0.0, 0.0
    elif (new_v > 0 and old_v < 0) or (new_v < 0 and old_v > 0):   # 2) 翻向 → 重置
        self.volume, self.price = new_v, float(price)
    elif old_v == 0:                                 # 3) 建仓
        self.volume, self.price = new_v, float(price)
    elif (old_v > 0 and qty_delta > 0) or (old_v < 0 and qty_delta < 0):  # 4) 同向加仓 → 加权
        self.volume = new_v
        self.price = (old_v * old_p + qty_delta * price) / new_v
    else:                                            # 5) 同向减仓 → 均价不变
        self.volume = new_v
```

**② 限价成交价（含「价格改善」分支，`paperaccount/engine.py:400-406` 的 bar 版扩展）**

```python
# 来源：vnpy/vnpy_paperaccount/vnpy_paperaccount/engine.py:400-406（LIMIT 分支）
#       成交价取 tick.ask_price_1 / bid_price_1 —— 比挂单价**更优**（价格改善）
# 提炼：ai_quant_lab/20261031_vnpy_vnpy_riskmanager/paper_risk_gateway.py:limit_fill_price
def limit_fill_price(limit, side, open_px, high, low) -> tuple[float, bool]:
    """返回 (成交价, 是否价格改善)；成交价 0.0 = 未成交。"""
    if side > 0:
        if open_px > 0 and open_px <= limit:
            return float(open_px), True        # 开盘已在限价下方 → 按开盘（改善）
        return (float(limit), False) if low <= limit else (0.0, False)
    if open_px > 0 and open_px >= limit:
        return float(open_px), True
    return (float(limit), False) if high >= limit else (0.0, False)
```

**③ 按需订阅（`riskmanager/engine.py:166-170`，✅ 正向，建议抄进 `core/events.py`）**

```python
# 来源：vnpy/vnpy_riskmanager/vnpy_riskmanager/engine.py:166-170
def needs_callback(rule, method_name: str) -> bool:
    """规则没重写该方法就不订阅 —— 5 条规则里只有 2 条收 on_order，其余全程静默。"""
    return getattr(rule, method_name).__func__ is not getattr(RuleTemplate, method_name)
```

## 6. 对各黑马策略的具体动作

| # | 动作 | 落点 | 验什么指标 |
|---|---|---|---|
| 1 | **拒绝语义**：`risk.py` 的 `blocked_rules` 从「字符串日志」升级为 `GateVerdict(code, gate, detail)`，回测状态里按 code 分桶 | `quant_app/core/risk.py` | 回测 `LAST_RISK_STATS["by_gate"]` 非空即可归因 |
| 2 | **减仓豁免升级为两层闸**：结构闸对减仓不豁免、敞口闸对减仓全豁免 | `core/risk.py` + `paper_risk_gateway.RiskGateway` | 已有 `risk` 自测 24/24 不得退化；新增「日上限到顶仍能平仓」用例 |
| 3 | **检查纯度**：所有 `check_*` 函数禁止写状态；有副作用的改 `peek/commit` | `core/risk.py` | 同一请求连续 `check` 3 次结果必须一致 |
| 4 | **出场改限价挂单（H-042）**：`core/backtest.py` 加 `exit_limit_premium` 开关（默认 0 = 旧语义零退化） | `core/backtest.py` | 默认关时权益曲线逐点零退化；开时 `exit_limit_fills / exit_limit_misses` 两个计数器都非零 |
| 5 | **入场挂单折价（H-041）判死**：不再投入，实盘若在挂折价单应改回市价或极浅折价（≤0.1%） | 实盘参数 | 成交率 ≥90% 档（d=0.1%）的 Δ 只有 +0.14/−0.09/+0.04/−0.00 ⇒ 不值得 |

## 7. B站学习（本日 30% 权重）

- **本轮实质产出 0** —— 第 10 轮已结案：B 站字幕接口对该批量化课程**恒返回空**，永久降级为「标题级清单」，不再记入未完成区。
- **替代（同族交叉阅读）**：用 `tests/test_rules.py`（99 行）+ `tests/test_matching.py`（188 行）做交叉验证 ——
  这不是「看视频」的等价物，但它做了视频做不到的事：**把「设计意图」钉成断言**。本轮 §4 的 D95 / D96 两条，
  正是「测试断言证明作者确实这么想」的直接证据（例：`assert trades[0].price == 3499` 而挂单价 3500，
  坐实「限价单按对手价成交」= 价格改善，这条断言是 H-041/H-042 的语义依据）。

## 8. 未完成 / 失败区（如实）

| 项 | 状态 | 原因 |
|---|---|---|
| **AtomCode 13460 推理** | ❌ **连续第 10 轮失败** | `/health` 200 + `logged_in=true`（到期 2026-10-26，本轮未报 403）→ **最小推理 240s 超时 HTTP=0**。非额度、非二进制（v5.2.3 第 13 轮已验）⇒ 上游推理层僵死。降级本地 Read/Grep，**0 积分** |
| **轮转仓库 `vnpy/vnpy_portfoliobacktester`** | ❌ 仓库不存在 | 镜像下 main/master 双 404，同镜像 `portfoliostrategy` 200 ⇒ 排除镜像故障。→ 已替换为 `vnpy_riskmanager`（**白名单第 2 次勘误已修表**） |
| **`ghfast.top` 镜像** | ❌ 000 | 本轮该域名不可达；`ghproxy.net` 正常（200），继续用 ghproxy |
| **H-042 资金复用效应** | ⚠️ 未建模 | 单笔口径条件换价，未成交样本占用资金的机会成本没算 ⇒ Δ 是**上界** |
| **H-042 实盘可成交性** | ⚠️ 未直接验证 | 只引 H-026「排队不紧 V/Q 中位 12155×」作旁证，没有 post-only 撤单率数据 |
| **入场折价 + 出场加价联合** | ⚠️ 未测 | 两条单独测了，组合效应（入场也挂单 → 进出都占时间）没跑 |
| **`core/backtest.py` 出场限价开关** | ⚠️ 未落地 | 本轮只做「独立复刻验证」，引擎开关留到下一轮（默认关零退化需逐点比权益曲线） |
| **B 站 30% 权重** | ⚠️ 实质 0 | 第 10 轮已结案降级（见 §7） |

## 9. 三条实测数字（别记错）

1. **H-041 已证伪**：入场挂单折价 **d=0.3% 档 3/4 标的劣于全样本基线**（BTC −0.6739 / ETH −0.8226 / BNB −0.5177 / DOGE +0.1070pp），且 3/4 标的「折价越深→净单笔越差」单调（BTC 2.2895→1.4782→0.2972）。**能成交的恰是要跌的，好单全跑掉**。
2. **H-042 已验证（执行改进，非 alpha）**：出场挂 `close×(1+e)` 限价，**12/12 格 Δ 全正**（+0.2009~+0.4791pp，中位 **+0.4039pp**），成交率 73.3~97.6%；**未成交样本 12/12 格差于基线**（最差 −1.7962pp）。Δ 含「限价不付 0.05% 滑点」的机械成分。
3. **模块自测 50/50**，`lab_bridge.get("paper_risk_gateway")` 加载成功、**零警告**。

## 10. 本轮踩的坑（写给自己）

1. **时序错置造出假改善**：出场限价单首版挂在**触发 bar 的开盘**（用 `close[j-1]` 当参考价），等于**提前知道 j 是止损 bar** → BTC +1.19pp / DOGE +1.40pp，好到不像话。改成「决策在 j 收盘后、挂单 j+1 生效」落到 +0.32pp。**数字太好先查时序，别先庆祝。**
2. **分母不同源**：入场折价用「成交样本的基线」比，得出「改善 +0.58pp」；换成**全样本基线**立刻变 −0.67pp。成交样本已被逆向选择筛过，它自己的基线本来就低。**这是「两边不同源 ⇒ 这个数没有意义」的第 N 次复现。**
3. **量纲（第 3 次）**：keep 过滤把「绝对 bar 索引 `used`」和「持仓时长 `hold_bars`」直接比 → 96% 样本被误杀、成交率假报 **6.25%**。之后又靠一次打印才确认 `open_time` 与 `exit_time` 都是**秒**。**判据比较前先打印两边单位。**
4. **接口不同形**：`paper_risk_gateway.limit_fill_price` 返回 `(价, 是否改善)` 元组，本地兜底返回标量 → `if px > 0` 直接 `TypeError`。**两份实现必须包一层对齐签名**，别指望「记得」。
5. **断言自己写错两次**：① `100.0 + 1e-7` 拿去当「1e-8 粒度的越界样本」，其实它是 10 个整 tick（合法）；② `bound method` 每次访问都新建对象，`is` 比较恒 False。**断言错 = 假 FAIL 或假 PASS，同一个坑的两面。**
6. **变量定义被自己的第二次编辑吃掉**：`unfill_worst` 在我替换代码块时被删掉，运行器报 `name not defined` → 落「搁置」。**行为是对的（执行失败≠证伪），但暴露「连续编辑同一段代码必须重跑一次全路径」。**
7. **台账证据被运行器静默覆盖**：`update_ledger` 只写 `verdict.evidence`（=结果路径），把手写的详细证据抹掉（bytes_delta −448 / −586）。→ 已做**合并**（模块路径 + 结果文件 + 关键数）。**同一列有两个作者时，后写的那个永远赢。**

## 11. 关联件

- 落地模块：`ai_quant_lab/20261031_vnpy_vnpy_riskmanager/paper_risk_gateway.py`（50/50）
- 任务卡：`ai_quant_lab/20261031_vnpy_vnpy_riskmanager/TASK_CARD.md`
- 假设：`策略假设/H-041`（已证伪）· `H-042`（已验证）
- 回测结果：`策略假设/回测结果/回测结果_20261031.json`
- 平台设计：[[AI量化平台_风控闸网关于模拟撮合语义对标vnpy_riskmanager设计_20261031]]
- 前序同类：[[20261030_vnpy_vnpy_portfoliostrategy]]（H-039/H-040）· [[20261027_vnpy_vnpy]]（H-031 费率口径）
