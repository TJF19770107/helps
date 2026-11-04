---
日期: 2026-10-13
仓库: backtrader（#10/12）
核心文件: backtrader/cerebro.py（1716 行）
轮次: 第 7 轮
副源: 降级（B站无 CC 字幕可达）→ 中文文档/教程级蒸馏
tags: [AI量化平台, 夜学, 代码拆解, 回填P0, 风控层, 事件层]
---

# 20261013 · backtrader · cerebro.py

## 0. 一句话结论

> **`Cerebro` 是「总编排器（Facade + 主循环）」**：它把数据层 / 策略层 / 撮合层 / 报告层
> 用一个**主循环 `_runnext()`** 串起来，并**显式声明档位差异**（`runonce` vs `runnext`、
> `exactbars`、`live`）—— 这条「**同源双引擎 + 差异显式化**」正是我方事件层最缺的那块。
> 本轮不只精读：**连续挂账 3 轮的 P0 回填真的动手做完了**（G1 + R7 + R8 + E1 全部进 `core/` 本体），
> 并且在回填过程中被 AtomCode 交叉复核**抓出两个真漏洞并当场修掉**。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：**总编排层 / 引擎门面**（横跨 撮合回测层 + 执行层 + 报告层，但不属于其中任何一层）
  —— 它是 backtrader 的 `bt.Cerebro`，用户唯一直接接触的入口对象。
- **上游依赖（被 Cerebro 持有）**：
  - `datas`（数据层，`DataFeed`/`PandasData`）· `feeds`（Store 提供的数据源）
  - `strategies` / `optstrategy`（策略层）· `sizers`（仓位层）
  - `broker`（撮合 + 执行层，默认内建 `BackBroker`）
  - `analyzers` / `observers` / `writers`（报告与观测层）· `stores`（外部网关层）· `_timers`（时间层）
- **下游调用者**：用户脚本（`cerebro = bt.Cerebro(); ...; cerebro.run()`）；
  策略基类通过 `cerebro._add_timer()` / `notify_timer()` 反向注册定时任务。
- **一句话**：**它是把「七层」组装成一个可运行系统的那一层** ——
  我方 `quant_app` 至今**没有这一层**（`cli.py serve` 只是把 core 模块拼起来，没有统一主循环与档位声明）。

---

## 2. 调用链（文字版时序图）

```
用户脚本
  └─ cerebro.run()                                  # cerebro.py:1030 — 门面入口
       ├─ 参数覆盖（kwargs → self.params）
       ├─ 缓存开关（LineActions/Indicator usecache）
       ├─ ★ 档位决策（D10/D13）：
       │     _dorunonce = p.runonce                  # 向量化开关
       │     _dopreload = p.preload                  # 预加载开关
       │     if _exactbars: _dorunonce = False       # 省内存 ⇒ 强制关向量化
       │     if _dolive : _dorunonce = _dopreload = False   # 实盘 ⇒ 两者全关
       └─ runstrategies(iterstrat)                   # cerebro.py:1171
            ├─ broker.start() / feed.start() / store.start()
            ├─ 二选一主循环：
            │    _runonce()   # cerebro.py:1649 指标预计算一次算完（快，无真实事件次序）
            │    _runnext()   # cerebro.py:1498 ===== 事件驱动主循环 =====
            │         while d0ret is not None:
            │           ① _storenotify()      # 外部网关消息回流
            │           ② _datanotify()       # 数据状态（LIVE/DELAYED）通知
            │           ③ for d in datas: d.next()      # 每路数据推进一根
            │           ④ dt0 = min(各数据 datetime)     # ★ 取最小时间 = 时间主控
            │           ⑤ _check_timers(runstrats, dt0)  # ★ 定时器绑数据时钟
            │           ⑥ 各策略 _next()                 # 策略逻辑
            │           ⑦ _brokernotify()     # cerebro.py:1360 撮合推进 + 订单通知回流
            │           ⑧ _next_writers()
            └─ stop_writers() → 返回 runstrats
出口：strategy 实例列表（含 analyzers 结果）
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `Cerebro` | 类 | 总编排器 / 门面；持有 datas/broker/strategies/analyzers/timers | `cerebro.py:60`，`MetaParams` 元类 |
| `Cerebro.run(**kwargs)` | 方法 | 门面入口；**档位决策**（runonce/preload/live/exactbars）后进入主循环 | `:1030`，D10/D13 的落点 |
| `Cerebro._runnext(runstrats)` | 方法 | **事件驱动主循环**：取 dt0 → 定时器 → 策略 → 撮合通知 | `:1498`，语义对齐我方 `EventEngine` |
| `Cerebro._runonce(runstrats)` | 方法 | 向量化主循环：指标预计算 → 一次性推进 | `:1649`，快但与实盘语义不同 |
| `Cerebro._check_timers(runstrats, dt0, cheat)` | 方法 | **定时器按数据时钟触发**（`t.check(dt0)`） | `:1706`，D11 的铁证 |
| `Cerebro.add_timer(...)` / `_add_timer(...)` | 方法 | 注册定时器（when/offset/repeat/weekdays/cheat） | `:446` / `:421`；`cheat=True` = 开盘前触发 |
| `Cerebro.notify_timer(timer, when, ...)` | 方法 | 定时回调（**默认空实现**，由子类/策略覆写） | `:410`；`when` 是**定时器值而非系统时间** |
| `Cerebro._brokernotify()` | 方法 | 撮合推进 `broker.next()` + 排空 `get_notification()` 回灌策略 | `:1360`，D12 的落点 |
| `Cerebro.runstrategies(iterstrat, predata)` | 方法 | 启动 broker/feed/store → 选择主循环 → 收尾 | `:1171` |
| `Cerebro.adddata/chaindata/replaydata/resampledata` | 方法 | 数据接入（含重采样/重播） | `:752` / `:776` / `:812` / `:831` |
| `Cerebro.optstrategy(...)` | 方法 | 参数网格搜索（返回多组 strats） | `:859`；对应我方「阶梯消融」 |
| `OptReturn` | 类 | 优化结果的轻量视图（可省内存） | `:53`，`optreturn=False` 才拿完整实例 |

---

## 4. 可迁移设计点（逐条写「为什么好」）

### D10 · 同源双引擎 + **档位差异显式声明**
`run()` 里 `_dorunonce / _dopreload / _dolive` 三者互相钳制：
`if self._exactbars: self._dorunonce = False`、`if self._dolive: _dorunonce = _dopreload = False`。
**为什么更好**：它不假装「两种模式完全一样」，而是**把差异写进约束**——
省内存⇒牺牲速度、实盘⇒牺牲可复现。我方 `EventEngine` 原本只有 `async_mode` 一个布尔，
从没说清 sync 模式下「哪些事做不到」。→ 已补 `RUN_MODE_SEMANTICS` 表（夜学模块）。

### D11 · 定时器绑**数据时钟**（`dt0`），不是墙钟 ★ 本轮直接回填
`_runnext` 先 `dt0 = min(各数据 datetime)`，再 `_check_timers(runstrats, dt0)`；
`notify_timer` 文档明写「`when` 是**定时器值而不是系统时间**」。
**为什么更好**：回测里没有真实时间流逝，墙钟定时器**既不准也不可复现**；
而 `cheat=True` 更进一步支持「开盘前触发」，把**时序语义**变成显式参数。
→ 与 hummingbot `clock.pyx` 的 D8 从两个独立方向印证同一结论。
→ 已回填 `core/events.py:advance_clock()`（+ 实盘独立线程，双模 Clock）。

### D12 · 撮合推进与**通知回流**分离
`_brokernotify()`：`broker.next()` 推进撮合 → `while True: get_notification()` 排空 → `owner._addnotification(order)`。
**为什么更好**：策略**不查询** broker 状态，只被动收通知 = 事件驱动订单状态机，
避免「策略轮询 broker」造成的时序耦合。我方 `core/live.py` 目前是回调直改状态，属耦合写法。

### D13 · 降级档位**显式化**（`exactbars`）
省内存必然牺牲向量化 —— 作者把它写成显式规则而非隐式惊喜。
**为什么更好**：**性能/内存取舍必须可见**，否则线上会出现「同一策略两个结果」。
这条直接催生了本轮 H-014 的立假设方式：**任何影响时序/规模的档位都必须独立验证**。

---

## 5. 可复用代码片段

```python
# 来源：backtrader/backtrader/cerebro.py:1706-1716（_check_timers 的 dt0 判定）
# 用途：定时器绑数据时钟 —— 我方已抽象为 EventEngine.advance_clock()
def _check_timers(self, runstrats, dt0, cheat=False):
    timers = self._timers if not cheat else self._timerscheat
    for t in timers:
        if not t.check(dt0):        # ← 判据是「数据时间」，不是 time.time()
            continue
        t.params.owner.notify_timer(t, t.lastwhen, *t.args, **t.kwargs)
        if t.params.strats:
            for strat in runstrats:
                strat.notify_timer(t, t.lastwhen, *t.args, **t.kwargs)

# 来源：backtrader/backtrader/cerebro.py:1360-1375（_brokernotify 的排空循环）
# 用途：撮合推进 + 订单通知回流（我方已抽象为 drain_notifications()）
def _brokernotify(self):
    self._broker.next()                       # ① 推进撮合
    while True:                               # ② 排空到 None 才算一次完整推进
        order = self._broker.get_notification()
        if order is None:
            break
        owner = order.owner or self.runningstrats[0]
        owner._addnotification(order, quicknotify=self.p.quicknotify)
```

> 以上两段已落地为 `ai_quant_lab/20261013_backtrader_vnpy/backtrader_engine_patterns.py`
> 的 `drain_notifications()` 与 `RUN_MODE_SEMANTICS`（自测 6/6，与 `core/risk.py` **等价性 diff = 0**）。

---

## 6. ★ 本轮核心：P0 回填真的做完了（G1 + R7 + R8 + E1）

> 前 3 轮（第 4/5/6 轮）「待跟进」里 P0 一直挂着「回填 `core/` 本体」却没动手。
> **本轮动手完成**，全部有自测数字。

### 6.1 改动清单（真实文件）

| 缺口 | 落点 | 改了什么 | 自测证据 |
|---|---|---|---|
| **G1** | `quant_app/core/risk.py` R1 | `qty = 预算/止损距离` → `qty = 预算/(止损距离 + price×fee_rate×2 [+ 滑点×2])` | 止损距离 1000/价 50000 场景：**2.0 → 1.8182 张**，超配 **+10%** |
| **R7/G3** | `core/risk.py` 新增 `reserve_order/release_order/release_fill/pending_*` | 挂单**提交即占额度**（顺序锁定），R2/R3 扣减在途名义 | 复刻血泪场景：余额 1000、两单各 601.2 → 第二单**601.2 → 398.8**（旧式仍 1202.4 超额） |
| **R8** | `core/risk.py` 新增令牌桶 `_rate_limit_ok` | `max_orders_per_sec`/`order_burst`；**只约束增大敞口方向，减仓豁免** | 前 2 笔放行、后 2 笔 `R8-报单限流`；减仓单**仍放行** |
| **E1/D8** | `core/events.py` 新增 `_run_timer()` + `advance_clock()` + `timer_stats()` | **双模 Clock**：同步=BAR 时钟推进；异步=独立定时线程 | 事件满负荷（300 根 bar）时定时任务触发 **42 次**（旧实现 0 次），最大迟到 **1.0 ms**；时钟驱动 13 次 = 首根 1 + 其后 4×3 ✓ |

### 6.2 自测结果（改动前 → 改动后）

| 模块 | 改动前 | 改动后 | 说明 |
|---|---|---|---|
| `core/risk.py` | **9/9** | **15/15** | 新增 R1含费 / R7挂单 / R8限流 / R8减仓豁免 / 反向穿越不豁免 / 滑点进分母 六项检查，**原有 9 项无退化** |
| `core/events.py` | `same_source_ok=true` | `same_source_ok=true` + `e1_independent_ok=true` + `e1_clock_ok=true` | 原有同源性验证无退化 |
| `quant_app` 冒烟 | — | **9/9 模块 import 通过**，`lab_bridge` **零警告** | — |

### 6.3 ★★ AtomCode 交叉复核抓到两个真漏洞（本轮最有价值产出之一）

走了 13460 OpenAI 兼容端点（免费档 `glm5.3-flash`），4 问 4 答，回复存 `atomcode_reply.md`（3222 B）。
**不盲从**：其建议的「实时对账 reconcile」「注入 5% 拒单率」因我方**尚无实盘接单通道**降优先级；
但下面两条**当场采纳并修掉**：

| 抓到的漏洞 | 我的原实现 | 真问题 | 修复 |
|---|---|---|---|
| **减仓判定按「方向」而非「净敞口」**（Q3） | `_is_reducing` = `(p.qty>0 and signed<0) or ...` | 持仓 **+10 卖 15** → 被判「减仓」**无条件放行**，实际净敞口从 +10 **翻成 −5** = 反向开仓！ | 判据改为「未平净 且 **不反向穿越** 且 绝对值下降」；自测：翻仓单被 `R2` 拦（`flip_allowed=False`），纯减仓仍放行 |
| **A 式闭式解漏掉滑点**（Q1） | 分母只有止损距离 + 手续费 | 滑点在多数品种贵过手续费（H-011 已证「乐观偏差主因=执行成本假设」） | 分母增加 `slippage_rate×price×2` 项；自测：1.8182 → **1.73913**（+0.0005 单边滑点） |

> AtomCode 原话（Q3）：「豁免判定用『持仓变化后的净敞口是否下降』，而非订单自身的买/卖属性。」
> 这条**修掉了一个我自己写了两次都没看见的洞** —— 且它与 2026-10-12「闸的默认值必须与多数情形一致」**同族**。

---

## 7. B站学习（本日 30% 权重 · **降级**）

- **状态**：❌ **未拿到 CC 字幕**（B站字幕需登录态 / cookie，本链路仍不可达）→ 按预案降级为「清单 + 文档级蒸馏」。
- **视频清单（待补，明日或拿到 cookie 后补字幕）**：
  - UP「**量化NPC**」· 《backtrader量化回测保姆级教学【合集】》
    - 【1.初识backtrader】·【2.backtrader框架介绍】—— 配套 CSDN 图文（`blog.csdn.net/weixin_38132951/article/details/129181631`）
    - 核心：`Cerebro` 六件套 = 策略 strategies + 数据 datafeeds + 分析器 analyzer + 输出 writer + 观测 observer + **大脑 cerebro**
    - 四步回测：**创建大脑 → 添加数据 → 添加策略 → 打印结果**
- **文档级素材（已蒸馏，非视频）**：
  - `juejin.cn/post/7357288361235775529`（BackTrader 中文文档）：
    ★ **「事件和矢量化：交易逻辑和经纪人**始终**基于事件运行；如果可能，指标的计算是矢量化的」**
    —— **与 D10 完全一致**：向量化只是**指标计算的优化**，**交易逻辑永远是事件驱动**。
    这是本轮最有价值的一句外部印证：我方 `_runonce` 类优化也只能限于指标层。
  - `poloxue.com/posts/2025-04-16-macross-using-backtrader/`：
    设置了 `cerebro.broker.setcommission(0.0005)` + `set_slippage_perc(0.0001)` ——
    **费率与滑点是两个独立参数**，正是 AtomCode Q1 指出的那一点。
  - 同文中的风险控制写法：「止损位置 = 当前价 − n×ATR；**最大亏损不超过账户 2%，按此目标反推下单金额**」
    —— 就是 G1 的中文社区版本（但同样**没扣手续费**，印证这是行业性通病，不是我们独有的疏忽）。
- **存疑处（待代码验证）**：backtrader 的 `set_slippage_perc` 是否对**止损单**同样生效（未读源码，不猜）。

---

## 8. 对黑马策略的启发（具体动作）

| # | 动作 | 落到哪里 | 已做/待做 |
|---|---|---|---|
| 1 | R1 仓位反推**含双边手续费** | `core/risk.py:pre_trade_check` R1 分支 | ✅ **已做**（1.8182 张，超配归零） |
| 2 | 报单统一走**顺序锁定**入口 | 调用方改用 `RiskEngine.reserve_order()` | ✅ API 已就绪；**调用点待接**（见未完成区） |
| 3 | 定时任务脱离事件线程 | `core/events.py` | ✅ **已做**（42 次 vs 0 次） |
| 4 | 订单状态走**通知回流**（禁轮询） | `core/live.py` | ⏳ 待做（无实盘通道，优先级 P2） |
| 5 | 黑马回测加 `stream=True` 逐 bar 模式与向量模式做差异对照 | `core/backtest.py` | ⏳ 待做（D10 的落地形式） |

### 本轮新增假设（详见台账）

| # | 假设 | 结论 | 关键数字 |
|---|---|---|---|
| **H-014** | 入场附加「波动率不高于自身 2000 根滚动中位数」门槛后，含成本单笔均值不下降 | **已证伪** | 1/4 不下降；BTC 2.0061→1.074（**−0.9321**）；ETH +0.7443；BNB −0.1538；**DOGE 0.6738 → −0.6217** |
| **H-015** | 平仓后强制冷却 96 根（1 天）后，含成本单笔均值不下降 | **已证伪** | 1/4；BTC 2.0061→1.3521；ETH 2.373→1.9546；BNB +0.2698；DOGE 0.6738→0.1791 |

> **★ H-014 的副产物（重要）**：DOGE 在**低波动门槛**下**从 +0.67% 恶化到 −0.62%** ——
> 说明 DOGE 的系统性亏损**不是**来自高波动时段。**「DOGE 亏损 = 波动率问题」这条归因路径被独立回测排除。**
> 卡玛说明：两条都是「让策略更保守」型假设，天然有证伪风险 —— **砍掉入场机会 ≠ 提升单笔质量**（第 4 次印证）。

---

## 9. 未完成 / 失败区（诚实留痕）

1. ❌ **B站 CC 字幕仍未拿到** —— 连续第 6 轮受登录态限制。本轮降级为「清单 + 中文文档级蒸馏」，不装懂。
2. ⏳ **R7 顺序锁定的「调用点」未接** —— `reserve_order()` API 与自测已就绪，但 `core/backtest.py`/`core/live.py` 的报单路径**尚未改用它**（仍是直接 `pre_trade_check`）→ 下一步 P0。
3. ⏳ **`slippage_rate` 默认 0（未启用）** —— 参数与分母已实现，但**滑点系数需按品种用实盘成交标定**，我没有实盘成交日志 → 属**已知缺口**，已在代码注释里写明，不静默填一个假数。
4. ⏳ **部分成交路径在回测里测不到** —— `release_fill()` 已实现并有 API，但回测撮合器**无拒单/部分成交模型**（AtomCode Q2 指出：回测里 reserve→成交几乎必然，属**结构性乐观**）→ 需给回测撮合器注入少量拒单/部分成交率才能覆盖 release 分支。
5. ⏳ **D1~D4（策略层）、D9（在途态 OMS）、G2（三态状态机）仍未回填** —— 本轮只完成了 G1/G3/G4/E1 四条。
6. ⏳ **`_runonce` vs `_runnext` 的结果差异未实测**（无 backtrader 运行环境，未 `pip install`）。
7. ⚠️ 前两轮报过的 **C 盘空间**问题本轮已缓解（自检显示 **45.28 GB**），不再列为风险项。

---

## 10. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
  `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\AI量化平台\学习笔记\20261013_backtrader_vnpy.md`
- [x] ② 可复用代码落盘：
  - `ai_quant_lab\20261013_backtrader_vnpy\backtrader_engine_patterns.py` —— 自测 **6/6**，
    含 `fee_aware_qty` / `over_allocation_curve` / `OrderLedger` / `drain_notifications` / `RUN_MODE_SEMANTICS`，
    与 `core/risk.py` **等价性 diff = 0.0**，`lab_bridge` **零警告**加载 ✓
  - `ai_quant_lab\20261013_backtrader_vnpy\TASK_CARD.md`（自检脚本自动生成，同目录）
  - `ai_quant_lab\20261013_backtrader_vnpy\atomcode_prompt.txt` / `atomcode_reply.md`（交叉复核留档）
- [x] ③ 策略假设已追加进 [[策略假设台账]]（H-014 / H-015 均**当日结清**，无悬空）
  结果文件：`策略假设/回测结果/回测结果_20261013.json`

---

## 11. 成本与技能

- **本次花费积分估算：0**（全程零积分）
  - 第零步 guard：本地脚本 + 13460 本地代理 → **0**
  - 第一步自检 / 精读 / 回填 / 自测：纯本地 Python（quant_env）→ **0**
  - AtomCode 交叉复核：走 13460 免费档 `glm5.3-flash` → **0**
  - hypothesis_runner：纯本地 numpy/pandas → **0**
  - B站：未抓取（降级）→ **0**
- **精读引擎**：① 13460 实测可用（guard `healthy`，推理 200 / 11.0 s / 回字「通了」）→ 用它做了交叉复核；
  主体精读走本地 Read/Grep（代码量大、需要精确行号，本地更可靠）。
- **技能**：`ai-quant-open-source-nightly-learning` **v1.1.4 → v1.1.5**（新增 §3.7 六条：回填类任务的验收姿势 / 交叉复核的正确用法 / 自测检查项命名 / 反向穿越漏洞 / 滑点缺口 / 台账新增行必须同步 REGISTRY）。

---

## 12. AI 分身 / 归档状态

- **归档节奏**：2026-10-13 是**周二（周中）** → 只落 **Obsidian + 工作区 `.workbuddy\memory\2026-10-13.md`**；
  六端归档等**周日（2026-10-18）**。
- **README 索引**：已挂本笔记 + 本轮新增设计文档。

---

## 附录 · 10 天学习蓝图（AI量化平台架构对标 × 黑马策略）

> 说明：原指令末尾的「针对【主题】制定 10 天学习蓝图」未指定具体主题；
> 我按本项目的**实际主题**（`AI量化平台七层架构对标 + 黑马策略实证`）制定，若需换题请告知。

**总目标**：把 `quant_app` 从「四化 2.4/4」推到**「七层全落地 + 回测与实盘同源 + 每个假设都有独立回测」**的研究平台水平。

| 天 | 主题（输入） | 每日练习任务（可执行） | 费曼输出检验题 | 自测节点 |
|---|---|---|---|---|
| D1 | 事件层（本日） | 已做：双模 Clock + timer 独立线程 | 用 3 句话向非量化者解释「为什么回测的定时器不能用墙钟」 | `events.py` 自测 `e1_independent_ok` 通过 |
| D2 | 风控层补全 | 回填 G2 三态状态机 + 同步改 `live.py`/`backtest.py` 调用点 | 「停机后为什么必须允许减仓？如果禁止会怎样？」 | `risk.py` 自测 ≥15/15 不退化 |
| D3 | 报单链路 | 报单路径改用 `reserve_order()`；接 `release_fill` | 「顺序锁定在回测里为什么结构上做不到？」 | 两单并发场景 A/B 差异可复现 |
| D4 | 成交现实化 | 给回测撮合器注入 5% 拒单 + 20% 部分成交率 | 「回测乐观偏差的主因是时点还是成本？证据是什么？」 | release 分支被覆盖（覆盖率而非感觉） |
| D5 | 策略层 D1/D2 | `safe_call` 隔离墙 + 引擎面/用户面分离 | 「为什么要把用户策略当不可信输入？」 | 注入一个会抛错的策略，引擎不崩 |
| D6 | 报告层 D4 | 信号归因进 `core/report.py`（毛/净双列） | 「归因观察值为什么不能直接当规则？」 | 报告能输出每 tag 的含成本单笔均值 |
| D7 | 数据层 | 15m 全历史 → 统一 `_agg_bars` 口径 + 缺口检测 | 「timestamp 与 open_time 的口径差会怎么静默改变结论？」 | 4 只标的聚合结果与已知基线一致 |
| D8 | 交叉学习 | 读 `freqtrade/optimize/backtesting.py` 撮合引擎 | 「freqtrade 的成交次序与我们的有什么不同？」 | 写出 1 条可回测假设并注册 |
| D9 | 间隔重复 | 重跑 H-001~H-015 全部验证器，检查状态机一致性 | 「哪条结论若换了尺子就会翻转？」 | 台账往返幂等（无列位移、无 warning） |
| D10 | 综合产出 | 出一份《平台七层落地度 + 未闭环清单》并做六端归档 | 「诚实说出 3 个我们**做不到**的事」 | 全部自测通过 + 归档 6 端可独立核验 |

**薄弱点识别（实事求是）**
1. **回测≠实盘的结构性乐观**（无挂单簿/无部分成交/无拒单）—— 本轮与上轮反复撞到，是**最大系统性风险**。
2. **执行成本未标定**（滑点默认 0、`k_vol` 未用实盘成交标定）—— 而 H-011 已证「乐观偏差主因就是它」。
3. **归因结论的可交易性**：H-013 已示范「同批样本内最优 → 独立回测即崩」，必须持续用 A/B 校验。
4. **B站学习链路**（登录态受限）连续 6 轮降级 —— 学习输入的多样性偏低，是方法层面的短板。
