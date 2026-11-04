---
日期: 2026-10-21
仓库: nautilus_trader
核心文件: crates/execution/src/reconciliation/orders.rs（1613 行）+ crates/execution/src/order_manager/manager.rs（5049 行）+ crates/model/src/enums.rs:1433 OrderStatus（15 态）
轮次: 第 11 轮
tags: [AI量化平台, 夜学, 代码拆解, 对账, 订单状态机]
---

# 20261021 · nautilus_trader · reconciliation/orders.rs

## 0. 一句话结论

> **nautilus 的对账层不是在「修不一致」，而是在「给不一致分类」** ——
> 同一个「成交从 40 变 10」，在快照通道里是「成交被撤销（要认）」，
> 在增量通道里是「旧消息乱序（要丢）」。
> **语义由通道决定，不由数字决定。** 我原来的 `live.py` 只有一条回报通道、
> 两态在途标记 —— 这就是它认不出「超时」和「拒单」区别的根因。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：**执行层**（`crates/execution`）→ 其下的**对账子层**（`reconciliation`）
- **它不管什么**（这点比它管什么更重要）：
  - 不管网络（不调 REST / WS，只吃 `OrderStatusReport` 结构体）
  - 不管撮合（不判断成交真伪，只按报告推进状态）
  - 不管风控（不批不拒，只产出事件）
  - **它只管一件事：把「交易所说的事实」翻译成「本地安全可施加的事件序列」**
- **上下游**：
  - 上游 → `crates/execution/src/engine/mod.rs`（执行引擎，5577 行）在收到
    `OrderStatusReport` / `FillReport` 后调用本文件
  - 上游 → `crates/adapters/{binance,bybit,...}`（各网关把自家私有字段映射成统一报告）
  - 下游 → `crates/model/src/orders/*`（`OrderAny.apply(event)` 才是真正改状态的地方）
  - 下游 → `crates/portfolio/src/manager.rs`（持仓/账户跟着订单事件走）
- **同层兄弟**：`reconciliation/positions.rs`（持仓对账 1038 行）·
  `reconciliation/ids.rs`（对账专用 ID 生成 303 行）· `order_manager/manager.rs`（订单簿 5049 行）
- **选它的理由**（按「能力清单而非文件清单」原则）：本轮挂账是
  **`live.submit_order()` 只有两态、无对账**，而全仓库里
  「订单状态 × 外部报告 × 不一致裁决」三者交汇的唯一地方就是这里。

---

## 2. 调用链（文字版时序图）

```
[交易所 WS/REST]
      │  私有协议 JSON
      ▼
[adapters/binance/.../parse_order_status_report]
      │  OrderStatusReport { order_status, filled_qty, venue_order_id, ts_last, ... }
      ▼
[crates/execution/src/engine/mod.rs :: 收到报告]
      │  按 client_order_id 从缓存取本地订单 OrderAny
      ▼
[reconciliation/orders.rs :: generate_reconciliation_order_events]   ← ★ 本文件入口
      │
      ├─(1) is_superseded_cancel_report(order, report)?
      │        └─ 是 → 只内部对一次账，返回 **空事件表**（旧 ID 回声，丢弃）
      │
      ├─(2) has_material_fill_decrease(order, report)?
      │        ├─ 增量通道 → 打 warn，退回 reconcile_fill_decrease_terminal（不认回退）
      │        └─ 快照通道 → create_reconciliation_fill_voids（生成 FillVoided）
      │
      ├─(3) prepare_reconciliation_order(order, report)
      │        ├─ should_accept_before_reconciliation → 先补 Accepted
      │        ├─ report_is_confirmed_state && local_accepts_amendment
      │        │      && should_reconciliation_update → 再补 Updated
      │        └─ 关键：`let mut working = order.clone()` —— **在克隆体上预投影**
      │
      ├─(4) 终态撤退：报告说 Canceled/Expired 但本地已 Filled → 直接返回（不让终态回退）
      │
      └─(5) reconcile_order_report_with_commission(working, ...)
               ├─ PendingUpdate/PendingCancel → **None**（未确认的意图不驱动本地）
               ├─ is_unchanged_accepted_report_during_pending_command → None
               ├─ is_superseded_cancel_report → None
               ├─ 状态+成交量都已同步 → 有修订则 Updated，否则 None
               └─ match report.order_status { Accepted/Rejected/Triggered/
                    Canceled/Expired/PartiallyFilled|Filled/Voided/... }
                      └─ 生成 OrderEventAny
      ▼
[model/src/orders :: OrderAny.apply(event)]
      │  真正的状态机推进（本地唯一写者）
      ▼
[portfolio/manager.rs :: 持仓与账户更新]
      │
      ▼
[风控 / 报告 / UI]
```

**一句话读懂这条链**：`reconciliation` 是**翻译器 + 过滤器**，
真正的状态变更只在 `OrderAny.apply` 发生一次 —— **单一写者**。

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `generate_reconciliation_order_events(order, report, instrument, ts_now) -> Vec<OrderEventAny>` | 函数 | **增量语义**入口（WS 回报） | 传 `allow_fill_decrease=false` |
| `generate_reconciliation_order_snapshot_events(...)` | 函数 | **快照语义**入口（REST 查询） | 传 `true` → 允许成交回退 |
| `generate_reconciliation_order_events_inner(...)` | 私有 | 真正的编排：superseded → fill decrease → prepare → 终态撤退 → 状态机 | 全部逻辑 100 行，是本文件的心脏 |
| `prepare_reconciliation_order(order, report, ts_now) -> (OrderAny, Vec<Event>)` | 私有 | **克隆体预投影**：先补 Accepted、再补 Updated，返回已推进的克隆 | nautilus 最关键的一手 |
| `reconcile_order_report_with_commission(order, report, instrument, ts_now, commission) -> Option<OrderEventAny>` | 函数 | 核心状态机：把一份报告映射成**至多一个**事件 | `Option` 而非 `Vec` —— 一次只走一步 |
| `has_material_fill_decrease(order, report) -> bool` | 私有 | 成交回退是否「实质」（带精度容差） | 亚单位差异不算回退 |
| `is_within_single_unit_tolerance(a, b, precision)` | 函数 | `max(prec_a, prec_b)` 容差判等 | 防浮点噪声触发状态机 |
| `create_reconciliation_fill_voids(order, report, ts_now) -> Vec<OrderFillVoided>` | 私有 | **逆序遍历**成交历史，逐笔部分撤销（含手续费按比例摊回） | 回退也留 trade_id，可追 |
| `is_superseded_cancel_report(order, report) -> bool` | 函数 | 旧 `venue_order_id` 的 Canceled 是回声 | 依赖 `venue_order_ids` **历史链** |
| `is_unchanged_accepted_report_during_pending_command(order, report) -> bool` | 私有 | 撤单/改单在途时收到未变化 Ack → 必须丢弃 | 本地意图优先级 > 旧回执 |
| `reconcile_fill_quantity_mismatch(...) -> Option<OrderEventAny>` | 私有 | 成交数量不一致的处理：多则补**推断成交**，少则「保持缓存不变」 | 增量语义下**拒绝回落** |
| `create_incremental_inferred_fill(...)` | 函数 | 交易所多报的成交量 → 生成「推断成交」事件 | 不丢成交，宁可补一条 |
| `OrderStatus`（15 态，`model/src/enums.rs:1433`） | enum | Initialized/Denied/Emulated/Released/**Submitted**/Accepted/Rejected/Canceled/Expired/Triggered/**PendingUpdate**/**PendingCancel**/PartiallyFilled/Filled/Voided | `is_open() \|\| is_inflight()` 才能覆盖「交易所仍持有」 |

---

## 4. 可迁移设计点（D30–D34 · 每条说明「为什么更好」）

### D30 · 未变化 Ack 必须被丢弃（本地意图优先于旧回执）
`orders.rs:445`
**做法**：订单处于 `PENDING_CANCEL/PENDING_UPDATE` 时，若收到 `Accepted`
且 `venue_order_id`、`filled_qty`、数量/价格**全都没变** → 返回 `None`，不产生事件。
**为什么更好**：交易所回报是异步的，撤单发出后**之前就排好队的 Accepted 还会到**。
照单全收 = 本地状态被拽回「挂单中」= 撤单请求静默失效 + 额度一直占着。
判据必须是**内容是否变化**，不能看时间戳（交易所时钟不可信）。
**我方缺口**：`live.py` 原 `pending` 只有两态，压根没有「撤单在途」这个态 → 这条保护无处施加。

### D31 · venue_order_id 是「链」不是「点」
`orders.rs:1350`
**做法**：本地保存 `venue_order_ids` 历史；收到某 ID 的 `Canceled` 时，
若该 ID **不等于当前 ID 但在历史里** → 判定为 cancel-replace 的「撤单那一半」，丢弃。
**为什么更好**：改单在协议层是「撤旧 + 建新」，旧单的 CANCELED 一定会回来，
但它描述的是**新单出现之前**的世界。把当前单关掉 = 本地空仓、交易所有仓（幽灵持仓）。
**我方缺口**：`risk.pending[order_id]` 是单键 → 无历史链概念。

### D32 · 成交回退的语义由**通道**决定，不由数字决定
`orders.rs:201, 112-155`
**做法**：`has_material_fill_decrease` 判断「是否实质回退」；
`allow_fill_decrease` 由**入口**决定 —— 快照入口 `true`（生成 FillVoided 逆序冲销），
增量入口 `false`（打 warn、保持缓存、只在终态时收口）。
**为什么更好**：同一个数字 `40→10`，
在 REST 快照里是**此刻真相**（那 30 张确实被撤销了，必须冲销）；
在 WS 增量里是**乱序旧消息**（认了就把已成交量抹掉，且下次对账又"修回来"，来回抖动）。
**我方缺口**：只有一个「成交回报」通道 → 两种语义被混成一种。

### D33 · 事件必须按 venue 时序生成，且在**克隆体**上预投影
`orders.rs:99-199, 261-311`
**做法**：`let mut working = order.clone()` → 先 `apply(Accepted)` → 再 `apply(Updated)`
→ 判下一事件时用的是**已推进的克隆**；且顺序固定为
`Accepted → Updated → 状态/成交`。
**为什么更好**：docstring 里点名的场景 —— 交易所把数量 100→120，同一份报告还带
`filled=120`。若不先 Updated：本地量还是 100 → 生成 Fill(120) → **超量成交被拒**
→ 订单永远停在在途，而交易所早已成交完毕。
用克隆体还有第二个好处：**生成失败不会把订单对象改脏**。

### D34 · 对账是「两次未命中」而非「一次未命中」
`reconciliation/positions.rs` + 本文件 `report_is_working` 的组合语义
**做法**：`report_is_working`（Accepted/Triggered/PartiallyFilled）与
`report_is_confirmed_state` 分开定义 —— 「交易所仍持有」和「状态已确认」是**两个正交问题**。
`enums.rs:1470` 的注释直接点破：过滤「交易所仍持有的单」必须用
`is_open() || is_inflight()`，**单测 `is_open()` 会静默漏掉 `Submitted`**。
**为什么更好**：把「看不到」直接判成「不存在」，是重复开仓的标准成因。
交易所接口偶发漏报一条太常见（限频/分页/时钟切面）。
**我方做法**：落地为 `missing_threshold=2`（第一次只告警，第二次才收口并释放额度）。

---

## 5. 可复用代码片段

**来源**：`crates/execution/src/reconciliation/orders.rs:445-456`（D30 的判据本体，13 行）

```python
# 来源：nautilus_trader/crates/execution/src/reconciliation/orders.rs:445-456
#       对应 Rust 的 is_unchanged_accepted_report_during_pending_command
# 用途：撤单/改单在途时，判断收到的 Accepted 是不是「过期回执」
def is_unchanged_ack_during_pending(local_state, report_state,
                                    local_vid, report_vid,
                                    local_filled, report_filled,
                                    has_amendment=False) -> bool:
    """返回 True = 这是旧回执，必须丢弃（不产生任何事件）。"""
    if local_state not in ("PENDING_CANCEL", "PENDING_UPDATE"):
        return False                      # 不在挂起态 → 不是本规则的事
    if report_state != "ACCEPTED":
        return False                      # 只有 Accepted 会与挂起态冲突
    if local_vid != report_vid:
        return False                      # 换了 ID = 新事实，不能丢
    if abs(float(local_filled) - float(report_filled)) > 1e-12:
        return False                      # 成交量变了 = 有新信息
    return not has_amendment              # 数量/价格也没改 → 纯旧回执
```

**我方落地版本**（已进平台，见 §9）：`core/order_lifecycle.py::OrderBook.on_ack`
+ `ai_quant_lab/20261021_nautilus_trader_vnpy/order_reconciliation_patterns.py::UnchangedAckFilter`

---

## 6. B站学习（本日 30% 权重）

- **本轮结论：不做**。2026-10-20（W3）已**终身结案**：
  `search/type` 需 wbi 签名（412）· `player/v2` 返回 `subtitles=[]`（需登录 cookie）·
  唯一可用的是 `search.bilibili.com/all?keyword=` 的 HTML 标题清单。
  → 副源**永久降级为「标题 / 目录级」笔记**，且**不再计入「未完成」**。
- 替代副源（本轮实做）：直接读 nautilus 官方仓库内的
  `docs/` + `crates/execution/src/reconciliation/proptests.rs`（1205 行 property-based 测试）
  —— 这比任何视频都更接近「可验证的知识」，因为**它自带反例生成器**。

---

## 7. 对黑马策略的启发（已落成假设并跑完）

### H-022 · 成本端「咬合力修正版」（**已验证 4/4**，首次真咬到）
- **问题**：H-019/H-021 都判「成本端成立」，但 H-021 的放行率是 **99.79%~100.00%** ——
  等于**没砍任何信号**，测到的只是「taker 0.1% → maker 0.02% 的费率差」。
- **做法**：把挂单价下移 `k`，`k` **由实测标定**（不是拍）：

  | k | BTC | ETH | BNB | DOGE |
  |---|---|---|---|---|
  | 0.00% | 99.19% | 99.14% | 98.72% | 99.02% |
  | 0.01% | 91.37% | 93.56% | 92.11% | 95.54% |
  | 0.02% | 88.22% | 90.72% | 88.97% | 93.14% |
  | **0.05%** | **79.44%** | **83.54%** | **79.81%** | **87.31%** |
  | 0.10% | 64.50% | 72.09% | 66.32% | 78.27% |
  | 0.30% | 23.59% | 33.56% | 29.80% | 47.33% |

  取 **k=0.05%**（4/4 落进 70%~95% 带）→ 净额单笔均值 **4/4 改善**
  （BTC +0.0627 / ETH +0.1425 / BNB +0.1796 / DOGE +0.1098 pp）。
- **★ 被否掉的写法（留档别再试）**：`min(low[t], close[t]×(1−0.1%))`
  → 信号级放行率 **35%~41%**，咬过头 3 倍。原因：15m 相邻 K 线**极值高度重叠**，
  「当根最低」当挂单价 ≈「要求下一根创新低」，这已经不是挂单问题了。

### ★★★ 本轮抓到的**度量 bug**（比假设本身更重要）
H-019/H-021/H-022 一直用「实验组**成交笔数** / 基线成交笔数」当成交率。实测同一条
H-022：**笔数比 = 99.29% / 108.53% / 96.04% / 93.43%**（看着"几乎没砍"），
而**信号级放行率 = 64.50% / 72.09% / 66.32% / 78.27%**（实际砍三成）。
原因：**笔数不是独立抽样** —— 策略只在空仓时开仓，丢掉一个信号后，
后面那个本来被「持仓中」屏蔽的信号会顶上来 → 「少做单」被「换一批单」掩盖。
→ **咬合力的分母必须是信号数，不是成交笔数。**
→ H-019/H-021 的「咬合力≈0」结论**口径有误**（它们确实砍了信号，只是被顶上来的单掩盖）。

### H-023 · 出场端「内部最优档 + 样本外」（**已验证 4/4**）
- **做法**：训练段（前 70%）扫 4 档 `8/6/4` · `10/8/5` · `15/12/8` · `20/15/10`
  → 取最优档 → **样本外**（后 30%，独立切片，先切数据再跑防泄漏）对比基线档。
- **训练段结果**（净额单笔均值%，4 只同向单调）：

  | 标的 | 8/6/4 | 10/8/5 | 15/12/8 | **20/15/10** |
  |---|---|---|---|---|
  | BTC | 1.1182 | 1.7041 | 2.5690 | **4.0208** |
  | ETH | 1.3719 | 1.8752 | 3.5710 | **4.5401** |
  | BNB | 1.3763 | 2.0298 | 3.5551 | **5.1811** |
  | DOGE | 0.1967 | 0.6691 | 2.2662 | **2.5836** |

- **样本外**（4 只全部选中 `20/15/10`）：0.6028→1.3515 / 0.8263→2.3208 /
  1.1740→3.6472 / **−0.9418→−0.4578** → **4/4 改善**。
- **★★ 必须一起读的两条铁律**：
  1. **最优落在网格边界**（`20/15/10` 是我给的 4 档里最松的一档）→
     真实最优点**可能还在网格外**，本轮结论只能是「**内部有最优**」，
     **不能**写成「越松越好」。
  2. **已知反证**：H-020 把方向推到极限（`exit_mode="let_run"`，完全不设回撤止盈）
     → **0/4，单笔均值全翻负**。
     → 把两条合起来：**最优必然在 `20/15/10` 与 `let_run` 之间**，
     下一轮必须补 `25/20/12`、`30/25/15` 两档才能定位。
     **H-023 的正确读法是「存在内部最优」，不是「放宽到 20/15/10 就最好」。**

### 落地动作（具体到文件）
- 平台：新建 `quant_app/core/order_lifecycle.py`（7 态 + 对账）→ 自测 **8/8**
- 平台：`core/live.py` 接线 → 自测 **4/4 → 8/8**
- 工具：`ai_quant_lab/.../manifest_min.py`（W7 最小版）→ 自测 **7/7**
- 假设：`hypothesis_runner.py` 新增 `verify_H022` / `verify_H023` + `_signal_fill_ratio`
- 台账：H-022 / H-023 两行已入 `[[策略假设台账]]`，状态已回写

---

## 8. 未完成 / 失败区（诚实留痕）

1. **AtomCode 本轮不可用（probe_failed）**
   - 现象链：首跑 `proxy_down` → 后台拉起 → 复跑 `probe_failed`
     （`AtomCode serial lock timed out after 30s`）→ 杀掉僵死 `atomcode.exe` 后
     **更糟**：`HTTP=0 / 240s timeout` → 重启代理（新 PID 监听正常）仍 `HTTP 000`。
   - 定性：**串行锁 + CLI 子进程僵死**，不是额度问题（`logged_in=true`，
     CodingPlan 有效期至 2026-10-26）。
   - 处置：按任务书降级为**本地 Read/Grep 精读**（本轮全部结论均来自直接读源码，
     未使用任何推理通道），**0 积分**。
   - 待办：下轮先把 `atomcode.exe` 全量清干净再起代理；若仍 `000`，
     需查 `serial lock` 锁文件（`~/.atomcode/`）是否残留。
2. **`crates/execution/src/engine/mod.rs`（5577 行）只读结构未逐行精读** ——
   本轮聚焦 `reconciliation/`，引擎主循环留待下轮。
3. **`reconciliation/positions.rs`（1038 行）只读语义未展开** —— 持仓对账
   （`cap_price_at_instrument_max` / `is_within_single_unit_tolerance`）是下一块富矿。
4. **`order_emulator/emulator.rs`（4371 行）完全未读** —— 这是「模拟单在本地撮合」
   的完整实现，直接对应我方回测撮合器缺的「拒单/部分成交」模型。
5. **H-023 最优档落在网格边界** → 真实最优点未定位（见 §7 铁律 1）。
6. **H-022 成交价仍按 close 计**，未模拟「成交价 = 挂单价」的价格改善 → 结果是**下界**。
7. **滑点系数仍未实盘标定**（连续第 4 轮挂账）。
8. **无 tick / 盘口** → 排队损耗不可测（所有 limit 类结论强度上限 = 方向性）。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘路径（真实文件 + 自测）：
  - `ai_quant_lab/20261021_nautilus_trader_vnpy/order_reconciliation_patterns.py` —— **17/17**，lab_bridge 零警告
  - `ai_quant_lab/20261021_nautilus_trader_vnpy/manifest_min.py` —— **7/7**，lab_bridge 零警告
  - `quant_app/core/order_lifecycle.py` —— **8/8**（平台回填）
  - `quant_app/core/live.py` —— `selftest_router` **8/8**（原 4/4）
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-022（已验证 4/4）· H-023（已验证 4/4）**
- [x] ④ lab_bridge 加载验证：`order_reconciliation_patterns` / `manifest_min` → 均 `OK`，`warnings=[]`

---

## 10. 成本与技能

- **本次花费积分估算**：**0**（AtomCode 全程不可用，未发生任何付费推理）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（v1.1.8，主流程）
- **沉淀 / 迭代了什么**：
  - 新增平台模块 `core/order_lifecycle.py`（7 态 + 对账）
  - 新增夜学模块 2 个（对账模式 / manifest 最小版）
  - `hypothesis_runner.py` 新增 `verify_H022`、`verify_H023`、`_signal_fill_ratio`、`_run_slice`
  - 技能待升级至 **v1.1.9**：新增「咬合力分母必须是信号数」+「最优落在网格边界时必须外推」
