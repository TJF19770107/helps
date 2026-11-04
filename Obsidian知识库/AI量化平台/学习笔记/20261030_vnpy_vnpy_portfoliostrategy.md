---
日期: 2026-10-30
仓库: vnpy/vnpy_portfoliostrategy
核心文件: portfolio_strategy/engine.py (639) + backtesting.py (1026) + template.py (316) + utility.py (325)
轮次: 第 19 轮
tags: [AI量化平台, 夜学, 代码拆解, 组合回测, 时间轴对齐, 前值填充, 冻结撮合]
---

# 20261030 · vnpy_portfoliostrategy · 组合回测的「时间轴 / 填充 / 冻结撮合」

## 0. 一句话结论
> **多标的组合回测的失真不在「策略」，在「对齐」**：vnpy 用「时间戳并集 + 前值填充合成 bar」把多标的拼成一条时间轴，
> 这一步会同时制造 **G1 量价因子失效（volume 默认 0）**、**G2 尾部冻结（价格常数）**、**G3 零流动性全量成交**。
> 本轮把三件事都量化了，并且**用真实数据给「实盘 4543 笔 vs 回测 129 笔（35 倍）」这条挂账定了第一刀**：
> **时间轴错位可以划掉**（真断档仅 37 条 = 0.0038%），**嫌疑收窄到「样本期不一致」**（ETH/DOGE 数据比 BTC/BNB 早停 48.1 天 / 4616 根）。

## 1. 这个文件在系统里管什么（架构定位）
- **所属层**：`engine.py` = 组合策略**执行层**（实盘）；`backtesting.py` = **撮合回测层**；`template.py` = **策略层**基类；`utility.py` = **工具层**（组合 K 线合成）。
- **上下游**：
  - 上游依赖 → `vnpy.trader.engine.BaseEngine/MainEngine`、`vnpy.event.EventEngine`、`vnpy.trader.database`（历史 bar）、`vnpy.trader.datafeed`
  - 下游被谁调用 → `strategies/*.py`（trend_following / pair_trading / pcp_arbitrage / portfolio_boll）只重写 `on_bars` + `calculate_price`；`ui/widget.py` 只读事件
- **一句话分工**：`engine.load_bars` 负责**把 N 个标的拼成一条时间轴**，`backtesting.new_bars` 负责**在同一个时间轴上先撮合旧单、再喂新 bar**。**两条链共用同一套填充语义**——所以这里的坑在回测与实盘是同一个坑。

## 2. 调用链（文字版时序图）

**回测链**
```
BacktestingEngine.load_data()            # backtesting.py:135-205 逐标的 load_bar_data → dts 并集 + history_data[(dt,sym)]
  └─ run_backtesting()                   # :206  dts 升序；先跑 days 天初始化，再跑剩余
       └─ new_bars(dt)                   # :588
            ├─ 对每个 vt_symbol: 有真 bar → self.bars/ bars；无 → synth_bar(prev_close)  # :595-617
            ├─ cross_limit_order()       # :625  用 self.bars 撮合挂单（全量成交）
            ├─ strategy.on_bars(bars)    # :620  ★ 先撮合后回调（时序正确）
            └─ update_daily_close()      # :623  用 self.bars（含合成）收盘价算权益
```

**实盘链**
```
StrategyEngine.init_engine → load_strategy_setting → init_strategy(线程池 max_workers=1)
  └─ strategy.load_bars(days, interval)  # template.py:297
       └─ engine.load_bars()             # engine.py:259  ★ 与回测同语义：dts 并集 + 前值填充
            └─ strategy.on_bars(bars)    # :304  ★ 但这里**不撮合**（实盘由交易所撮合）
```

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `StrategyEngine.load_bars(strategy, days, interval)` | 方法 `engine.py:259-304` | 逐标的取历史 → `dts_set` 并集 → 逐 dt 拼 `bars` → `on_bars` | ★ **合成 bar 不填 volume**（`BarData` 默认 0），`bars` 字典**永不重置** |
| `StrategyEngine.load_bar(vt_symbol, days, interval)` | 方法 `:306-341` | 接口→datafeed→database 三级兜底取数 | `end = datetime.now(DB_TZ)` ⇒ **实盘路径**，不是回测 |
| `StrategyTemplate.rebalance_portfolio(bars)` | 方法 `template.py:200-262` | 按 `target-pos` 差量下单 | ★ 开头无条件 `cancel_all()`；只对 `bars` 里的标的发单（但 bars 恒被填充 ⇒ 保护失效） |
| `StrategyTemplate.calculate_price(sym, dir, ref)` | 方法 `:264-271` | 报价钩子，默认 `return ref` | ★ 默认 = 用**当根收盘价**挂限价 |
| `PortfolioBarGenerator.update_tick(tick)` | 方法 `utility.py:45-89` | tick→1min 组合 bar | ★★ 用**全局单一** `last_dt` 判跨分钟，多标的 tick 交替到达时会**互相触发推 bar** |
| `PortfolioBarGenerator.update_bar_minute_window(bars)` | 方法 `:100-142` | 1min→N min 组合 bar | ★★ `(bar.datetime.minute+1) % window`（与 vnpy/vnpy `utility.py:315` **同一个坑第二次出现**），且 `bar` 是 for 循环泄漏变量 |
| `BacktestingEngine.new_bars(dt)` | 方法 `backtesting.py:588-623` | 推进一根 → 撮合 → 回调 → 记收盘 | ★ 填充逻辑与实盘同语义 |
| `BacktestingEngine.cross_limit_order()` | 方法 `:625-687` | 限价撮合（唯一撮合入口） | ★ **`order.traded = order.volume` 全量成交，不看 volume / 不看盘口 / 无分批** |
| `ContractDailyResult.calculate_pnl(...)` | 方法 `:818-857` | 逐合约 `holding_pnl + trading_pnl − commission − slippage` | ★ `pre_close` 缺省 **0**（同族于 vnpy CTA 的 `pre_close=1`） |
| `PortfolioDailyResult.calculate_pnl(...)` | 方法 `:896-928` | 汇总到组合 | ★★ `sizes[vt]`/`rates[vt]`/`slippages[vt]` **直接下标无默认** → 缺合约即 KeyError，但 `pre_closes` 用 `.get(vt,0)`，**同一个函数两套缺省风格** |

## 4. 可迁移设计点（D82~D90，逐条写「为什么好 / 哪里是反例」）

**D82 · 时间轴必须显式区分「未上市」与「断档」**
`elif vt_symbol in bars` 这个隐式判据把两件事混成一件：上市前缺失（安全，不填充）与上市后断档（危险，被填充）。落地方案是给每格一个 `stale` 整数：`-1 = 尚未出现`、`0 = 真实`、`>0 = 填充了 N 根`。**为什么好**：只有把「缺失类型」编码进数据结构，下游才能一句话写出「只允许 stale==0」这种可审计的闸；靠 `in bars` 这种隐式状态，任何新加的策略文件都可能绕过它。

**D83 · 前值填充的合成 bar 必须带「合成」标记，且不得进入量价因子**
vnpy 合成 bar 只给 OHLC 四价 + `gateway_name`，`volume/turnover/open_interest` **全部默认 0**。于是「量比 > 1.5」这类黑马核心因子在填充 bar 上恒为 0（分母 0 或分子 0）。**为什么好**：给 bar 打 `is_synthetic=True`，让因子层**主动拒用**，比事后排查「为什么这段信号少了」便宜一个数量级。

**D84 · 冻结（越过最后一根真实 bar）必须与「停牌几根」分开，且放宽 stale 也绝不放行冻结**
价格恒定 ⇒ 波动率 0 ⇒ 追踪止损（`close <= long_stop`）**永不触发** ⇒ 持仓被无限延长。停牌 3 根可能可容忍，冻结 4616 根意味着「这只标的的行情已经结束了」。**反例**：vnpy 没有任何 stale 概念，两者一视同仁。

**D85 · 撮合器必须知道「这根 bar 是不是合成的」**
`cross_limit_order` 用 `order.price >= bar.low` 判成交，而合成 bar 的 `low == high == close == 前收` ⇒ **任何贴价挂单 100% 成交**，且 `trade_price = min(price, open) = 冻结价`。**这是本轮实测的核心**（H-040）。

**D86 · `trade_price = min(order.price, bar.open)` 的语义是对的，别误判成 bug**
开盘跳空越过你的限价时，真实撮合按开盘价成交（更优），所以取 min/max 正确。**真正的 bug 是它不看 volume、不分批**。⇒ **验收纪律**：看一个撮合函数，先分「定价口径」与「容量口径」两条线，别把定价正确的部分当 bug 一起改。

**D87 · 定长窗口指标在组合面板上会「时间跨度失真」**
若某标的在 U 根并集里只占 N_i 根真 bar，那 `ArrayManager(window=60)` 的「60 根」实际覆盖的真实时间被拉长 `U/N_i` 倍 ⇒ **同一个参数在单标的与组合两种跑法下不是同一个指标**。落地方案：窗口按「真实 bar 计数」推进，填充 bar 只更新价格不推进计数。

**D88 · 无条件的 `cancel_all()` 会把「挂单成交率」压成 0**
`rebalance_portfolio` 每次调仓先全撤再重发 ⇒ 跨 bar 的挂单永远等不到成交。**为什么危险**：回测里因为「下一根 bar 立刻撮合」而看不出差别，实盘里这会直接让 maker 策略失效。⇒ **凡「先全撤再重发」的实现，必须同时报告「挂单存活根数」中位数，否则成交率不可解释。**

**D89 · 同一函数内两套缺省风格 = 埋雷**
`PortfolioDailyResult.calculate_pnl` 里 `pre_closes.get(vt, 0)` 但 `sizes[vt]` 直接下标。**为什么必须统一**：`.get` 的 0 会在「缺合约」时**静默**产出一个错的盈亏（0 前收 × 持仓 = 凭空盈亏），而直接下标会**当场炸**。两者混用，等于「一部分错被吞、一部分错被炸」——排障时你会以为只有一处问题。

**D90 · 组合 K 线合成的「边界判定」不能用循环泄漏变量**
`update_bar_minute_window` 用 `bar.datetime.minute`（for 循环最后一个 symbol 的 bar）去判**全体**符号是否收口。两标的分钟戳不同时，会用一个的边界切另一个。**为什么好**：边界判定必须**按 symbol 独立**，或显式声明「本引擎要求所有标的时间戳严格同一网格」——后者也可接受，但必须写成断言，不能靠巧合。

## 5. 可复用代码片段

```python
# 来源：portfolio_strategy/backtesting.py:607-616（合成 bar）
# 用途：复刻 vnpy 的填充语义 —— 注意它**没有**填 volume，这就是 G1 的根
bar = BarData(
    symbol=old_bar.symbol, exchange=old_bar.exchange, datetime=dt,
    open_price=old_bar.close_price, high_price=old_bar.close_price,
    low_price=old_bar.close_price,  close_price=old_bar.close_price,
    gateway_name=old_bar.gateway_name,
)   # volume / turnover / open_interest 全部默认 0
```

```python
# 来源：portfolio_strategy/backtesting.py:642-671（撮合判据 + 成交价）
long_cross  = order.direction == Direction.LONG  and order.price >= bar.low_price  and bar.low_price  > 0
short_cross = order.direction == Direction.SHORT and order.price <= bar.high_price and bar.high_price > 0
if long_cross or short_cross:
    order.traded = order.volume            # ★ 全量成交，不看 bar.volume
    order.status = Status.ALLTRADED
    trade_price = min(order.price, bar.open_price) if long_cross else max(order.price, bar.open_price)
```

落地版（本项目）：`ai_quant_lab/20261030_vnpy_vnpy_portfoliostrategy/portfolio_alignment_guard.py`
—— `build_panel / audit_panel / grid_compliance / synth_bar / cross_limit_order_vnpy / freeze_fill_probe / factor_usable_mask / tradable_mask`，**自测 40/40**，`lab_bridge` 零警告可直接 `lab_bridge.get("portfolio_alignment_guard")`。

## 6. B站学习（本日 30% 权重）
- **未执行**。第 10 轮已结案：B 站量化课程字幕接口恒返回空，按纪律**永久降级为「标题+目录级」笔记，不再记入未完成区**。本日实质产出 **0**，如实留痕（不参与任何结论）。

## 7. 对黑马策略的启发（已落到具体动作）

- **假设 H-039（已验证）**：时间轴错位**不是** 35 倍笔数差的原因。
  - 实测：网格合规率 **100.0%**、非整倍数间隔 **0.0%**、上市内真断档 **37 条 / 968156 槽位 = 0.0038%**。
  - 但尾停冻结 **9232 槽位**（ETH 4616 + DOGE 4616 = **48.1 天**），占「危险槽位」**99.6%** ⇒ 嫌疑从「错位」转到「**样本期不一致**」。
- **假设 H-040（已验证）**：冻结期限价单成交率 **100%**（加价 5% 后仍 100%），成交价恒等于冻结价 ⇒ **零流动性全量成交**。
- **若成立，改哪**：
  1. 组合回测入口（未来要做时）**必须先过 `audit_panel`**，`frozen > 0` 直接拒跑，不许「先跑完再说」。
  2. 面板层加 `tradable_mask(max_stale=0)` 硬闸 —— 我方第 12/13/14 轮做的部分成交 / 容量 / 排队三条护栏**在合成 bar 上全部失效**，不能指望撮合器拒单。
  3. **样本期必须截齐**：以四标的「末个真实 bar 的最小值」为统一终点，或按标的分段报结论 —— 48 天的尾部由 2/4 标的的假持仓决定，任何总收益数字都不可比。

## 8. 未完成 / 失败区（诚实留痕）

- ❌ **第零步 AtomCode guard：连续第 9 轮失败**。`verdict=proxy_down` → 后台拉起 `atomcode_proxy.py 13460` → 复测 `timeout 150` 直接被杀（推理层僵死，`/health` 200 但推理 HTTP=0）。非额度、非二进制（第 13 轮 `--version` 5.2.3 已验）。**降级本地 Read/Grep，全程 0 积分**，按收敛纪律不再投入时间。
- ❌ **B 站 30% 权重实质产出 0**（第 10 轮已结案降级，见 §6）。
- ⚠️ **`PortfolioBarGenerator.update_tick` 的多标的时间轴 bug 只做了静态判读，未写复现用例** —— 因为本项目没有 tick 级多标的数据（只有 15m OHLC），搭 tick 复现属"造数据验证"而非"真实数据验证"，本轮不做，记 P2。
- ⚠️ **H-039 只能排除「错位」这一个候选**，不能证明「样本期不一致」就是主因 —— 后者需要**实盘逐笔导出**才能判（挂账第 3 轮）。本条的措辞已按此收紧为「嫌疑收窄」而非「原因确认」。
- ⚠️ **自测里我自己写错 4 处判据**（详见 §10 坑 #1），全部由自测抓出后修正，非事后粉饰。

## 9. 三件套自检
- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：`ai_quant_lab/20261030_vnpy_vnpy_portfoliostrategy/portfolio_alignment_guard.py`（**40/40**，`lab_bridge` 零警告）
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-039 已验证 · H-040 已验证**（台账 40 条：已验证 21 / 已证伪 17 / 搁置 2，无悬空）

## 10. 成本与技能
- **积分 0**（AtomCode 全程不可用，纯本地 Read/Grep + 本地 Python 运算）
- **本轮踩到的真坑（自己的，不是 vnpy 的）**：
  1. **`factor_usable_mask` 首版把「历史不足」当「全真」**：`acc[k:] &= ok[:-k]` 让前 `need_bars-1` 根自动为 True，自测「需 3 根连续 → 期望 3 实得 5」抓出。★ **窗口类掩码必须显式把头部置 False**。
  2. **判据写错两次**：①「5 根 × 15min = 1.25 **小时**」被我写成「1.25 天」；②`round(...,2)` 把 0.0521 天压成 0.05 天导致量级失真。★ **判据要用操作定义，别抄口诀**（第 16 轮已记，本轮再犯一次）。
  3. **补丁回执的 `b'\\r'` 又一次数到字面反斜杠**：第一版补丁打印 `lone_cr = 1`（假），实际文件是 0。★ f-string 里嵌 bytes 转义是**固定陷阱**，改用 `bytes([13])`。
  4. **回归脚本按错的键名读结果**：`risk.demo_selftest()` 用的是 `_all_ok/_pass`，`events.demo_selftest()` 只给一组 `*_ok` 语义键 —— 我按 `all_ok/passed/total` 读，得到 `None/None` 假 FAIL。★ **只认名字里带 `ok` 的自报键，绝不外部重数布尔值**（第 18 轮已记）。

## 11. 六端归档
- 周五（周中）→ **仅 Obsidian + 工作区 `.workbuddy\memory\2026-10-30.md`**。
- ⚠️ 六端归档仍欠 **10-18 / 10-25** 两轮顺延，**2026-11-01（周日）**一并补。
