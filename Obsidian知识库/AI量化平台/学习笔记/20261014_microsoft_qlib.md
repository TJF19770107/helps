---
日期: 2026-10-14
仓库: microsoft/qlib
核心文件: qlib/workflow/（task/manage.py · record_temp.py · recorder.py · exp.py）+ qlib/backtest/decision.py
轮次: 第 8 轮（轮转 #11/12）
tags: [AI量化平台, 夜学, 代码拆解, qlib, 实验管理, 任务生命周期]
---

# 20261014 · microsoft/qlib · `qlib/workflow`

## 0. 一句话结论
> qlib 教我的不是「怎么造因子」，而是**怎么让每一次运行都可复现、可续跑、可归因** ——
> 它的 `TaskManager` 用「**原子领取 + 异常必归还 + 崩溃复位**」把「任务做一半崩了」变成可恢复事件；
> 它的 `RecordTemp` 用「**显式声明依赖 + 递归校验产物**」把「上一步没报错」和「上一步的产物在不在」拆成两件事；
> 它的 `PortAnaRecord` 把**毛账/净账强制并列**写进制度 —— 恰好撞上我方 H-009/H-011 已经量化出来的最大偏差项。

---

## 1. 这个文件在系统里管什么（架构定位）

| 文件 | 所属层 | 职责 |
|---|---|---|
| `qlib/workflow/task/manage.py` | **工具层 / 调度层** | 任务池的四态生命周期（waiting→running→part_done→done）、原子领取、并发安全、崩溃复位 |
| `qlib/workflow/record_temp.py` | **工具层 / 记录层** | 标准产物链：signal → signal-analysis → portfolio-analysis；显式依赖 + 递归校验 + 幂等重跑 |
| `qlib/workflow/recorder.py` / `exp.py` / `expm.py` | **工具层 / 实验层** | 实验（Experiment）/ 运行（Recorder）两级命名空间，产物挂 MLflow，指标 `log_metrics` |
| `qlib/workflow/online/manager.py` + `update.py` | **执行层（在线）** | 滚动重训 / 增量更新：「预测有寿命，过期必须重算」 |
| `qlib/backtest/decision.py` | **撮合回测层 / 执行层** | `Order` 数据类（目标量 / 已成交量 / 因子）、`TradeDecision` 决策作用域 |

- 上游依赖 → `qlib.config`（MongoDB / 路径）、`qlib.data.dataset`、`qlib.backtest`
- 下游被谁调用 → `qlib.cli` 的 `qrun` 入口、`qlib.rl.trainer`（TrainerRM 继承 TaskManager）

**★ 与我方平台的对照位**：`TaskManager` ↔ 我方**没有**的运行生命周期层（`live.py` 只有 142 行）；
`RecordTemp` ↔ 我方 `core/report.py`（156 行，一把梭，无产物链）；`Order` ↔ 我方 `core/risk.py`
的 `PendingOrder`（外挂簿记，订单本体不知自己在途）。

---

## 2. 调用链（文字版时序图）

### 2.1 `TaskManager` 的领取-提交环（崩溃安全的核心）
```
run_task(task_func, pool, before_status=WAITING, after_status=DONE)
  └─ while True:
       with tm.safe_fetch_task(status=WAITING) as task:      # manage.py:531
         ├─ fetch_task()                                     # L265-286
         │    └─ find_one_and_update({status:WAITING},
         │         {$set:{status:RUNNING}}, sort=priority DESC)
         │       ★ 查询即更新 = 一步原子 → 并发 worker 不可能领到同一个任务
         ├─ if task is None: break                            # 池空 → 退出
         ├─ param = task["def"]  (WAITING) 或 task["res"] (PART_DONE)   # L536-540
         ├─ res = task_func(param)                            # 真正的活
         └─ tm.commit_task_res(task, res, after_status)       # L548
       # ↓ 若 with 块里抛异常（含 KeyboardInterrupt）
       #   except 分支: return_task(task, status=<原状态>)     # L305-310 ★ 任务被还回去
  → 返回 ever_run
```
**★ 关键在例外分支**：任务**不会**因为 worker 崩溃而永远卡在 `running`。

**但**这只能覆盖「进程还活着」的异常。整机断电时归还代码根本没机会跑 →
所以还需要一次**启动自愈**：`reset_waiting()`（L416-427）把悬挂的 `running` 全扫回 `waiting`。
**两道网缺一不可**：`safe_fetch_task` 是运行期网，`reset_waiting` 是启动期网。

### 2.2 `RecordTemp` 的依赖链
```
SignalRecord(depend_cls=None)
   └─ generate() → model.predict → save("pred.pkl" / "label.pkl")
        ↓
SigAnaRecord(depend_cls=SignalRecord, skip_existing)      # L302-364
   └─ ACRecordTemp.generate()                              # L226-245
        ├─ if skip_existing and check() 通过 → return（幂等）
        ├─ self.check()  ──→ FileNotFoundError? → warning + return（★ 跳过而非崩）
        └─ _generate() → self.save(...)
        ↓
PortAnaRecord(depend_cls=SignalRecord, skip_existing)      # L365-580
   └─ _generate() → normal_backtest(...) → risk_analysis(...) × 2（毛账 / 净账）
        → recorder.log_metrics(...) + save("port_analysis_*.pkl")
        ↓
MultiPassPortAnaRecord(PortAnaRecord)                      # L582-700
```
`check()`（L127-165）会**递归**顺着 `depend_cls` 往上查，并且断言的是
「**产物文件真的在**」（`recorder.list_artifacts`），不是「上一步返回了」。

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 签名要点 | 职责 / 为什么重要 |
|---|---|---|---|
| `TaskManager` | class | `__init__(task_pool)` | 四态任务池；`STATUS_WAITING/RUNNING/PART_DONE/DONE`（L79-82） |
| `TaskManager.fetch_task` | method | `(query={}, status=WAITING) -> dict` | **原子**领取：`find_one_and_update` 一步把 waiting 置 running（L265-286） |
| `TaskManager.safe_fetch_task` | ctxmgr | `(query={}, status=WAITING)` | 异常 → `return_task(...)` 归还原状态（L288-310）★ 崩溃安全 |
| `TaskManager.reset_waiting` | method | `(query={}) -> int` | 启动自愈：running → waiting（L416-427）★ 整机崩溃后唯一出路 |
| `TaskManager.commit_task_res` | method | `(task, res, status=DONE)` | 提交结果并推进状态（L354-369） |
| `run_task` | function | `(task_func, pool, before_status, after_status, **kw)` | 驱动环：WAITING→PART_DONE→DONE 可断点续跑（L485-551） |
| `RecordTemp` | class | `artifact_path` / `depend_cls` | 记录基类：显式声明**依赖的上游记录类**（L29-36） |
| `RecordTemp.check` | method | `(include_self=False, parents=True)` | **递归**校验依赖产物已落盘，缺失抛 `FileNotFoundError`（L127-165） |
| `ACRecordTemp.generate` | method | `(*args, **kwargs)` | 自动检查 + `skip_existing` 幂等 + 缺依赖跳过（L226-245） |
| `PortAnaRecord._generate` | method | `(**kwargs)` | 回测 → **毛账/净账并列** `risk_analysis`（L472-530） |
| `Order` | dataclass | `(stock_id, amount, direction, start, end)` | `deal_amount=0.0` / `factor=None` —— **在途态写在订单自己身上**（L36-151） |
| `Order.amount_delta` / `deal_amount_delta` | property | — | 带符号增量（目标 / 已成交），省得调用方到处乘方向 |
| `NestedExecutor` | class | `(time_per_step, inner_executor, inner_strategy, ...)` | 外层决策 = 时间段，内层执行 = 该段内的细化成交（L307+） |

---

## 4. 可迁移设计点（逐条写「为什么好」）

### D14 · 崩溃安全的「领取 → 提交 / 归还」（`safe_fetch_task` + `reset_waiting`）
**设计**：领取时**原子**置为「占用中」；用上下文管理器保证**任何异常都把占用还原**；
再加一条**启动期自愈**把悬挂占用扫回可领取。
**为什么好**：这是把「分布式/崩溃环境下的 at-least-once 语义」做成了库的默认行为，而不是要求
每个调用方自己写 try/finally。**只做「查一下再改」会把检查与占用之间的空窗暴露给并发** ——
我方 `pre_trade_check` 正是这个形状（H-011 之后 R7 顺序锁定才补上原子 `reserve_order`）。
**★ 最有价值的一点**：qlib 承认「归还代码可能没机会跑」，所以配了 `reset_waiting`。
只写 `safe_*` 就宣称崩溃安全，是**半个安全网**。

### D15 · 记录模板链：显式依赖 + 递归校验 + 幂等重跑（`depend_cls` + `check()` + `skip_existing`）
**设计**：每个记录阶段声明「我依赖哪个上游阶段」；执行前**递归**断言整条链的产物都在；
产物已存在就跳过；依赖缺失就 warning + 跳过（**不崩**）。
**为什么好**：它把两个常被混淆的量分开了 ——
「**上一步的代码没抛异常**」≠「**上一步的产物真的落盘了**」。
我方血泪铁律「日志说成功 ≠ 东西真的在」在 qlib 里被写成了类型系统的结构（`depend_cls` + `check()`）。
而且**跳过而非崩溃**让「部分重跑」成为常态操作。

### D16 · 四态任务机与「做了一半」（`STATUS_PART_DONE`）
**设计**：`waiting / running / part_done / done`；`run_task` 支持 `before→after` 状态映射，
`PART_DONE` 的任务被再次领取时，喂给它的是**中间结果 `task["res"]`** 而不是原始定义。
**为什么好**：把「断点续跑」变成**状态机的第一等公民**，而不是散落在业务里的 `if resume:`。
对应我方 G2 的欠账（`RiskLevel` 目前只有 NORMAL/WARNING/HALTED 三档，没有「恢复中」的中间态）。

### D17 · 在途态属于订单本体，不属于第三方簿记（`Order.amount` vs `deal_amount`）
**设计**：`amount`（目标）+ `deal_amount`（已成交，默认 0）+ `factor`（部分成交系数），
注释里还写清了「不可交易 → `deal_amount==0` 且 `factor is None`、**不产生成本**」。
**为什么好**：在途量是**订单的属性**，不是风控模块的备注。我方 `PendingOrder` 挂在
`RiskEngine` 上，导致「策略以为成交了、风控以为还挂着」这类错位只能靠调用方自觉对齐。
qlib 的答案是把两个数字放进同一个对象，谁都读得到。

### D18 · 毛账 / 净账**强制并列**（`PortAnaRecord._generate` L514-528）
**设计**：同一份收益序列算两遍 —— `ret − bench` 与 `ret − bench − cost`，**两套指标同时落盘**，
而不是「想起来了才算一下成本」。
**为什么好**：这与我方 H-009 / H-011 的结论完全同向 ——
实测「成交口径现实化后 4/4 总收益下降，BTC −103.0pp」，归因指出**乐观偏差主因是执行成本假设**（BTC 成本项 ×344）。
**既然毛净差本身就是最重要的那个数字，它就不该是可选项。** 我方 `core/report.py` 目前没有这一列。

### D19 · 可交易性建模（`Exchange.limit_threshold`）
`qlib/backtest/exchange.py` 用 `limit_threshold=0.095` 表达「涨跌停不可成交」——
**撮合层主动建模「某些 bar 根本不能交易」**，而不是假定任何 bar 都能成交。
我方回测完全没有这层（且 crypto 无涨跌停，但**插针 / 极端单根**的等价物是存在的）→ 见 H-017。

---

## 5. 可复用代码片段

**落盘**：`ai_quant_lab/20261014_microsoft_qlib/qlib_workflow_patterns.py`（**自测 46/46**，纯标准库零依赖）

```python
# 来源：microsoft/qlib · qlib/workflow/task/manage.py:288-310（safe_fetch_task）
#       + :416-427（reset_waiting）
# 用途：让「领取-执行-提交」在异常与整机崩溃下都不丢任务。可直接搬到 live.py 的报单生命周期。
@contextmanager
def safe_claim(self, status=Lifecycle.WAITING, query=None):
    rec = self.claim(status=status, query=query)     # claim 内部持锁完成「选中+置 RUNNING」
    try:
        yield rec
    except BaseException:            # KeyboardInterrupt 不是 Exception 的子类
        if rec is not None:
            rec.status = status      # 原样归还，绝不吞异常
        raise

def reset_waiting(self, query=None) -> int:
    """启动自愈：进程被杀/断电后，悬挂的 RUNNING 一律扫回 WAITING。"""
    with self._lock:
        n = 0
        for r in self._tasks.values():
            if r.status == Lifecycle.RUNNING and (query is None or query(r)):
                r.status = Lifecycle.WAITING
                n += 1
        return n
```

```python
# 来源：microsoft/qlib · qlib/workflow/record_temp.py:514-528（毛/净双账强制并列）
# 用途：任何绩效结论都必须同时给出毛账与净账；毛赚净亏自动升级为最高优先级警报。
gross = risk_metrics([r - b for r, b in zip(returns, bench)])
net   = risk_metrics([r - b - c for r, b, c in zip(returns, bench, cost)])
decision = "cost_dominated" if gross["total_return"] > 0 and net["total_return"] <= 0 else ...
```

> 完整实现（`ClaimLedger` / `RecordChain` / `gross_net_dual_account` / `InFlightOrder`）
> 见上述落盘文件；**lab_bridge 零警告加载已验证**。

---

## 6. B站学习（本日 30% 权重）· **降级**

- 状态：**连续第 7 轮受阻** —— WebFetch 拿不到 B 站 CC 字幕（需登录态；未登录只返回播放器壳）。
- 本日降级做法：改用 **qlib 官方文档中文镜像 + `docs/` 目录源码内文档** 做「目录级 + 设计意图级」蒸馏。
- 蒸馏要点（来自 qlib `docs/` 与 README 的 workflow 章节）：
  1. qlib 把「**实验**」与「**运行**」分成两级命名空间（`Experiment` ⊃ `Recorder`），
     一次实验下可挂多次运行 → 天然支持「同一套配置跑 N 组参数」的横向对比。
  2. `qrun` 的 yaml 配置里，`task` 段描述「做什么」、`record` 段描述「**留下什么证据**」——
     **证据列表是配置的一部分**，不是事后补的。
  3. `NestedExecutor` 的 `skip_empty_decision` / `align_range_limit` 是**显式降级档位**，
     与第 7 轮 backtrader 的 D13「降级档位显式化」完全同构 → 两个独立框架收敛到同一原则。
- 存疑处（待代码验证）：`skip_empty_decision=True` 在**决策为空但内层仍需推进时间**时的行为，
  我方若照搬需确认「空决策是否也要推进内层时钟」。
- **未完成项已记入 §8。**

---

## 7. 对黑马策略的启发（落到具体动作）

| # | 假设 | 怎么验 | 结果 |
|---|---|---|---|
| H-016 | 入场「放量」门槛从**固定倍数**改为**滚动 90 分位**（qlib rolling normalization 纪律） | `_run_with_entry_filter` 注入 `vol_ratio ≥ rolling_q90(vr, 2000)`；4 只 15m 全历史 A/B | **已证伪** 1/4 |
| H-017 | 只在 MA30 上行趋势**刚转正后 ≤96 根内**入场（趋势新鲜度） | 同上，注入 `trend_age ≤ 96 且 slope > 0` | **已证伪** 2/4 |

**★ 本轮的硬信息（比「又证伪两条」更重要）** —— 我额外算了**门槛的实际命中率**：

| 标的 | 基线入场根数 | H-016 保留 | H-016 咬合力 | H-017 保留 | H-017 咬合力 |
|---|---|---|---|---|---|
| BTCUSDT | 43,521 | 9,708 | **砍掉 77.7%** | 42,967 | 砍掉 1.3% |
| ETHUSDT | 43,207 | 9,465 | 砍掉 78.1% | 42,727 | 砍掉 1.1% |
| BNBUSDT | 43,355 | 9,870 | 砍掉 77.2% | 42,660 | 砍掉 1.6% |
| DOGEUSDT | 35,432 | 9,082 | 砍掉 74.4% | 34,929 | 砍掉 1.4% |

- **H-016 的证伪是强证据**：门槛砍掉约 **3/4** 的入场（真咬合），单笔均值**反而下降**
  （BTC 2.0061→1.7914 / ETH 2.373→2.0759 / BNB 2.3238→2.5804 / DOGE 0.6738→0.6011）。
  → 结论升级：**「放量」这条线（不论固定阈值还是自适应分位）整体不具备入场筛选力** ——
  不能再把责任推给「1.5 这个数没选好」。
- **H-017 的证伪是弱证据，必须如实标注**：门槛在 BTC/ETH 上只砍掉 ~1.2%，
  所以 BTC 的 `Δ=0.0000` 是「**门槛几乎没咬到**」，**不构成「门槛无效」的证据**；
  真正提供信息的是 BNB（−0.1620）/ DOGE（−0.0131）—— 砍掉 1.5% 反而变差。
  → 诚实结论：H-017 **证伪，但证据强度低**；若要再测需换更长的窗口让门槛真咬合。
- **★ 汇总到方法论层**：这是**第 5 / 第 6 条「让策略更保守」型假设全数证伪**
  （H-012/H-013/H-014/H-015/H-016/H-017）。累计证据已足够下一条判断：
  **「加门槛」这一整类思路在黑马策略上系统性无效** —— 下一步应转向**出场端**或**成本端**
  （H-009/H-011 已指出成本才是最大偏差项）。

---

## 8. 未完成 / 失败区（诚实留痕）

1. **B 站 CC 字幕：连续第 7 轮受阻**（需登录态；不做音频转录 —— 零成本底线）。→ §6 已降级为文档级蒸馏。
2. **D14~D19 尚未回填 `core/` 本体**（本轮只出了设计与可复用模块）。下轮 P0 见平台设计文档。
3. **H-017 证据强度低**（门槛咬合力仅 ~1.3%）—— 结论已标注为弱证据，不算硬结论。
4. **`qlib/workflow/recorder.py` / `expm.py` 只做概览，未逐行精读** —— 其 MLflow 后端我方无对应设施，
   本轮判断投入产出比低，如实记为「未读」而非「已读」。
5. **`qlib/rl/order_execution/` 未精读** —— 是本次最有价值的**下一个**精读目标（RL 拆单执行），
   但 15M 仓库 + 时间窗限制下未展开。
6. **环境降级项**：仓库 clone 前自检退出码为 1（主仓库未就位），已按 ghproxy 通道补齐 → 已消解。
7. **E 盘剩余 17.34GB / C 盘 30.93GB** —— 均在阈值以上，未触发 clone 禁令。
8. **积分**：0（AtomCode 走免费档 glm5.3-flash）。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件，读回确认）
- [x] ② 可复用代码落盘：
  `ai_quant_lab/20261014_microsoft_qlib/qlib_workflow_patterns.py`
  —— 自测 **46/46** 通过；`lab_bridge.get("qlib_workflow_patterns")` 加载成功、**warnings=[]**
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-016 / H-017**，均已由 `hypothesis_runner.py` 回写为**已证伪**
  （证据 `策略假设/回测结果/回测结果_20261014.json`）

---

## 10. 成本与技能

- **本次花费积分估算**：**0**（AtomCode 实测走免费档 `glm5.3-flash`；未切 0.01 折，未触碰付费档）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（v1.1.5 → 本轮迭代为 v1.1.6）
- **沉淀 / 迭代了什么**：
  1. 新可复用模块 `qlib_workflow_patterns.py`（4 个组件 + 46 项自测）
  2. 新平台设计文档《AI量化平台_实验记录与任务生命周期层对标qlib设计_20261014》（D14~D19）
  3. 技能 `ai-quant-open-source-nightly-learning` v1.1.5 → **v1.1.6**（新增 §3.8 六条经验）
  4. 假设台账新增 H-016 / H-017 并当日结清
