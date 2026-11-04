---
日期: 2026-10-19
仓库: vnpy/vnpy_portfoliostrategy（组合回测引擎）
核心文件: vnpy_portfoliostrategy/backtesting.py（1026 行）
轮次: 第 9 轮
tags: [AI量化平台, 夜学, 代码拆解, 组合回测, 毛净双账, R7顺序锁定]
---

# 20261019 · vnpy_portfoliostrategy · backtesting.py

## 0. 一句话结论

> **组合回测引擎的「资金约束」根本不在引擎里 —— 它把额度交给策略自己算。
> 这句话反向证明了我们 R7 顺序锁定必须落在「报单唯一入口」，而不是策略或校验函数里。**
> 顺带用它把两块挂账 3 轮/1 轮的 P0 回填完（R7 调用点 + 毛净双账），
> 并在回填过程中抓到一个**影响全部 17 条历史假设**的口径 bug（详见 §7.1）。

### 0.1 ★ 命名勘误（白名单写错了一个仓库名）

| 项 | 实测结果 |
|---|---|
| 白名单写的是 | `vnpy/vnpy_portfoliobacktester` |
| GitHub 实际 | **404**（archive/codeload 三镜像均 404，而同 org 的 `vnpy_portfoliostrategy`、`vnpy_ctabacktester` 均 200） |
| 真实位置 | `vnpy/vnpy_portfoliostrategy` 仓库内的 **`vnpy_portfoliostrategy/backtesting.py`**（1026 行），组合回测引擎就在这个 app 里 |
| 本地落点 | `E:\龙虾AI主控中心\vnpy\vnpy__vnpy_portfoliostrategy\` |

**这条要写进白名单修正**：下周轮转不要再去找 `vnpy_portfoliobacktester`。
另：`git clone --depth 1` 走 ghproxy **本轮挂死 8 分钟**（.git 建了 61KB 就停），
改走 **`ghfast.top` + archive tar.gz** 一次成功（48KB / 40 秒）——**克隆通道要补这一条**。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：撮合回测层（组合级）—— 它把「多个标的 × 同一时间轴 × 同一账户」拼成一个回测。
- **上游依赖**：
  - `vnpy.trader.object`（BarData / OrderData / TradeData）
  - `vnpy.trader.database`（历史 K 线）
  - `vnpy.trader.utility`（BarGenerator / ArrayManager 由策略侧用）
- **下游被谁调用**：
  - `portfolio_strategy/engine.py`（实盘侧同名引擎，接口对齐）
  - GUI 里的「组合回测」页
- **关键判断**：`BacktestingEngine` 实现了 **`send_order / cancel_order / cross_limit_order / new_bars / update_daily_close`** 五件事，
  也就是 **撮合推进 + 通知回流 + 日终结算** 三合一。**它没有风控层，也没有资金校验层** —— 这是与我们最大的结构差。

---

## 2. 调用链（文字版时序图）

```
run_backtesting()                       # :206
  └─ for dt in 日期轴:
       new_bars(dt)                     # :588  ← 每根 bar 的「推进器」
         ├─ 为每个 vt_symbol 取本根 bar（取不到 → 用上根 close 造平盘 bar）   :594-617
         ├─ cross_limit_order()         # :625  ← 先撮合**上一根挂的单**
         │    ├─ SUBMITTING → NOTTRADED（推状态）
         │    ├─ 判 cross：long 用 low / short 用 high
         │    ├─ 成交价 = min(限价, open) 或 max(限价, open)
         │    └─ order.traded = order.volume（**全成，无部分成交**）
         │       → strategy.update_order / update_trade
         ├─ strategy.on_bars(bars)      # :620  ← 再让策略看本根做决策
         └─ update_daily_close()        # :572  ← 缓存收盘价，供日终结算
  └─ calculate_result() / calculate_statistics()   # :249 / :297
       └─ PortfolioDailyResult.calculate_pnl()      # :896
            └─ ContractDailyResult.calculate_pnl()  # :818  ← 三账分离在这里
```

**结构上最重要的一点**：`cross_limit_order()` 在 `on_bars()` **之前**。
→ 本根决策产生的单，**只能等下一根撮合**。这是「无未来函数」的**结构性保证**，
不是靠开发者自觉。我们 `core/backtest.py` 用 `entry_on="close"` 时是「本根收盘决策 + 本根收盘价成交」，
这层保证**我们没有**（H-009 已量化其代价）。

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `BacktestingEngine.new_bars(dt)` | method `:588` | 单根推进：补数据 → 撮合 → 推策略 → 记收盘 | 时序的**唯一入口** |
| `cross_limit_order()` | method `:625` | 限价撮合，long `price>=low`、short `price<=high` | 成交价 `min/max(限价, open)`；**全成** |
| `send_order(...)` | method `:698` | 建 OrderData 入 `active_limit_orders` | **零资金校验**（见 D20） |
| `cancel_order(...)` | method `:735` | 从 active 弹出 + 推 CANCELLED | **不释放任何额度**（因为它本来就不管额度） |
| `ContractDailyResult.calculate_pnl()` | method `:818` | 单合约日结：holding/trading/total/net 四笔账 | **D21 三账分离** |
| `PortfolioDailyResult.calculate_pnl()` | method `:896` | 汇总各合约 + 组合级手续费/滑点 | 组合层只做加总 |
| `evaluate()` / `wrap_evaluate()` | func `:965 / :1004` | 参数优化用的单值目标 | 与 `get_target_value` 配套 |

---

## 4. 可迁移设计点（逐条说「为什么更好」）

### D20 资金/额度**不在引擎**，而在策略 —— 这恰恰证明我们必须反向做

`send_order()` 全程**没有任何**「够不够钱/够不够额度」检查；策略自己算 `target volume`，
差额下 `send_order`。单策略单标的时没毛病；**多策略并存时两处同时算 target 必然超配**，
而引擎无从发现（它连 `capital` 字段都没有）。

→ **为什么我们反过来做**：黑马平台的报单路径是**唯一入口**，风控粒度就该在入口上。
本轮把 `core/backtest.py` 的报单改成 `risk.reserve_order()`（过闸 + 原子占额度），
就是因为「只在策略里算」这条路上，**没有任何东西阻止两笔单用同一份余额过闸**（2026-10-12 血泪场景：余额 1000，两单各 601.2 双双放行）。

### D21 三账分离：`holding_pnl` + `trading_pnl` = `total_pnl`（毛），减手续费滑点 = `net_pnl`

```python
self.holding_pnl = self.start_pos * (self.close - self.pre_close) * size   # 隔夜仓
self.trading_pnl += pos_change * (self.close - trade.price) * size         # 当日开仓浮盈
self.total_pnl = self.trading_pnl + self.holding_pnl
self.net_pnl  = self.total_pnl - self.commission - self.slippage
```
**为什么更好**：把「这笔钱是持仓赚的还是今天开仓赚的」拆开，**归因才可能**。
我们的 `perf` 只有总收益与含成本单笔，**持仓段/交易段混在一起**，回撤归因时说不清是哪一半拖的。

### D22 手续费与滑点**各自独立累计**（不折算成一个"综合成本率"）

`self.slippage += volume*size*slippage` 与 `self.commission += turnover*rate` 是两条独立通道。
**为什么更好**：这两条通道的**可控性完全不同** —— 手续费可以靠改下单方式（maker/taker）降 5 倍，
滑点只能靠降频/拆单降。混成一个数，就永远算不清「该改哪一头」。→ 直接催生了 H-019。

### D23 缺数据用上根 close 造「平盘 bar」保证时序对齐 —— 但必须配「不可成交」标记

`new_bars` 里取不到 bar 就用 `old_bar.close_price` 造一根 `open=high=low=close` 的 bar。
**好处**：多标的组合的事件时序不会因为某个标的停牌而错位（否则「第 N 根」不同标的含义不同）。
**坑（vnpy 自己踩了）**：这根**合成 bar 照样进 `cross_limit_order`** ——
`low = high = close`，任何限价买单 `price >= low` 都成立 → **在假 bar 上凭空成交**。
→ 我们的 `portfolio_engine_patterns.FlatBarFiller` + `cross_limit_order(allow_synthetic=False)` 把这两半补齐。

### D24 撮合**全额成交**（`order.traded = order.volume`）

没有部分成交、没有排队、没有拒单。→ 我们 `risk.release_fill()` 的**部分成交分支永远测不到**，
这正是 2026-10-13 记录过的「`release_fill` 未覆盖」。本轮用 `fill_ratio` 参数第一次把它跑通了（27/27 笔走了部分成交路径）。

---

## 5. 可复用代码片段

**来源**：`vnpy_portfoliostrategy/backtesting.py:818-857`（三账分离）
**用途**：把「持仓段盈亏」与「当日交易段盈亏」拆开，毛/净并列。

```python
def calculate_pnl(self, pre_close, start_pos, size, rate, slippage):
    self.pre_close = pre_close
    self.start_pos = start_pos
    self.end_pos = start_pos
    self.holding_pnl = self.start_pos * (self.close_price - self.pre_close) * size

    self.trade_count = len(self.trades)
    for trade in self.trades:
        pos_change = trade.volume if trade.direction == Direction.LONG else -trade.volume
        self.end_pos += pos_change
        turnover = trade.volume * size * trade.price
        self.trading_pnl += pos_change * (self.close_price - trade.price) * size
        self.slippage += trade.volume * size * slippage
        self.turnover += turnover
        self.commission += turnover * rate

    self.total_pnl = self.trading_pnl + self.holding_pnl
    self.net_pnl = self.total_pnl - self.commission - self.slippage
```

**已落地版本**（我方、去 vnpy 依赖、带自测）：
`ai_quant_lab/20261019_vnpy_vnpy_portfoliostrategy/portfolio_engine_patterns.py:→three_account()`
（自测 **19/19**，`lab_bridge.get("portfolio_engine_patterns")` 零警告加载）

---

## 6. B站学习（本日 30% 权重）

- **结果：降级（连续第 8 轮）**。`api.bilibili.com/x/web-interface/search/type` 返回 **HTTP 412**（风控要求 wbi 签名 + 登录态），
  直接 WebFetch 视频页只能拿到标题，拿不到 CC 字幕文本。
- **替代素材（已读）**：vnpy 官方文档中文版「组合策略 / 回测」章节 + `vnpy_portfoliostrategy/README.md` + `script/` 下的示例脚本。
- **蒸馏要点**：
  1. 组合策略的 `on_bars(bars: dict[str, BarData])` 是**同一时间戳的一批 bar**，不是单标的流 —— 这决定了组合层必须做时序对齐。
  2. 组合回测的「资金」是**策略自己维护的现金池**，引擎只负责撮合与统计 —— 与 D20 一致。
  3. 多标的策略的经典坑：**先算 A 再算 B 时，A 的成交还没回写现金池** → 与 R7 完全同源的顺序锁定问题。
- **待补清单**：有 CC 的 vnpy 实战课（需登录态 cookie）；本轮未取得，如实记在 §8。

---

## 7. 对黑马策略的启发（已落地，不是"待办"）

### 7.1 ★★ 口径 bug：历次「含成本单笔均值」**不含手续费**

| 项 | 实测 |
|---|---|
| 旧指标 | `pnl_pct = (出场价/入场价 − 1) × 100` —— 价格已按滑点偏移，**但手续费只影响 `pnl_abs` 与持仓数量，不进这个百分比** |
| 实测差额 | **0.2041 pp/笔**（BTC 40k 根样本，双边 0.1%×2 = 0.2%） |
| 影响面 | H-001~H-017 **全部**用这个指标判的「含成本」 |
| 为什么旧结论不推翻 | 配对 A/B 的**两边同受此偏**，差值基本不受影响 → 「6/6 证伪」「成本线」方向不变 |
| 结论怎么改 | 总纲「幅度 < 0.20% 成本线」的**真实门槛比原先认为的高 0.2pp**；新假设一律用 `net_pnl_pct`（净盈亏/实际投入本金） |

已落地：`core/backtest.py:add_net_pnl()` + `core/report.py:build_cost_account()`（毛/净双列 + `cost_dominated` + k 敏感性「是否横跨零」）。

### 7.2 假设 H-018（**出场端**）→ **已验证，4/4**
把三段止盈追踪回撤 **10%/8%/5% → 15%/12%/8%**：

| 标的 | 净额单笔均值 | 总收益 | 最大回撤 |
|---|---|---|---|
| BTC | 1.8021 → **2.2416** (+0.4395) | 219.3 → 297.7 | 78.1 → 77.0 |
| ETH | 2.1683 → **3.3502** (+1.1819) | 863.2 → 1686.1 | 77.0 → 75.6 |
| BNB | 2.1193 → **3.3327** (+1.2134) | 706.9 → 933.7 | 79.7 → 69.6 |
| DOGE | 0.4726 → **1.6195** (+1.1469) | −79.8 → −61.7 | 99.5 → 99.1 |

**这是第 1 条出场端假设，也是 7 连败之后第一条成立的方向** ——
入场端「加门槛」6/6 全证伪（砍机会不提纯），而放宽出场（让利润跑）4/4 全改善。
★ 注意 DOGE 依然亏：**出场端能减亏，但改不了「这只标的本身不该做」**。

### 7.3 假设 H-019（**成本端**）→ **已验证，4/4**，但**咬合力必须先说清**
maker 0.02%/边 + 70% 确定性成交率 vs taker 0.1%/边：BTC +0.1698 / ETH +0.3844 / BNB +0.0878 / DOGE +0.1386（pp/笔）。

> **诚实标注（咬合力）**：笔数几乎没变（BTC 140→140 / ETH 211→204 / BNB 202→203 / DOGE 472→465，仅 −3.3%~+0.5%）。
> 原因：单仓位策略里「这根没挂上」会被**下一根信号顺延补上**，`_hash_keep(0.70)` 的折损几乎**不咬合**。
> → 所以本条的增益**几乎全部来自费率降低，不是来自"省费率 vs 丢机会"的取舍**。
> 要真测那个取舍，得改成「限价单只在当根有效、过期作废且不追」，—— 记为下轮 P1。

### 7.4 平台动作（本轮真的改了代码，不是只出设计）

| 文件 | 改动 | 验收 |
|---|---|---|
| `core/backtest.py` | `run_backtest(..., risk=None, symbol, fill_ratio)`：报单走 `reserve_order()`→`release_fill()`/`release_order()`；平仓走 `reduce_only=True`；新增 `add_net_pnl()` / `selftest_risk_wiring()` / `_ts_ms()` | 接线自测 **10/10**；`risk=None` 路径与旧版**逐字节等价**（总收益 32.856 完全一致） |
| `core/report.py` | `build_cost_account()`（毛/净双列 + `cost_dominated`）、`cost_k_sensitivity()`（k∈[0.5,2] 区间 + 横跨零）、报告新增「毛账/净账」段 | BTC 40k 根实测：毛 2.10% / 净 1.89% / 拖累 0.2041pp / 占毛利 9.73% |
| `core/risk.py` | **显式 `reduce_only` 白名单通道**（AtomCode 建议）：`reducing = reduce_only or _is_reducing(...)` | 自测 **15/15 → 16/16**（新增「显式reduce_only」项，原 15 项无退化） |

**回填进度**（这是挂账问题的正面回应）：
- R7 调用点：**第 7 轮起挂账 → 本轮接通**（`reserve_order` 首次真正被回测调用，日志里出现 27 次 reserve 动作）
- 毛/净双列 + k 敏感性：**第 8 轮挂账 → 本轮接通**
- 仍挂账：G2 三态 · D1~D4 · D9 · D14~D19（下轮优先级见 §8）

---

## 8. 未完成 / 失败区（诚实留痕）

1. **B站 CC 字幕连续第 8 轮拿不到**（HTTP 412，需 wbi 签名 + 登录态）→ 已降级为文档蒸馏，**未补上**。
2. **`vnpy_portfoliobacktester` 仓库不存在** —— 白名单需改成 `vnpy_portfoliostrategy`（§0.1）。
3. **ghproxy `git clone` 本轮挂死 8 分钟**（61KB 后停滞），靠 `ghfast.top` archive 绕过；
   **克隆通道优先级表要加一条**：`ghfast.top + /archive/refs/heads/master.tar.gz`。
4. **部分成交/拒单仍是注入法**（`fill_ratio`），不是撮合器内生模型 —— 真实盘口没有，属已知边界。
5. **k 敏感性只覆盖线性成本**：AtomCode 指出还缺三层 —— ①冲击成本随单量非线性 ②容量上限（按 ≤1% bar volume）③保证金峰值/强平路径。**未做**。
6. **`net_pnl_pct` 未做时间归一**：AtomCode 建议补「占用时长 × 本金」的年化口径，否则长持仓的百分比不可比。**未做**。
7. **合成 bar 的缺口处理只做了一半**：禁成交能防凭空成交，但**长缺口期的止损/止盈会被静默跳过**（回测低估尾部风险）。
   AtomCode 建议：短缺口（≤2 根）禁成交；长缺口按缺口后真实开盘价**一次性市价清算**并计入损益。**未实现**。
8. **DOGE 依然系统性亏损（−61.7%）** —— H-018/H-019 都改善但它仍亏；「该不该做这条标的」仍未回答。
9. G2 三态 / D1~D4 / D9 / D14~D19 **仍未回填 `core/` 本体**。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件，读回确认）
- [x] ② 可复用代码：`ai_quant_lab/20261019_vnpy_vnpy_portfoliostrategy/portfolio_engine_patterns.py`
      （自测 **19/19** · `lab_bridge.get()` **零警告** · `core` 全模块 import **13/13**）
- [x] ③ 假设已追加进 [[策略假设台账]]：**H-018（已验证）/ H-019（已验证）**，`hypothesis_runner --only` 实跑回写，`changed` 均非空
- [x] ④ 平台回填验收：接线自测 10/10 · risk 16/16 · events 三项全 True 无退化

---

## 10. 成本与技能

- **积分**：0（AtomCode 走 `glm5.3-flash` 免费档，1 次 4 问交叉复核 / HTTP 200 / 45.6s / 694 字）
- **CodingPlan**：本轮首跑 `CodingPlan 403`（10-16 已到期）→ guard 自动 `login` 重领成功，
  新周期 **Lite-体验版 expires 2026-10-26**，模型 `glm5.3-flash`。
- **技能**：`ai-quant-open-source-nightly-learning` v1.1.6 → **v1.1.7**（新增 §3.9 六条；补命名勘误与克隆通道）
