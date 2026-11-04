---
日期: 2026-10-29
仓库: vnpy/vnpy_ctabacktester（主，首次精读）· vnpy/vnpy `vnpy/trader/optimize.py`（交叉）· vnpy/vnpy_ctastrategy `backtesting.py:1184-1235`（交叉）
核心文件: vnpy_ctabacktester/engine.py（498）· ui/widget.py（1580）· tests/test_engine.py（569）· vnpy/trader/optimize.py（276）
轮次: 第 18 轮
tags: [AI量化平台, 夜学, 代码拆解, 参数优化, 网格可信度, 实验可追溯]
---

# 20261029 · vnpy/vnpy_ctabacktester · engine.py + ui/widget.py + trader/optimize.py

> 主题锁定：**参数优化的「网格可信度」与「实验产物可追溯」**。
> 为什么是它：第 17 轮挂账 P0-1 是 `exit_trigger × 宽档位交互`，P1-4 是「回测结果按日单文件被覆盖」，
> 两条其实是**同一个病灶的两面** —— 我们的「最优参数」既可能没被测到、也可能无法复现。
> 而 vnpy 家族的**参数优化层**（backtester 编排 + trader/optimize 网格 + UI 目标选择）
> 恰是这套问题的完整现场，且从没读过。

---

## 0. 一句话结论

> **vnpy 的参数优化有三个同族缺陷，我们全踩了其中两个：**
> ① 网格端点会被**浮点累积**吃掉（`(0.1, 0.3, 0.1)` 实测只产出 2 档，0.3 从未被测，6 用例丢 2 个）；
> ② 优化目标是**裸单目标取最大**（5 个目标互斥、无「约束下最大化」），单调响应必然推着参数往端点跑；
> ③ 优化结果**只存内存、无 run_id、不落盘**，关窗即失。
> 我们的 H-023 连挂 5 轮「端点第 4 次外移」，本质是**缺一个能当场判死「这个最优点能不能外推」的组件** ——
> 本轮把它做出来了：`opt_grid_guard.py`（**40/40** 自测，含 3 处 A/B 反测）。

---

## 1. 这个文件在系统里管什么（架构定位）

| 文件 | 所属层 | 管什么 | 上游依赖 | 下游调用者 |
|---|---|---|---|---|
| `vnpy_ctabacktester/engine.py`（498） | **工具层 / 研究编排层**（不是交易链路） | 把「跑一次回测 / 跑一次参数优化 / 下一段历史数据」包装成**可线程化、可事件通知、同一时刻只允许一个任务**的引擎 | `vnpy.trader`（MainEngine / EventEngine / database / datafeed / **optimize**）· `vnpy_ctastrategy`（CtaTemplate / BacktestingEngine / OptimizationSetting） | `ui/widget.py`（1580，PyQt 面板）· `script/run.py`（28） |
| `vnpy/trader/optimize.py`（276） | **工具层** | 参数网格构造 + 穷举/遗传两套优化执行器 | `concurrent.futures` / `multiprocessing(spawn)` / `deap` / `tqdm` | `vnpy_ctastrategy/backtesting.py:583,615`；`ctabacktester/engine.py:325,331` |
| `ui/widget.py`（1580） | **表现层** | 参数表单、优化对话框（目标选择 / 网格区间 / 进程数）、结果表 | `engine.py` 全部公开方法 | 人 |

★ **它不是「回测引擎」，是「回测任务的调度器 + 结果的容器」**。
真正的撮合与结算在 `vnpy_ctastrategy.BackingtestingEngine` 里（第 17 轮已精读）。
这个区分很重要：**编排层出问题，症状会伪装成「策略出问题」** ——
比如「同一组参数两次跑结果不一样」，八成不是策略不确定，是编排层把上一次的结果没清干净。

---

## 2. 调用链（文字版时序图）

### 2.1 单次回测
```
UI 点「开始回测」 (widget.py:483 起)
  → BacktesterEngine.start_backtesting (engine.py:216)
      ├─ if self.thread: 写日志「已有任务在运行中」→ return False   ← 互斥在这里
      └─ Thread(target=run_backtesting).start()  → return True
          → run_backtesting (engine.py:146)
              ├─ self.result_df = None; self.result_statistics = None   ← 先清，再跑
              ├─ BacktestingEngine.set_parameters / add_strategy        (149-189)
              ├─ engine.load_data()                                     (191)
              │    └─ if not history_data: 写日志 → self.thread=None → return   ← 失败①
              ├─ try: engine.run_backtesting()
              │    except: 写日志 → self.thread=None → return                     ← 失败②
              ├─ self.result_df = engine.calculate_result()             (206)
              ├─ self.result_statistics = engine.calculate_statistics() (207)
              ├─ self.thread = None
              └─ EventEngine.put(EVENT_BACKTESTER_BACKTESTING_FINISHED) (213)
                  → widget 事件回调 → ResultMonitor.set_data(df) (893) → 画资金曲线/回撤/盈亏分布
```

### 2.2 参数优化
```
UI「优化参数配置」对话框 OptimizationSettingEditor (widget.py:958)
  → 用户在 5 个目标里选 1 个 (DISPLAY_NAME_MAP:958-964)
  → 每个数值参数填「开始 / 步进 / 结束」三格 (1010-1035)
  → 点「多进程优化」/「遗传算法优化」→ generate_setting (1076)
      └─ optimization_setting.set_target(target_name)              (1072)
      └─ optimization_setting.add_parameter(name, s, e, step)      (1089)
            → optimize.py:44   ★ 浮点累积 while value <= end: value += step   (67-69)
  → start_optimization (engine.py:345) → Thread(run_optimization)
      → run_optimization (engine.py:274)
          ├─ result_values = None
          ├─ set_parameters / add_strategy(cls, {})     ← ★ 传空 setting
          ├─ max_workers==0 → None（不限制）            (321-322)
          └─ engine.run_bf_optimization / run_ga_optimization   (324-335)   ← ★ 无 try/except
              → optimize.py:116 run_bf_optimization
                  ├─ ProcessPoolExecutor(max_workers, mp_context=spawn)     (132-135)
                  ├─ executor.map(evaluate, settings)                       (137)
                  │    → backtesting.py:1184 evaluate(setting)
                  │        ├─ 为**每一组参数新建一个 BacktestingEngine**
                  │        ├─ load_data / run_backtesting / calculate_result（**结果丢弃**）
                  │        ├─ calculate_statistics(output=False)
                  │        └─ return (setting, statistics.get(target_name, 0), statistics)  ← ★ 缺键默认 0
                  └─ results.sort(reverse=True, key=key_func)               (141)  ★ 裸单目标
      → thread=None → EVENT_BACKTESTER_OPTIMIZATION_FINISHED
          → OptimizationResultMonitor (widget.py:1100) → 表格**只有两列**：[参数, 目标值]
              → 点「保存」→ save_csv (1165) → 用户自选路径，无 run_id
```

### 2.3 最容易误读的一处
`evaluate` 的返回值是**三元组** `(setting, target_value, statistics)`，
`statistics` 里明明有 40+ 项（笔数/胜率/回撤/夏普/日均盈亏…），
但 `OptimizationResultMonitor.init_ui` 只取 `setting, target_value, __`（widget.py:1135）
⇒ **完整的风险指标被生产出来又被丢掉，用户在「看不到回撤」的表上挑「最优参数」**。
这不是 UI 审美问题，是**强制单指标决策**。

---

## 3. 关键类 / 函数（签名 + 职责）

### 3.1 `vnpy_ctabacktester/engine.py`

| 名称 | 位置 | 签名要点 | 职责 | 备注 |
|---|---|---|---|---|
| `BacktesterEngine.__init__` | 42 | `(main_engine, event_engine)` | 建 `classes` 容器、`thread` 互斥位、`result_df/result_statistics/result_values` 三个结果槽 | 结果**全在内存** |
| `init_engine` | 60 | `()` | 建 BacktestingEngine、把它的 `output` 重定向到 `write_log`、加载策略类、初始化 datafeed | 日志外流设计好 |
| `load_strategy_class_from_module` | 111 | `(module_name)` | `importlib.import_module` + **`reload`** 后再 `dir()` 扫 CtaTemplate 子类 | `reload` 让改完策略立即生效 |
| `run_backtesting` | 146 | `(class_name, vt_symbol, interval, start, end, rate, slippage, size, pricetick, capital, setting)` | 主回测流程 | 见 D88 |
| `start_backtesting` | 216 | 同上 + `→ bool` | 互斥检查 + 起线程 | 互斥靠 `self.thread` 非空 |
| `run_optimization` | 274 | `(... optimization_setting, use_ga, max_workers)` | 分派穷举/遗传 | ★ **无 try/except**（见 D87） |
| `run_downloading` | 389 | `(vt_symbol, interval, start, end)` | 下载历史数据入 DB | 有 try/except |
| `get_all_trades/orders/daily_results` | 474-487 | `() → list` | 把 BacktestingEngine 的明细透出去 | 直接转发，不做转换 |

### 3.2 `vnpy/trader/optimize.py`

| 名称 | 位置 | 签名要点 | 职责 | 备注 |
|---|---|---|---|---|
| `OptimizationSetting.add_parameter` | 44-73 | `(name, start, end=None, step=None) → (bool, str)` | 单值或**闭区间等距网格** | ★ 浮点累积（D82） |
| `OptimizationSetting.generate_settings` | 81-95 | `() → list[dict]` | `itertools.product` 笛卡尔积 | 顺序由 dict 插入序决定 |
| `check_optimization_setting` | 98 | `(setting, output) → bool` | 空组合 / 无目标名 两条前置校验 | 有校验，但只管这两条 |
| `run_bf_optimization` | 116-147 | `(evaluate_func, setting, key_func, max_workers, output) → list[tuple]` | `ProcessPoolExecutor(spawn).map` → `sort(reverse=True, key=key_func)` | ★ 裸单目标（D83） |
| `run_ga_optimization` | 150-254 | 同上 + `pop_size=100, ngen=30, cxpb=0.95…` | DEAP `eaMuPlusLambda` + `selNSGA2` + 共享 dict 缓存 | ★ 伪多目标（D84b） |
| `ga_evaluate` | 257-275 | `(cache, evaluate_func, key_func, parameters) → (float,)` | 带缓存的单目标求值 | 缓存键是 `tuple(parameters)` |

### 3.3 `ui/widget.py` 的三处关键

| 名称 | 位置 | 职责 | 备注 |
|---|---|---|---|
| `OptimizationSettingEditor.DISPLAY_NAME_MAP` | 958-964 | 中文显示名 → 统计字段名：总收益率/夏普比率/EWM夏普/收益回撤比/日均盈亏 | ★ **5 个目标互斥使用** |
| `OptimizationSettingEditor.generate_setting` | 1076-1096 | 读三格文本 → `add_parameter` | ★ 无整除校验（D90） |
| `OptimizationResultMonitor` | 1100-1185 | 两列表格 + 手动 save_csv | ★ 丢弃 statistics（D85）· 无 run_id（D86） |

### 3.4 `tests/test_engine.py`（569 行 · 11 个用例）

| 用例 | 位置 | 断言什么 | 为什么值得抄 |
|---|---|---|---|
| `test_run_backtesting_without_bars_skips_statistics` | 284 | 空数据后 `result_df is None` **且** `result_statistics is None` | ★ 官方把「没数据」的返回值**写进测试**，但它和「跑挂了」的返回值**一模一样** |
| `test_start_backtesting_rejects_when_busy` | 344 | `engine.thread = sentinel` → `start_backtesting` 返回 `False` 且 `thread is sentinel` | 互斥是**被测试保护的契约**，不是顺手写的 |
| `test_run_optimization_zero_workers_means_unlimited` | 380 | `max_workers==0` 传下去变成 `None` | 用测试固化「0 = 不限制」这种魔法值 |
| `test_run_optimization_use_ga_keeps_worker_count` | 435 | GA 分支同样尊重 worker 数 | 两条分支都被覆盖 |

---

## 4. 可迁移设计点（D82 ~ D90）

### D82 · 网格端点必须用「整数索引 + 端点断言」，禁止浮点累积
`optimize.py:64-71` 的写法：
```python
value = start
while value <= end:
    value_list.append(value)
    value += step
```
**实测复现（本机跑，6 个用例）**：

| start | end | step | vnpy 产出 | 末值 | 正确档数 | 结论 |
|---|---|---|---|---|---|---|
| 0.1 | 0.3 | 0.1 | 2 档 | 0.2 | 3 | ★ **端点 0.3 从未被测** |
| 1.0 | 1.3 | 0.1 | 3 档 | 1.2000000000000002 | 4 | ★ 端点 1.3 丢失 |
| 0.01 | 0.05 | 0.01 | 5 档 | 0.05 | 5 | ok |
| 0.02 | 0.10 | 0.02 | 5 档 | 0.1 | 5 | ok |
| 10 | 40 | 10 | 4 档 | 40 | 4 | ok |
| 0.05 | 0.30 | 0.05 | 6 档 | 0.3 | 6 | ok |

**端点丢失 2/6。** 为什么这么设计不好：用户填「结束 = 0.3」的心智模型是「0.3 会被测到」。
端点被浮点误差吃掉后，最优点自然落在「最后一个被测点」，报告里写「最优在端点」，
实际那个端点**根本没进过回测**。
→ **正确写法**：`levels = [round(start + i*step, d) for i in range(n+1)]`，`n = round((end-start)/step)`，
并**断言 `levels[-1] == end`**；步进不整除时直接报错，而不是静默少一档。
**这条对我们是同形风险**：H-023 的 8 个档位写成显式列表躲过了它，
但只要有人用 range 式写法扫 `trail = 0.05~0.20 step=0.01`，就会踩上。

### D83 · 优化目标不能只有「裸单目标取最大」
`optimize.py:141` 只有 `results.sort(reverse=True, key=key_func)`。
vnpy 给了 5 个可选目标（`widget.py:958`），但它们是**互斥选择**，不存在
「在最大回撤 ≤ X 的前提下最大化净单笔」这种写法。
**后果**：单目标 + 单调响应 ⇒ 数学上必然把参数推到网格边界。
**这正是 H-023 连挂 5 轮的病根** —— 我们每轮的处置是「人工看表 → 再加一档」，
加 4 次还是端点。说明问题不在档位，在**判据**。
→ 正解是**约束式优化**（`pick_with_constraints`）+ **Pareto 前沿**（`pareto_front`），
由人在前沿上选，而不是由排序替你选。

### D84 · 缺键默认 0，让「没算到」和「算到 0」长得一模一样
`backtesting.py:1223`：`target_value: float = statistics.get(target_name, 0)`。
若目标名拼错、或某组参数在 `calculate_statistics` 里因零成交没产出该字段，
该组一律得 0 分 —— 排序时它既不显眼也不报错，只是**安静地排在最后**。
★ 与我们第 17 轮踩的「时区混用 → mask 全 False → 假 0 个半桶」是**同一族**：
**默认值是静默错误的最佳伪装**。→ 缺键必须 `None` + 显式丢弃，并在报告里报「丢弃几档」。

### D84b · 「多目标」在代码里存在，在行为里不存在
`run_ga_optimization` 装了 `selNSGA2`（`optimize.py:201`），看着像多目标遗传算法；
但文件开头 `creator.create("FitnessMax", base.Fitness, weights=(1.0,))`（第 28-29 行）
只有**一个**权重 ⇒ NSGA2 退化成普通单目标选择。
→ 判「是不是多目标」不能看**用了哪个算子**，要看**适应度向量的长度**。

### D85 · 结果表只展示目标列 = 强制单指标决策
`evaluate` 老老实实返回了 `(setting, target, statistics)` 三元组，`statistics` 里 40+ 项俱在；
`OptimizationResultMonitor` 只渲染 2 列（参数 + 目标值），其余**全部丢弃**。
用户于是只能在「看不到回撤/胜率/笔数」的表上挑参数。
★ 这是我们 D65 / D66 的同族：**单笔均值是幸存者偏差放大器**，而「只显示单笔均值」
比「不显示」更危险。→ 我们 `core/report.py` 的毛净并列区已反超（第 17 轮补了 `n_trades`），
但**优化结果表**这一层还没有对应物 —— 记 P1。

### D86 · 优化结果无 run_id、不落盘 ⇒ 结论不可追溯
全仓库 `grep to_csv` 在 `widget.py` 只有一处，是用户点「保存」时的**手动导表**（`save_csv:1165`），
`engine.py` 里没有任何持久化。⇒ 关窗即失，且即使保存也**不知道是哪个代码版本 / 哪段数据**跑出来的。
★ 我们更糟：有落盘但**按日单文件、同一天第二次跑整文件覆盖**（第 17 轮 P1-4）。
**「有落盘」不等于「可追溯」** —— 本轮已改为 append + run_id（见 §5）。

### D87 · 用「线程对象非空」做互斥，异常路径必须 `finally` 释放
`run_backtesting`(146) 和 `run_downloading`(389) 都有 `try/except`；
**`run_optimization`(274) 一行 try 都没有**，而 `self.thread = None` 写在成功路径末尾（338）。
⇒ 只要优化抛异常（参数名不在策略里 / 数据为空 / 多进程 pickle 失败 / `tqdm` 断掉），
`self.thread` **永久非空**，之后所有回测/优化都被「已有任务在运行中，请等待完成」挡死，
**只能重启进程**。
★ 而 `test_start_backtesting_rejects_when_busy`(344) 恰恰把这个互斥**当成契约**测了 ——
契约有了，**释放路径没被覆盖**。→ 互斥锁必须 `try: … finally: self.thread = None`，
并且补一个「异常后能再次启动」的用例。

### D88 · 两种失败共用一个返回值 = 调用方无法区分
`run_backtesting` 的两条失败路径（空数据 191-195、异常 197-204）都只写日志然后 `return`，
`result_df` / `result_statistics` 都停在 `None`。
官方测试 `test_run_backtesting_without_bars_skips_statistics`(284) 把「两个都是 None」**断言下来了** ——
所以这不是 bug，是**设计**：返回值没有区分度。
★ 后果：UI 只能显示「没结果」，人分不清是「数据缺失」还是「策略炸了」，
而这在夜里无人值守时是致命的（我们夜学就是无人值守）。
→ 失败必须返回**带原因的结构体**（`{"ok": False, "reason": "no_data" | "exception", ...}`），
不许用 `None` 兼表两种意思。

### D89 · 测试必须先断掉「隐式全局路径」
`tests/conftest.py`（29 行）做三件很小但很关键的事：
1. 在**第一次 import vnpy 之前** `os.chdir()` 到临时目录，并在里面建空的 `.vntrader`
   （`vnpy.trader.utility` 导入时按 CWD 决定配置/数据落点）；
2. `SETTINGS["log.file"] = False` 且**必须在 `vnpy.trader.logger` 被导入之前**设
   （logger 在 import 时就按 `log.file` 建目录）；
3. `pytest_unconfigure` 里 `os.chdir(ORIGINAL_CWD)` 收尾还原。
★ 为什么能迁移到我们头上：`quant_app/core/*.py` 有一堆**模块级路径常量**
（`REPORT_DIR` / `OBSIDIAN` / `DATA_15M`）。任何测试若不先把它们 monkeypatch 掉，
就会**往真实报表目录写假数据** —— 这比测试不通过更糟。
→ 我们做 `quant_app` 测试的第一件事，是 `conftest` 里把这几个常量全部重定向到 tmp。

### D90 · 校验做了却被丢弃返回值 = 没做校验
`optimize.py:58-62` **确实**校验了非法网格：
```python
if start >= end:  return False, _("参数优化起始点必须小于终止点")
if step  <= 0:    return False, _("参数优化步进必须大于0")
```
但 `widget.py:1085-1092` 的调用方：
```python
if start_value == end_value:
    self.optimization_setting.add_parameter(name, start_value)          # 返回值丢弃
else:
    self.optimization_setting.add_parameter(name, start_value, end_value, step_value)  # 返回值丢弃
```
**两个返回值都被丢掉**（`add_parameter` 返回的 `(bool, str)` 里第二个正是
`"范围参数添加成功，数量{}"` —— **档数本来是要告诉用户的，被扔了**）。
⇒ 用户把「结束」填得比「开始」小、或步进填 0，点「优化」后**什么都没发生、也没有报错**，
只能靠猜。同理 `(end-start)` 不被 step 整除时（D82）也是**静默少一档**。

★ 另外 `type_(d["start"].text())`（widget.py:1084）对空字符串抛 `ValueError`，
在 PyQt 槽函数里**只打 traceback、界面不动** —— 又一种「静默失败」。
→ 结论：**校验函数的存在 ≠ 校验生效**。凡返回 `(ok, msg)` 的校验，
调用方必须消费它并把 `msg` 显示出来，否则等于没写。

> ⚠️ **自我更正（本轮内）**：初稿我写成「step=0 会进 `while value <= end: value += 0` 死循环」——
> **这是错的**。只有 `end is None or step is None` 才走单值分支；`end` 一旦给出，
> `step <= 0` 一定会被那条 `return False` 拦住，**不存在死循环**。
> 真实症状是「**拒绝被吞掉**」，不是「卡死」。已按代码阅读改正，未实测（见 §8）。

---

## 5. 可复用代码片段（真实文件）

**落点**：`我的黑马策略/ai_quant_lab/20261029_vnpy_vnpy_ctabacktester/opt_grid_guard.py`
**自测**：`python opt_grid_guard.py` → **40/40 通过**
**lab_bridge**：`from core import lab_bridge; lab_bridge.get("opt_grid_guard")` → 加载成功、**零警告**

| API | 解决什么 | 对应设计点 |
|---|---|---|
| `param_grid(start, end, step, decimals=None)` | 整数索引生成 + **端点断言**；步进不整除直接抛 `GridError` 并说明端点必漏 | D82 |
| `grid_audit(levels, scores, higher_is_better, tol, flat_tol)` | 判定最优点可信度：`端点最优·单调` / `端点最优·非单调` / `内部最优·可外推` / `内部最优·平坦顶` / `样本不足`；输出 `extrapolation_allowed` | D83（判据补位） |
| `pick_with_constraints(rows, objective, constraints, maximize)` | 约束下取最优（`{"回撤": ("<=", 30)}`），全不可行时返回 `None` 而**不退回取最差** | D83 |
| `pareto_front(rows, objectives, maximize)` | 真·多目标：返回**前沿行号**，由人来选 | D84b |
| `append_run(path, payload, tag)` | 追加式落盘 + `run_id`；旧格式自动塞进 `legacy`，**绝不丢历史** | D86 |
| `make_run_id(tag)` | `YYYYMMDD_HHMMSS_<6位hash>`，同秒重复跑不撞 | D86 |

```python
# 来源：我写的 ai_quant_lab/20261029_vnpy_vnpy_ctabacktester/opt_grid_guard.py:param_grid
# 用途：含端点的等距网格（vnpy/trader/optimize.py:64-71 的正确版）
def param_grid(start, end, step, decimals=None):
    if step <= 0:
        raise GridError(f"步进必须 > 0，收到 {step!r}")
    if start > end:
        raise GridError(f"起始点必须 <= 终止点，收到 {start!r} > {end!r}")
    span = end - start
    n_raw = span / step
    n = int(round(n_raw))
    if abs(n_raw - n) > 1e-6:            # 不整除 → 端点必漏，宁可报错不许静默
        raise GridError(f"步进 {step!r} 不能整除跨度 {span!r} → 端点 {end!r} 必被漏掉")
    decimals = _decimals_of(step) if decimals is None else decimals
    levels = [round(start + i * step, decimals) for i in range(n + 1)]
    if not math.isclose(levels[-1], end, rel_tol=0, abs_tol=1e-9):
        raise GridError(f"网格末点 {levels[-1]!r} != end {end!r}（端点丢失）")
    return levels
```

```python
# 来源：同上，grid_audit 的「诚实」版内点判据
# 用途：判断「内部最优」是真峰还是平坦顶 —— H-023 的守门器
neigh = [sc[j] for j in (best_i - 1, best_i + 1) if 0 <= j < n]
runner_up = max(neigh) if higher_is_better else min(neigh)
drop = (sign * (sc[best_i] - runner_up)) / (abs(sc[best_i]) or 1.0)
# ★ 判据必须是「峰比次优高多少」，不能是「两侧邻档是否更差」——
#   内点定义上两侧必然更差，那条判据恒真、等于没判（「断言永远为绿」的另一种形态）。
verdict = VERDICT_INNER if drop > flat_tol else VERDICT_INNER_PRESSURED
```

**自测里三处 A/B 反测（这是关键，不是装饰）**：
1. 同一组档位 `[10,20,30,40]`，分数 `[1,2,3,4]` → 判「端点」；改成 `[1,3,2,0.5]` → 必须翻成「内部」。断言 `a["verdict"] != b["verdict"]`。
2. 峰/次优只差 1%（`4.95 vs 5.0`）→ 判「平坦顶」；把次优改成 `4.0`（差 20%）→ 必须翻成「真峰」。断言两者不同。
3. `scores=[1.0, None, 3.0, 4.0]` 与 `scores=[1.0, 0.0, 3.0, 4.0]` 必须产生**不同的单调性结论** ——
   这条直接证明「把 None 当 0」会被检测到（vnpy 的 `statistics.get(k, 0)` 正是这个坑）。
4. 落盘：同一文件连写两次 → `n_runs==2`、`run_id` 不同、**第一次的 payload 仍在**（覆盖式写入会被这条打死）。

---

## 6. B 站学习（本日 30% 权重）

- **本轮产出：0。**
- 状态：**永久降级**（第 10 轮结案，第 17/18 轮确认）。字幕接口连续空返回、API 返回 HTTP 412 风控，
  且本机无 audio 转录通道（零成本底线不允许上 ASR 付费 API）。
- 替代源（本轮实际用的）：`vnpy_ctabacktester` **自带 `tests/test_engine.py` 569 行 / 11 个用例** ——
  官方测试是比口播视频**更硬**的「设计意图说明书」：它把「空数据时两个结果都是 None」
  「忙碌时必须拒绝」这类**契约**断言下来了。
- 存疑处：无（本轮所有结论均可在源码行号上核验）。

---

## 7. 对黑马策略的启发（已落到具体动作）

### 7.1 已跑完的两条假设

#### H-037 · 宽档位 × bar 内触发 的交互 → **已证伪**
「`40/32/20` 相对 `10/8/5` 的净单笔增益，在 `intrabar` 口径下还能留存多少？」

| 标的 | 净单笔 基线·close | 基线·intrabar | 宽档·close | 宽档·intrabar | gain_close | gain_intrabar | **留存率** |
|---|---|---|---|---|---|---|---|
| BTC | 1.7020 | 1.7986 | 18.9078 | 11.5054 | +17.2058 | +9.7068 | **56.42%** |
| ETH | 1.6910 | 1.3333 | 10.0900 | 9.1329 | +8.3990 | +7.7996 | **92.86%** |
| BNB | 1.8864 | 1.6132 | 14.3717 | 12.2748 | +12.4853 | +10.6616 | **85.39%** |
| DOGE | 0.2587 | −0.1754 | 7.1567 | 5.6002 | +6.8980 | +5.7756 | **83.73%** |

- **判定**：缩水 ≥30% 只有 **1/4**（BTC 56.42%），阈值 ≥3 未达 ⇒ **已证伪**。
- **含义**：**放宽档位的收益，不是「收盘确认」这个乐观口径喂出来的** ——
  H-023 的「放宽有效」在 intrabar 口径下**仍成立**（3/4 留存 ≥80%）。
- **★ 但 BTC 是例外**：留存 56.42%，即 BTC 的 17.21pp 宽档增益里有 **7.50pp 靠「收盘才确认离场」**。
  这与 H-035 的方向一致（intrabar 更早离场 → 更差），并在 BTC 上被放大。
- **★★ 必须挂上的限流阀（本轮最重要的自我约束）**：宽档把**样本压得极薄** ——
  笔数 `[157→36]`(BTC) / `[249→75]`(ETH) / `[232→58]`(BNB) / `[509→160]`(DOGE)。
  **BTC 宽档只有 36 笔**，18.91% 的净单笔极可能是少数极端交易的产物（D65：单笔均值是幸存者偏差放大器）。
  ⇒ H-037 的「已证伪」判定**可信**（它比较的是同一批参数下的两种口径，偏差同向），
  但**不能**由此推出「宽档对 BTC 好」。
- **★★ 交叉反证（必须记下来，别自我美化）**：全样本下 **DOGE 宽档 + close = 总收益 +508.9%**
  （基线 −86.6%），宽档 + intrabar 也是 **+153.8%**。
  而第 17 轮 H-023 的**样本外**结论是「DOGE 不许放宽（−1.05）」。
  ⇒ **同一参数在全样本与后 30% 样本外方向相反** ⇒ DOGE 的改善是**时段依赖**的，
  两边的数字都真，只是回答不同问题。**许不许放宽 DOGE，取决于你敢不敢假设「未来像前 70%」** ——
  这是个**判断**，不是回测能回答的。台账里 H-023 与 H-037 必须并列读。

#### H-038 · DOGE 的「净单笔为正、总收益 −86.61%」是波动拖累吗 → **已验证**

| 指标 | 值 |
|---|---|
| 笔数 | 509 |
| 算术均值 A（未乘仓位） | **+0.2587%** |
| 算术均值 A(pos)（×95% 仓位） | **+0.2457%** |
| 几何均值 G（由权益曲线反推） | **−0.3943%** |
| 波动率 σ / σ(pos) | 13.0891% / 12.4346% |
| 实测拖累 A(pos) − G | **0.6400pp/笔** |
| 理论拖累 A(pos) − σ(pos)²/200 | **−0.5274%**（与 G 差 **0.1331pp**） |
| 实际总收益 / 复利重构 | **−86.61%** / **−86.61%（偏差 −0.00pp，路径已反解）** |
| 剔除最长持仓 top-1%（5 笔）后近似总收益 | **−94.40%（更差）** |

- **判定**：A(pos) > 0 而 G < 0，理论拖累与 G 同号且同阶（差 0.13pp）⇒ **已验证，波动拖累成立**。
- **含义（重要，改写对 DOGE 的表述）**：DOGE 的正确表述**不是**「信号无效」，
  而是「**信号有正期望，但单笔波动 σ≈13% 吃掉了全部复利**」。
  处置方式因此不同：不是删标的，而是**降仓位或做波动率目标**。
- **★★ 反直觉副产物**：剔除「持仓最长 top-1%」之后**更差**（−86.61% → −94.40%）
  ⇒ **长持仓是 DOGE 的盈利来源，不是亏损来源**。
  这同时否掉了一个很容易被采纳的「加最长持仓上限」的想法。
- **★★ 单位坑（本轮自造假数字，已修）**：首跑把公式写成 `A − 0.5·σ²`（A、σ 都用百分点），
  得出「理论拖累 −85.40%」，而真实 G 是 −0.3943% —— **差 200 倍**。
  正确写法 `A − σ²/200`（等价 `(σ/100)²/2×100`）。
  ★ 这个假数字**差一点就写进台账**。教训是第 13 轮那条的翻版：
  **凡「结果比预期夸张一个量级」，先怀疑单位，再怀疑结论。**

### 7.2 本轮落到平台上的真改动

| 改动 | 文件 | 证据 |
|---|---|---|
| `write_results` 改**追加式 + run_id**（P1-4 结清） | `ai_quant_lab/hypothesis_runner.py:3502` | 实测同一天连跑两次：`runs` 长度 2、`run_id` 不同（`20261029_041013_097689` / `20261029_041204_509739`）、**第一次的 payload 仍在**；顶层保留 `verdicts` 键 → `strategy_to_binance_ai.load_verdict()` 无需改动 |
| 新增 `opt_grid_guard.py` | `ai_quant_lab/20261029_vnpy_vnpy_ctabacktester/` | **40/40** · lab_bridge 零警告 |
| H-037 / H-038 注册进 REGISTRY 并跑通 | `ai_quant_lab/hypothesis_runner.py` | 台账两行状态已回写（已证伪 / 已验证） |

### 7.3 下一步动作（按 ROI 排）

1. **P0** · `opt_grid_guard.grid_audit` 必须**挂进 H-023 的判定里** —— 现在它还是「独立模块」，
   没接进假设回测链。接法：`verify_H023` 跑完 8 档后调用 `grid_audit(档位, 净单笔)`，
   把 `verdict` 和 `extrapolation_allowed` 直接写进 `Verdict.metrics`，让「又落端点了」变成**机器判**而不是人看表。
2. **P0** · **宽档的样本数下限**：H-037 暴露 BTC 宽档只剩 **36 笔**。
   给所有 A/B 加 `min_trades` 闸（建议 ≥100），不足即标「样本不足」而不是给结论。
3. **P0** · **实盘 4543 笔 vs 回测 129 笔（差 35 倍，挂账第 2 轮）** —— 仍未解决，
   必须先导出实盘逐笔才能判「标的池/周期不一致」。这是全台账最贵的一个未解项。
4. **P1** · DOGE 的「降仓位 / 波动率目标」假设（H-038 的直接后续）：
   `position_pct 0.95 → 0.30/0.20/0.10` 扫一遍，看 A(pos) 是否仍 > 0 而 G 是否转正。
   ★ 这条是**唯一由本轮结论直接推出的可交易改进**。
5. **P1** · `core/report.py` 的**优化结果表**（对应 D85）：目前只有单次回测报告，
   没有「多参数组对比表」。要补 `n_trades / 总收益 / 最大回撤` 三列强制并列。
6. **P2** · `core/backtest.py` 风控喂数的 `try/except: pass`（第 17 轮 P1-6）仍挂着。

---

## 8. 未完成 / 失败区（诚实留痕）

- **AtomCode 连续第 8 轮不通**（10-21/22/23/24/26/27/28/29）：
  `proxy_down` → 后台拉起 → `/health` 200 + `logged_in=true` + 3 个免费模型，
  但最小推理 **240s 超时 HTTP=0**。⇒ 上游推理层挂死（非额度、非二进制）。
  按收敛纪律降级本地 Read/Grep，**0 积分**，本轮未在它上面再耗时间。
- **B 站（30% 权重）实质产出 0** —— 永久降级，不再自我安慰（见 §6）。
- **副仓库未读**：本轮只做主仓库 + 交叉读 `vnpy/trader/optimize.py`（276）与
  `backtesting.py:1184-1235`，没有独立副仓库。
- **D90 的死循环分支未实测**：初稿误称 `step=0` 会死循环，复核源码后**已改正为「拒绝被吞掉」**
  （见 D90 的自我更正框）。改正来自代码阅读，**未写复现代码实测**，故标为「阅读结论、非实测」。
- **本轮自己踩的第 3 个「数出来的假数字」**：跑平台回归时用「递归数 dict 里的布尔值」当通过数，
  得到 `risk 44/48`、`fill_realism 11/14` 两个 FAIL；实际这四个模块**各自返回了权威字段**
  （`_pass/_checks/_all_ok` 或 `passed/all_ok`），我数到的 44/48 里混进了 `'allowed': False`
  这种**业务结果**（R4 单笔名义本来就该被拒）。
  ⇒ 正确口径：**自测自己报的 `_all_ok` 才算数**，不许外部重新数。
  这与 D84 是同一个坑的两端：**默认值/计数口径会让你把「绿」看成「红」，也会把「红」看成「绿」**。
- **H-037 的样本量问题未解决**：宽档把 BTC 压到 36 笔，`min_trades` 闸还没加（见 §7.3 P0-2）。
- **H-038 只解释了机制，没给解药**：降仓位能否救 DOGE 属**下一条假设**（§7.3 P1-4），本轮未跑。
- **实盘 4543 vs 回测 129（差 35 倍）**：挂账第 2 轮，未动。
- **`grid_audit` 尚未接进 `verify_H023`**：模块独立可用，但判定链还没接线（§7.3 P0-1）。

---

## 9. 三件套自检

- [x] **① 拆解笔记已落盘**
      `E:\龙虾AI主控中心\我的AI分身\Obsidian知识库\AI量化平台\学习笔记\20261029_vnpy_vnpy_ctabacktester.md`
- [x] **② 可复用代码已落盘（真实路径 + 自测 + lab_bridge 加载）**
      `我的黑马策略\ai_quant_lab\20261029_vnpy_vnpy_ctabacktester\opt_grid_guard.py` → **40/40**
      `from core import lab_bridge; lab_bridge.get("opt_grid_guard")` → 加载成功，零警告
- [x] **③ 策略假设已追加进台账（读回确认）**
      `策略假设台账.md` → H-037（**已证伪**）· H-038（**已验证**），两行均 12 段（10 列）校验通过，
      CRLF 保持 272 组、无裸 CR
- [x] **④ 前日悬空假设已结**：H-037/H-038 当日登记当日结清；H-035/H-036 上轮已结
- [x] **⑤ README 索引已挂**（页面不能是孤岛，且脚本断言了被链接的笔记文件真实存在 32611 B）
- [x] **⑥ 平台回归全绿（改完 `hypothesis_runner` 后确认零退化）**

| 模块 | 通过 | 状态 |
|---|---|---|
| `risk.demo_selftest` | **24/24** | OK |
| `events.demo_selftest` | 3/3 | OK |
| `live.selftest_router` | 8/8 | OK |
| `order_lifecycle.selftest_lifecycle` | 10/10 | OK |
| `backtest.selftest_fill_realism` | 10/10 | OK |
| `backtest.selftest_slip_lot_wiring` | 14/14 | OK |
| `backtest.selftest_participation_wiring` | 7/7 | OK |
| `backtest.selftest_risk_wiring` | 10/10 | OK |
| `lab_bridge.get("opt_grid_guard")` | **40/40** | OK |

合计 **9 项，失败 0 项**。

---

## 10. 成本与技能

- **本次花费积分**：**0**。本地 Read/Grep + `quant_env` 本地回测，无任何外部 API 调用。
- **用时**：guard 约 4 分钟（含 240s 超时等待）· 精读与实现约 35 分钟 · 回测 1 分 27 秒。
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程，v1.1.15）。
- **沉淀 / 迭代**：
  - 新增模块 `opt_grid_guard.py`（40/40）
  - `hypothesis_runner.write_results` 追加式改造（P1-4 结清）
  - 新增 D82~D90 九条设计点
  - 技能 `ai-quant-open-source-nightly-learning` **v1.1.15 → v1.1.16**（§3.18）
- **归位节奏**：今日**周四（周中）** → 仅 Obsidian + 工作区 `.workbuddy\memory\2026-10-29.md`。
  ⚠️ 六端归档仍欠 **2026-10-18 / 10-25** 两轮顺延，下个周日（**2026-11-01**）一并补。
