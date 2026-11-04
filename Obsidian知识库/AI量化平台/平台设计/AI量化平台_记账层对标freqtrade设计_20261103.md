---
日期: 2026-11-03
设计点: D123 ~ D131
对标: freqtrade persistence/trade_model.py + wallets.py + exchange.py(强平段)
状态: 设计定稿 / 待落地
轮次: 第 23 轮
tags: [AI量化平台, 平台设计, 记账层, Order实体, 幂等重算]
---

# AI量化平台 · 记账层对标 freqtrade 升级设计（D123~D131）

> **一句话**：我方回测引擎目前**没有独立的订单实体** —— 成交直接落成 `tr` 表的一行，
> 「分批建仓/分批出场/部分成交」全是字符串标签。freqtrade 的做法是
> **给每笔订单一个可重放的主键，然后从全部订单重算交易状态**。
> 这样做的好处不是"更优雅"，而是**可对账**：任何时刻都能从订单流水重建出完全相同的持仓与盈亏。

---

## 一、现状差距（先摆事实）

| 维度 | freqtrade | 我方 `core/backtest.py` | 差距 |
|---|---|---|---|
| 订单实体 | `Order` + 唯一约束 `(ft_pair, order_id)` | 无 | **结构性** |
| 交易状态 | `recalc_trade_from_orders` 从**全部** order 重算 | 循环内增量累加 | 缺幂等 |
| 分批出场 | 每笔出场独立记账 | 只有 `exit_reason` 字符串 | 无法归因 |
| 毛净字段 | `ProfitStruct` 四字段并列 | `pnl_pct`（不含费）+ `net_pnl_pct` | 已吃过亏 |
| 成本口径 | `fee_open` / `fee_close` 两侧分开 | 汇总一个 `fee_rate` | 无法分辨 |
| 强平价 | 档位查表 + `liquidation_buffer` 二次缓冲 | 无 | 待接 |
| 余额 | `_strip_unrealized_pnl` 剥离浮盈 | 无概念 | 待接 |

---

## 二、设计点

### D123 · 引入 `Order` 实体（数据层）

```python
@dataclass
class Order:
    order_id: str            # 内部唯一
    ft_pair: str             # 标的
    ft_side: str             # "buy" / "sell"
    ft_is_entry: bool
    ft_price: float          # 我方记账价（成交均价）
    ft_amount: float
    ft_fee_cost: float
    ft_fee_currency: Optional[str]   # ★ None = 费率未知（见 D126）
    status: str              # "open" / "closed" / "canceled" / "expired"
    timestamp: int           # 毫秒
```

**关键约束**：`UniqueConstraint(ft_pair, order_id)`。
⇒ **重放同一笔回报不会产生第二行**，这是幂等的根基。

**迁移路径（零退化）**：
1. 先只**新增**（不改现有逻辑），在 `run_backtest` 里旁路收集 Order 列表并随结果返回；
2. 用 `selftest` 断言「Order 流水重算出的 PnL == 现有 `tr` 表 PnL」逐位一致；
3. 一致之后才把主路径切到 Order 记账。
⇒ **不允许一步切换** —— 一步切换就失去了"新旧对撞"这个唯一的验收手段。

### D124 · 从全部订单重算（幂等）

```python
def recalc_from_orders(orders, entry_side):
    avg_price = 0.0
    current_stake = current_amount = 0.0
    close_profit_abs = 0.0
    for o in sorted(orders, key=lambda x: x.timestamp):
        if o.status != "closed":
            continue                       # 未成交不记账
        is_exit = (o.ft_side != entry_side)
        side = -1.0 if is_exit else 1.0
        price = avg_price if is_exit else o.ft_price
        current_stake += price * o.ft_amount * side
        current_amount += o.ft_amount * side
        if current_amount > 0 and not is_exit:
            avg_price = current_stake / current_amount
        if is_exit:
            close_profit_abs += calc_profit(price, o.ft_amount, avg_price)
    return avg_price, current_amount, close_profit_abs
```

**D124 附注（今天证伪过的点）**：`price = avg_price if is_exit` **不是**会计漏洞。
出场批次的成交价与均价在**最终 PnL 上代数闭合**（`stake` 是线性量）。
这一行的真实作用只有一个：**让均价在出场期间保持不变**，从而「剩余持仓成本」不被出场行为污染。
⇒ **不要在"按均价 vs 按原价"上做优化，那条线上没有收益。**

### D125 · 毛净四字段强制并列

```python
@dataclass
class ProfitStruct:
    profit_abs: float          # 净绝对值（已扣双边费）
    profit_ratio: float        # 净比率
    total_profit: float        # 毛绝对值（含价差）
    total_profit_ratio: float  # 毛比率
```

**为什么必须四个**（D65 的延续）：
- `report.py` 现有输出只有 `pnl_pct` + `net_pnl_pct` 两个，
  使用者无法分辨「这个 gross 含不含买入费」；
- 今天实测：我方口径的 gross 比 freqtrade 式 gross 少**恰好一个买入费**。
  **同一符号、同一个名字、两种含义 = 最凶的坑。**

⇒ **落地要求**：`report.py` 的输出表加两列 `gross_before_fee` / `fee_total`，
并在表头正下方写一行口径说明。**口径必须写在看得见的地方，不能只写在文档里。**

### D126 · `fee_currency is None` 才是"费率未知"

freqtrade 的 `update_fee`：
```python
if order.fee_open_currency is None:      # ← 只在"从未写过"时才写
    trade.fee_open_currency = ...
    trade.fee_open_cost = order.fee_cost
```

**判据是「从未写过」，不是「当前值为 0」。**
⇒ 我方若写 `if not fee:` 就会把「费率真为 0（如 BNB 抵扣）」当成「未写」而反复覆盖。
**这是一条只差一个语义就能咬死人的判据。**

### D127 · 强平价两段式

```python
def liquidation_price(open_rate, amount, wallet_balance, mm_ratio, taker_fee, is_short):
    value = wallet_balance / amount
    mm_ratio_taker = mm_ratio + taker_fee
    if is_short:
        return (open_rate + value) / (1 + mm_ratio_taker)
    return (open_rate - value) / (1 - mm_ratio_taker)

def with_buffer(liq, open_rate, is_short, buffer):
    gap = abs(open_rate - liq) * buffer
    return liq + gap if is_short else liq - gap      # ★ 往"远离现价"方向推
```

- **第一段**闭式解，`mm_ratio` 从档位表**降序**查（`for tier in reversed(pair_tiers)`，
  名义值越大的档配越严的维持保证金率）；
- **第二段**缓冲必须**把强平点往远离现价的方向推**，
  方向写反就等于**主动放宽风险**（今天 S9 抓到的真 bug：首版写成 `liq - gap if is_short`）。

### D128 · 余额剥离未实现盈亏

交易所的 `total` 余额**已含未实现盈亏**，而持仓又单记一次 ⇒ **算两遍**。
`_strip_unrealized_pnl` 的做法：`balance = total - unrealized_pnl` 后再与持仓合并。

⇒ 我方若接实盘，`wallets` 层必须显式剥离，否则**总资产虚高**，
且虚高幅度随浮盈波动 —— **回测与实盘永远对不上，还会以为是别的原因**。

### D129 · 「参数真正生效区间」自动识别（实验方法层，非代码层）

今天 H-045 首跑判「已证伪」却打印「改善中位 +0.8069pp」，自相矛盾。
根因：`tp1 ≥ 0.35` 时 T1 门槛 **未被消费**（持仓早已进 T2 档），结果逐位相同。

⇒ **固化进 `_effective_thresholds()`**：扫描一维网格时，
**先剔除"相邻两档结果逐位相同"的空档，只在真正生效的区间上判单调**，
并把被剔除的档位显式登记为「空档，未参与判定」。

**这是 SOUL §5.2「参数给了 ≠ 参数给够了」的自动化版本**：
以前靠人工发现"三档结果一样"，现在由代码自查。

### D130 · 判据按证据强度分级（今天第二次用）

H-045 首版要求「4/4 标的 ρ_net == 1.000」，实测 ETH 在 0.25→0.35 回落（ρ=0.900）
⇒ 整条判「已证伪」，可它的**中位改善是 +1.2970pp**、**胜率 4/4 严格单调（ρ=−1.000）**。

⇒ **判据分级**：
- 主判据 = 机理是否成立（胜率反向单调 4/4 —— 这决定了"胜率被操纵"这条机理）
- 副判据 = 净单笔 ≥3/4 单调 **且** 中位改善 ≥0.30pp

**「一个标的没排到完美」不等于「方向错」。**
但反过来也不能放松到「只要有一个好就成立」——所以副判据要有**幅度门槛**（0.30pp = 手续费 3 倍）。

### D131 · 端点纪律（今天出现 2 次，必须升格）

今天两条假设的**最优都落在网格端点**：
- H-045：`tp1` 最优落上端 0.35（3/4 标的）
- H-046：`trail1` 最优落上端 0.20（多数格子）

⇒ **凡最优落端点，结论只能读作「方向性单调」，并强制登记「真实最优可能在端点之外、本轮未测」。**
**不许把端点值当最优点写进任何报表。**

---

## 三、落地顺序（每步都要能退回）

| 步 | 动作 | 验收判据 | 退化风险 |
|---|---|---|---|
| 1 | `Order` 实体旁路收集（不改主路径） | 新增 selftest：Order 流水重算 PnL == `tr` 表 PnL，**逐位一致** | 零（纯新增） |
| 2 | `ProfitStruct` 四字段输出 | `report.py` 新增两列，**旧列名与数值不变** | 零（纯新增） |
| 3 | `recalc_from_orders` 接管（可开关） | 开关关闭时与基线**逐字节一致**（baseline 56 笔 / 179.347%） | 中（需 A/B 对撞） |
| 4 | 强平价 + 余额剥离 | selftest 覆盖长短两方向 + 缓冲方向反测 | 低 |
| 5 | `_effective_thresholds` 接入所有一维扫描 | 旧结论重跑，判定与历史一致 | 低 |

---

## 四、不做的事（明确排除，防止范围蔓延）

- ❌ **不做 freqtrade 的 `protections` / `hyperopt`** —— 那是参数搜索层，我方 `opt_grid_guard` 已覆盖。
- ❌ **不做 Telegram/RPC** —— 无实盘时是纯成本。
- ❌ **不重写 `core/backtest.py` 主循环** —— 只旁路加实体，主循环一行不动。

---

## 五、关联

- 精读笔记：`学习笔记/20261103_freqtrade_vnpy.md`
- 落地代码：`ai_quant_lab/20261103_freqtrade_vnpy/position_accounting_guard.py`（21/21）
- 假设：H-045（已验证）/ H-046（已验证）
- 前序设计：`平台设计/AI量化平台_订单对账层对标nautilus_trader设计_20261021.md`（D91~D94）
