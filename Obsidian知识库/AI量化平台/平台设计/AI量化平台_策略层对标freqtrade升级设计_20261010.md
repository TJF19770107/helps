# AI量化平台 · 策略层对标 freqtrade 升级设计

> **日期**：2026-10-10（夜学第 4 轮）
> **来源**：`freqtrade/freqtrade` 精读 —— `strategy/interface.py`（1908 行）+ `strategy/strategy_wrapper.py`
> **性质**：**设计稿 + 差距清单**，非已实现。落地需按下方优先级逐项做，每项必须带自测。
> **绑定**：[[20261010_freqtrade_vnpy]] · [[AI量化平台架构蓝图]] · [[AI量化平台_风控层对标nautilus升级设计_20261009]]

---

## 一、为什么现在要动「策略层」

前两轮补的是**事件层**（`core/events.py`，7 层补满）和**风控层**（`core/risk.py`，六道闸）。
但**策略层** `core/strategy.py` 至今仍是一个**纯函数**：

```python
def compute_signals(df, p) -> DataFrame:   # 一次性向量化出 enter/exit 列
```

它**没有契约面**。后果有三：

| # | 症状 | 证据 |
|---|---|---|
| S1 | 策略代码出错 = 引擎直接抛异常 | 无 `safe_call` 等价物；`hypothesis_runner` 里 H-003 首次跑就 KeyError 崩掉，且**崩掉被静默当成结论** |
| S2 | 交易无法归因到「哪条信号」 | `core/backtest.py` 已记录 `sig_hs/sig_breakout/sig_vol`，但**从没有任何代码读过它做归因**（直到今天 H-007） |
| S3 | 回测与实盘的出场语义没有显式契约 | `core/backtest.py` 的成交次序是**隐式**偏保守，无 policy 开关、无对照实验 |

---

## 二、四条设计（对标 freqtrade）

### D1 · 策略回调隔离墙（P0，最低成本最高收益）

**对标**：`strategy_wrapper.py:28-61` `strategy_safe_wrapper`
**我们的落点**：`core/strategy.py` 新增 `safe_call()` 包装器（已实现于夜学模块）
**做什么**：所有「策略侧可写」的调用点（未来接用户策略、或接入 lab_bridge 的可插拔模块）一律经它。
异常 → 记警告 + 返回默认值，**引擎面永不因策略异常而崩**。
**验收**：构造一个必抛异常的策略钩子，验证 `run_backtest` 仍返回结果 + 警告列表非空。

### D2 · 引擎面 / 用户面冻结分离（P1）

**对标**：`interface.py:1817-1876`（`advise_*` 标注 "should not be overridden"）
**我们的落点**：`core/strategy.py` 拆两层 ——
- **引擎面（冻结）**：`advise_indicators()` / `advise_entry()` / `advise_exit()`（含旧名兼容 rename）
- **用户面（自由）**：`populate_indicators()` / `populate_entry_trend()` / `populate_exit_trend()`

**做什么**：把 `compute_signals` 改为「引擎面编排 + 用户钩子」结构，保留现有向量化实现作为**默认钩子**。
**为什么现在做**：`lab_bridge` 已能自动加载 `ai_quant_lab/` 的模块 —— 契约面一冻，夜学产物就能**直接当策略钩子插入**，
不用再靠「import 后手动调」。这是「学的→用的」从「能加载」升级到「能编排」。
**验收**：默认钩子与现状逐笔等价（复用今天的 `run_backtest_policy` 等价性自测法，要求 diff = 0）。

### D3 · 出场判定的成交次序 policy（P1 · 回测诚实性）

**对标**：`interface.py:1419-1522`（止损优先入列 + ROI 用 `bound_profit` 分离计价）
**我们的现状**：`core/backtest.py:136`（止损用 `low` 判、止损价成交）+ `:130,149`（止盈用 `close` 判）
→ **已经偏保守**，但这是**隐式**的，无法量化「若不保守会高估多少」。
**我们的落点**：新增 `resolve_intrabar_exit(..., policy=STOP_FIRST|TP_FIRST)`（已实现于夜学模块）。
**做什么**：让 `run_backtest` 接受 `fill_policy` 参数，并**输出两套结果**（保守 / 乐观）。
**为什么值得做**：这是**唯一能量化「回测乐观偏差」的手段**。很多「翻倍策略」的价差就在这条。
**验收**：BTC/ETH/BNB/DOGE 上跑保守 vs 乐观两套，报告偏差幅度；**并把偏差异常大的标的登记为红线**。

### D4 · 信号归因（P2 · 迭代效率）

**对标**：`interface.py:1854-1857` `enter_tag`
**我们的落点**：`attribute_by_signal(trades)`（已实现于夜学模块）+ 回测报告里加一节「按信号归因」。
**做什么**：`core/report.py` 输出每个加分信号的样本/胜率/含成本单笔均值/平均持仓。
**为什么值得做**：今天正是靠它才发现「**放量信号单信号最强（仅放量 376 笔 / 单笔 +1.835%），
头肩底最弱（仅头肩底 204 笔 / 单笔 +0.753%）**」。没有归因面，这类结论永远出不来。
**验收**：报告章节存在且数字可回溯到 `回测结果_<日期>.json`。

---

## 三、与既有两层的接线关系

```
                    ┌──────────────────────────────┐
   引擎面（冻结）    │  core/strategy.py  D2 契约层  │
                    │   advise_entry/exit  ← 用户钩子 │
                    └───────────┬──────────────────┘
                                │ D1 safe_call 包裹
     ┌──────────────────────────┼──────────────────────────┐
     ▼                          ▼                          ▼
core/events.py            core/risk.py             core/backtest.py
（事件层·7层之一）      （风控层·六道闸 R1-R6）      （撮合回测层）
                            ▲                          ▲
                            │  G1~G4 四条缺口          │  D3 fill_policy
                            │  （上轮设计·待回填）      │  D4 attribute_by_signal
                            └──────────┬───────────────┘
                                       │
                          core/lab_bridge.py（夜学↔平台 唯一通道）
                                       │
              ai_quant_lab/20261010_freqtrade_vnpy/freqtrade_exit_patterns.py v1.0.0
              （D1 safe_call · P2 TimeStopPolicy · P3 TimeDecayROI · P4 resolve_intrabar_exit
                · D4 attribute_by_signal · 扩展回测 run_backtest_policy）
```

**★ 关键状态**：`freqtrade_exit_patterns.py` **已在平台外环就位**（`lab_bridge` 零警告加载），
但 **D1~D4 尚未回填 `core/` 本体** —— 与上轮 nautilus 四条缺口（G1~G4）处境相同。下一轮 P0 就是回填。

---

## 四、下一轮落地优先级（P0 → P2）

| 优先级 | 项 | 落点 | 为什么排这个序 |
|---|---|---|---|
| **P0** | 回填 **G1**（风险预算含费口径）+ 执行 **D1**（safe_call） | `core/risk.py` · `core/strategy.py` | 两条都是「一行公式/一个包装器」级别，成本极低、收益确定；G1 已有 H-005 数学证明 |
| **P0** | 回填 **E1**（事件层 timer 独立线程） | `core/events.py` | 时间止损/定时巡检的实盘安全项 |
| **P1** | 执行 **D3**（fill_policy 双口径回测） | `core/backtest.py` | 量化回测乐观偏差，是「对标对冲基金工程纪律」的实质动作 |
| **P1** | 执行 **D4**（信号归因进报告） | `core/report.py` | 迭代效率；今天已实证其价值 |
| **P1** | 回填 **G3 + G4**（挂单占用额度 R7 + 报单限流 R8） | `core/risk.py` | 实盘爆仓类缺口 |
| **P2** | 执行 **D2**（引擎面/用户面分离） | `core/strategy.py` | 结构改动最大，需先有 D1 兜底；为 lab_bridge 插拔铺路 |
| **P2** | 回填 **G2**（三态状态机） | `core/risk.py` + `live.py`/`backtest.py` 调用点 | ⚠️ 必须保留我们「停机仍可平仓」的实战语义，不照搬 nautilus |

---

## 五、诚实边界

- 本设计**不含任何收益承诺**。四条目的一是**工程约束**（隔离、契约、诚实、归因），不是盈利手段。
- **今天的实验反证了一条流行设计**：freqtrade 的 `minimal_roi` 时长分段止盈搬到黑马策略上
  **严重劣化**（H-008：胜率 19%→51%，但含成本单笔均值 2.006%→0.2275%，总收益由正转负）。
  → **对标一流框架 ≠ 照搬其默认值**。设计思想可搬，参数必须用我们自己的数据重定。
- 基线策略最大回撤 **77%~99.5%**、4 只标的中 **1 只总收益为负** —— 这是风险声明，不粉饰。
