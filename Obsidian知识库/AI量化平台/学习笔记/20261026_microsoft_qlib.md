---
日期: 2026-10-26
仓库: microsoft/qlib
核心文件: qlib/backtest/exchange.py（958 行）+ account.py（417 行）
轮次: 第 15 轮
tags: [AI量化平台, 夜学, 代码拆解, 成本模型, 手续费档位, lot粒度]
---

# 20261026 · microsoft/qlib · `qlib/backtest/exchange.py`（成本层）

## 0. 一句话结论

> **qlib 的 Exchange 教会我一件事：费率不是世界常数，是可参数化输入 —— 所以正确的问法不是「费率是多少」，
> 而是「这策略最多能承受多少」。今天量出来：BTC/ETH/BNB 的盈亏平衡费率 r\* > 1%（= taker 的 10 倍以上），
> DOGE r\* = 0.335%（3.35 倍）。⇒ 第 14 轮那句「资源必须转到让真实成本更低」，
> ROI 天花板比原先以为的低得多 —— 因为对 3 只标的来说，手续费根本不是生死线。**

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：**撮合回测层的「交易所替身」** —— 它同时扮演四个角色：
  1. **行情源**（`quote_df` / `NumpyQuote`：把 `$close/$volume/$factor` 缓成可 O(1) 取的数组）
  2. **可交易性判定**（涨跌停 `limit_buy/limit_sell`、停牌 `$close is NaN`）
  3. **撮合器**（`deal_order`：量裁 → 取整 → 现金裁定 → 算费）
  4. **成本模型**（`open_cost/close_cost/min_cost/impact_cost` 四件套）
- **上游依赖**：
  - `qlib/data/data.py:D.features()` → 取字段
  - `qlib/config.py:C` → 全局默认（`trade_unit` / `limit_threshold` / `deal_price`）
  - `qlib/backtest/high_performance_ds.py:BaseQuote` → 高性能取数实现（`NumpyQuote` / `PandasQuote`）
- **下游被谁调用**：
  - `qlib/backtest/executor.py:BaseExecutor.trade_cal` → **唯一实际调用 `deal_order` 的地方**
  - `qlib/backtest/account.py:Account.update_order` → 接 `(trade_val, trade_cost, trade_price)` 三件套
  - `qlib/backtest/position.py:BasePosition.update_order` → 真正扣现金/记成本
  - `qlib/backtest/decision.py:OrderHelper` → 拿 `exchange` 反算「目标仓位 → 委托量」

> ★ **注意架构差异**：qlib 把「成本」和「撮合」**放在同一个对象里**（Exchange）。
> 我们的 `core/backtest.py` 也是这么做的（`fee_rate` + `slip_price` + `quantize_qty` 同文件）。
> 两边都选了「简单优先」，代价是**成本模型不可替换**（想换 maker/taker 分档要改主循环）。
> 这是今天第一个「要不要重构」的判断点 —— 结论：**暂不重构**，理由见 §4-D60 的落地方式（外挂模块而非侵入主循环）。

## 2. 调用链（文字版时序图）

```
[策略]
  └─ decision.py:OrderHelper.create_orders_by_target_pos()        # 目标仓位 → 委托量
       └─ exchange.generate_order_for_target_amount_position()    # ← 本文件 611
            ├─ is_stock_tradable() → check_stock_suspended()      # 停牌
            │                     → check_stock_limit()           # 涨跌停（按方向）
            ├─ get_real_deal_amount()  ← ★ 清仓豁免 lot 取整（604-605）
            └─ random.seed(0) + shuffle(ids)                      # 固定打乱 → 可复现
  ↓  返回 sell_order_list + buy_order_list（★ 先卖后买）
[执行器] executor.py:BaseExecutor.trade_cal()
  └─ exchange.deal_order(order, trade_account, position, dealt_order_amount)   # ← 421
       ├─ check_order()                                           # 不可交易 → deal_amount=0, 返回 (0,0,nan)
       └─ _calc_trade_info_by_order()                             # ← 859 核心六步
            ① get_deal_price()                                    # 取成交价（缺→回退 close）
            ② total_trade_val = 当根 volume × deal_price           # 冲击成本的分母
            ③ order.deal_amount = order.amount                    # 先设满额
            ④ _clip_amount_by_volume()                            # ★ 量裁（cum 要减已成交额）
            ⑤ adj_cost_ratio = impact_cost × (成交额/总量)²        # ★ 平方冲击
            ⑥ 按方向算 cost_ratio = open_cost|close_cost + adj
               · SELL：按持仓夹断 + 取整（除非全平）+ 现金不得为负
               · BUY ：现金三档判定（不够费 / 不够钱 / 够钱）+ 取整
            ⑦ trade_cost = max(trade_val × cost_ratio, min_cost)   # ★ 两段式
               trade_val ≤ 1e-5 → trade_cost = 0                   # 没成交不收费
[账户] account.py:update_order()
  ├─ SELL：先 update_state_from_order（此时持仓还在）再 update_position
  └─ BUY ：先 update_position 再 update_state_from_order
       （★ 顺序不同，因为卖出会清空该标的的价格记录）
```

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `Exchange.__init__(..., open_cost=0.0015, close_cost=0.0025, min_cost=5.0, impact_cost=0.0, **kwargs)` | 构造 | 一次配齐四类成本 | `trade_unit` 走 `kwargs`，为的是**区分「未设置」与「显式禁用」**（`exchange.py:109-112` 注释明说） |
| `schedule_cost`（我们新增）↔ `exchange.py:948` | 纯函数 | `max(trade_val×rate, min_cost)` | ★ 两段式；小单有效费率被放大 |
| `critical_trade_value`（我们新增）↔ `exchange.py:850` | 纯函数 | `min_cost/rate` | qlib 版本 `+min_cost` 是因为它判「现金」不是「成交额」 |
| `impact_rate`（我们新增）↔ `exchange.py:892` | 纯函数 | `impact_cost×(tv/total)²` | ★ 平方，不是线性 |
| `deal_order(order, trade_account=None, position=None, dealt_order_amount=defaultdict(float))` | 方法 | 撮合单笔委托 | 返回 `(trade_val, trade_cost, trade_price)`；**会原地改 `order.deal_amount`** |
| `_calc_trade_info_by_order(order, position, dealt_order_amount)` | 私有 | 六步撮合核心 | 步骤见 §2 |
| `_clip_amount_by_volume(order, dealt_order_amount)` | 私有 | 按当期成交量截断 | ⚠️ 返回 `Optional[float]` 但**恒返回 None**，靠原地改 `order.deal_amount` |
| `round_amount_by_trade_unit(deal_amount, factor)` | 方法 | `(amount×factor+0.1)//unit×unit/factor` | ★ `+0.1` 是浮点容差，不是魔法数 |
| `get_real_deal_amount(current, target, factor)` | 方法 | 目标-当前差额再取整 | ★ `target==0 → return -current`（**清仓豁免**） |
| `_get_buy_amount_by_cash_limit(trade_price, cash, cost_ratio)` | 私有 | 现金不足时的最大可买量 | ★ 两段式闭式解，见 §4-D60 |
| `Account.update_portfolio_metrics()` | 方法 | 逐 bar 记 `return_rate` | ⚠️ `return_rate = (earning+cost)/last_value` ⇒ **实为毛收益** |

## 4. 可迁移设计点（D60~D66，逐条写「为什么好」）

### D60 · 两段式最低佣金 + 临界额闭式解（qlib `exchange.py:848-857`、`947-951`）

```python
trade_cost = max(trade_val * cost_ratio, self.min_cost)
# 现金约束下的最大可买量，分两段：
critical_price = self.min_cost / cost_ratio + self.min_cost
if cash >= critical_price:  max_amount = cash / (1 + cost_ratio) / price   # 线性区
else:                       max_amount = (cash - self.min_cost) / price   # 固定区
```

**为什么这么设计更好**：纯百分比费率会让「$10 的单」和「$10 万的单」享受同一个费率，
而现实里**券商的每笔最低 5 元佣金**会让小额单的有效费率膨胀到 3%~5%。
qlib 把它写成**闭式解**而不是迭代试算 —— 因为两段函数的断点可以解析求出（`tv* = min_cost/rate`），
求出来之后就能在 `O(1)` 内算「这笔钱最多能买多少」，不必二分。
⇒ **可迁移性**：币安现货没有最低佣金（我们 `min_cost=0`），但**“固定成本”在数学上同形** ——
通道费、最小滑点、转账费都是「每笔一个绝对数」。所以这个函数在我们平台里不是死代码，
它的真正用途是**回答「单笔要多大，固定成本才不占主导」**。

### D61 · 平方冲击成本（`exchange.py:886-892`）

```python
adj_cost_ratio = self.impact_cost * (trade_val / total_trade_val) ** 2
```

**为什么这么设计更好**：我们平台一直用**线性**参与率（`volume × participation`）。
线性假设说「吃掉 10% 成交量 = 5% 的量冲击的一半」，平方假设说「只占 1%」。
真实市场介于两者之间，但**方向明确**：流动性越薄，边际冲击越陡。
qlib 选平方（Almgren-Chriss 的简化式），代价是对小单**低估**冲击、对超大单**不低估**。
⇒ **对我们的意义**：黑马策略是 15m 级别、$10k 规模、单笔占当根成交量百万分之一量级
（第 13 轮标定 P99 参与率极低）。在这个量级上**线性与平方都≈0**（第 13 轮 H-025 已实测 Δ=+0.0000pp）。
所以这条**不是缺口，是边界确认**：冲击模型只在「资金上到 $1M+」时才需要换平方。

### D62 · 清仓豁免 lot 取整（`exchange.py:597-609`、`761-784`）

```python
def get_real_deal_amount(self, current_amount, target_amount, factor=None):
    if current_amount == target_amount:  return 0
    elif current_amount < target_amount: return round_by_unit(target - current)
    else:
        if target_amount == 0:  return -current_amount      # ★ 全平不做 lot 取整
        return -round_by_unit(current - target)
```

**为什么这么设计更好**：如果平仓也按 lot 取整，那么「持仓 0.0015、lot 0.001」永远只能卖 0.001，
剩下 0.0005 变成**永远平不掉的幽灵仓位** —— 而这在实盘里根本不存在（交易所允许卖出全部余额）。
qlib 用一个 `if` 就把「部分调仓」和「清仓」分开，语义极干净。
⇒ **我们平台已天然对齐**：`core/backtest.py` 平仓走整仓卖出，不经过 `quantize_qty`。
今天**验证过**（读码 + `$1` 本金实测：平仓没有残留），记作「已对齐项」而非缺口。

### D63 · 毛净字段名必须自证 —— qlib 自己踩的坑（`account.py:283`）

```python
return_rate=(now_earning + now_cost) / last_account_value,
# 第 284 行注释写："here use earning to calculate return, position's view, earning consider cost, true return"
```

**这里注释和代码是矛盾的**：`now_earning = now_account_value - last_account_value`，
而 `now_account_value` 里的现金**已经扣过手续费**（`position.update_order` 扣的）。
所以 `earning` 已含成本，`earning + cost` 是**把成本加回去** ⇒ 这个叫 `return_rate` 的字段**其实是毛收益率**。

**为什么单列这一条**：这是我们**第 9 轮踩过的同一个坑**（`pnl_pct` 不含手续费却被当含成本用，
乐观 0.2041pp/笔）。qlib 是微软出品、被引上万次，照样在这件事上把注释写反了。
⇒ **教训升级**：光加一个 `net_xxx` 字段**不够** —— 毛字段名必须显式带 `gross_`。
本平台 `core/report.py` 第 78-86 行已经是 `毛账(含滑点)` / `净账(含手续费)` 强制并列 + `fee_drag_pp` +
`cost_dominated` 三件套 ⇒ **这一项我们已经反超 qlib**，不是缺口。

### D64 · 先卖后买 + 固定种子打乱（`exchange.py:633-639`、`677`）

```python
sorted_ids = sorted(set(list(current_position) + list(target_position)))
random.seed(0); random.shuffle(sorted_ids)      # ★ 固定种子 → 可复现
...
return sell_order_list + buy_order_list          # ★ 先卖后买（现金释放）
```

**为什么这么设计更好**：多标的调仓时「先买后卖」会因现金不足被误拒 ——
卖单没成交，买单就没钱。qlib 用**顺序**解决现金耦合，而不是搞两阶段结算。
而 `random.seed(0)` 是必要的：`set` 的迭代顺序是不确定的，
不固定种子的话**同样的参数跑两次结果不同**（qlib 自己在注释里解释了这一点）。
⇒ **对我们的意义**：黑马策略是单标的，不涉及此问题。但 `quant_app/core/scanner.py` 全市场扫描时
**多标的并发**会撞同一个问题。记作 P2 待办（当前 scanner 不落单，只出信号，暂无风险）。

### D65 · ★★★ 「单笔均值」是幸存者偏差的放大器（今天实测，不是抄来的）

qlib 没有这条 —— 这是今天回测打出来的。H-030 的 `$10` 本金档：

| BTCUSDT `$10` 本金 | 笔数 | 净额单笔均值 |
|---|---|---|
| lot 关闭 | 129 | 2.1521% |
| lot 开启（23836 次归零） | **42** | **6.5311%** |

**粒度约束砍掉 67% 的信号，单笔均值反而涨了 +4.379pp。**
如果只看「净额单笔均值」，会得出「加粒度限制能提升 4.4pp」的**荒谬结论** ——
而真相是：被砍掉的 87 笔里**赢的和输的一起被砍**，剩下 42 笔恰好运气好。
总收益从 +438.9% 掉到几乎为零（42 笔 × 6.5% 且复利被中断）。

⇒ **纪律升级**：任何「单笔均值改善」都必须同时报 **笔数** 与 **总收益**。
三者缺一，结论作废。这条与第 10 轮「胜率 19%→51% 而单笔均值 2.006%→0.2275%」是同一类陷阱的两个变体。

### D66 · 测试顺序：先证明开关能咬，再验效果（今日踩坑复盘）

H-030 首跑用 `CASH_GRID = (100, 300, 1000, 10000)`，**16 格全 0** → 只能判「搁置」。
问题不是结论错，是**测试设计错**：$100 本金 × 95% ÷ BTC@$60k 最小一手 $60 ⇒ 根本够得着，
当然不归零。改成 `(1, 5, 10, 50, ...)` 之后，`$1` 档 42827 次归零、129 笔全灭 ⇒ **机制立刻现形**。

⇒ **纪律**：约束类开关的验收必须三段齐全：
① **能咬**（极值档下咬合力 > 0）② **咬得合理**（中间档咬合力 ∈ (0,100%)）③ **真实档不咬**
（业务规模下无影响）。**只有 ③ 没有 ①，那个 ③ 是假的。**

## 5. 可复用代码片段

```python
# 来源：microsoft/qlib qlib/backtest/exchange.py:848-857 + 947-951
# 落地：ai_quant_lab/20261026_microsoft_qlib/fee_schedule_model.py（30/30 自测）
import math

def schedule_cost(trade_val: float, rate: float, min_cost: float = 0.0) -> float:
    """单边成本 = max(成交额×费率, 最低佣金)。tv<=0 或 rate<0 → 0（没成交不收费）。"""
    if trade_val <= 0.0 or rate < 0.0:
        return 0.0
    return max(trade_val * rate, min_cost)


def critical_trade_value(min_cost: float, rate: float) -> float:
    """两段式临界成交额：低于此额走固定成本区。rate=0 → inf。"""
    if min_cost <= 0.0:
        return 0.0
    if rate <= 0.0:
        return math.inf
    return min_cost / rate


def effective_rate(trade_val: float, rate: float, min_cost: float = 0.0) -> float:
    """有效费率 = 成本 / 成交额。小单会被最低成本放大。"""
    return schedule_cost(trade_val, rate, min_cost) / trade_val if trade_val > 0 else 0.0


def impact_rate(impact_cost: float, trade_val: float, total_trade_val: float) -> float:
    """平方冲击（qlib 原式）：ic × (tv/total)²；total 缺失退化为 ic。"""
    if impact_cost <= 0.0:
        return 0.0
    if total_trade_val <= 0.0:
        return impact_cost
    share = max(0.0, min(1.0, trade_val / total_trade_val))
    return impact_cost * share * share
```

```python
# 来源：同上 · 二分求盈亏平衡费率（本平台新增，qlib 没有）
def breakeven_rate_by_bisect(evaluate, lo=0.0, hi=0.02, tol=1e-6, max_iter=40):
    """在真实回测上二分求 r*（使 evaluate(r)==0）。evaluate(lo)>0>evaluate(hi) 否则返回 None。
    ★ None 不代表证伪 —— 只代表「r* 不在区间内」或「费前就不赚」。"""
    f_lo, f_hi = float(evaluate(lo)), float(evaluate(hi))
    if not (f_lo > 0.0 > f_hi):
        return None
    a, b = float(lo), float(hi)
    for _ in range(int(max_iter)):
        m = (a + b) / 2.0
        fm = float(evaluate(m))
        if abs(fm) <= tol or (b - a) <= tol:
            return round(m, 8)
        a, b = (m, b) if fm > 0.0 else (a, m)
    return round((a + b) / 2.0, 8)
```

## 6. B站学习（本日 30% 权重 · 按 2026-10-20 结论永久降级为标题级）

| 标题 | 链接 | 判断 |
|---|---|---|
| 【全298集】B站最用心最全的Python量化交易教程,2025年最新版 | `bilibili.com/video/BV1D52CBREpX/` | 营销型合集（"学不会我退出IT界"），298 集不可能有深度 |
| 【量化交易教程】全100集 清华大佬…系统python金融分析与量化交易实战 | `bilibili.com/video/BV1Zi6AYjEG8/` | 营销型（"评论区领取资料"），内容大概率是 pandas 基础 |
| 【2026新版】Python金融量化教程：时间序列预测分析到回归分析 | `bilibili.com/video/BV14mrsBQEbh/` | 偏 ML 因子侧，与本平台当前阶段（成本模型）无交集 |

**蒸馏要点**：三条都是**引流型合集**，不是工程实现课。对本轮「费率档位 / 撮合成本」零增量。
**结论**：B 站这条线**继续降级**，不投入时间；等需要「ML 因子挖掘」时再回来（对应 qlib/workflow 那条线）。
**存疑处**：无（未获取字幕，不做任何内容级判断）。

## 7. 对黑马策略的启发（必须落到具体动作）

### 7.1 H-029 实测：盈亏平衡费率 r\*（4 只标的，2.4~5.3 分钟/轮）

| 单边费率 | BTCUSDT | ETHUSDT | BNBUSDT | DOGEUSDT |
|---|---|---|---|---|
| 0（纯毛额） | +2.3567% | +2.3730% | +2.3173% | +0.6738% |
| **0.1%（当前）** | **+2.1521%** | **+2.1683%** | **+2.1128%** | **+0.4726%** |
| 0.2% | +1.9477% | +1.9639% | +1.9085% | +0.2715% |
| 0.5% | +1.3357% | +1.3518% | +1.2967% | **−0.3304%** |
| 1.0% | +0.3198% | +0.3357% | +0.2812% | **−1.3296%** |
| **r\*** | **> 1%（>10×）** | **> 1%（>10×）** | **> 1%（>10×）** | **0.3354%（3.35×）** |
| 费率吃掉 pp | 0.2046 | 0.2047 | 0.2045 | 0.2012 |

**三条读法（必须一起读）**：
1. **`费率吃掉 pp` 四只全部落在 0.2012~0.2047** —— 与第 9 轮记的 **0.2041pp/笔** 完全吻合。
   这是一个**口径自洽性验证**：相隔 7 轮、两次独立实现，数字对得上 ⇒ 旧口径可信。
2. **BTC/ETH/BNB 的 r\* > 1%，即「费率涨 10 倍也不亏」** ⇒ 对这三只标的，
   「降费（maker/BNB抵扣/VIP阶梯）」的**边际收益 ≈ 0**。第 14 轮把资源押在「真实成本」上，
   **今天量出来这个赛道的天花板极低**。这是对我自己上一轮结论的**收窄**（不是推翻：
   手续费确实是最大的**单项**成本，但它**不是**瓶颈）。
3. **DOGE 是唯一有改善空间的**：r\* = 0.3354%（3.35× taker），0.5% 就转负。
   DOGE 的 `毛额只占 0.67%`，费率吃掉 **29.86%** 的毛额（BTC 只有 8.68%）
   ⇒ **低波动标的才是成本敏感型**，降费要**按标的**做，不能一刀切。

### 7.2 H-030 实测：lot 粒度「机制有效但真实规模不生效」

| 本金 | BTCUSDT | ETHUSDT | BNBUSDT | DOGEUSDT |
|---|---|---|---|---|
| $1 | 42827 归零 / 129 笔**全灭** | 0 | 10441 归零 / −21 笔 | 0 |
| $5 | 42827 归零 / **全灭** | 0 | 0 | 0 |
| $10 | 23836 归零 / −87 笔（129→42），**Δ净额 +4.379pp（假改善，见 D65）** | 0 | 0 | 0 |
| $50 | 0 | 0 | 0 | 0 |
| $100 ~ $10k | 0 | 0 | 0 | 0 |
| **归零阈值** | **(10, 50] USD** | < $1 | **(1, 5] USD** | < $1 |

**结论**：
- ✅ **机制已被证明有效**（`$1` 档 42827 次归零不是假的）—— 第 14 轮挂账的「粒度未观测」
  **今天用「降低本金」正解结掉了**，且给出**精确触发阈值**（BTC $10~$50 之间、BNB $1~$5 之间）。
- ✅ **真实资金规模（≥$100）下不构成约束** —— 这不再是「没测到」，而是**测到了边界**。
- ⚠️ ETH / DOGE 在 `$1` 都不归零，因为历史价格低（ETH 早期 $100~$200、DOGE $0.1），
  `$1 × 0.95 ÷ 价格` 仍能凑够 1 个 lot。**不是 bug，是标的差异**。

### 7.3 具体动作

| # | 动作 | 落到哪一行 | 优先级 |
|---|---|---|---|
| 1 | 台账增加「r\*」列（分标的），不再用统一 `fee_rate` 讨论成本 | `策略假设台账.md` 结论区 | **P0** |
| 2 | **停止**把「降费」当主赛道；改成「DOGE 单独降费 + BTC/ETH/BNB 转向信号/出场」 | 下轮夜学主题选择 | **P0** |
| 3 | 实盘 4543 笔净 −15.90 USDT 与回测 +2.15%/笔的**巨大矛盾**必须查（见 §8） | `core/live.py` 对账链 | **P0** |
| 4 | `core/report.py` 增加「笔数」进毛净并列区（防 D65 类假改善） | `report.py:78-90` | P1 |
| 5 | `scanner.py` 多标的并发时的先卖后买顺序（D64） | `scanner.py` | P2 |
| 6 | 冲击成本换平方形式（D61）—— 只在资金上 $1M 时才需要 | `core/backtest.py` | P2 |

## 8. 未完成 / 失败区（诚实留痕）

1. **★★★ 最大疑点：回测与实盘的量级矛盾未解决。**
   回测：BTC 净额单笔 **+2.1521%**、4/4 只费前为正、能扛 10 倍费率。
   实盘：4543 笔真实成交，已实现 +6.78 / 手续费 22.68 / **净 −15.90 USDT**（第 14 轮回溯）。
   两者**不可能同时为真**。候选解释（未验证，按嫌疑排序）：
   - ① **标的池不同**：回测 4 只主流高流动性品种；实盘 4543 笔可能覆盖大量小币
   - ② **时段不同**：回测是全历史（含 2019-2021 大牛），实盘是近期
   - ③ **`net_pnl_pct` 与实盘手续费记账口径不同**（实盘 22.68/4543 = 0.5 USDT/笔，占比需按名义额算）
   - ④ **回测存在未来函数**（`entry_on='close'` 用当根收盘价入场 —— 信号也是用当根收盘算的）
   ⇒ **下轮 P0**：把实盘 4543 笔按「标的 / 时段 / 单笔名义额」切片，与回测同样本对照。
   **在查清之前，§7.1 的 r\* 只能读作「回测口径下」，不能外推为「实盘能扛 10 倍费率」。**

2. **★ 数据口径疑点（今天新发现）**：`币安15m_K线数据/*_永续_15min_全历史.csv` 是**永续合约**数据，
   但 `StrategyParams.fee_rate=0.001` 是**现货 taker 0.1%**。永续 USDT-M 的 taker 是 **0.05%**。
   ⇒ **当前基线可能系统性高估单边成本约 1 倍**（0.1% vs 0.05%）。
   影响：H-029 的「费率吃掉 0.2041pp」在真实永续口径下应是 **≈0.102pp**。
   本轮**未修正**（改费率=改基线，会让历史假设不可比），记作 **P0 待办**：要么换现货数据，要么改费率并**整批重跑**。

3. **AtomCode 第零步：连续第 5 轮失败（10-21/22/23/24/26，10-25 未运行）。**
   今日 `proxy_down` → 后台拉起 → `/health` 200 + `logged_in=true`（账号 `gcw_1D1KA17b`）
   + 但最小推理 **240s 超时 HTTP=0** ⇒ 上游推理层挂死（非额度、非二进制，第 13 轮已验 `--version` 完好）。
   ⇒ 全程本地 `Read`/`Grep` 精读，**0 积分**。按收敛纪律不再耗时间。

4. **10-25（周日）夜学轮未运行，六端归档（本应 10-25 执行）未做。**
   今日周一按第九步节奏只落 Obsidian + 日志。**归档缺口需在下一个周日补做，且包含 10-18/10-25 两轮顺延。**

5. **B 站无增量**（见 §6，按 2026-10-20 结论永久降级，不记失败）。

6. **qlib `_clip_amount_by_volume` 的 `dealt_order_amount` 只在 `executor.py` 里累加，
   本轮未逐行核对其更新时机** —— 理论上「同 bar 多笔委托」时 `cum` 型限量可能重复扣减。
   本轮未测（我们的 `participation` 走当根 `volume` 总量，不走 `cum`，暂无同等风险）。

## 9. 三件套自检

- [x] ① 拆解笔记已落盘：本文件（`Obsidian知识库/AI量化平台/学习笔记/20261026_microsoft_qlib.md`）
- [x] ② 可复用代码落盘：`ai_quant_lab/20261026_microsoft_qlib/fee_schedule_model.py`
      （**30/30** 自测通过，`lab_bridge.get("fee_schedule_model")` 加载零警告）
- [x] ③ 策略假设已追加：**H-029 已验证** / **H-030 已验证**（台账已回写，`bytes_delta=3`）
      证据：`策略假设/回测结果/回测结果_20261026.json`
      manifest：`ai_quant_lab/_manifests/manifest_20261026_042234.json`（`scope=full`）

## 10. 成本与技能

- **花费积分**：**0**（AtomCode 全程不通，本地 Read/Grep + Python 回测，无任何云端调用）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程 v1.1.12）、
  `币安量化数据通路与黑马策略诊断`（回测与口径纪律）
- **没用哪些技能**：`六端空间归位`（周中不归档，第九步节奏）、
  `云端四端归档通道`（同上）、`分身之眼`（与本任务无关）
- **沉淀 / 迭代**：技能 `v1.1.12 → v1.1.13`（新增 §3.15 七条：D60~D66 + 两条实测纪律）
- **本轮新增平台资产**：`fee_schedule_model.py`（30/30）、`hypothesis_runner.py` 新增 H-029/H-030
  （+11760 B，二进制安全，行尾 LF 保持）
- **修的真 bug**：`_load_fee_model()` 首版**没先插 `quant_app` 到 `sys.path`** →
  首次调用必然导入失败 → `_FS=None` → DOGE 的 r\* 被记成「二分异常 AttributeError」。
  **表现像结论、根因是导入失败** —— 已修为加载器自己兜住 sys.path，重跑后 DOGE r\*=0.003354 正常算出。

---

*关联：[[策略假设台账]] · [[20261014_microsoft_qlib]]（一刷读 workflow 层）· [[20261024_hummingbot_vnpy]]（滑点/粒度前序）*
