# AI量化平台 · 夜学笔记库

> **建立**：2026-10-07 · 汤小龙（WorkBuddy 宿主分身）
> **触发源**：汤哥 2026-10-07 下令 —— 用 AtomCode 每天凌晨 4:00 精读 GitHub 开源量化项目（对标 VNPY 家族 + 机构级框架），反哺「AI 量化平台」与「黑马策略」
> **驱动任务**：「AI量化平台·开源精读夜学（AtomCode·零积分）」
> **成本**：零积分优先（免费档模型 + 本地 CLI 精读），不烧付费档

---

## 一、这个库是干什么的

把「读别人代码」变成**能变现的生产力**，不是读书笔记收藏夹。每天晚上 4 点自动跑一轮，产出「四件套」：

| # | 产出 | 落点 | 验收 |
|---|------|------|------|
| ① | 代码拆解笔记（架构图 + 调用链 + 可迁移设计点） | `学习笔记/` | 能讲清「这个文件在系统里管什么」 |
| ② | 可复用代码/模块片段（真实文件，能跑） | `我的黑马策略/ai_quant_lab/<日期>_<仓库>_<模块>/` | 有真实路径 + **能被 `core/lab_bridge.py` 加载** |
| ③ | 可回测的策略假设（入场/出场/止损 + 待验指标 + **可证伪条件**） | `策略假设/策略假设台账.md`（追加式） | 次日能挂回测 |
| ④ | **台账状态推进**（前日悬空假设必须结掉） | 跑 `hypothesis_runner.py` → 回写台账 + `策略假设/回测结果/` | 状态从「待验」推进到 已验证/已证伪/搁置 |

**缺一件 = 当日算失败**，失败原因必须写进当日笔记的「未完成」区。
**回测执行失败只能标「搁置」，严禁把失败翻译成「已证伪」。**

---

## 二、目录结构

| 目录 | 装什么 | 更新频率 |
|---|---|---|
| `学习笔记/` | 每日拆解笔记 `YYYYMMDD_<仓库>_<文件>.md` | 每天 1 篇 |
| `代码拆解/` | 专题深拆（按主题聚合，如「事件引擎」「回测撮合」「风控」） | 攒够 3 篇同类后归并 |
| `策略假设/` | 可回测假设台账（追加式，带状态：待验 / 已验证 / 已证伪） | 每天 +≥1 条 |
| `平台设计/` | AI 量化平台架构沉淀（从对标框架里薅出来的设计） | 有结论才写 |

---

## 三、铁律（不可违反）

1. **不承诺收益率**。只写「可验证的结构/因子假设 + 回测证据」。任何「翻倍 / 10 倍 / 100 倍」的说法，**必须回测证实后才能进结论区**，否则只能留在「假设」区并标记未验证。
2. **验证优先于观点**。听到的说法（含 B 站课程、博主口播）一律先当假设，不当结论。
3. **密钥脱敏**。`sk-` / `token` / `secret` 不进笔记、不进 git、不进云端正文。
4. **未完成要留痕**。克隆失败、依赖缺失、环境不通 —— 如实写进「未完成」区，不粉饰。
5. **G 盘不可依赖**。外接盘常离线（2026-10-07 实测未挂载），本库以 E 盘为准。

---

## 四、索引

### 规范与总账
- [[_每日笔记模板]] —— 每日笔记的标准骨架
- [[_拆解规范]] —— 怎么拆一个代码文件才算合格
- [[策略假设台账]] —— 假设总账（追加式，唯一入口）
- [[AI量化平台架构蓝图]] —— 目标架构 v0.2（验证中，已含 3 条源码实证设计）

### 平台设计评估
- [[AI量化平台_四化成熟度评估_20261008]] —— 1234 四化打分（总分 ≈2.4/4）+ 七层对照 + get 化三步路径
- [[AI量化平台_七层补口与假设闭环打通_20261009]] —— **七层补满 7/7**：事件层 + 风控层落地自测；台账升级为状态机；AtomCode 403 根因修复
- [[AI量化平台架构蓝图]] —— 目标七层架构（蓝图，非实现）
- [[AI量化平台_风控层对标nautilus升级设计_20261009]] —— **风控层对标升级**：nautilus 四条缺口（含费风险预算 / 三态状态机 / 挂单占用 / 报单限流）+ vnpy 事件层三条（timer 独立线程等），含落地优先级
- [[AI量化平台_策略层对标freqtrade升级设计_20261010]] —— **策略层对标升级**：freqtrade 四条设计（回调隔离墙 D1 / 引擎面冻结分离 D2 / 出场成交次序 policy D3 / 信号归因 D4）+ 下一轮落地优先级 P0→P2
- [[AI量化平台_成交现实化层对标hftbacktest设计_20261011]] —— **成交现实化层**：hftbacktest 五条设计（延迟=架构层时间戳 / 拒单用负延迟 / 手续费毛净两套账 / 可插拔费用模型 / 差距必须可归因）+ 三级成交口径 + 阶梯消融；实测**结构性时点效应极小、收益对未标定滑点系数极敏感**
- [[AI量化平台_订单预算前置层对标hummingbot设计_20261012]] —— **订单预算前置层**：hummingbot 四条设计（D5 顺序锁定 / D6 手续费进抵押品 / D7 闸只缩不放 / D8 双模 Clock 同 c_tick）+ D9 在途态建模；直接对症风控层 G1/G3 与事件层 E1；含 AtomCode 复核的四条实盘前置
- [[AI量化平台_编排层对标backtrader设计_20261013]] —— **编排层**：backtrader `cerebro.py` 四条设计（D10 同源双引擎+档位差异显式声明 / D11 定时器绑数据时钟 / D12 撮合推进与通知回流分离 / D13 降级档位显式化）；★ **本轮把连续挂账 3 轮的 P0 真的做完了** —— G1 含费闭式解 + R7 顺序锁定 + R8 令牌桶 + E1 双模 Clock 全部进 `core/` 本体（`risk.py` 自测 9/9 → **15/15**，`events.py` 新增 E1 双项自测）；AtomCode 交叉复核**抓出并修掉两个真漏洞**（减仓判定按方向→按净敞口、闭式解漏滑点）
- [[AI量化平台_实验记录与任务生命周期层对标qlib设计_20261014]] —— **实验记录与任务生命周期层（首个非交易链路对标）**：qlib 六条设计（**D14** 领取→提交/归还崩溃安全三段式 / **D15** 显式依赖+递归校验+幂等重跑 / **D16** 四态含 `PART_DONE` / **D17** 在途态属于订单本体 / **D18** 毛账净账**强制并列** / D19 可交易性建模）；★ 缺口已从「交易链路」移到「工具/生命周期链路」（`live.py` 142 行 · `report.py` 156 行两张最薄的皮）；AtomCode 复核给出三条关键修正（**manifest 轻量替代** / **净账必须给 k 敏感性区间** / **订单只读视图+单一写者**）
- [[AI量化平台_组合回测层对标vnpy_portfoliostrategy设计_20261019]] —— **组合回测层**：vnpy 组合回测引擎五条设计（**D20** 额度必须在报单唯一入口(vnpy 反向印证) / **D21** 三账分离 holding+trading=毛、减费滑=净 / **D22** 手续费与滑点各自独立累计 / **D23** 平盘 bar 保时序但**合成 bar 不可成交** / **D24** 全额成交是已知乐观需外部注入折损）；★ **两块挂账 P0 真的接通了**：`run_backtest(risk=)` 走 `reserve_order()`（接线自测 **10/10**，`risk=None` 路径逐字节等价）+ `build_cost_account()` 毛净双列/k 敏感性；★★ **抓到影响全部 17 条历史假设的口径 bug：`pnl_pct` 不含手续费，实测乐观 0.2041pp/笔**
- [[AI量化平台_多市场组合网关对标vnpy_binance设计_20261020]] —— **多市场组合网关层**：vnpy 组合保证金网关四条设计（**D25** 端点路由下沉网关(fail-open 反例) / **D26** 先落库再发请求 / **D27** 本地 ID 即幂等键 / **D28** 拒单与网络未知必须分开）+ **D29 反例**（持仓归零必须推送）；★ 本轮真改动：**G2 风控四态状态机**（HALTED→RECOVERING→NORMAL，`risk.py` 16/16→**24/24**）+ **`live.py` 补上报单唯一入口**（**4/4**）；AtomCode 三条建议全采纳（**reduce_only 声明必须与持仓交叉校验**、R 归一晋级、系数随回撤递减）
- [[AI量化平台_订单对账层对标nautilus_trader设计_20261021]] —— **订单对账层**：nautilus 五条对账设计（**D30** 未变化 Ack 必须丢弃(本地意图优先旧回执) / **D31** `venue_order_id` 是链不是点 / **D32** 成交回退语义由**通道**决定(快照可认·增量必丢) / **D33** venue 时序 + 克隆体预投影 / **D34** 对账两次未命中才收口）+ **D35** `is_open()\|\|is_inflight()`；★ 本轮真改动：新建 **`core/order_lifecycle.py`**（7 态 + 对账，自测 **8/8**）+ `live.py` 接线（**4/4→8/8**）+ **W7 manifest 最小版**（自测 **7/7**）
- [[AI量化平台_撮合现实化层对标freqtrade设计_20261022]] —— **撮合现实化层（二刷改读撮合仿真）**：freqtrade `optimize/backtesting.py` 五条设计（**D36** 二元成交必须被显式承认为上限 / **D37** 止损成交价走「开盘穿越优先」而非止损价 / **D38** 限价报价必须夹在当根区间内 / **D39** 撤单三态（删单·撤单·保持）不能压成布尔 / **D40** 撮合约束必须自带咬合力计数）；★ 本轮真改动：`core/backtest.py` 新增 `gap_stop`/`participation`/`reject_prob` 三开关 + `selftest_fill_realism()` **10/10**（默认全关零退化）；★ **H-024 已证伪**：4 只标的 6 年全历史 **835 笔止损 / 0 笔跳空穿损** → 乐观偏差主因**不是**止损成交价；★ **H-023 补档**：加 `25/20/12`、`30/25/15` 两档后 4 只**又全选最松档（端点第二次外移）**
- [[AI量化平台_撮合队列层与持仓对账对标hftbacktest设计_20261023]] —— **撮合队列层 + 持仓对账**：hftbacktest 十条设计（**D41** 成交判据是队列位置不是价格触及 / **D42** `trade`+`depth` 双通道必须用 `cum_trade_qty` 去重 / **D43** 数量减少直接夹断不做概率分摊 / **D44** 部分成交按 `lot_size` 取整 / **D45** 队列概率无唯一解只能标定 / **D46** taker 单不受队列约束→容量须单独建模）+ nautilus 四条（**D47** 容差绑 `size_precision`、`precision=0` 零容差 / **D48** 生命周期按归零切不按翻转切 / **D49** 合成价只封上侧且向下取整 / **D50** 合成回报前判"快照是否已含"）；★ 本轮真改动：`core/backtest.py` **参与率标定表接线**（`participation_for(symbol)`，自测 **6/6**）+ `core/order_lifecycle.py` **持仓三态对账**（`reconcile_position`，自测 **9/10→10/10**）
- [[AI量化平台_成交价格模型对标hummingbot与backtrader设计_20261024]] —— **成交价格模型层（二刷改读撮合仿真）**：hummingbot `paper_trade_exchange.pyx` + backtrader `bbroker.py:994-1036` 九条设计（**D51** 成交价应来自簿级 VWAP 而非收盘价+常数→无盘口快照故降级 P2 / **D52** 延迟必须是参数 / **D53** 限价成交是双通道 OR（maker 方向取反）/ **D54** 资金不足时限价 Cancel、市价 Failure 两种终态 / **D55** 量化在报单前且不足一 lot 归零 / **D56** 费进抵押品 / **D57** ★反例：hummingbot VWAP 分母用请求量，把「深度不足」吃掉了 / **D58** ★★滑点必须夹回当根 `[low,high]`（越界占比 12.6%~22.4%）/ **D59** `slip_out=False`：宁可不成交也不给不存在的价）；★★ **结论是「撮合模型这条线到此为止」**：滑点夹断实测只值 **+0.0014~+0.0038pp/笔**，而手续费 **0.2041pp/笔** ⇒ 乐观偏差 98% 的账在手续费档位，不在撮合模型 ⇒ **换赛道**
- [[学习蓝图_10天_平台工程化与黑马实证_20261014]] —— **10 天学习蓝图**：基于费曼输出·主动回忆·间隔重复·交叉学习；含 7 行可量化诊断表、**8 条有证据的薄弱点（W1~W8）**、10 天日程（每日 3 小时）、**10 道费曼检验题（各带 2 层追问）**、12 张知识卡片清单、5 个自测节点（N1~N5）；★ 诚实边界：目标 = 工程严谨度进入细分前 10，**不是**收益前 10（**D6 实况见 §九**）

### 每日笔记（夜学流水线产出）
| 日期 | 仓库（主/副） | 核心文件 | 笔记 | 三件套 |
|---|---|---|---|---|
| 2026-10-08 | vnpy/vnpy_binance · vnpy/vnpy_ctastrategy | linear_gateway.py · template.py | [[20261008_vnpy_vnpy_binance]] | ✅ 笔记+代码+假设(H-001/002/003) |
| 2026-10-09 | nautilus_trader · vnpy/vnpy | crates/risk/src/（风控层）· event/engine.py | [[20261009_nautilus_trader_vnpy]] | ✅ 笔记+代码(2 模块 25/25 自测)+假设(H-004/005) |
| 2026-10-10 | freqtrade · （副源降级：B站无字幕） | strategy/interface.py · strategy_wrapper.py | [[20261010_freqtrade_vnpy]] | ✅ 笔记+代码(1 模块自测全通过+lab_bridge 零警告)+假设(H-006/007/008 当日结清) |
| 2026-10-11 | hftbacktest（#8）· （副源降级：B站无字幕） | Rust 核心 evs.rs / mod.rs / order.rs / models/{latency,fee}.rs · stats/metrics.py | [[20261011_hftbacktest_vnpy]] | ✅ 笔记+代码(1 模块自测全通过+lab_bridge 零警告)+假设(H-009/010/011 当日结清)+修复台账回写器真 bug |
| 2026-10-12 | hummingbot（#9）· （副源降级：B站无 CC，改用官方文档中文镜像 + AS 科普补足） | pure_market_making.pyx(`c_apply_budget_constraint`) · connector/budget_checker.py · core/clock.pyx · strategy/order_tracker.pyx | [[20261012_hummingbot_vnpy]] | ✅ 笔记+代码(order_budget_guard.py 自测 21/21+lab_bridge 零警告)+假设(H-012/013 当日结清)+AtomCode 交叉复核 |
| 2026-10-13 | backtrader（#10）· （副源降级：B站无 CC，改用 BackTrader 中文文档 + 社区教程蒸馏） | cerebro.py（`run`/`_runnext`/`_check_timers`/`_brokernotify`/`add_timer`） | [[20261013_backtrader_vnpy]] | ✅ 笔记 + 代码(backtrader_engine_patterns.py 自测 6/6 + 与 core/risk.py **等价性 diff=0** + lab_bridge 零警告) + 假设(H-014/015 当日结清) + **★ P0 回填完成**(risk 9/9→**15/15**，events 新增 E1 自测) + AtomCode 抓出 2 个真漏洞并修复 |
| 2026-10-14 | microsoft/qlib（#11）· （副源降级：B站无 CC，连续第 7 轮，改用 qlib 官方文档中文镜像 + docs 目录蒸馏） | workflow/task/manage.py（TaskManager 四态）· workflow/record_temp.py（RecordTemp/ACRecordTemp）· backtest/decision.py（Order）· backtest/executor.py（NestedExecutor） | [[20261014_microsoft_qlib]] | ✅ 笔记 + 代码(qlib_workflow_patterns.py 自测 **46/46** + lab_bridge 零警告) + 假设(H-016/017 当日结清) + AtomCode 4 问 4 答 + **门槛咬合力诊断**（H-016 砍 77.7% / H-017 砍 1.3%） |

| 2026-10-19 | vnpy/vnpy_portfoliostrategy（#12）· （副源降级：B站 API **HTTP 412** 风控，连续第 8 轮；改用官方文档中文版+README+script 蒸馏） | vnpy_portfoliostrategy/backtesting.py（1026 行：`new_bars` / `cross_limit_order` / `send_order` / `ContractDailyResult.calculate_pnl`） | [[20261019_vnpy_vnpy_portfoliostrategy]] | ✅ 笔记 + 代码(portfolio_engine_patterns.py 自测 **19/19** + lab_bridge 零警告 + core import 13/13) + 假设(**H-018/H-019 均已验证 4/4**) + **P0 回填**(R7 接线 10/10、risk 15/15→**16/16**、毛净双账) + AtomCode 4 问 4 答(采纳 reduce_only) |

| 2026-10-20 | vnpy/vnpy_binance（#5 二刷，改读**同层最大且从未读过**的文件）· （副源：B站字幕**永久放弃**（W3 结案）→ 标题/目录级笔记） | portfolio_gateway.py（2146 行：`get_market_type` / `send_order` / `on_send_order_failed|error` / `on_query_*_position` / `UserApi.on_order|on_execution_report`） | [[20261020_vnpy_vnpy_binance]] | ✅ 笔记 + 代码(portfolio_gateway_patterns.py 自测 **13/13** + lab_bridge 零警告) + 假设(**H-020 已证伪 0/4**、**H-021 已验证 4/4 但咬合力≈0**) + **P0 回填**(G2 四态 risk **16/16→24/24**、`live.py` 报单入口 **4/4**、接线 10/10 无退化) + AtomCode 3 问 3 答(**Q1 绕过路径已修**) |
| 2026-10-21 | **已验证（4/4，★首次咬合力合规）**（**成本端·咬合力修正版**：挂单价下移 **0.05%**（k 由实测标定，信号级放行率 **79.44%/83.54%/79.81%/87.31%**，全部落进 70~95% 带）；净额单笔均值 BTC 1.8021→**1.8648**(+0.0627) / ETH 2.1683→**2.3108**(+0.1425) / BNB 2.1193→**2.2989**(+0.1796) / DOGE 0.4726→**0.5824**(+0.1098)。★ 同时抓出**度量 bug**：`笔数比` 99.29%/108.53%/96.04%/93.43% ≠ 信号级放行率 64.50%/72.09%/66.32%/78.27% —— 策略只在空仓开仓，「少做单」会被「换一批单」掩盖 → **咬合力的分母必须是信号数**（H-019/H-021 的「咬合≈0」口径有误）） | **已验证（4/4，样本外）**（**出场端·内部最优档 + 样本外**：训练段前 70% 扫 4 档 `8/6/4`/`10/8/5`/`15/12/8`/`20/15/10`，4 只标的全选 `20/15/10`；样本外后 30% 净额单笔均值 BTC 0.6028→**1.3515** / ETH 0.8263→**2.3208** / BNB 1.1740→**3.6472** / DOGE −0.9418→**−0.4578**。★★ **但最优落在网格边界**，而 H-020 已知 `let_run` 是 0/4 全负 → 最优必在 `20/15/10` 与 `let_run` 之间，下轮须补 `25/20/12`/`30/25/15` 才能定位；**结论只能写「存在内部最优」，不能写「越松越好」**） | `策略假设/回测结果/回测结果_20261021.json` |
| 2026-10-22 | freqtrade（#7 二刷，改读**撮合仿真层**：`backtest_loop` 是 hyperopt 每次迭代都调的路径）· （副源：B站**永久降级**；改用仓库自带测试当反例源 —— `tests/optimize/test_backtesting.py` 2956 行 / 49 个 test 里，`_get_order_filled`/`_get_close_rate*` **被直接引用 0 次**） | optimize/backtesting.py（1977 行：`_get_order_filled` 787 / `_get_close_rate_for_stoploss` 597 / `get_valid_entry_price_and_stake` 1025 / `check_order_cancel` 1377 / `backtest_loop` 1519）+ exchange/exchange.py（4380 行 · 滑点常数 1261） | [[20261022_freqtrade_vnpy]] | ✅ 笔记 + 代码(fill_realism.py **24/24** + 与 core **diff=0** · lab_bridge 零警告) + 假设(**H-024 已证伪**：跳空穿损 0/835 · **H-023 补档 6 档**：端点第二次外移，样本外 3/4) + **P0 回填**(`core/backtest.py` 撮合三开关 + `selftest_fill_realism` **10/10**、回写器 CRLF bug 修掉) |
| 2026-10-23 | hftbacktest（#5 二刷，改读**队列层**：`models/queue.rs` 1366 行 + `proc/nopartialfillexchange.rs` 649 行） · （副源：nautilus_trader 三刷，改读**持仓对账层** `reconciliation/positions.rs` 1038 行；B站**永久降级**为标题级） | models/queue.rs（`RiskAdverseQueueModel` L44 / `ProbQueueModel` L139-217 / `is_filled` 按 `lot_size` 取整 L207-216） + proc/nopartialfillexchange.rs（`check_if_buy_filled` L139-162 / `process` L529-607） · positions.rs（`check_position_reconciliation` L431 / `is_within_single_unit_tolerance` L1026 / `adjust_fills_for_partial_window` L218） | [[20261023_hftbacktest_vnpy]] | ✅ 笔记 + 代码(queue_position_model.py **20/20** · position_reconciliation.py **25/25** · participation_calibration.py **11/11** + 真实标定表 · lab_bridge 零警告) + 假设(**H-025 已验证：容量不咬** · **H-026 已证伪：排队不紧** · **H-023 补第 7 档 `40/32/20` 已验证 3/4，端点第三次外移**) + **P0 回填**(参与率标定接线 6/6、持仓三态对账 10/10、**`manifest_min` 接进假设回测链**：跑完自动落清单 + 与上一份 diff、修 `update_ledger` 空证据清空 bug) |
| 2026-10-24 | hummingbot（#9 二刷，改读**撮合仿真层**：纸面交易所的真成交路径）· backtrader（#11 二刷，改读**撮合价格层** `brokers/bbroker.py`） | `connector/exchange/paper_trade/paper_trade_exchange.pyx`（1139 行：`c_execute_buy` 445 / `simulate_buy` 逐档吃量 454-460 / `TRADE_EXECUTION_DELAY` 144 / `c_quantize_order_amount` 1078-1086 / `c_match_trade_to_limit_orders` 895-939 / `c_process_crossed_limit_orders` 836-892）+ `core/data_type/order_book.pyx`（483 行 · `simulate_buy/sell` 283-309）+ `connector/budget_checker.py`（161）+ `brokers/bbroker.py`（`_slip_up/_slip_down` 994-1036） | [[20261024_hummingbot_vnpy]] | ✅ 笔记 + 代码(`fill_price_model.py` **26/26** + 标定表 + `core/backtest.py` 新增 `slip_price`/`quantize_qty` 与 `clamp_slip`/`lot_size` 两开关 `selftest_slip_lot_wiring` **13/13**，lab_bridge 加载成功) + 假设(**H-027 已证伪**：入场越界占比 4/4 **低于**全样本，BTC −13.91pp；**H-028 已验证**：夹断不劣化 4/4，Δ +0.0014~+0.0038pp，咬合力占比 12.5%~29.6%，但 `qty_zeroed=0` ⇒ 粒度半边**未观测**) + 回归全绿（fill_realism **10/10** · participation **6/6** · risk_wiring **10/10**） |

### 假设验证结果（hypothesis_runner 自动产出）
| 日期 | H-001 | H-002 | H-003 | H-004 | H-005 | 结果文件 |
|---|---|---|---|---|---|---|
| 2026-10-09 | 搁置（缺 funding_rate 数据） | **已验证·但不可交易**（23824 样本，z=-15.32，含成本单笔 -0.19%） | 搁置（前提未出现） | **已证伪**（8184 样本，收阳率低 7.20pp，z=-13.02；即「持续买压=更强反转」，含成本仍不可交易） | **已验证**（R1 不扣费超预算 +5.00%~+50%，含费解残差 0） | `策略假设/回测结果/回测结果_20261009.json` |

| 日期 | H-006 | H-007 | H-008 | 结果文件 |
|---|---|---|---|---|
| 2026-10-10 | **已证伪**（时间止损 384 根：4 只中 3 只含成本单笔均值下降，BTC 2.006%→1.333%） | **已验证（弱）**（剔除头肩底 sig_hs：4/4 单笔均值不下降，+0.026~+0.170pp，幅度低于噪声尺度 → 只判「无正向边际」） | **已证伪**（minimal_roi 时长分段止盈：0/4，胜率 19%→51% 但单笔均值 2.006%→0.2275%、总收益由正转负 → 「胜率骗人」教科书案例） | `策略假设/回测结果/回测结果_20261010.json` |

| 日期 | H-009 | H-010 | H-011 | 结果文件 |
|---|---|---|---|---|
| 2026-10-11 | **已验证**（成交口径现实化：4/4 含成本总收益下降，BTC 219.3%→116.3% / −103.0pp，单笔 2.006%→1.655% → 量化了「回测乐观偏差」） | **已证伪**（跳空穿越止损占比 **0.00%（0/840）**：15m 加密单根跳空 >5% 概率极低 → 「止损按 bar 边界价成交」的乐观化可忽略） | **已验证**（消融归因：3/4 满足「结构 ≤100pp 且成本 ≥3×结构」，BTC ×344 / BNB ×3.7 → **乐观偏差主因是执行成本假设，不是成交时点**） | `策略假设/回测结果/回测结果_20261011.json` |

| 日期 | H-012 | H-013 | 结果文件 |
|---|---|---|---|
| 2026-10-12 | **已证伪**（入场加「当根量 ≥ 48 根均量」流动性门槛：2/4 不下降，BTC +0.054 / ETH −0.107 / BNB +0.315 / DOGE −0.066 pp → 「突破必须带量」是直觉不是统计，门槛只减样本不提纯） | **已证伪（★过拟合检验失败）**（入场限定 `signal_score==2`：1/4，BTC −0.312 / ETH −0.485 / BNB +0.046 / DOGE −0.329 pp → 上一轮「score=2 层最优」是同批样本内的归因观察，**做独立 A/B 回测即崩** → 今后归因结论必须附「已过独立回测」标记） | `策略假设/回测结果/回测结果_20261012.json` |

| 日期 | H-014 | H-015 | 结果文件 |
|---|---|---|---|
| 2026-10-13 | **已证伪**（入场加「rv_ma ≤ 自身 2000 根滚动中位数」波动率门槛：1/4 不下降，BTC 2.0061→1.074(−0.9321) / ETH +0.7443 / BNB −0.1538 / **DOGE 0.6738→−0.6217**） | **已证伪**（平仓后强制冷却 96 根：1/4，BTC −0.6540 / ETH −0.4184 / BNB +0.2698 / DOGE −0.4947） | `策略假设/回测结果/回测结果_20261013.json` |

> ★ **H-014 副产物（重要）**：DOGE 在低波动门槛下**从 +0.67% 恶化到 −0.62%** →
> 「DOGE 系统性亏损 = 波动率问题」这条归因路径**被独立回测排除**。

| 日期 | H-016 | H-017 | 结果文件 |
|---|---|---|---|
| 2026-10-14 | **已证伪（强证据）**（入场放量门槛改为「`vol_ratio` ≥ 其 2000 根滚动 90 分位」：**1/4** 不下降，BTC 2.0061→1.7914(−0.2147) / ETH 2.373→2.0759(−0.2971) / BNB 2.3238→2.5804(+0.2566) / DOGE 0.6738→0.6011(−0.0727)。★ **咬合力：砍掉 74~78% 入场**（真咬合）→ 否掉的是**阈值形式**（自适应分位），不只是某个倍数） | **已证伪（弱证据）**（只在 MA30 趋势转正后 ≤96 根内入场：2/4 不下降，BTC +0.0000 / ETH +0.0000 / BNB −0.1620 / DOGE −0.0131。★ **咬合力仅砍 1.1~1.6%** → BTC/ETH 的 Δ=0 是「门槛没咬到」**不构成无效证据**，提供信息的只有 BNB/DOGE） | `策略假设/回测结果/回测结果_20261014.json` |

> ★★ **H-016 / H-017 的方法论级产出（本轮最重要）**：
> 这是**第 5 / 第 6 条「让策略更保守」型假设**，连同 H-012/H-013/H-014/H-015 **6/6 全数证伪** →
> 累计证据已足够下判断：**「加门槛」这一整类思路在黑马策略上系统性无效**，
> 下一步应转向**出场端**或**成本端**（H-009/H-011 已指认成本才是最大偏差项）。
> ★ **新增纪律**：今后任何「加门槛」结论**必须附门槛咬合力（砍掉多少 %）** ——
> 否则无法区分「门槛无效」与「门槛没咬到」（本轮 H-017 差点把「没咬到」误报成「无效」）。

| 日期 | H-018 | H-019 | 结果文件 |
|---|---|---|---|
| 2026-10-19 | **已验证（4/4）**（**出场端**：三段止盈追踪回撤 10%/8%/5% → 15%/12%/8%；净额单笔均值 BTC 1.8021→**2.2416**(+0.4395) / ETH 2.1683→**3.3502**(+1.1819) / BNB 2.1193→**3.3327**(+1.2134) / DOGE 0.4726→**1.6195**(+1.1469)；总收益 BTC 219→298 / ETH 863→1686 / BNB 707→934 / DOGE −79.8→−61.7） | **已验证（4/4，弱咬合）**（**成本端**：maker 0.02%/边 + 70% 确定性成交率 vs taker 0.1%/边；BTC +0.1698 / ETH +0.3844 / BNB +0.0878 / DOGE +0.1386 pp/笔。★ **咬合力：笔数仅 −3.3%~+0.5%** → 折损几乎不咬合，**增益几乎全部来自费率降低**，不是「省费率 vs 丢机会」的取舍） | `策略假设/回测结果/回测结果_20261019.json` |

> ★★ **本轮方向性结论（7 连败后第一条成立的方向）**：入场端「加门槛」**6/6 全证伪**，
> 而**出场端放宽追踪回撤 4/4 全改善** → 黑马策略的问题**不在「买得太宽松」，而在「卖得太早」**。
> ★ 但 DOGE 在两条假设下都改善仍亏 **−61.7%** → 出场/成本能**减亏**，改不了「该不该做这只标的」。
> ★ **口径修正**：历次「含成本单笔均值」用 `pnl_pct`（**不含手续费**），实测乐观 **0.2041pp/笔**；
> 本轮起新增 `net_pnl_pct` 净额口径，H-018/H-019 一律用净额判定。

| 日期 | H-020 | H-021 | 结果文件 |
|---|---|---|---|
| 2026-10-21 | nautilus_trader（#6 二刷，改读**挂账痛点同形**且从未读过的对账子层）· （副源：B站**永久降级**，改用仓库自带 `proptests.rs` 当反例源） | reconciliation/orders.rs（1613 行：`generate_reconciliation_order_events` / `prepare_reconciliation_order` / `has_material_fill_decrease` / `is_superseded_cancel_report` / `is_unchanged_accepted_report_during_pending_command`）+ order_manager/manager.rs（5049）+ OrderStatus 15 态 | [[20261021_nautilus_trader_vnpy]] | ✅ 笔记 + 代码(order_reconciliation_patterns.py **17/17** · manifest_min.py **7/7** · 均 lab_bridge 零警告) + 假设(**H-022 已验证 4/4 · 首次真咬到 79~87% 放行率**、**H-023 已验证 4/4 · 样本外**) + **P0 回填**(`core/order_lifecycle.py` **8/8**、`live.py` **4/4→8/8**、`manifest_min` W7 结清) |
| 2026-10-20 | **已证伪（0/4，强证据）**（**出场端极端档**：关掉三段止盈、只跌破 MA30 或 −5% 止损才走 `exit_mode="let_run"`；净额单笔均值 BTC 1.8021→**−0.2735**(−2.0756) / ETH 2.1683→**−0.2359**(−2.4042) / BNB 2.1193→**−0.2136**(−2.3329) / DOGE 0.4726→**−0.2317**(−0.7043)。★ **推论：「越松越好」不成立** —— H-018 的 15/12/8 有效只说明存在**内部最优档**，不是单调方向；MA30 是滞后均线，等它跌破时利润已被吃掉 2pp+） | **已验证（4/4）但★咬合力≈0，不可当取舍证据**（**成本端真取舍版**：maker 0.02%/边 + 成交率由数据决定 `low[t+1] ≤ close[t]`；BTC 1.8021→1.9587(+0.1566) / ETH +0.1637 / BNB +0.1548 / DOGE +0.1731 pp/笔。★ **实际成交率 BTC/ETH/BNB = 100.00%、DOGE = 99.79%** → 挂单价取「当根收盘」在 15m 上几乎必然被次根触及 → **测到的只是降费率，不是限价单取舍**；修法见 P1） | `策略假设/回测结果/回测结果_20261020.json` |

> ★★ **H-020 的方法论价值**：它是第一条**证伪「H-018 方向可持续外推」**的假设 ——
> 「出场端有效」不等于「越松越有效」。今后任何「放宽某参数有效」的结论，
> 都必须回答「**放宽到极限会怎样**」，否则只是单调性幻觉。
> ★ **H-021 的教训**：`已验证` 三个字必须配咬合力读数。成交率 100% 的实验组
> 与「只改费率」在数学上等价 —— **没有取舍，就没有取舍结论**。

---

## 五、学习源白名单（轮转）

| 序 | 仓库 | 主攻 |
|---|---|---|
| 1 | `vnpy/vnpy` | 事件引擎 / 网关 / 数据 / 回测 / 工具 |
| 2 | `vnpy/vnpy_ctastrategy` + `vnpy_ctabacktester` | CTA 策略模板 + 回测引擎 |
| 3 | `vnpy/vnpy_portfoliostrategy`（**组合回测引擎就在本仓库 `backtesting.py`**；`vnpy_portfoliobacktester` 实测 GitHub **404**，2026-10-19 勘误） | 多合约组合策略 + 组合回测 |
| 4 | `vnpy/vnpy_binance` | 币安网关（REST/WS/合约） |
| 5 | `nautilus_trader` | 机构级事件驱动（数据/执行/风控引擎） |
| 6 | `freqtrade` | 策略接口 / freqAI / 超参优化 |
| 7 | `hftbacktest` | 高频回测（订单簿 / 延迟建模 / 做市） |
| 8 | `hummingbot` | 做市 / 套利框架 |
| 9 | `backtrader` | 经典回测（指标 / Cerebro） |
| 10 | `microsoft/qlib` | AI 量化（因子库 / 模型训练 / 滚动回测） |

副源：B 站量化课程（**优先有字幕/CC**，抓字幕蒸馏；无字幕只做目录级笔记，不做音频转录 —— 零成本）。

---

*本库由「AI量化平台·开源精读夜学」定时任务自动维护。手动补充请遵循同一命名与结构。*

### 2026-10-22 轮（撮合现实化 · freqtrade）

| 日期 | H-023（补档 6 档） | H-024（跳空止损） | 结果文件 |
|---|---|---|---|
| 2026-10-22 | **已验证（3/4）但★最优再次落端点**（训练段前 70% 扫 6 档：`8/6/4`/`10/8/5`/`15/12/8`/`20/15/10`/`25/20/12`/`30/25/15`，**4 只全选 `30/25/15`**；样本外后 30% 净额单笔均值 BTC 0.6028→**1.7425** / ETH 0.8263→**2.5727** / BNB 1.1740→**1.2539** / DOGE −0.9418→**−1.2141（恶化）**） | **已证伪（0/835）**（止损按「开盘穿越则按 open」成交；4 只标的 6 年全历史 **835 笔止损 / 0 笔跳空穿损**，Δ 全 **+0.0000pp** → 15m + 5% 止损下跳空风险不存在，旧口径**未被证明高估**；判「已证伪」不判「搁置」——事件发生率是**市场属性**，0 次本身就是观测结果） | `策略假设/回测结果/回测结果_20261022.json` |
| 2026-10-23 | **已验证（3/4）★端点第三次外移**（训练段前 70% 扫 **7 档**，4 只全选 `40/32/20`；样本外净额单笔均值 BTC 0.6028→**3.2842**(+2.6814) / ETH 0.8263→**2.5311**(+1.7048) / BNB 1.1740→**1.5521**(+0.3781) / DOGE −0.9418→**−1.9930**(−1.0512 恶化)；训练段单调上升 1.12→1.70→2.57→4.02→6.10→7.82→**15.72** → 网格内**没测到内部最优**，只能说"最优点在 `40/32/20` 与 `let_run` 之间") | **H-025 已验证（容量不咬）**（逐标的 P99 参与率下 Δ 全 **+0.0000pp**、部分成交 2 笔、未成交 0；**对照组 1e-7 下 100% 被截断** 140/140·211/211·202/202·472/472 → H-021「咬合力≈0」是假观测） ／ **H-026 已证伪（排队不紧）**（V/Q 中位 BTC **12155×**/ETH **1938×**/BNB **195×**/DOGE **738×**；k=1 与 k=10 上界成交率均 **100%**，DOGE k=10 才 97.46% → 15m + $10k 下排队不是约束，H-022 未被否定） | `策略假设/回测结果/回测结果_20261023.json` |

> ★★ **H-023 补档后的硬结论**：端点从 `20/15/10` 外移到 `30/25/15` 且**仍是端点** →
> 「存在内部最优」成立，但 **最优点仍未定位**，且 **DOGE 反向恶化**说明单调性在低波动标的上断裂。
> ⇒ 下一轮须插 `40/32/20` 逼近 `let_run`（已知 0/4 全负）才算定位。
> ★★ **H-024 的价值是「结清挂账」而非「发现优势」**：台账里 H-010 早写过「15m 加密要单根跳空 >5% 概率低」，
> 本轮用 835 笔止损把它钉成事实 → **乐观偏差的主因是执行成本假设，不是止损成交价**，
> 有限时间应继续投在手续费/滑点/maker 成交率上。缺口清单里「撮合无部分成交」由 `participation` 开关补上。
> ★ **口径纪律（本轮新增）**：**模型参数类**假设（放行率/成交率类）咬合力为 0 ⇒ 判**搁置**（未观测）；
> **市场属性类**假设（事件发生率类）数出 0 次 ⇒ 判**已证伪**。两者混用会把真结论误挂成"未观测"。

### 2026-10-23 轮（撮合队列层 + 持仓对账 · hftbacktest / nautilus_trader）

| 日期 | 主仓库 | 核心文件 | 笔记 | 三件套 |
|---|---|---|---|---|
| 2026-10-23 | hftbacktest（#5 二刷 · 队列层）· nautilus_trader（三刷 · 持仓对账） | `models/queue.rs`（1366）／`proc/nopartialfillexchange.rs`（649）／`reconciliation/positions.rs`（1038） | [[20261023_hftbacktest_vnpy]] | ✅ 笔记 + 3 模块（20/20 · 25/25 · 11/11）+ 3 条假设 + 2 项 P0 结清 |

> ★★ **本轮最重要的结论是「两条都不咬」**：H-025（容量）已验证不咬、H-026（排队）已证伪不紧。
> V/Q 中位 BTC **12155 倍** —— 我们的委托量比 15m 成交量小 4 个量级。
> ⇒ **继续在"成交现实度"上加码的边际收益已接近 0**，剩下的唯一乐观源是**滑点系数**（挂账第 5 轮）→ 上调为 **P0**。
> ★★ **H-025 顺带坐实了一个方法论**：`participation=1e-7` 这个演示值下 **4 只标的 100% 的委托全被截断**
> （140/140·211/211·202/202·472/472）—— 所谓"容量约束"**从没生效过**。
> ⇒ 任何「约束类开关」的验收必须两项齐全：**① 咬合力计数落在 (0,100%) 之间；② 对真实标定值重跑**。
> 100% 和 0% 都是**未观测**，不是结论。
> ★★ **H-023 端点第三次外移（20/15/10 → 30/25/15 → 40/32/20）**：训练段净额随档位单调上升，
> 说明网格内**根本没测到内部最优**；而 `let_run` 已知 0/4 全负 ⇒ 最优点夹在两者之间。
> **不能再靠外推**，下一步必须**分标的给结论**（DOGE 样本外 −1.0512 说明低波动标的上单调性断裂）。
> ★ **本轮修了 1 个数据丢失级 bug**：`update_ledger` 无条件写证据列 → **证据为空就把已有证据清空**
> （H-024 的 `回测结果_20261022.json` 曾被静默抹掉，进度打印只显示"状态未变"）。
> 已改为「空证据只允许不写」，并把"保留原证据"记进 warnings；H-024 证据已复原。

### 2026-10-24 轮（成交价格模型 · hummingbot / backtrader）

| 日期 | 主仓库 | 核心文件 | 笔记 | 三件套 |
|---|---|---|---|---|
| 2026-10-24 | hummingbot（#9 二刷，改读**撮合仿真层**：纸面交易所的真成交路径）· backtrader（#11 二刷，改读**撮合价格层** `brokers/bbroker.py`） | `connector/exchange/paper_trade/paper_trade_exchange.pyx`（1139 行：`c_execute_buy` 445 / `simulate_buy` 逐档吃量 454-460 / `TRADE_EXECUTION_DELAY` 144 / `c_quantize_order_amount` 1078-1086 / `c_match_trade_to_limit_orders` 895-939 / `c_process_crossed_limit_orders` 836-892）+ `core/data_type/order_book.pyx`（483 行 · `simulate_buy/sell` 283-309）+ `connector/budget_checker.py`（161）+ `brokers/bbroker.py`（`_slip_up/_slip_down` 994-1036） | [[20261024_hummingbot_vnpy]] | ✅ 笔记 + 代码(`fill_price_model.py` **26/26** + 标定表 + `core/backtest.py` 新增 `slip_price`/`quantize_qty` 与 `clamp_slip`/`lot_size` 两开关 `selftest_slip_lot_wiring` **13/13**，lab_bridge 加载成功) + 假设(**H-027 已证伪**：入场越界占比 4/4 **低于**全样本，BTC −13.91pp；**H-028 已验证**：夹断不劣化 4/4，Δ +0.0014~+0.0038pp，咬合力占比 12.5%~29.6%，但 `qty_zeroed=0` ⇒ 粒度半边**未观测**) + 回归全绿（fill_realism **10/10** · participation **6/6** · risk_wiring **10/10**） |

> ★★★ **本轮把「最后一个没被动过的乐观源」量掉了，并对整条线做了收口。**
> 滑点夹断（D58）的真实影响只有 **+0.0014~+0.0038pp/笔**；对照手续费 **0.2041pp/笔**（第 9 轮），
> 成交价模型的乐观量是手续费的 **1/50**。加上前几轮已结清的容量（H-025 ≈0）、
> 排队（H-026 不紧）、止损成交价（H-024 零穿损）——
> ⇒ **「让回测更真实」这条路的边际收益已经耗尽，资源必须转到「让真实成本更低」**（maker/BNB 抵扣/VIP 阶梯）。
> ★★ **H-027 是被 4/4 打死的先验**：我原以为突破型入场 close 贴近最高价 ⇒ 入场端滑点越界更严重，
> 实测**全面相反**（BTC 8.53% vs 全样本 22.43%，低 **13.91pp**）。黑马策略的入场 bar
> 落在相对温和的中段 ⇒ **旧口径在入场端并没有系统性高估成本**。先验错了就写真错，不粉饰。
> ★★ **H-028 必须拆成两半读**：夹断半边 `slip_clamped` 22/40/60/59 次、占成交 **12.5%~29.6%**（咬合力充足，观测成立）；
> 粒度半边 `lot_applied` 129/211/203/472（开关确实执行）但 `qty_zeroed` **4 只全为 0**
> ⇒ 按第 13 轮纪律，**「lot 粒度不咬」不成立，正确表述是「没被测到」**（$10k 仓位量级远高于 0.001 的 lot）。
> ★ **学 hummingbot 也指出它错在哪**：`paper_trade_exchange.pyx:460` 的 VWAP 分母用**请求量**，
> 深度不足时 `order_book.pyx:286-294` 用最后一档价硬吃剩余量 ⇒ VWAP 永远"算得出"、**深度不足被算法吃掉**。
> 我们的 `vwap_from_levels()` 改用 `Σ entry.amount` 做分母并返回 `depth_short` —— 宁可报"没吃到"，不报假均价。
> ★ **AtomCode 连续第 4 轮不通**（`/health` 200 + `logged_in=true` + 3 个免费模型，但最小推理 240s 超时 HTTP=0）
> ⇒ 全程本地 Read/Grep，**0 积分**。收敛纪律：第 3 轮起不再在这上面耗时间。
> ★ **归档**：周六（周中）→ 仅 Obsidian + 工作区日志；**六端归档 2026-10-25（周日）**。

### 2026-10-26 轮（交易成本档位 · qlib Exchange 二刷）

| 日期 | 主仓库 | 核心文件 | 笔记 | 三件套 |
|---|---|---|---|---|
| 2026-10-26 | microsoft/qlib（#11 **二刷**，一刷读 workflow 层，本轮改读**成本层**） | `qlib/backtest/exchange.py`（958 行：`Exchange` 四角色 · `deal_order` 421 · `_calc_trade_info_by_order` 859 · `schedule_cost↔948` 两段式费率 · `critical_price↔850` 闭式解 · `impact_cost↔892` 平方冲击 · `get_real_deal_amount 597-609` 清仓豁免 lot）+ `account.py`（417 · `return_rate↔283` **毛净错名**） | [[20261026_microsoft_qlib]] | ✅ 笔记 + 代码(`fee_schedule_model.py` **30/30**，lab_bridge 零警告) + 假设(**H-029 已验证**：r\* >1%(>10× taker) 3 只、DOGE 0.3354%(3.35×)；**H-030 已验证**：粒度机制被 `$1` 档 42827 次归零**证明有效**，但 ≥$100 本金下不咬) |

> ★★★ **本轮是对第 14 轮结论的「收窄」，不是推翻。** 第 14 轮说「撮合模型边际收益耗尽 → 换赛道到真实成本」。
> 今天把「真实成本」这条赛道的**天花板量出来了**：BTC/ETH/BNB 的**盈亏平衡费率 r\* > 1%**（= taker 的 10 倍以上），
> DOGE r\* = **0.3354%（3.35×）**。⇒ 对 3 只主流标的，**降费（maker/BNB抵扣/VIP阶梯）的边际收益 ≈ 0**；
> 只有 DOGE 这类低波动标的（费率吃掉 **29.86%** 毛额 vs BTC 8.68%）才是成本敏感型 ⇒ **降费要按标的分**，不能一刀切。
> ★★ **`费率吃掉 pp` 四只落在 0.2012~0.2047，与第 9 轮记的 0.2041pp/笔 完全吻合** ——
> 相隔 7 轮、两次独立实现，数字对得上 ⇒ 旧口径可信（这是一次**口径自洽性验证**，不是新结论）。
> ★★ **H-030 结掉第 14 轮挂账的「粒度未观测」**：首跑用 $100~$10k 十六格全 0 只能判「搁置」——
> **那是测试设计错，不是结论**。改成 `$1/$5/$10/$50/...` 后 `$1` 档 **42827 次归零、129 笔全灭**，
> 机制立刻现形，并给出**精确阈值**：BTC ∈ ($10,$50]、BNB ∈ ($1,$5]、ETH/DOGE 在 $1 已不咬（历史价格低）。
> ⇒ 新纪律 **D66**：约束类开关验收要三段齐全 —— ① 极值档能咬 ② 中间档咬合力∈(0,100%) ③ 真实档不咬。
> **只有 ③ 没有 ①，那个 ③ 是假的。**
> ★★★ **D65「单笔均值是幸存者偏差的放大器」**（今天回测打出来的，不是抄的）：
> BTC `$10` 本金下粒度砍掉 87/129 笔，**单笔均值从 2.1521% 涨到 6.5311%（+4.379pp）**，
> 而总收益从 +438.9% 掉到近零。**只看单笔均值会得出「加粒度限制提升 4.4pp」的荒谬结论。**
> ⇒ 今后任何「单笔均值改善」必须同时报 **笔数** 与 **总收益**，三者缺一结论作废。
> ★★ **D63 qlib 自己踩了我们的老坑**：`account.py:283` `return_rate=(earning+cost)/value`，
> 注释却写「earning consider cost, true return」—— **字段名叫 return_rate，实为毛收益**。
> 与我们第 9 轮 `pnl_pct` 名不副实是同一个坑（微软出品、引上万次也照踩）。
> 本平台 `core/report.py:78-86` 已是「毛账/净账强制并列 + fee_drag_pp + cost_dominated」⇒ **这项我们反超 qlib**。
> ★★★ **最大未解疑点（P0）**：回测说 BTC 净额单笔 **+2.1521%**、4/4 费前为正、能扛 10 倍费率；
> 实盘 4543 笔却是 **净 −15.90 USDT**。**两者不可能同时为真。** 候选解释（标的池/时段/记账口径/未来函数）未验证
> ⇒ 查清前 r\* 只能读作「回测口径下」，**不可外推为「实盘能扛 10 倍费率」**。
> ★ **新口径疑点**：数据是 `*_永续_15min_全历史.csv`（永续），但 `fee_rate=0.001` 是**现货 taker**；
> 永续 USDT-M taker 是 0.05% ⇒ 当前基线**可能高估单边成本约 1 倍**，真实「费率吃掉」应 ≈0.102pp。本轮未修正（改基线会让历史假设不可比），记 P0。
> ★ **AtomCode 连续第 5 轮不通**（`/health` 200 + `logged_in=true`，但最小推理 240s 超时 HTTP=0）
> ⇒ 全程本地 Read/Grep，**0 积分**。
> ★ **归档缺口**：10-25（周日）夜学轮未运行，六端归档未做 ⇒ 需在**下一个周日补做，含 10-18/10-25 两轮顺延**。
> ★ 今日周一（周中）→ 仅 Obsidian + 工作区日志。

### 2026-10-27 轮（数据模型 / 记账口径 · vnpy MainEngine + OMS + BarGenerator）

| 日期 | 主仓库 | 核心文件 | 笔记 | 三件套 |
|---|---|---|---|---|
| 2026-10-27 | vnpy/vnpy（#0 轮转首位；第 3 轮曾作副源只读事件引擎，本轮改读**OMS 容器 + 数据模型 + 聚合器**） | `vnpy/trader/engine.py`（887 行：MainEngine 服务定位器 · `init_engines 149` 把 OMS 19 个方法绑成属性 · `close 321` 先停总线 · OmsEngine `process_order_event 420` 在途三态）+ `object.py`（427 行：`ACTIVE_STATUSES:14` · `OrderData.traded:127` · `PositionData/AccountData` **全无手续费字段** · `available` 只在 `__post_init__ 212` 算一次）+ `utility.py`（1304 行：`BarGenerator.update_bar_minute_window 281` 按 `(minute+1)%window` 判闭合 · `ArrayManager 504` 零填充预热） | [[20261027_vnpy_vnpy]] | ✅ 笔记 + 代码（`vnpy_oms_accounting.py` **37/37**，lab_bridge 零警告）+ 假设（**H-031 已验证 4/4** · **H-032 已验证 1/4** · **H-033 已验证 4/4**）+ 平台侧（`report.py` 补 `n_trades` 与 `total_return_basis` 口径自证；`risk.demo_selftest` **24/24** 零退化） |
| 2026-10-28 | vnpy/vnpy_ctastrategy（轮转 #1；首次精读，**专攻出场端**） | `cta_strategy/template.py`（507 行：CtaTemplate 回调族 · `variables.copy()` 防多实例串写 · `TargetPosTemplate.send_new_order 455` **回测用开仓/实盘先平后开**）+ `backtesting.py`（1294 行：`new_bar 666` **先撮合后回调** · `cross_stop_order 762-850` bar 内穿越 + 跳空按 open · `DailyResult.calculate_pnl 1110` **`pre_close=1` 量纲错误** · `calculate_statistics 409-448` 三套收益口径 + 240/252 两因子 · `x[x<=0]=nan→fillna(0)` **爆仓日抹平** · `run_backtesting 243` **吞异常静默 return**）+ `engine.py`（986：`STOP_STATUS_MAP 61` **REJECTED 并进 CANCELLED** · `check_stop_order 223-252` 触发后按 **ask5/bid5 追价**） | [[20261028_vnpy_vnpy_ctastrategy]] | ✅ 笔记 + 代码（`vnpy_cta_exit_patterns.py` **44/44**，lab_bridge 零警告）+ 假设（**H-035 已验证 4/4**：出场触发口径高估 **0.0439~0.8277pp/笔** · **H-036 已证伪**：bar/日夏普比值仅 **0.771~1.031**，自我纠错）**+ H-023 分标的结论结清**（BTC/ETH 可放宽 40/32/20 · BNB 维持基线 · DOGE 不许放宽）+ 平台侧（`core/backtest.py` 新开关 `exit_trigger`，默认 `close` 零退化；回归全绿 risk 24/24 · router 8/8 · lifecycle 10/10 · fill_realism 10/10 · slip_lot 13/13 · participation 6/6 · risk_wiring 10/10） |
| 2026-10-29 | vnpy/vnpy_ctabacktester（轮转 #2；首次精读，**专攻参数优化层**） · 交叉读 `vnpy/vnpy` `vnpy/trader/optimize.py`（276）与 `vnpy_ctastrategy/backtesting.py:1184-1235` | `vnpy_ctabacktester/engine.py`（498 行：`start_backtesting 216` 用 **`self.thread` 非空**做互斥 · `run_backtesting 146` 两条失败路径都只 `return`（结果停 None） · **`run_optimization 274` 无 try/except** → 异常后 `thread` 永久非空、只能重启） + `ui/widget.py`（1580：`DISPLAY_NAME_MAP 958` **5 个优化目标互斥** · `generate_setting 1076` 丢掉校验返回值 · `OptimizationResultMonitor 1100` **只渲染 2 列**、丢弃 statistics 40+ 项 · `save_csv 1165` 手动导表、无 run_id） + `tests/test_engine.py`（569 / 11 用例：`284` 把「空数据→两个 None」写成断言 · `344` 把忙碌拒绝写成契约） + `vnpy/trader/optimize.py`（276：`add_parameter 44-73` ★**浮点累积丢端点** · `run_bf_optimization 116-147` ★裸单目标 `sort(reverse=True)` · `selNSGA2 201` 但 `weights=(1.0,)` → 伪多目标） | [[20261029_vnpy_vnpy_ctabacktester]] | ✅ 笔记 + 代码（`opt_grid_guard.py` **40/40**，含 3 处 A/B 反测，lab_bridge 零警告）+ 假设（**H-037 已证伪**：宽档增益在 intrabar 下留存 BTC 56.42% / ETH 92.86% / BNB 85.39% / DOGE 83.73%，缩水≥30% 仅 1/4 ⇒ 放宽收益**不是**收盘口径喂出来的 · **H-038 已验证**：DOGE A(pos) **+0.2457%** 而 G **−0.3943%**，实测拖累 0.64pp/笔、理论 −0.5274%（差 0.133pp）⇒ **波动拖累**解释「单笔正/总收益负」；★剔除最长持仓 top-1% 后**更差**（−86.61%→−94.40%））+ 平台侧（`write_results` 改**追加式 + run_id**，P1-4 结清：同一天连跑两次 runs=2、旧 payload 仍在；新增 D82~D90 九条设计点） |
| 2026-10-30 | vnpy/vnpy_portfoliostrategy（轮转 #3；**首次专攻组合面板层**，第 9 轮只读过回测引擎） | `portfolio_strategy/engine.py`（639 行：`load_bars 259-304` ★**时间轴并集 + 前值填充**，合成 bar `open=high=low=close=前收` 且 **volume 默认 0**；`bars` 字典**永不重置**；`load_bar 306` 用 `datetime.now(DB_TZ)` ⇒ 实盘路径不是回测） + `backtesting.py`（1026：`new_bars 588-623` **同语义填充**；`cross_limit_order 625-687` ★**`order.traded=order.volume` 全量成交、不看 volume**；`ContractDailyResult.calculate_pnl 818` `pre_close` 缺省 **0**；`PortfolioDailyResult.calculate_pnl 896-928` ★**同一函数两套缺省风格**（`pre_closes.get(vt,0)` vs `sizes[vt]` 直接下标）） + `template.py`（316：`rebalance_portfolio 200-262` ★**无条件 cancel_all 再重发** ⇒ 挂单存活根数→0；`calculate_price 264` 默认用**当根收盘价**挂限价） + `utility.py`（325：`update_tick 45-89` ★★**全局单一 last_dt 判跨分钟**，多标的 tick 交替会互相触发推 bar；`update_bar_minute_window 100-142` ★★`(minute+1)%window` **同一个坑第二次出现**且用循环泄漏变量判全体边界） | [[20261030_vnpy_vnpy_portfoliostrategy]] | ✅ 笔记 + 代码（`portfolio_alignment_guard.py` **40/40**，含 4 处变更反测，lab_bridge 零警告）+ 假设（**H-039 已验证**：网格合规 **100.0%** / 非整倍数间隔 **0.0%** / 上市内真断档 **37 条=0.0038%** ⇒ **「时间轴错位」可从 35 倍笔数差的候选里划掉**；但尾停冻结 **9232 槽位**（ETH/DOGE 各 4616 根 = **48.1 天**，占危险槽位 **99.6%**）⇒ 嫌疑收窄到**样本期不一致** · **H-040 已验证**：冻结期限价单成交率 **100%**（加价 5% 后仍 100%）、成交价恒等于冻结价 ⇒ **零流动性全量成交**，撮合护栏在组合面板上必须靠 `is_filled` 硬闸）+ 平台侧（**P0-1 结清**：`grid_audit` 接进 `verify_H023` 判定链，4/4 标的判「**端点最优·单调·可外推=N**」⇒ 训练段 7 档**严格单调**（BTC 1.2358→17.9424），「存在内部最优」应改写为「**方向性单调、无可定位的内部最优**」）+ 回归 **ALL GREEN**（risk 24/24 · events 3/3 · lifecycle 10/10 · fill_realism 10/10 · slip_lot 13/13 · participation 6/6 · risk_wiring 10/10 · lab_bridge 40/40） |
| 2026-10-31 | vnpy/vnpy_riskmanager（轮转 #4 的替代：原 `vnpy_portfoliobacktester` **main/master 双 404**，同镜像下 `portfoliostrategy` 200 ⇒ 排除镜像故障，仓库确实不存在；已修轮转表，白名单第 2 次勘误） · 副 `vnpy/vnpy_paperaccount` | `vnpy_riskmanager/engine.py`（268：`patch_functions 137` ★★二次 init 把已 patch 的 bound method 存成「原始函数」→ **无限递归**；`send_order 199` ★★拦截后 **`return ""`**，拒因不可区分；`check_allowed 207` 遍历 dict 插入序，规则顺序来自 `glob` 文件序 ⇒ 换台机器换执行序；`needs_callback 166` ✅ **按「是否重写」决定订阅**） + `template.py`（105：`update_setting 46` 只 setattr，**无范围校验、无重算钩子**） + `rules/*.py`（298：`duplicate_order_rule 30-41` ★★★**检查函数里自增计数**→ 被别的闸拒的漏计、被自己拒的照计，且 10 笔**全历史累计永不衰减** ⇒ 网格/追踪止损被**永久锁死**；`order_size_rule 29` ★★`if contract and req.price` 用**字段真值当类型判据** ⇒ 市价单绕过整条市值闸；`order_validity_rule 28` ★容差**固定 1e-6**，pricetick=1e-8 时 = 100 倍 tick；`daily_limit_rule 90` ★首见即终态 ⇒ 撤单漏记） + `tests/test_rules.py`（99 / 4 用例） | `vnpy_paperaccount/engine.py`（673：`cross_order 387-435` ★★`if trade_price:` **用「成交价非零」当「成交」判据**（`ask_price_1=0` 时市价单静默不成交或 0 附近成交）、**恒 `traded=volume` 不看 `ask_volume_1`**；`check_order_valid 349` 三种拒因共用一条「不支持的委托类型」日志；`update_position 484-560` ✅净持仓**五情形**显式列举；`process_tick_event 129` ★直接改 `tick.gateway_name` **污染上游对象**（与第 14 轮 hummingbot 盘口污染同形）；`save_data 587` ★★**漏存 `frozen`** ⇒ 重启后可平量虚高） + `tests/test_matching.py`（188） | [[20261031_vnpy_vnpy_riskmanager]] | ✅ 笔记 + 代码（`paper_risk_gateway.py` **50/50**，含 6 处变更反测，lab_bridge 零警告）+ 假设（**H-041 已证伪**：入场挂单折价 d=0.3% 档 **3/4 标的劣于全样本基线**（BTC −0.6739 / ETH −0.8226 / BNB −0.5177 / DOGE +0.1070pp），3/4 标的单调「折价越深→净单笔越差」（BTC 2.2895→1.4782→0.2972）⇒ **逆向选择**：能成交的恰是要跌的、好单全跑掉，「入场端加门槛」第 8 条证伪 · **H-042 已验证**：出场挂 `close×(1+e)` 限价，**12/12 格 Δ 全正**（+0.2009~+0.4791pp，中位 **+0.4039pp** > 手续费 0.10pp），成交率 73.3~97.6%，但**未成交样本 12/12 格差于基线**（最差 −1.7962pp）⇒ 仅**执行改进**不是新 alpha；★时序坑：首版把卖单挂在触发 bar 开盘（用 `close[j-1]`）＝提前知道 j 是止损 bar，造出 +1.19pp 假改善，改从 j+1 起后落到 +0.32pp）+ 平台侧（**白名单死条目已修**：`REPO_ROTATION` 第 5 位 → `vnpy/vnpy_riskmanager`；新增 D91~D100 十条设计点，其中 D92「按需订阅」建议抄进 `core/events.py`） |
| 2026-11-01 | vnpy/vnpy_binance（轮转 #5/12；⚠️ TASK_CARD 的 `core_file` 仍写 `binance_gateway.py` —— **仓库无此文件**，实读 `linear_gateway.py` 1770 行；这是白名单第 3 次文件名失真，下轮 P0 直接改 `REPO_ROTATION`） | `vnpy_binance/linear_gateway.py`（1770：`STATUS_BINANCE2VT 46` 六态映射含 `EXPIRED→CANCELLED` 合并语义；`ORDERTYPE_VT2BINANCE 59` ✅**`(type, timeInForce)` 二元组**双向映射（设计好，但 `MARKET→("MARKET","GTC")` 契约错，D111）；`RestApi.sign 375` ★★**有 `time_offset` 双向校正** vs `TradeApi.sign 1525` ★★★**零校正** ⇒ 同一网关「REST 全通、WS 下单必报 -1021」（D101）；`on_query_time 587` ✅「先公共对时 → 再私有查询」顺序是硬约束；`keep_user_stream 570` ★★★`keep_alive_count < 600` 按 **timer 计数**判续期，`6s×600=3600s` **正好等于 listenKey 寿命 ⇒ 零余量**（D102）；`on_query_account 620` `frozen=wb-available` vs `on_account 1012` `frozen=wb-cw` ★★**同一字段两条通道两套定义**（D103）；`on_account 1016` ★★`if account.balance:` 真值过滤 ⇒ **余额归零事件永不推送**（D104）；`on_order 1082` `datetime=packet["E"]`（事件时间）vs `on_query_order 697` `d["time"]`（订单时间）★★**同名字段两套语义**（D105）；`on_query_order 694` / `on_order 1076` ★★`STATUS_BINANCE2VT[d["status"]]` **裸下标** ⇒ 交易所新增状态即 KeyError 打断**整批**推送（D106）；`on_send_order 1663` ★★★`if not error: return` ⇒ **成功响应里的 `result.orderId`（交易所真 ID）被丢弃**，只剩 clientOrderId 是链条（D107）；同函数 `error_code: str` 而币安返回 `int`（D108）；`resubscribe_market_channels 1226` ★遍历 `self.ticks.keys()` 反推订阅 —— 经查 `subscribe()` 里 `ticks[symbol]=tick` 建在 send **之前**，所以「订阅成功但无 tick」侥幸成立；**真缺陷只在「一次都没连上过就断线」时触发**（初判被自己证伪后改写，D109）；`get_public_channels 1199` `@depth10` 硬编码（D110）；`grep reduceOnly\|positionSide\|closePosition` **全网关零命中** ★★★ ⇒ 不能下「只平仓」单、不能 Hedge Mode；**而我方 `core/risk.py` 第 9 轮已加 `reduce_only`、`core/live.py:166` 已透传 ⇒ 风控语义层平台反超网关**（D112）） | [[20261101_vnpy_vnpy_binance]] | ✅ 笔记 + 代码（`gateway_consistency_guard.py` **72/72**，11 类一致性缺陷 / 12 站点，含 6 组变更反测，lab_bridge 零警告）+ 假设（**H-043 搁置**：入场折价 × 出场加价**联合挂单**首次实测，9 格 × 4 标的；中档 (0.3%/0.3%) Δpp **4/4 为正**（BTC +1.2243 / ETH +0.2480 / BNB +0.0256 / DOGE +0.9327），Δpp>0 格数 6/8/5/8，但**中档优于单边 H-042 中位 +0.4039pp 的仅 2/4** ⇒ 支持未达、证伪亦未达 ⇒ 方向不一致；★伴生证据：`0.5%/0.5%` 深档崩塌（BTC −1.7407 / BNB −1.5815pp，联合成交率仅 38~49%）、`in 0.3%/out 0.1%` 在 BNB 上 −0.4944pp ⇒ **入场折价是拖累**，从第二个独立角度再次印证 H-041 逆向选择）+ 平台侧（新增 D101~D112 十二条设计点；第 20 轮 P1「入场/出场联合挂单未测」**本轮已结清**） |

> ★★★ **本轮把第 15 轮挂账的「永续数据 + 现货费率」这块 P0 结清了 —— 结论是「腰斩」，不是「翻盘」。**
> `fee_rate 0.001 → 0.0005` 四只标的配对回测：Δ净单笔 **+0.1006~0.1023pp**（= 0.05%×2 边，4/4 命中），
> 成本拖累 **0.2012~0.2046pp → 0.1006~0.1023pp**，**笔数一只未变**（129/211/203/472）。
> ⇒ 第 15 轮 H-029 的 `r*` 与「费率吃掉 pp」**全部要读作减半**：r* 从「>1%（>10× taker）」→「>2%（>40× 永续 taker）」，
> DOGE 0.3354% → **0.67%**。**方向不变**（手续费仍是最大单项成本、仍不是瓶颈），只是量级修正。
> ★★★ **DOGE 才是本轮最有价值的反证**：费率腰斩后它**还是 −68.3%** ⇒ **亏损不是费率造成的**。
> 第 15 轮「降费要按标的分」因此**收紧**为「降费对 DOGE 无效」——力气别花在它身上。
> ★★★ **H-032 抓出比 D65 更狠的一条**：DOGE **净单笔 +0.5732%（正的）而总收益 −68.3%**（胜率 16.5%、回撤 99.2%）。
> D65 说「单笔均值是幸存者偏差的放大器」，今天证到**二者可以方向相反** ⇒
> **任何「单笔改善」都不构成可交易证据**，必须同屏报 笔数 + 总收益 + 最大回撤。
> ★★ **H-033 是一堂「不咬也要数出来」的课**：4H 半桶 **22 个 / 57,927 桶（0.027%~0.047%）**，ETH 有个桶**只有 1 根 15m 子 bar**；
> 剔除后「下一根收阳率」变化 **−0.0064~+0.0039pp** ⇒ 确实不咬。但**必须先数**：
> 过程中自己就踩了一次 —— 时区混用让 mask 全 False，**「0 个半桶」和「没测」长得一模一样**（第 13 轮 `qty_zeroed=0` 同形）。
> ★★ **D67 是本轮最想扩散的一条**：vnpy `BarGenerator` 按 `(minute+1)%window` 判闭合，**docstring 写了「必须整除 60」但代码一行不校验**。
> 实测 `15m + window=16`（想合成 4H）→ 稳态跨度 **60 分钟**（应为 240），触发点 `[15,31,47]`，**静默产出 1H bar，小 4 倍**。
> ⇒ 判据要用**操作定义**（稳态跨度 == 输入粒度 × window），别抄文档口诀（口诀会把合法的 `15m+window=4` 误判成非法）。
> ★ **对 P0「实盘 4543 笔 vs 回测 129 笔」的新线索**：BTC 全历史 6.8 年回测只有 **129 笔**，实盘 4543 笔 ⇒ **差 35 倍**。
> 若实盘跑的就是这套 15m 策略，两者**不可能是同一条策略** ⇒ 「标的池/周期不一致」应升为第一嫌疑，而不是先查记账口径。
> ★ **AtomCode 连续第 6 轮不通**（`/health` 200 + `logged_in=true` + 3 个免费模型，最小推理 240s 超时 HTTP=0）⇒ 本地 Read/Grep，**0 积分**。
> ★ **B 站（30% 权重）今日实质产出 0** —— 第 10 轮已结案降级为标题级，如实记在案，不再自我安慰。
> ★ 今日周一（周中）→ 仅 Obsidian + 工作区日志；六端归档待下个周日（含 10-18 / 10-25 两轮顺延）。

### 2026-11-02 轮（撮合内核 · 「成交判据」是档位不是事实 · nautilus `matching_core.rs` + `matching_engine/mod.rs`）

| 日期 | 主仓库 | 核心文件 | 笔记 | 三件套 |
|---|---|---|---|---|
| 2026-11-02 | nautilus_trader（轮转 #6/12；第 3 轮读过 `reconciliation`，第 5 轮读过 `crates/risk`，本轮首次读**撮合内核 + 撮合引擎**） | `crates/execution/src/matching_core.rs`（2056 行：`iterate 362` **先买后卖是硬编码契约** · `match_order 386` 三路分派 · `is_limit_matched 396` **跨价=严格档**（BUY `ask ≤ px`）· `is_limit_fillable 459` **双档开关**，`fill_limit_inside_spread` 开时再加「价差内」（BUY `px ≥ bid`）· `set_fill_limit_inside_spread 448` 由 fill model 注入、**读失败落 false（严格）** `mod.rs:563` · `add_order 300` `debug_assert` 挡重复 ID，**release 下静默双成交** · `delete_order 330` · `locate 534` · `match_limit_order 542` · `market_price_for_trigger 580` · **模块文档 `:61-74` 自己承认 "Snapshot Ordering Limitation"：快照无法恢复 bar 内穿越顺序，limits 一律先于 stops 发出**） + `matching_engine/mod.rs`（12889：`new 189` 注入宽松档 · `fill_resting_limit_order 4335` · `should_process_match_action 4348` · `determine_limit_price_and_volume 4478` · `determine_limit_fill_model_price_and_volume 4716` **有深度用深度/无深度落报价且自行再判一次跨价** · `fill_limit_order_with_snapshot 4907` · **`at_limit 4948` maker 用 `last == order_price` 精确等值、不是穿越** · `4976` `determine_trade_fill_qty` 把 `None \| Some(0)` 合并 ⇒ 丢可诊断性 · `4991` `reduce_only` 无持仓**取消**而非拒单 · `4508` 注释明写「别重复查 `is_limit_filled()`，否则概率 p²」· `4927/4762` 幂等用「已落库成交量 ≥ 委托量」） | [[20261102_nautilus_trader_vnpy]] | ✅ 笔记 + 代码（`limit_fill_semantics.py` **26/26**，三级阶梯 `exact ⊂ close_confirm ⊂ touch` + `same_bar_barriers` 路径枚举 + `ProbGuard` 概率单次不变量 + `MatchingIndex` 幂等索引；lab_bridge 零警告）+ 假设（**H-044 已证伪**：出场限价成交判据从「触及即成交」换成「触及且收盘确认」，**严格档 7/12 格 Δ<0、中位 −0.0713pp**（宽松档 +0.4039pp），成交率 73.3~97.6% → 50.5~75.6%，**插针占宽松档成交 20.6~34.4%** ⇒ **H-042 的增益有 1/5~1/3 是靠插针凑出来的**；★内部分层：**BTC 3/3 全正**、ETH 2/3 正、**BNB 3/3 负**、**DOGE 3/3 负** ⇒ 流动性越好越稳）+ 平台侧（**P0-2 换形结清**：`core/backtest.py` 新增 `exit_confirm ∈ {none, close}` 开关，默认 `none` **逐点零退化**（基线 56 笔 / 179.347% 与历史一致）；且**非法组合直接报错**——`exit_confirm` 只许与 `exit_trigger='intrabar'` 组合，防「参数给了但变成静默空操作」；新增 `selftest_exit_confirm` **8/8**（零退化 / 咬合力自证 / 变更测试 / 非法组合抛错 / rejected==0 则两档必等价）；**P0-1 结清**：`REPO_ROTATION` 的 `core_file` 第 3 次失真已修 `binance_gateway.py → linear_gateway.py`）+ 回归 **ALL GREEN**（exit_confirm 8/8 · fill_realism 10/10 · slip_lot 13 · participation 6 · risk_wiring 10/10 · risk 24/24 · lifecycle 10/10 · live 8/8） |
| 2026-11-03 | freqtrade（轮转 #7/12；首次读**记账层**——前 6 轮读的是网关/风控/组合/撮合，本轮落到「钱怎么记」） | `persistence/trade_model.py`（2198 行：`Order 65` 唯一约束 `(ft_pair, order_id)` ★**`ft_` 前缀=我方记录 / 无前缀=ccxt 镜像** 两合一 · `safe_price 130-165` 四级回退 `average or price or stop_price or ft_price` · `LocalTrade 385` **回测与实盘共用同一记账类**（无 DB 时走 `bt_trades` 类变量） · `stoploss_or_liquidation 472` 多头 `max(...)` / 空头 `min(...)` · `_calc_open_trade_value 1057` 多头 `+fees` / 空头 `−fees` · `calculate_profit 1157` ★**`ProfitStruct` 毛净四字段并列** · `calc_close_rate_for_roi 1238` ★★**反解 ROI 目标价的闭式解**（利用 `close_value` 对 rate 仿射，rate=0/1 取两点求 alpha/beta） · **`recalc_trade_from_orders 1267` ★★★从全部 order 重算而非增量累加**（`price = avg_price if is_exit` / 只有入场才更新均价 / `close_profit = close_profit_abs/total_stake*leverage`） · `adjust_stop_loss 839` 「只上不下」+ `allow_refresh` 才双向 · `update_trade 910` `status=='open'` 直接 return；出场量 `isclose(abs_tol=MATH_CLOSE_PREC)` 才 close · `update_fee 983` ★★**`fee_open_currency is None` 才是「费率未知」，一次侧只写一次**（判据是「从未写过」不是「当前为 0」——`if not fee:` 会把 BNB 抵扣费率 0 当未写）） + `wallets.py`（538 行：`_update_dry 107` 从 `_start_cap` 重算 · `_strip_unrealized_pnl 225` ★**剥离浮盈避免算两遍**（交易所 `total` 已含 uPnL） · `validate_stake_amount 408` `stake*1.3 < min_stake` 则放弃） + `exchange.py` 强平段（`get_liquidation_price 4230` / `dry_run_liquidation_price 4279` 闭式解 `value=wb/amount`、`mm_ratio_taker=mm+taker_fee`；**档位降序查表** `for tier in reversed(pair_tiers)`；`liquidation_buffer 4270` 二次缓冲） | [[20261103_freqtrade_vnpy]] | ✅ 笔记 + 代码（`position_accounting_guard.py` **21/21**，D123~D128 五设计点落地：`Fill`/`Books`/`Accountant` 幂等重算 · `flat_exit_by_avg_price` 等价性对照 · `COST_BASIS` 成本口径分档 · `LeverageTier`/`pick_tier` 降序查表 · `liquidation_with_buffer` 方向修正 · `strip_unrealized` 剥离；lab_bridge 零警告）+ 假设（**H-045 已验证**：出场第一档门槛 `tp1` 推后 → **胜率 4/4 标的严格单调递减（ρ_win 全=−1.000）**、净单笔 3/4 单调递增，判定区间 0.05→0.35 改善 **+0.7540~+1.9043pp（中位 +1.2970pp）**，明细 BTC 1.606→3.072 / ETH 1.559→2.313 / BNB 1.789→3.694 / DOGE 0.038→1.167 ⇒ **黑马策略是「赢大亏小」型，「让第一档更早激活」只是换胜率不是换收益**（胜率同时降 10.8~13.5pp，**「胜率被操纵」第 4 次实例**）；★ 端点纪律：最优落区间上端 0.35（3/4 标的）⇒ 仅读作**方向性单调**。**H-046 已验证**：`tp1×trail1` 4×5=20 格，**4/4 标的在 4 个 tp1 水平上 ρ 同号** ⇒ 两参数作用近似可加、H-045 不是 `trail1=0.10` 的局部现象；★但 `trail1` 侧**又是端点**——0.20 在 tp1=0.08 的 4/4 标的上全最优、0.15/0.25 各 3/4 最优，**单调且落网格上端，本轮未往上扫** ⇒ 今天**第 2 个端点未封口**；DOGE 最敏感（tp1=0.08：`trail1` 0.03 的 **−0.3022** → 0.20 的 **+1.1623**，**跨零**）；`tp1=0.35` 列全档逐位相同（T1 被 T2 覆盖 ⇒ **空档不是证据**））+ 平台侧（新增 **D123~D131** 九个设计点；★★**今天最重要的方法论产出：我证伪了自己的「会计漏洞」假设** —— `price = avg_price if is_exit` 与「按当时均价结转」**数学恒等**（`stake` 线性 ⇒ `avg=stake/qty` 代数闭合），真实差异只在**手续费口径**（毛收益含不含买入费，差额恰等于买入费）；⇒ **不要在「按均价 vs 按原价」上找记账改进，那条线上没有收益**，该改的是手续费字段显式分档）+ 回归（台账全表 **289 行 / 列结构异常 0**；`update_ledger` 加**双闸回读断言**——① 状态列必须合法 ② **证据列首 token 不得是状态词**（第 ① 条单独会假绿放过）） |

> ★★★ **本轮把「成交判据」这个从未被量化的口径敞口量出来了。** nautilus 把「限价单可成交」
> **显式做成两档开关**（跨价=严格 / 价差内=宽松），**默认严格**，读 fill model 失败也落严格。
> 我方回测从第 1 轮起用的 `low ≤ px ≤ high` 就是**宽松档**，且从未声明过。
> 把 H-042（出场挂限价，12/12 格全正、中位 +0.4039pp）换到严格档重测：
> **中位 +0.4039pp → −0.0713pp，7/12 格转负，成交率 87% → 62%，插针占成交 20.6~34.4%**。
> ⇒ **H-042 的结论从「4 只通用」收窄为「大市值标的可用」**：BTC 3/3 全正、ETH 2/3 正、
> BNB/DOGE **3/3 全负**。已**回溯改写台账结论区**（沉淀不是只做加法）。
> ★★ **但严格档也不是真值**：插针瞬间单子**可能**确实成交了 ⇒ 宽松档是**上界**、严格档是**下界**，
> 真值在两档之间。**任何单档数字都不许直接当结论**——这条写进台账。
> ★★ **D120 是今天最想扩散的一条**：nautilus 在 `matching_core.rs:61-74` **主动承认**自己的撮合
> 「快照恢复不了 bar 内穿越顺序」，并明确给出出口（补价格路径 / 改引擎按穿越顺序发成交），
> 而不是含糊带过。我方 `exit_trigger=intrabar` 面临**完全同构**的问题（同一根 15m 既触及止损
> 又触及止盈，谁先？），当前「止损优先」**是假设不是事实** ⇒ 已落成 `same_bar_barriers()` 的
> `olhc`/`ohlc` 双路径枚举，并用「两档结论必须相反」在 selftest 里证明它真起作用。
> ★★ **D119 概率被平方的防线**：`mod.rs:4508` 注释明写「别重复查 `is_limit_filled()` 否则 p²」。
> 我方同时有 `participation` 与 `queue` 两个概率型开关 ⇒ 已落 `ProbGuard`，同 scope 第二次 `claim` 直接抛错。
> ★ **D114 的边界**：「maker 用 `==` 判成交」是**观测粒度**决定的（tick 流看不到路径），
> **不能直接搬到 bar 级**（bar 的 low/high 本来就是路径极值摘要）。语义可以借，**粒度不能借**。
> ★ **AtomCode 连续第 12 轮不通**（`/health` 200 + `logged_in=true`，最小推理 240s 超时 HTTP=0）⇒ 本地 Read/Grep，**0 积分**。
> ★ **B 站（30% 权重）今日实质产出 0**（第 10 轮已结案）⇒ 改用「内核 + 引擎 + 本地模拟器」三处对读同一语义替代；
> 交叉阅读直接产出 D115（降级路径自己再判一次跨价）—— **只看内核根本看不出这条**，是交叉学习有效性的证据。
> ★ 今日周一（周中）→ 仅 Obsidian + 工作区日志；六端归档待下个周日（2026-11-08）。
