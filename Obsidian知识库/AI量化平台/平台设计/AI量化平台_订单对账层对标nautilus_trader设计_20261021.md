---
日期: 2026-10-21
轮次: 第 11 轮
对标仓库: nautilus_trader
对标层: 执行层 · 对账子层（reconciliation）
tags: [AI量化平台, 平台设计, 对账, 订单生命周期, 风控]
---

# AI量化平台 · 订单对账层对标 nautilus_trader 升级设计

> 前置：[[AI量化平台_多市场组合网关对标vnpy_binance设计_20261020]]（D25–D29，`live.py` 报单唯一入口）
> 本轮补的是**报单之后**那一段：订单出去了，回来五条路怎么分辨。

---

## 零 · 本轮要解的痛点（一句话）

`core/live.py` 有报单入口了（10-20 补的），`core/risk.py` 有 24 项自测的风控了，
但**订单发出去之后平台不知道发生了什么** —— `risk.pending` 只有「在途 / 不在途」两态。
后果是三个具体的、会亏钱的问题：

| 现象 | 真实后果 | 根因 |
|---|---|---|
| 网络超时被当拒单 → 释放额度 | **重复开仓**（一次抖动变双倍仓位） | 「不知道」与「明确失败」被混为一态 |
| 撤单在途时收到旧 Ack → 状态回「挂单中」 | 撤单静默失效，额度锁死到成交 | 本地意图不接受旧回执的保护缺失 |
| 改单后旧 ID 的 Canceled 回来 → 订单被关 | **幽灵持仓**（本地空仓、交易所有仓） | `venue_order_id` 被当点而非链 |

---

## 一 · nautilus 的做法（源码实证，非二手转述）

文件：`crates/execution/src/reconciliation/orders.rs`（1613 行）

### 1.1 它把「不一致」分成五类，而不是笼统「修不一致」

| 不一致类型 | nautilus 的判据（行号） | 处置 |
|---|---|---|
| 旧回执 vs 新意图 | `is_unchanged_accepted_report_during_pending_command`:445 | **丢弃**（不产生事件） |
| 旧单 vs 新单（改单） | `is_superseded_cancel_report`:1350 | **丢弃**（只内部对一次账） |
| 成交回退（快照） | `has_material_fill_decrease`:201 + `allow_fill_decrease=true` | 生成 `FillVoided` 逆序冲销 |
| 成交回退（增量） | 同上 + `allow_fill_decrease=false` | **拒绝**（保持缓存，只在终态收口） |
| 精度噪声 | `is_within_single_unit_tolerance` | 判等，**不触发状态机** |

### 1.2 三条容易被忽略但决定成败的实现细节

1. **`let mut working = order.clone()`**（`:123`/`:266`）
   —— 所有事件在**克隆体上预投影**后才决定下一个事件该不该生成。
   好处①：同一份报告里「数量 100→120」+「成交 120」能按正确顺序施加，
   否则 `Fill(120)` 会被「超量成交」拒掉，订单永远停在在途。
   好处②：生成失败**不会把订单对象改脏**。

2. **`Option<OrderEventAny>` 而不是 `Vec`**（`:327`）
   —— 一次对账只推进一步。状态推进是**逐步可验证**的，
   而不是一口气推多步再回头 debug。

3. **`OrderStatus` 15 态 + `is_open() || is_inflight()`**（`model/src/enums.rs:1433,1470`）
   —— docstring 自己写明：过滤「交易所仍持有的单」时**单测 `is_open()` 会静默漏掉 `Submitted`**。
   我方的 `pending` 只有两态，连「漏」的机会都没有 —— 是压根没有这个概念。

---

## 二 · 五条可迁移设计（D30–D34）+ 一条状态枚举纪律（D35）

### D30 · 未变化 Ack 必须丢弃（本地意图优先于旧回执）
- **判据**：`local_state ∈ {PENDING_CANCEL, PENDING_UPDATE}` ∧ `report=ACCEPTED`
  ∧ `venue_order_id` 未变 ∧ `filled_qty` 未变 ∧ 无数量/价格修订 → 丢弃。
- **为什么**：交易所回报异步，撤单发出后**之前排队的 Accepted 还会到**。
  照单全收 = 撤单静默失效。**不能用时间戳判**（交易所时钟不可信），只能看**内容是否变化**。

### D31 · `venue_order_id` 是「链」不是「点」
- **判据**：收到 `Canceled` 且 `report.vid ≠ 当前 vid` 但 `report.vid ∈ vid_history` → 历史回声，丢弃。
- **为什么**：改单在协议层是「撤旧 + 建新」，旧单的 CANCELED 必然回来，
  但它描述的是**新单出现之前**的世界。认了 → 幽灵持仓。

### D32 · 成交回退的语义由**通道**决定，不由数字决定
- **快照通道**（REST 查询）：回退 = 之前的成交被 void → **必须冲销**（`FillVoided`，手续费按比例摊回）。
- **增量通道**（WS 推送）：回退 = 乱序旧消息 → **必须拒绝**（认了会后面对账再"修回来"，来回抖动）。
- **为什么**：同一个 `40→10`，两种通道里含义完全相反。**语义是通道的属性，不是数字的属性。**

### D33 · venue 时序 + 克隆体预投影
- **顺序固定**：`Accepted → Updated → 状态/成交`。
- **为什么**：数量 100→120 且成交 120 的报告，不先 Updated 就会超量成交被拒。

### D34 · 对账「两次未命中」才收口
- **做法**：`missing_threshold=2`。第一次只告警（额度保留），第二次才判「已消失」并释放。
- **为什么**：交易所接口偶发漏报一条太常见（限频/分页/时钟切面）。
  **把「看不到」当「不存在」是重复开仓的标准成因。**

### D35 · 状态枚举必须区分「工作 / 在途 / 未知」三类正交属性
`is_open()`（交易所仍持有）≠ `is_inflight()`（已发未确认）≠ `is_terminal()`。
我方 7 态映射：

```
SUBMITTED ──ack──► ACCEPTED ──fill──► PARTIALLY_FILLED ──fill──► FILLED(终态)
    │                 │                     │
    │                 ├──begin_cancel──► PENDING_CANCEL ──canceled──► CLOSED(终态)
    │                 │                        ▲
    │                 └──(未变化 Ack)── 丢弃 ───┘     ← D30
    │
    ├──error(网络)──► UNKNOWN ──reconcile──► ACCEPTED / CLOSED   ← **额度保留**
    └──rejected──► CLOSED(reason=REJECTED)                      ← **额度释放**
```

---

## 三 · 本轮已落地的代码（真实回填，不是设计稿）

| 文件 | 内容 | 自测 |
|---|---|---|
| `quant_app/core/order_lifecycle.py`（新建 480 行） | `OrderRecord` 订单本体 + `OrderBook` 7 态推进 + `reconcile()` 快照对账 + `reconcile_missing()` 两次未命中 | **8/8** |
| `quant_app/core/live.py`（4/4 → **8/8**） | `submit_order(book=...)` 先落库再发；新增 `on_order_ack` / `on_order_error` / `on_order_rejected` / `reconcile_orders` | **8/8** |
| `ai_quant_lab/20261021_nautilus_trader_vnpy/order_reconciliation_patterns.py`（新建） | P1 `UnchangedAckFilter` · P2 `SupersededIdGuard` · P3 `FillDecreasePolicy` · P4 `PrecisionTolerance` · P5 `VenueTemporalOrdering` + 与平台模块的**等价性自测** | **17/17** |
| `ai_quant_lab/20261021_nautilus_trader_vnpy/manifest_min.py`（新建） | **W7 结清**：data/params/code 三段指纹 + `diff()` 指出该重算哪几段 | **7/7** |

### 3.1 顺带结清的两块历史挂账

- **W7 manifest（挂账第 1 轮 → 结清）**：`manifest_min.build_manifest()` + `diff()`。
  规则：**仅参数变 → 只重算 backtest/report；数据或代码变 → 全量重算；全同 → 复用**。
  逐文件级 `detail` 能指出具体是哪个 CSV / 哪个 .py 变了。
- **OrderLifecycle 7 态（挂账第 1 轮 → 结清）**：见上表。

---

## 四 · 自测抓到的坑（比设计更值钱）

### 坑 1 · 「成交量超量」不能静默截断
`on_fill` 里若 `fill_qty > leaves_qty`，**必须拒绝并让调用方看见**（返回 `ignore` + 原因），
不能 `min(fill_qty, leaves)` 悄悄截断。截断 = 账实不符被吃掉，后面永远对不出来。

### 坑 2 · `reconcile_missing` 若一次未命中就释放 → 自测必挂
第一版写 `missing_count >= 1` 就收口。后果：**第一次对账（交易所接口还没准备好）就把所有在途单关掉**，
额度全放 → 下一轮全量重开。改 `>= 2` 后自测通过，且这个阈值本身就是业务参数（可配）。

### 坑 3 · 终态必须幂等（`released` 标志）
`FILLED` 和 `CLOSED` 都可能产生 `release` 动作。若风控层重复 `release_order` 同一单，
额度会被「减两次」。→ `OrderRecord.released` 做一次性闸门，**释放只发生一次**。

---

## 五 · 与既有设计的衔接（别把新层搞成孤岛）

```
live.submit_order ──过闸──► risk.reserve_order（R1-R8 + G2 四态）
        │
        └──先落库──► order_lifecycle.OrderBook.submit（SUBMITTED）
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   on_order_ack      on_order_error    on_order_rejected
   （D30 保护）      （UNKNOWN，额度保留）（CLOSED，额度释放）
        │
        └──reconcile_orders（D31/D32/D34）──► risk.release_order（只在收口时）
```

**单一写者原则**：状态只由 `OrderBook` 写；额度只由 `risk` 写；
`live.py` 只做**转发与编排**，不自己改任何状态。

---

## 六 · 下一轮 P0 / P1 / P2

### P0（不许连续挂账）
1. **`core/backtest.py` 的撮合器注入拒单/部分成交率** → 才能真正覆盖
   `OrderBook` 的 `UNKNOWN` / `PARTIALLY_FILLED` 分支（现在只有单测覆盖，回测跑不到）。
2. **H-023 补档**：`25/20/12`、`30/25/15` 两档 + 样本外 → 定位真实最优点
   （已知 `20/15/10` 是网格边界、`let_run` 是 0/4，最优在两者之间）。
3. **`manifest_min` 接进假设回测链**：每次 `hypothesis_runner` 跑完自动落一份 manifest
   → 下次「同一假设两个数」时能立刻说清是哪段变了。

### P1
4. `reconciliation/positions.rs`（1038 行）→ **持仓对账**（`cap_price_at_instrument_max` / 单手容差）。
5. `order_emulator/emulator.rs`（4371 行）→ 本地撮合模型（直接补回测缺口）。
6. 滑点系数实盘标定（连续第 4 轮挂账）。

### P2
7. `crates/execution/src/engine/mod.rs`（5577 行）主循环。
8. 订单只读视图 + 对账不一致即 HALTED 的联动（G2 已有 RECOVERING，但没有「对账失败」入口）。

---

## 七 · 诚实边界

- 本轮所有结论来自**直接读 Rust 源码**，AtomCode 推理通道**不可用**（probe_failed，见笔记 §8）。
- nautilus 是**机构级 Rust 实现**，我方是**Python + 无 tick/盘口**。
  可迁移的是**语义与判据**，不是性能与撮合精度。
- 对账层能做的只是「让账与外部世界一致」，**不能创造成交质量**。
- 无实盘接单通道 → 本轮 `OrderBook` 的 `UNKNOWN` 分支**只在单测里跑过**，
  真实环境未验证（这是必须写明的边界）。
