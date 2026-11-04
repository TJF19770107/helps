# AI量化平台 · 风控层对标升级设计（nautilus_trader）

> **建立**：2026-10-09 · 汤小龙 · 夜学第 3 轮
> **来源**：精读 `nautilus_trader` `crates/risk/src/`（sizing.rs / engine/mod.rs / engine/config.rs）+ `vnpy` `event/engine.py`
> **对标对象**：平台自研 `quant_app/core/risk.py`（六道闸 R1-R6 + 状态机，2026-10-09 新建）
> **状态**：**设计已定稿，代码未回填**（本轮只做到「模块可跑 + lab_bridge 可加载」，未动 `core/risk.py` 本体）
> **诚实边界**：本文对标的是 nautilus 的**工程约束与风控纪律**，不是收益率。不承诺任何倍数。

---

## 一、结论先行：六道闸方向对，但差四道「实盘才暴露」的闸

我们 `core/risk.py` 的六道闸（R1 单笔风险 / R2 单标的 / R3 组合敞口 / R4 单笔名义 / R5 回撤闸 / R6 日亏连亏熔断）**方向完全正确**，
自测 9/9 也全过。但和 nautilus 生产级 `RiskEngine` 一比，有 **4 处会导致真实亏损的逻辑差异**（不是风格）：

| # | 缺口 | 我们的现状 | nautilus 的做法 | 后果 |
|---|---|---|---|---|
| **G1** | 风险预算**没扣手续费** | `q1 = (eq×risk) / stop_dist` | `riskable = eq×risk − eq×risk×c×2`，再除止损 | 实际单笔风险**超预算**（止损 1000 点 +5%，止损 100 点 +50%） |
| **G2** | 状态机**只有两态** | NORMAL / HALTED（「只许减仓」挂 HALTED 上） | Active / Reducing / Halted **三态** | 语义混叠，日志说不清「停在哪一档」 |
| **G3** | **挂单不占持仓额度** | 只看净持仓 | `可平量 = 净持仓 − 未成交挂单 leaves_qty` | 重复申报 → 超卖/反向裸空 |
| **G4** | **没有报单限流** | 无 | `Throttler` 默认 100 单/秒 | 一个 while bug 几秒打上千单手续费 |

**核心判断**：G1/G3 是「回测永远看不到、实盘一炸就爆」的坑；G2/G4 是「事故复盘说不清、防不住失控」的坑。**四条都必须在实盘前补上。**

---

## 二、四条缺口的详细设计与落地动作

### G1 · 风险预算扣双边手续费（R1 修正）

**nautilus 原文**（`sizing.rs:132-152`）：
```
risk_money = equity × risk
commission = risk_money × commission_rate × 2      # 双边
riskable   = risk_money − commission
```

**精确解（比 nautilus 的近似更严）**：
设止损距离 `d`、入场价 `p`、单边费率 `c`，实际最坏亏损 = `qty×d + qty×p×c×2`。
令其 = 预算 `B`：
```
qty = B / (d + p×c×2)          # ★ 含费精确解
```
**实测对比**（100k 权益 / 2% 风险 / p=50000 / c=0.0005）：

| 口径 | 张数 | 实际最坏亏损 | 偏差 |
|---|---|---|---|
| 旧口径（现状） | 2.0000 | 2100.00 | **+5.00%** |
| 含费精确解 | 1.9048 | 2000.00 | **0.0000** |
| nautilus 近似 | 1.9980 | 2097.90 | −0.10%（略保守，安全） |

→ **落地动作**：`core/risk.py` 的 `pre_trade_check` R1 分支替换为
`qty = budget / (stop_dist + price*commission_rate*2)`，新增 `commission_rate` 到 `RiskConfig`。
→ 验证器 H-005（已跑，**已验证**）：`ai_quant_lab/hypothesis_runner.py::verify_H005`。

### G2 · 状态机拆三态（语义正交）

| 状态 | 语义 | 开仓 | 减仓 | 对应我们什么 |
|---|---|---|---|---|
| `Active` | 正常 | ✅ | ✅ | 现有 NORMAL |
| `Reducing` | 只许减仓 | ❌ | ✅ | 现有 HALTED **的实战语义** |
| `Halted` | 全停（含平仓） | ❌ | ❌ | 新增（账户冻结/合规） |

**⚠️ 关键决策——不照搬 nautilus 的 Halted 语义**：
nautilus 的 `Halted` **连平仓单都拒**（合规/账户冻结场景）。
我们的 HALTED 实际是 nautilus 的 `Reducing`。
**保留我们的实战优势**（回撤闸停机后**仍能平仓**，否则风控会变成爆仓加速器——这是 2026-10-09 自测抓到的真 bug），
只是把语义**拆开**：回撤闸 → `Reducing`；账户级异常 → `Halted`。

→ **落地动作**：`core/risk.py` 的 `RiskLevel` 扩为三态；`RiskConfig` 增 `halt_on_account_error`；
`pre_trade_check` 按状态门分派（对标 `execution_gateway` 的三态 match）。

### G3 · 挂单占用持仓额度（新增 R7）

**nautilus 原文**（`engine/mod.rs:1405-1446`）：
```
position_quantity = Σ 同标的未平持仓
pending_quantity  = Σ 未成交挂单 leaves_qty
available = position_quantity − pending_quantity
```
**为什么必须**：净多 1.0，已挂 0.8 止损平仓单；再发 1.0 平仓单 → 合计 1.8 > 持仓 1.0 →
两单先后成交 → **净空 −0.8**。单边行情里这是灾难。

→ **落地动作**：`core/risk.py` 增 `pending_orders: dict[symbol, list[qty]]`；
`pre_trade_check` 在减仓路径上加 `available = |pos.qty| − Σ|pending|` 校验；
`core/events.py` 的 `OrderEvent` 到达时更新挂单集合（用 `OmsCache` 范式）。

### G4 · 报单限流（新增 R8）

**nautilus 原文**（`config.rs:52-56`）：`max_order_submit = RateLimit(100, 1s)`。
→ **落地动作**：`core/risk.py` 增 `OrderThrottler`（滑动窗口），
`pre_trade_check` 入口先过限流；超限 = 拒单（`rule="R8-限流"`）。
建议参数：`rate=100`、`per_seconds=1.0`（与 nautilus 默认对齐）。

---

## 三、事件层同步升级（来自 vnpy）

| # | 缺口 | 现状 | vnpy 做法 | 落地动作 |
|---|---|---|---|---|
| **E1** | timer 寄生在事件线程 | `_run()` 里 `queue.get(timeout=timer_ms)` | `_run_timer()` **独立线程** | `TimerEmitter` 独立线程（已实现于 `vnpy_event_patterns.py`） |
| **E2** | 无「功能引擎」抽象 | handler 裸函数，无生命周期 | `BaseEngine` 自带 `close()`/`name` | 引入 `BaseEngine` 抽象（可选，低优先） |
| **E3** | 无事件→状态缓存 | 只有派发 | `OmsEngine` 增量缓存 + 活跃集合维护 | 引入 `OmsCache`（**G3 依赖它**，优先） |

**E1 对黑马的直接影响**：实盘的「时间止损/定时巡检」若挂在被拖慢的 timer 上，
行情暴动时（最该准点）它最不准。**这是实盘安全项，不是性能优化。**

---

## 四、升级后的风控层全貌（R1-R8 + 三态）

```
下单请求 OrderRequest
  │
  ├─ R8 报单限流      ← G4 新增（Throttler 100/s）
  │
  ├─ 状态门：Active / Reducing / Halted   ← G2 三态
  │     Reducing → 仅减仓放行 ；Halted → 全拒
  │
  ├─ R7 挂单占用      ← G3 新增（可平量 = 净持仓 − 活跃挂单）
  │
  ├─ R4 单笔名义上限
  ├─ R1 单笔风险（★含费口径）  ← G1 修正
  ├─ R2 单标的仓位上限
  ├─ R3 组合总敞口上限
  │
  └─ 放行 → 执行层
        ↑
    账户级（每根 K 线喂一次权益）
      ├─ R5 回撤闸 → Reducing（可平不可开）
      └─ R6 日亏/连亏熔断 → 停机待人工
```

---

## 五、实施优先级（下一轮夜学执行）

| 优先级 | 动作 | 文件 | 依赖 |
|---|---|---|---|
| **P0** | R1 换含费口径（G1） | `core/risk.py` | 无（H-005 已证） |
| **P0** | timer 独立线程（E1） | `core/events.py` | 无 |
| **P1** | R7 挂单占用（G3）+ OmsCache（E3） | `core/risk.py` + `core/events.py` | E3 先行 |
| **P1** | R8 限流（G4） | `core/risk.py` | 无 |
| **P2** | 状态机三态（G2） | `core/risk.py` | 需同步改 `live.py`/`backtest.py` 调用点 |

**纪律**：每项改完必须重跑 `core/risk.py` 的自测（现有 9/9 必须保持不退化，并新增对应用例）。

---

## 六、诚实边界

- 本文所有 nautilus 结论均来自**源码行号可查**的实现，非二手转述。
- 「对标一流对冲基金」= 对标**工程约束与风控纪律**，不是收益率数字。
- 本设计**尚未回填平台本体**。在回填并重跑自测之前，`core/risk.py` 仍是六道闸版本。
- H-004/H-005 的回测结论见 `策略假设/回测结果/回测结果_20261009.json`。

---

*关联：[[20261009_nautilus_trader_vnpy]] · [[策略假设台账]] · [[AI量化平台架构蓝图]]*
