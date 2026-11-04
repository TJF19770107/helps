---
日期: 2026-10-10
仓库: freqtrade/freqtrade（主·#7/12）· vnpy/vnpy（副·事件引擎，本轮未重读）
核心文件: freqtrade/strategy/interface.py（1908 行）· freqtrade/strategy/strategy_wrapper.py
轮次: 第 4 轮
tags: [AI量化平台, 夜学, 代码拆解, freqtrade, 策略接口]
---

# 20261010 · freqtrade · strategy/interface.py

## 0. 一句话结论

> **freqtrade 把「策略」定义成一组**可被引擎包裹的用户回调**，而不是一段自由代码。**
> 它靠四道工程约束把用户策略与引擎隔离：① 回调全走 `strategy_safe_wrapper`（异常不外泄）；
> ② 引擎调用面（`advise_*`）标记「should not be overridden」，用户只填 `populate_*`；
> ③ 出场判定里**止损优先且与 ROI 分离计价**（`bound_profit`），杜绝同根 K 线「用最有利价成交」；
> ④ 每笔交易带 `enter_tag/exit_tag` **信号归因**。
> 这四条我们 `core/strategy.py` **一条都没实现** —— 它是「一次性向量化出信号」的函数，没有契约层。

---

## 1. 这个文件在系统里管什么（架构定位）

| 项 | 结论 |
|---|---|
| 所属层 | **策略层（策略契约 / 接口层）** |
| 本质 | 引擎（回测/实盘）与「用户策略」之间的**唯一契约面** |
| 上游依赖 | `configuration.TimeRange`（时间区间）、`data.dataprovider.DataProvider`（行情）、`persistence.Trade/Order/PairLocks`（持仓与挂单）、`wallets.Wallets`（余额）、`strategy.hyper.HyperStrategyMixin`（超参） |
| 下游调用者 | `freqtrade/optimize/backtesting.py`（回测）、`freqtrade/freqtradebot.py`（实盘/dry-run）、`freqtrade/optimize/hyperopt*`（超参优化）、`freqtrade/rpc/`（Telegram/API 查询） |
| 反向依赖 | 引擎**不直接读用户策略属性**，一律经本文件的方法（`advise_entry` / `should_exit` / `confirm_trade_entry`） |
| 同类对标 | vnpy `CtaTemplate` + `CtaEngine`；nautilus `Strategy` + `StrategyEngine`。**freqtrade 的差异点：把用户代码当「不可信输入」来防** |

---

## 2. 调用链（文字版时序图）

**A. 信号生成（回测与实盘同一条链）**
```
FreqtradeBot.process() / Backtesting._get_ohlcv_as_lists()
  → IStrategy.analyze_pair(pair)
      → dp.ohlcv(pair, timeframe)                    # 取 K 线
      → _analyze_ticker_internal(dataframe, metadata)
          ├─ new_candle?（process_only_new_candles 且 __last_candle_seen_per_pair 变了）
          │     ├─ strategy_safe_wrapper(analyze_ticker)   ★ P1 隔离墙
          │     │     → advise_indicators()   → @informative 装饰器 → populate_indicators()
          │     │     → advise_entry()        → populate_entry_trend() → enter_long/enter_tag
          │     │     → advise_exit()         → populate_exit_trend()  → exit_long/exit_tag
          │     └─ StrategyResultValidator.assert_df()      ★ 反未来函数校验
          │     └─ dp._set_cached_df() / dp._emit_df()
          └─ else：remove_entry_exit_signals(dataframe)     # 旧 K 线一律剥掉信号
  → 引擎读 enter_long / exit_long 列
```

**B. 持仓中每根 K 线的出场判定**
```
FreqtradeBot.handle_trade() / Backtesting 逐根循环
  → IStrategy.should_exit(trade, rate, current_time, enter=, exit_=, low=, high=)
      ├─ current_profit_best = calc_profit_ratio(bound)      ★ P4 分离计价（多头 bound=high）
      ├─ ft_stoploss_reached(...)    → ft_stoploss_adjust()  # 止损（用 current_rate / low）
      │     ├─ dir_correct 守卫：止损只在「方向正确」时收紧   ★ 防自定义止损放错边
      │     ├─ custom_stoploss()（仅 use_custom_stoploss）
      │     └─ trailing_stop 处理
      ├─ min_roi_reached(current_profit_best)                # ROI（用 bound_profit！）
      └─ 顺序装填 exits：① exit_signal/custom_exit ② STOP_LOSS/LIQUIDATION ③ ROI ④ TRAILING
  → 引擎取 exits[0] 执行
```

**C. 下单前闸门**
```
引擎准备下单 → IStrategy.confirm_trade_entry(...)  → bool（False 则中止）
引擎准备平仓 → IStrategy.confirm_trade_exit(...)   → bool
成交回报    → IStrategy.order_filled(...)          → None（幂等回调）
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 行范围 | 职责 | 备注 |
|---|---|---|---|---|
| `IStrategy(ABC, HyperStrategyMixin)` | 类 | 52 | 策略契约基类 | 同时是超参容器 |
| `minimal_roi: dict` | 属性 | 72 | `{持仓分钟: 要求收益率}` **按时长递减的止盈表** | 与 `custom_roi` 取更小者生效 |
| `process_only_new_candles` | 属性 | 110 | 仅在出现新 K 线时重算指标 | 性能闸 |
| `startup_candle_count` | 属性 | 128 | 指标预热所需 K 线数 | 防「指标未热就出信号」 |
| `protections` | 属性 | 131 | 保护器（冷却/连亏停牌等）列表 | 与我们的风控层同族 |
| `populate_entry_trend` | 用户钩子 | 254 | 写 `enter_long / enter_tag` 列 | **用户唯一入口** |
| `advise_entry` | 引擎面 | 1842 | 初始化 `enter_tag` → 调 `populate_entry_trend` → 兼容 rename(`buy`→`enter_long`) | 「should not be overridden」 |
| `confirm_trade_entry/exit` | 用户钩子 | 359/395 | 下单/平仓前最终裁决，返回 bool | 默认 `True` |
| `custom_stoploss` | 用户钩子 | 446 | 返回**相对 current_rate 的止损比例** | 硬上限仍是 `self.stoploss` |
| `adjust_trade_position` | 用户钩子 | 654 | 加仓/减仓（需开 `position_adjustment_enable`） | 默认禁用 |
| `analyze_ticker` | 引擎面 | 1190 | indicators→entry→exit 三段串起来 | 仅 live 用 |
| `_analyze_ticker_internal` | 内部 | 1206 | **新 K 线缓存** + 校验 + 写 dp 缓存 | 性能与正确性双闸 |
| `should_exit` | 引擎面 | 1419 | 汇总止损/ROI/信号/custom 四条出场为 `list[ExitCheckTuple]` | **止损排在 ROI 之前** |
| `ft_stoploss_adjust` | 内部 | 1524 | 动态调止损：`dir_correct` 守卫 → custom → trailing | 只在方向正确时收紧 |
| `ft_stoploss_reached` | 内部 | 1605 | 判定止损/强平是否触及 | 返回 `ExitCheckTuple` |
| `min_roi_reached_entry` | 内部 | 1675 | 按时长取 ROI 档，与 `custom_roi` 取更小值 | **minimal_roi 的实现核心** |
| `ft_check_timed_out` | 内部 | 1734 | 挂单超时判定（`unfilledtimeout` + 用户 `check_*_timeout`） | 本轮回填假设 H-006 的来源 |
| `strategy_safe_wrapper` | 装饰器 | wrapper:28 | 用户回调异常隔离墙 + trade deepcopy | **P1 的原始出处** |
| `StrategyResultValidator.assert_df` | 类 | validation:12 | 断言 dataframe 长度/末根 close/末根 date **未被策略改动** | 反未来函数（改历史=立刻报错） |

---

## 4. 可迁移设计点（逐条写「为什么好」）

### P1 · 用户回调隔离墙 `strategy_safe_wrapper`（`strategy_wrapper.py:28-61`）
所有用户方法调用点都写成 `strategy_safe_wrapper(self.xxx, default_retval=None, supress_error=True)(...)`。
捕获 `ValueError` 与通用 `Exception`，记带调用点 traceback 的警告，返回默认值；
并对传入的 `trade` 做 `deepcopy`（仅当方法不是 `IStrategy.` 自带实现时）。
**为什么好**：策略是「不可信输入」。用户写错一行，不该让整台机器人挂掉，更不该让持仓状态被策略偷偷改坏。
我们 `core/strategy.py` 的策略是纯函数、风险低，但一旦接入「用户可写策略」，这层必须先有。

### P2 · 引擎面 / 用户面分离 + 向后兼容改名（`interface.py:1817-1876`）
`advise_indicators / advise_entry / advise_exit` 明确标注 **"should not be overridden"**，
内部才调用户钩子 `populate_indicators / populate_entry_trend / populate_exit_trend`；
且用 `if "enter_long" not in df.columns: df.rename({"buy":"enter_long"})` 做旧 API 兼容。
**为什么好**：引擎的调用面**冻结**，用户的扩展面**自由演化**。升级引擎不改用户策略；
改用户 API 时在唯一一处做兼容层，不必全库搜 `buy`。

### P3 · 出场判定：止损优先 + ROI 用 candle bound 分离计价（`interface.py:1419-1522`）
```python
current_profit        = trade.calc_profit_ratio(rate)              # 止损用
current_profit_best   = trade.calc_profit_ratio(high or low)       # ROI 用（多头高、空头低）
...
exits.append(stoplossflag)   # 止损先入列
if roi_reached: exits.append(ExitCheckTuple(ExitType.ROI))         # ROI 后入列
```
**为什么好**：同一根 K 线内「既破止损又够止盈」在小时级数据里无法分辨先后。
freqtrade 把 **止损放前面 + ROI 用最有利边界计价**，结果是**偏保守**。
反过来（止盈优先）就是无数「翻倍回测」的真实来源。这条是**回测诚实性的硬闸**。
> 我们 `core/backtest.py` 已天然偏保守（止损用 `low` 判、止盈用 `close` 判），
> 但**没有显式的 policy 开关**，也没把「乐观口径」量化出来做对照。→ 已做成 `resolve_intrabar_exit(policy=STOP_FIRST|TP_FIRST)`。

### P4 · 时长函数化的止盈/止损（`minimal_roi` / `ft_check_timed_out`）
- `minimal_roi: {分钟: 收益率}` 是一个**关于持仓时长的分段函数**，越久要求越低；
- `ft_check_timed_out` 对**挂单**做超时撤单。
**为什么好**：它承认「时间本身是成本」。持仓不涨 = 机会成本，需要一条与价格无关的退出理由。
（⚠️ 但本条被我们今天的回测证伪，见 H-008 —— 设计思想正确 ≠ 适用于本策略。）

### P5 · 信号归因 `enter_tag` / `exit_tag`（`interface.py:1854-1857, 1871`）
每个入场信号可写一个 tag 字符串，交易记录永久带这个 tag。
**为什么好**：能从「整体胜率」下钻到「哪条信号真赚钱」，这是策略迭代的**唯一有效归因面**。
我们今天正是靠等价物（`core/backtest.py` 已存的 `sig_hs/sig_breakout/sig_vol`）才算出 H-007。

---

## 5. 可复用代码片段

> 完整实现见 `ai_quant_lab/20261010_freqtrade_vnpy/freqtrade_exit_patterns.py` v1.0.0（自测全通过，
> `lab_bridge` 零警告加载）。此处只贴最核心两段的**意图**，不整段搬运源码（开源许可 + 篇幅纪律）。

```python
# 来源：freqtrade/freqtrade/strategy/strategy_wrapper.py:38-59（重写，非搬运）
# 用途：用户回调隔离墙 —— 引擎调用面永不因策略异常而崩
def safe_call(fn, *args, default=None, mute=True, message="", **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        if mute:
            logger.warning("%s回调异常被隔离: %s: %s", message, type(e).__name__, e)
            return default
        raise
```

```python
# 来源：freqtrade/freqtrade/strategy/interface.py:1443-1462（语义重写）
# 用途：出场判定里的「分离计价」—— 止损用现价，ROI 用最有利边界；双触时止损优先
def resolve_intrabar_exit(low, high, close, stop_price, tp_arm_price, policy="stop_first"):
    stop_hit = stop_price is not None and low <= stop_price
    tp_hit   = tp_arm_price is not None and high >= tp_arm_price
    if stop_hit and tp_hit:
        return ("stop", stop_price) if policy == "stop_first" else ("tp", tp_arm_price)
    if stop_hit: return ("stop", stop_price)
    if tp_hit:   return ("tp", tp_arm_price)
    return None
```

**指针**：`freqtrade/freqtrade/strategy/interface.py:1419-1522`（should_exit 全貌）、
`freqtrade/freqtrade/strategy/strategy_validation.py:19-42`（assert_df）。

---

## 6. B站学习（本日 30% 权重）

| 项 | 结论 |
|---|---|
| 抓取方式 | `WebFetch` 直取 B 站页面 |
| **有无字幕** | ❌ **无**（页面 HTML 不暴露 CC/字幕轨，需登录 cookie + 播放器 API） |
| 抓到的内容 | 仅视频简介（无正文） |
| 处理 | 按技能 §3 降级为**目录级笔记**（不做音频转录，守零成本底线） |

**视频清单（已入清单，明日补）**

| # | 标题 | UP / 来源 | 链接 | 字幕 |
|---|---|---|---|---|
| 1 | 三、vn.py基础操作-（1-2）CTA策略编写（面向个人交易员的量化投资课程） | 系列课程 | `bilibili.com/video/BV1ov4y1q7Ms/` | ❌ 无 |
| 2 | 如何编写一个完整可实盘的策略（简单框架·止损止盈·跨周期·逻辑优化） | 论坛自荐 UP | `bilibili.com/video/BV1pV411r7Kt` | ❌ 未验证 |
| 3 | 野生量化员 · VNPY 视频教程 40 节（BarGenerator / CtaTemplate / 回测撮合机制） | quant666 转载 | `quant666.com/458.html` | ❌ 未验证 |

**从简介能蒸馏出的要点（当假设看，不当结论）**：
- 该课程明确写：**「移动止损并不能取得明显优于固定止损的收益 …… 回测是检验策略的唯一正确方法」**
  → 与我们今天的 **H-006（时间止损）被证伪**、**H-008（时长止盈）被证伪** 方向一致。
  但这是**博主口播级别的主张**，只能作为「同类结论的旁证」，不能算证据。
- 课程目录里的高价值专章（待明日带字幕精读）：`BarGenerator` K 线合成/过滤方法、**回测引擎撮合机制**、
  `ArrayManager` 源码、**实盘与回测策略的差异分析** —— 最后这条正是我们平台最缺的「回测/实盘同源」章节。

---

## 7. 对黑马策略的启发（已落成具体动作）

| # | 动作 | 对应假设 | 结果 |
|---|---|---|---|
| 1 | 把 `ft_check_timed_out` 的超时思想移植到**持仓层**：持仓 ≥384 根且从未触发止盈档 → 离场 | [[策略假设台账\|H-006]] | **已证伪**（4 只中 3 只单笔均值下降） |
| 2 | 用 enter_tag 归因思想审计招牌信号：把 `sig_hs` 置零做 A/B | [[策略假设台账\|H-007]] | **已验证（弱）**（4/4 不下降，但幅度小） |
| 3 | 把 `minimal_roi` 时长分段止盈搬进来做对照 | [[策略假设台账\|H-008]] | **已证伪**（0/4，胜率翻倍但总收益转负） |
| 4 | 补一个显式的「同根 K 线成交次序」policy 开关（保守/乐观对照） | 已落代码 `resolve_intrabar_exit` | 待挂假设（下轮） |

**若 H-007 坐实（头肩底无正向边际），改哪一行**：
`quant_app/core/strategy.py` — `StrategyParams` 增 `use_hs_signal: bool = True`，
在 `compute_signals` 里 `out["signal_score"] = sig_breakout + sig_vol (+ sig_hs if use_hs_signal)`；
`detect_head_shoulders_vectorized` 可短路跳过（它是全场最重的计算，24 万根上逐根扫局部极值）。
⚠️ 但今天只判到「无正向边际」，**不足以**直接改为默认关闭 —— 需先补「头肩底在其他周期 / 其他标的池」的复测。

**若 H-006 被证伪（已发生），改哪**：不改。时间止损**不加入**默认出场链；但保留 `TimeStopPolicy`
为可选闸（`max_holding_bars=0` 即关闭），供资金受限场景下的「周转优先」模式使用。

---

## 8. 未完成 / 失败区（诚实留痕）

| # | 事项 | 状态 | 原因 |
|---|---|---|---|
| 1 | B 站字幕抓取 | ❌ 未完成 | 页面不暴露 CC 字幕轨；需登录 cookie 或播放器 API（明日补，不转录音频） |
| 2 | 副仓库 vnpy 本轮未重读 | ⚠️ 降级 | 主仓库 freqtrade 精读已占满当日份额；vnpy `event/engine.py` 已于第 3 轮读过 |
| 3 | `freqtrade/optimize/backtesting.py`（撮合引擎）未读 | ⚠️ 待补 | 这是 freqtrade 的「回测/实盘同源」核心，应列下一轮重点 |
| 4 | `strategy/parameters.py`（超参空间）未读 | ⚠️ 待补 | 与我们 `StrategyParams` 直接对标 |
| 5 | **DOGE 系统性亏损未归因** | ❌ 未完成 | 基线 DOGE -79.8%、最大回撤 99.5%，而 BTC/ETH/BNB 为正 → **策略泛化性存疑**，必须单独立假设 |
| 6 | 头肩底 A/B 的**统计显著性**未做 | ⚠️ 部分完成 | 4/4 方向一致但单标的幅度 < 噪声尺度（±0.026pp vs SE≈0.85pp）→ 只判「无正向边际」 |
| 7 | 本轮未用 AtomCode 做交叉校验 | ⚠️ 降级 | guard 实测 `healthy`（glm5.3-flash / 28.1s 回字「通了」），但本地 Read/Grep 已足够定性；**未消耗额度** |

**诚实边界（不写进口号）**：
- 本轮**未发现任何可交易的正向改进**。三条新假设里 **2 条被证伪**，1 条只是「无正向边际」。
- 基线策略本身的最大回撤 **77%~99.5%**，且 4 只标的中 1 只总收益为负 —— 这属于**风险声明**，不是卖点。
- 「黑马策略高倍数表现」仍为**待独立复核项**，不因本轮回测而有任何改变。
- 本轮回测全部为**本地 CSV + 纯 pandas/numpy**，零外部 API、零积分。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘路径：
      `我的黑马策略/ai_quant_lab/20261010_freqtrade_vnpy/freqtrade_exit_patterns.py`（v1.0.0，自测全通过，
      **`lab_bridge.get("freqtrade_exit_patterns")` 零警告加载成功**，6 个公开接口）
      · 同目录含当日自动生成的 `TASK_CARD.md`
- [x] ③ 策略假设已追加进 [[策略假设台账]]（H-006 / H-007 / H-008）
- [x] ④ 台账状态推进：`hypothesis_runner.py` 全量跑完，8 条假设**无悬空**，结果落
      `策略假设/回测结果/回测结果_20261010.json`，回写前已备份 `策略假设/backup/策略假设台账_20261010_040830.md`

---

## 10. 成本与技能

- **本次花费积分估算：0**（本地 Read/Grep 精读 + 本地 CSV 回测；AtomCode 仅跑守护探活，未消耗推理额度）
- **用了哪些技能**：
  - `ai-quant-open-source-nightly-learning` v1.1.1 —— 全套流程骨架（第零~九步）
  - `币安量化数据通路与黑马策略诊断`（隐性复用其数据口径与「真实性回测 + 回撤归因」方法论）
- **没用哪个技能及原因**：
  - AtomCode 精读引擎（虽 guard `healthy`）—— 本轮以本地源码事实为准，无需额外交叉校验，守零消耗
  - `tencent-docs-*` / 可视化类技能 —— 无文档交付需求
- **沉淀 / 迭代了什么**：
  - 🆕 新模块 `freqtrade_exit_patterns.py` v1.0.0（4 条可迁移设计 + 信号归因 + 扩展回测，自测全通过）
  - 🔧 `hypothesis_runner.py` 升级：新增 `_load_15m` 缓存 / `_exit_patterns` 惰性加载 /
    `_bt_metrics` / `_paired_verdict` 通用 A-B 判定器 + `verify_H006/H007/H008` 三个验证器
  - 📓 台账新增 3 条假设，全部当日结清
  - ⏳ 技能 `ai-quant-open-source-nightly-learning` 待迭代项见下（v1.1.2 计划）
