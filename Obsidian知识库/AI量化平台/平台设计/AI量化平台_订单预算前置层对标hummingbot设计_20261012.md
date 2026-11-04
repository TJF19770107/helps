# AI量化平台 · 订单预算前置层 · 对标 hummingbot 升级设计（2026-10-12）

> **来源**：第 6 轮夜学（主仓库 `hummingbot` #9/12）· 笔记 [[20261012_hummingbot_vnpy]]
> **定性**：这是**风控层**的第二次对外对标（第一次是 2026-10-09 对标 nautilus）。
> **核心结论**：hummingbot 给出了我方风控层 **G1（含费风险预算）与 G3（挂单占用额度）的完整答案**，
> 并额外提供了一条我方**事件层 E1** 的干净解法（双模 Clock）。**D5~D7 可直接落到 `core/risk.py` 本体。**
> **成本**：0 积分（本地精读 + AtomCode 免费档 `glm5.3-flash`）。

---

## 一、对标结论总表

| # | hummingbot 设计 | 源码位 | 直接对症的我方缺口 | 优先级 |
|---|---|---|---|---|
| **D5** | **顺序锁定**：一批订单共用一个递减余额，逐个预扣 | `pure_market_making.pyx:937-953` · `budget_checker.py:38-80` | **G3** 挂单不占持仓额度 | **P0** |
| **D6** | **手续费进抵押品**：`quote_size = size*price*(1+fee.percent)`；`OrderCandidate` 把本金/百分比费/固定费并列 | `pure_market_making.pyx:942` · `order_candidate.py:41-50` | **G1** R1 风险预算不扣双边手续费 | **P0** |
| **D7** | **闸只缩不放**：预算闸只有「缩小」与「归零」两条出路 | `budget_checker.py:82-105` | 复述我方血泪规则 #1（风险闸只约束增大敞口） | **P0**（已有，需写进注释） |
| **D8** | **双模 Clock 同 `c_tick`**：`REALTIME` 睡到 tick / `BACKTEST` 步长自增，同一接口 | `clock.pyx:88-155` · `time_iterator.pyx:9-40` | **E1** timer 寄生在事件消费线程 | **P1** |
| **D9** | **在途态是一等状态**：`_in_flight_pending_created` / `_in_flight_cancels`（60s 窗口）/ 影子单（3 分钟） | `order_tracker.pyx:25-38, 148-177` | 我方无 OMS，撤单幂等无保障 | **P2**（前置：先有实盘通道） |

---

## 二、P0 落地：把 G1 + G3 装进 `core/risk.py`

### 2.1 G1 — 含费风险预算（闭式解）

```python
# 现状（core/risk.py R1）：qty = budget / stop_dist        ← 未扣双边手续费
# 目标：把手续费也当成「一定会发生的亏损」
def risk_qty(budget: float, price: float, stop_dist: float,
             fee_rate: float, fee_sides: int = 2) -> float:
    denom = stop_dist + price * fee_rate * fee_sides
    return budget / denom if denom > 0 else 0.0
```

**验收（必须能复现 H-005 的数字）**
- `budget=100, price=60000, stop_dist=1000, fee=0.001` → 旧口径止损亏损 **108.0 > 100**（超配 **8%**）；新口径 **≤100.0**。
- 超配率闭式解 `price*fee*2/stop_dist`：止损 1000 → 12%、止损 100 → **120%**（止损越近越危险）。
- 自测断言：`loss_new <= budget + 1e-6` 且 `loss_old > budget`。

### 2.2 G3 — 挂单占用额度（顺序锁定）

```python
# 现状（core/risk.py R7 缺失）：可平量 = 净持仓
# 目标：可平量 = 净持仓 − 未成交挂单占用
def tradable_qty(net_qty: float, pending_same_dir_qty: float) -> float:
    return net_qty - abs(pending_same_dir_qty)      # 可为负 → 调用方必须拒单

# 批量申报（招标若一次发多单，必须逐个预扣）
def adjust_batch(intents, balances):
    locked = {}
    for it in intents:
        avail = balances.get(it.token, 0.0) - locked.get(it.token, 0.0)   # ★ 只读一次
        it.constrain_by(avail)                     # 只缩不放
        if it.increases_exposure:
            locked[it.token] = locked.get(it.token, 0.0) + it.collateral + it.fee  # ★ 同币种需求累加
    return intents
```

**★ 两条血泪坑（本轮自测抓到的真 bug，写进 `core/risk.py` 注释）**
1. **默认值语义**：`increases_exposure` 若默认 `False`（=减仓），普通开仓单会被**无条件放行** → 顺序锁定整体失效。
   语义默认必须与「多数订单是开仓」一致。**复现**：两单各 601.2 对着 1000 余额竟然都通过。
2. **同币种余额只能读一次**：本金与手续费常同为 USDT；写成 `avail_c + avail_f` 会把**同一个余额读两遍再相加**
   → 覆盖率翻倍（398.8 → 797.6）→ 顺序锁定失效。**正确写法**：需求侧金额相加、可用侧只读一次。
   （对标 `order_candidate.collateral_dict` 用 defaultdict **累加需求**，而 `_get_available_balances` 每币种 `balance_fn(token) − locked[token]` **只读一次**。）

### 2.3 落点与不退化要求
- 落点：`quant_app/core/risk.py`（新增 R7「挂单占用」+ 修正 R1 含费口径；R8「报单限流」见 §三）
- **硬要求**：改完重跑 `core/risk.py` 自测，**不得低于现有 9/9**；对照自测 `lab_bridge.get("order_budget_guard")` 的 21/21。
- 本模块已就绪：`ai_quant_lab/20261012_hummingbot_vnpy/order_budget_guard.py`（自测 21/21，lab_bridge 零警告加载）

---

## 三、P1 落地：D8 双模 Clock → 治 E1

**现状**：`core/events.py` 的 timer **寄生在事件消费线程**（`queue.get(timeout)`）→ 事件一忙，定时任务就迟。
**目标**：引入一个**主动驱动者**，把所有定时组件（时间止损、定时巡检、日亏熔断检查）改为**被推着走**。

```python
class Clock:
    def __init__(self, mode: str, tick_size: float):   # mode ∈ {"realtime","backtest"}
        self._mode, self._tick_size = mode, tick_size
        self._iters, self._t = [], 0.0

    async def run_til(self, until):        # 实盘：睡到下一个 tick 边界
        while True:
            now = time.time()
            if now >= until: return
            nxt = ((now // self._tick_size) + 1) * self._tick_size
            await asyncio.sleep(nxt - now)
            self._t = nxt
            for it in self._iters: it.tick(self._t)

    def backtest_til(self, until):         # 回测：固定步长，绝不等真实时间
        while self._t < until:
            self._t += self._tick_size
            for it in self._iters: it.tick(self._t)      # ★ 同一个 tick 接口
```

**验收**
- `backtest_til` 与 `run_til` 调用**同一个** `it.tick(t)`；组件只从 `self.current_timestamp` 读时间（无 `time.time()` 直读）。
- 断言：同一份事件序列下，`mode="backtest"` 与 `mode="realtime"` 的**事件顺序与语义一致**（沿用 `events.py` 现有 `same_source_ok` 自检思路）。
- 断言：人为让事件队列积压 1000 条，定时任务仍按 `tick_size` 被调用（**这是 E1 的验收判据**）。

### P1 追加：R8 报单限流（沿用 G4）
`Throttler`：默认 **100 单/秒**，超出即**排队而非丢弃**；同时给出「单轮 tick 内最大报单数」上限，防 while bug 几秒打上千单。

---

## 四、AtomCode 交叉复核的四条实盘前置（本轮新增 · 未验证项）

> 原始回复：`ai_quant_lab/20261012_hummingbot_vnpy/atomcode_reply.md`

| # | 前置条件 | 为什么它是**前置**而不是增强 |
|---|---|---|
| 1 | **实时余额源**（成交回报 / PnL 对账钩子） | 无此源，顺序锁锁的是**幻影余额** —— 锁得再严也没意义 |
| 2 | **本地↔交易所状态同步**（reconcile） | 撤单失败 / 部分成交 / 强平都会造成**预算泄漏**；泄漏会累积到爆仓 |
| 3 | **费率的动态性** | maker/taker、券扣、滑点都变；`c_get_fee(...)` 每单实时取，不能取常数 |
| 4 | **实时对账 reconcile 的验收标准**（AtomCode 建议的「下一轮只做一件事」） | 注入人为余额偏差的故障演练 → 系统在 **1 个轮询周期内自动停机并发出事件** |

**⚠️ 我方的优先级裁决（不盲从）**：第 4 条被**降优先级**。理由：我方**尚无实盘接单通道**（未对接交易所 API），
reconcile 没有对象可对 —— 先做 R7/R8 与 `core/` 本体回填，reconcile 登记为「实盘前置」。

---

## 五、★ 本轮最重要的认知（写进架构注释）

**D5 的顺序锁定在回测里是「结构上做不到」的。**
回测没有真实挂单簿、没有撤单竞争、没有部分成交 → 锁定的只是「本地名义余额 + 估算费」，
**必然高估预算可用性、低估占用时长**（AtomCode Q2 独立指出）。
→ 因此 D5 必须被标注为**实盘增强项**，而不是「回测可验证项」；
→ 也正因如此，它的落点是 **`core/risk.py`（风控层）**，而不是 `core/backtest.py`（回测层）。
→ 这补上了我方「回测乐观偏差」清单的**第 5 项**（前 4 项见 2026-10-11 成交现实化设计）。

---

## 六、优先级汇总（下一轮 P0→P2）

| 级别 | 动作 | 验收 |
|---|---|---|
| **P0** | 回填 **G1**（含费风险预算）+ **G3/R7**（挂单占用顺序锁定）进 `core/risk.py` | `core/risk.py` 自测 **≥9/9 不退化** + 复现 H-005 数字 |
| **P0** | 回填 **E1**（双模 Clock，timer 独立于事件线程）进 `core/events.py` | 事件积压 1000 条时定时任务仍准时 |
| **P1** | **R8** 报单限流（100 单/秒）+ **D3**（`fill_policy` 双口径）+ **D4**（信号归因进 `core/report.py`） | 各自自测 + 一页对照数字 |
| **P2** | **D9** 在途态建模（OMS 最小可用版） | 撤单幂等自测（重复撤单只生效一次） |
| **挂账** | D1/D2（freqtrade）+ G2（三态状态机） | 已连续 3 轮挂账，下一轮必须动手 |

---

*建立：2026-10-12 · 汤小龙 · 绑定「AI量化平台·开源精读夜学」第 6 轮*
