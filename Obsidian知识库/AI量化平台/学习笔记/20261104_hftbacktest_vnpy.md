---
日期: 2026-11-04
仓库: hftbacktest
核心文件: hftbacktest/src/backtest/data/reader.rs（494 行）+ backtest/data/npy/mod.rs（381 行）+ backtest/data/types.rs（1033 行）+ backtest/proc/partialfillexchange.rs（867 行）+ collector/src/binancefuturesum/mod.rs（99 行）+ collector/src/file.rs（92 行）+ py-hftbacktest/hftbacktest/data/validation.py（152 行）+ data/utils/binancefutures.py（297 行）
轮次: 第 24 轮
tags: [AI量化平台, 夜学, 代码拆解, 数据采集层, 数据校验, 事件位掩码, fail-closed, 判据分辨率]
---

# 20261104 · hftbacktest · 数据采集与转换层（三刷收口）

## 0. 一句话结论

> **今天我抓到的最值钱的东西不是 hftbacktest 的代码，是我自己写的自测"假绿"。**
> 一个只有两态返回值的函数去表达三态现实，34/34 全绿；扩成三态后 40/40 才是真的。

今天做了三件事：

1. **换了一个从没碰过的层** —— 前 23 轮把 hftbacktest 的撮合层（第 5 轮）、队列层（第 13 轮）
   都翻过了，今天专门读**数据采集与转换层**：`collector/` + `data/` + `py-hftbacktest/data/`。
   选它的理由很直白：**我方最大的短板就是"只有 15m OHLC"**，这一层正好对标那个短板。
2. **落地 `bar_integrity_guard.py`**（`ai_quant_lab/20261104_hftbacktest_vnpy/`），
   把「数据坏了」和「策略变差了」这两件事**第一次在代码层面分开**。
3. **两条假设结清**：H-047（已验证，**收窄了 H-042 的可信区间**）、
   H-048（已验证，**结掉第 14 轮悬案**）。

---

## 1. 这一层在系统里管什么（架构定位）

hftbacktest 的分层很清楚，今天读的三块各管一段：

| 层 | 目录 | 职责 | 时间基准 |
|---|---|---|---|
| **采集层** | `collector/src/` | 连交易所 WS → 按 symbol 落 `.gz` 日志 | **交易所时间**（原样） |
| **转换层** | `py-hftbacktest/hftbacktest/data/utils/` | 交易所 JSON → 定长 `Event` 结构体（npy） | 毫秒 → 纳秒（`× 1000000`） |
| **校验层** | `py-hftbacktest/hftbacktest/data/validation.py` | 乱序修复 / 负延迟平移 | **双流**（`exch_ts` / `local_ts`） |
| **加载层** | `src/backtest/data/{reader.rs, npy/mod.rs}` | 按需把 npy 读进缓存、喂给撮合 | 双流原样保留 |

**核心认知：hftbacktest 的时间戳不是一个值，是两个流。**
`Event` 结构体（`types.rs:1-1033`）里 `exch_ts` 和 `local_ts` **并列存在**，永远不合并。
- `exch_ts` = 交易所认为这件事发生在什么时候
- `local_ts` = 我这边实际收到这件事是什么时候
- `local_ts - exch_ts` = **延迟**，这是回测里唯一能建模「我的单子到底排第几」的依据

我方 `core/backtest.py` 只有**一个** `open_time`，没有延迟概念 ——
所以第 5 轮、第 13 轮做的所有队列/撮合改进，本质上都缺了输入。

---

## 2. 调用链（文字版时序图）

```
collector: 交易所 WS
    │  pu != prev_u ?  ──→  warn!("missing depth feed") + 异步抓快照补回
    ↓
RotatingFile.write("{timestamp_nanos} {json}\n")      ← 按 UTC 日期切 .gz
    ↓
[离线] convert(): json.loads → Event { ev, exch_ts, local_ts, px, qty, ... }
    │  ev 是位掩码：BUY_EVENT|TRADE_EVENT = (1<<29)|2
    ↓
validation.correct_local_timestamp()   ← 先扫 min(local-exch)，负则**整体平移**
validation.correct_event_order()       ← 乱序行**拆两份**，按 exch / local 各排一遍
    ↓
             npy 落盘（六道 fail-closed 硬闸）
    ↓
Reader::next_data() ──→ Cache.checkout(key) [引用计数 +1]
    │                     while !is_ready { rx.recv().unwrap() }   ← 通道断 = panic
    ↓
DataPreprocess.preprocess()  ← FeedLatencyAdjustment: local_ts += offset
    │                                              并断言 local_ts > exch_ts
    ↓
PartialFillExchange.process()  ← 深度更新 / 成交事件分派
```

---

## 3. 精读硬指标（六项）

### 3.1 架构定位

见上表。一句话：**这一层的全部设计都在回答一个问题 —— 「两个时间戳不同时，我该信谁」。**
答案是：**谁也不全信，两个都留着，让后面的撮合模型自己决定。**

### 3.2 关键类 / 函数（签名 + 职责）

| 位置 | 签名 | 职责 / 陷阱 |
|---|---|---|
| `types.rs:Event::is()` | `fn is(&self, event: u64) -> bool` | 位掩码判定。`(ev & event) != event → false`；再取 `event_kind = event & 0xff`，为 0 直接 true，否则比 `self.ev & 0xff` |
| `reader.rs:Reader::next_data()` | `fn next_data(&mut self) -> Option<&mut [Event]>` | `while !cache.is_ready(&key) { self.rx.recv().unwrap() }` —— **通道断开会 panic** |
| `reader.rs:Cache::checkout/turn_in` | 引用计数 | `CachedData` 带 `refs`；`remove()` 归零才真删。`data_eq` 用 `Rc::ptr_eq` 比指针不比内容 |
| `reader.rs:FeedLatencyAdjustment::preprocess()` | `fn preprocess(&mut self, data: &mut [Event])` | `local_ts += offset`，**随后断言 `local_ts > exch_ts`**，否则报错 |
| `npy/mod.rs:read_npy()` | `fn read_npy<R: Read+Seek>(...)` | 六道硬闸 + `while read_size < size { read_size += reader.read() }` —— **`read()` 返 0 时死循环** |
| `npy/mod.rs:check_field_consistency()` | | 字段**名字**不同只 `println!("Warning")`，**类型**不同才报错 |
| `partialfillexchange.rs:fill()` | `fn fill(&mut self, order: &mut Order)` | `(leaves_qty/lot_size).round() > 0 → PartiallyFilled else Filled`；**`maker=true` 时成交价恒等于 `price_tick`** |
| `partialfillexchange.rs:ack_new()` | | TIF 语义：GTX 穿价→Expired / FOK 量不够→全撤 / IOC 逐档吃后撤 / GTC 吃穿后**剩余量按限价硬成交**（作者明写这是不现实来源） |
| `validation.py:correct_local_timestamp()` | | 求 `min(local-exch)`，负则**整体平移**（不是逐行裁剪）⇒ 保持相对间隔 |
| `validation.py:correct_event_order()` | | `sorted_final = np.zeros(data.shape[0] * 2, event_dtype)` —— **双倍缓冲**，乱序行拆两份各排一遍 |
| `binancefuturesum/mod.rs` | `pu != prev_u` | 用交易所自带连续性字段检测断流，**不靠时间间隔** |

### 3.3 可迁移设计点（本轮 9 条，D132 起）

**D132 · 位掩码分层（`BUY_EVENT=1<<29` / `SELL_EVENT=1<<28` / `EXCH_EVENT=1<<31` / `LOCAL_EVENT=1<<30` + 低 8 位事件种类）**
为什么好：**一个 u64 里同时编码了「方向」「来源」「种类」三个正交维度**，判定时用 `&` 而非 `==`，
于是 `TRADE_EVENT|SELL_EVENT` 既能单独匹配，也能被 `TRADE_EVENT` 粗匹配到。
我方对应物：`core/backtest.py` 的 `exit_reason` 是字符串（`"trail"` / `"sl"` / `"tp1"`），
**无法表达「既是追踪止盈又是 T2 档」这种组合**。迁移方式见 §7。

**D133 · 引用计数缓存 + 「永不就绪」闸**
`checkout`/`turn_in` 加 `refs`，`Rc::ptr_eq` 比指针；但 `while !is_ready { rx.recv().unwrap() }`
是**真 bug**：加载线程死了，`recv()` 返回 `Err`，`unwrap()` 直接 panic，而 panic 信息是
`called Option::unwrap() on a None value` —— 看不出根因是「数据准备失败」。
⇒ 迁移：《加载器必须有等待预算》，我用**计数式**（`NeverReadyGuard(budget=1000)`）而非挂钟超时，
因为**挂钟超时会让回测不可复现**（同一份数据跑两次可能一次超时一次不超时）。

**D134 · 加载器 fail-closed 六道闸**
魔术字节 / 版本 / fortran_order / 1-d / 缓存行对齐 / 字段类型 —— **全部 fail-closed，一个都不放过**。
对比：我方 `_load_local_15m` 只做 `usecols` + `rename` + `volume > 0` 一条过滤。

**D135 · 「名字松、类型严」必须配一道严出闸**
`check_field_consistency` 名字不同只 Warn、类型不同才 Err。
这个设计本身是对的（字段重命名很常见），但**宽进必须配严出** ——
我方 `usecols=["timestamp", ...]` 一旦 CSV 列序变了，pandas 会按**名字**取到，
但如果哪天换成 `read_csv(header=None)` 就是按**位置**取，**静默错位**。
⇒ 迁移：`audit_bars` 里 `SHORT_ROW` + `NON_FINITE` 是那道严出闸。

**D136 · 乱序「双投不猜」**
`correct_event_order` 把乱序行拆两份各排一遍再投放。作者的洞察：
**「不是重排，是重复投放」，因为真实先后不可知。**
⇒ 迁移：`dual_order_keys()` 只返回**两套顺序 + 差异计数**，不替调用方做不可知的猜测。
这条比「怎么排」重要：**不可知就标注不可知，不要用默认值蒙一个。**

**D137 · 断流用交易所连续性字段，不用时间间隔**
`pu != prev_u` 能抓「单条丢失」，时间间隔只能抓「长断」。
⇒ 迁移：我方 `data_mirror/` 的 `manifest.json` 只记文件级 CRC，
**没有 row 级连续性字段** —— 这是下一个要补的点（见 §10）。

**D138 · lot 判定不得依赖语言舍入模式**（→ 今天在这条上栽了，见 §5）

**D139 · 整体平移不改相对间隔**
`correct_local_timestamp` 为负时整体平移，**不逐行裁剪**。
为什么好：延迟的相对大小是有信息的（A 单比 B 单晚 3ms），逐行裁剪会把这个信息抹平。
⇒ 迁移：`shift_local_timestamps()` 返回 `offset` 和 `min_latency`，明确写出「平移了多少」。

**D140 · 大跳变走字典遍历（`partialfillexchange.rs:747-825`）**
成交事件分派时按 `(orders.len() < price_tick - best)` 决定遍历全字典还是遍历价位梯。
即：**订单簿稀疏时用 O(n) 字典、密集时用 O(档位) 梯**。
⇒ 迁移：我方回测笔数 129~472，**根本用不上**，记为「知道但不用」。

### 3.4 可复用代码片段 → 已落地为 `bar_integrity_guard.py`（v1.1.0，自测 40/40）

| 函数 | 对标来源 | 作用 |
|---|---|---|
| `audit_bars()` | D134/D135 | 八类 fatal + 两类 warn：`EMPTY/SHORT_ROW/NON_FINITE/DUP_TS/TS_NOT_INCREASING/OHLC_ORDER/HIGH_LT_LOW/NEG_VOLUME/TAKER_OUT_OF_RANGE/TRADES_BAD`+`GAP` |
| `NeverReadyGuard` | D133 | **计数式**等待预算（不是挂钟），保回测可复现 |
| `qty_status()` | D138 | **三态** `filled/partial/leaves`（今天从两态改过来，见 §5） |
| `gap_fillable()` | `correct_local_timestamp` | 跳空判定容差绑 `tick_size`，不绑绝对常数 |
| `dual_order_keys()` | D136 | 两套顺序 + 差异计数 |
| `shift_local_timestamps()` | D139 | 整体平移 + 返回 `offset` |

### 3.5 对各黑马策略的具体动作

| 动作 | 对象 | 优先级 | 状态 |
|---|---|---|---|
| 把 `audit_bars` 接进 `_load_local_15m`，读 CSV 后强制审计一遍 | `core/backtest.py:805` | **P0** | 模块已就绪，接线未做（见 §10） |
| 用 `qty_status` 三态替换 `fill_realism` 的布尔判定 | `core/backtest.py` 撮合段 | P1 | 未做 |
| `data_mirror/manifest.json` 加 row 级连续性校验 | `_tools/binance_mirror_sync_v2.py` | P1 | 未做 |
| 「双流时间戳」暂不迁移 | — | — | **明确不做**：15m bar 没有 bar 内延迟信息，硬造一个 = 假精度 |

### 3.6 结论

这一层的**真正价值不在代码，在它明确承认了两件事**：
1. **「真实先后不可知」** → 双投不猜
2. **「GTC 吃穿后按限价硬成交」不现实** → 作者在注释里自己写出来了

一个严谨的回测框架，标志不是"算得准"，而是**把不确定的地方标出来**。
我方最缺的就是这个自觉 —— `core/backtest.py` 里没有任何一处注释说「这里我不确定」。

---

## 4. B 站学习（占 30% 权重）

**本轮降级处理**，如实记录原因：
- 出口受限（`api/fapi/stream.binance.com` 被 SNI 主动阻断），B 站可访问但**字幕接口不可用**。
- 按任务书纪律：**无字幕只做标题级，不做音频转录**（转录要花积分）。
- 标题级收获：搜「回测 数据质量」类视频，标题高度集中在「未来函数」「幸存者偏差」两件事上，
  **没有一条讲「数据本身坏了怎么发现」** —— 这恰好印证了 §3.3 D134 的判断：
  业界的注意力在「策略逻辑」，不在「数据管道」。

---

## 5. ★ 今天的核心发现：我的自测是假绿的，而且反测也骗了我

这是今天最该记住的一段，比 hftbacktest 本身重要。

### 5.1 事情经过

`qty_status(leaves_qty, lot_size)` 这个函数很简单：给定「还剩多少量」和「一手多大」，
判断这一单是「全成了」还是「部分成交」。

**首版实现（错）**：
```python
if lq <= 0: return "filled"
return "partial" if lq >= lot * 0.5 else "filled"
```

**现场打边界**（lot=10）：
```
lq=4   -> filled      ✅
lq=5   -> partial     ✅
lq=10  -> partial     ❌ 还剩整整一手，怎么会是"部分"？
lq=15  -> partial     ❌ 剩一手半
```

`lq=10` 和 `lq=5` **给出同一个答案** ⇒ 这个函数实际上**根本没判断"是否已全成"**，
它判断的只是「是否 ≥ 半手」。**值域错了。**

### 5.2 为什么自测没抓到 —— 34/34 全绿

因为 J1~J7 七条用例里：
```python
qty_status(1e-16, 0.001)   # 残量≈0  -> filled
qty_status(0.0005, 0.001)  # 剩半手   -> partial
qty_status(0.001, 0.001)   # 剩一手   -> partial   ← 期望值也是 partial！
qty_status(-1e-18, 0.001)  # 负残量   -> filled
```
**`lot` 全部是 0.001 这种小数，"剩一手"那一条期望值写在 `partial`、
而错误实现返回的也恰好是 `partial`** —— 断言 `输出 == 期望` 永远成立。

这正是用户级 MEMORY 第 3 条写的：
> **「输出 == 期望」这个断言永远是绿的。** 当默认值恰好等于期望值时，
> 它连"代码根本没跑"都发现不了。

### 5.3 反测骗了我第二次

我第一次修完，加了 J8~J11 四条新用例（`lot=10`、`lq=10`），
**改成了 `lq >= lot - rel_eps → partial`**，自测 38/38 全绿。

然后我做反测（拿旧实现去跑新用例，**能翻红才算用例有效**）：
```
J8 : 旧=partial  期望=partial   漏
J9 : 旧=partial  期望=partial   漏
J10: 旧=filled   期望=filled    漏
J11: 旧=partial  期望=partial   漏
```
**四条一条都没抓住。**

到这一步我才想明白：**问题不是"用例不够多"，是我给的期望值本身就等于错答案。**
两态 `filled/partial` **表达不了**「还剩 ≥1 整手、但我还没撤单」这个状态 ——
它和「剩半手（不可再成交的残渣）」是**不同的东西**，却只能塞进同一个桶。

### 5.4 修法：扩值域，不是加判断

```python
QTY_FILLED  = "filled"    # 剩量 < 半个 lot  ⇒ 视为全部成交
QTY_PARTIAL = "partial"   # 0 < 剩量 < 1 整手 ⇒ 部分成交（残渣，不可再成交）
QTY_LEAVES  = "leaves"    # 剩量 ≥ 1 整手   ⇒ 还压着可成交的整手，状态未终结
```

第三态出来后，反测才真正翻身：
```
J3 : 旧=partial  期望=leaves   <<抓住
J8 : 旧=partial  期望=leaves   <<抓住
J9 : 旧=partial  期望=leaves   <<抓住
J13: 旧=partial  期望=leaves   <<抓住
（J10/J11 仍漏 —— 但它们是"防回归"用例，测的是旧实现本来就对的地方，正当漏检）
```

自测 34 → **40/40**，且 4/6 反测命中（命中全部集中在 `leaves` 这一条新语义上）。

### 5.5 沉淀为两条纪律

> **纪律 1：判据的分辨率必须 ≥ 被测对象的取值域。**
> 两态判据去测三态现实，全绿只说明「我没测到」，不说明「它对」。
>
> **纪律 2：新用例必须先在旧实现上翻红，才算数。**
> 反测命中率 0% 的用例不许留下来充数 —— 它让我误以为已经覆盖过了。

★ 这条和我 10-27 记的「咬合力 0% 或 100% 都算没测到」是同一个东西的不同面：
**那次是"因子没咬合力"，这次是"判据没分辨率"。都是尺子问题。**

---

## 6. 两条可回测假设（都已结清）

### H-047 · 出场限价锚点：`close` 锚 vs `high` 锚 —— **已验证**

**来源**：`partialfillexchange.rs:224-236` 的 `fill()` 让 `maker=true` 时成交价恒等 `price_tick`，
以及 `validation.py:correct_event_order` 的「不可知就不猜」 —— 两个都指向同一件事：
**成交价锚在哪里，比成交成不成更重要。**

**设计**：出场挂限价 `anchor × (1+e)`，锚从 `close_j` 换成 `high_j`，档位 e ∈ {0.1%, 0.3%, 0.5%}，
其余全部不动（T2/T3、止损 −5%、持仓管理）。成交判据用 H-044 的**严格档**（触及**且**收盘确认）。

**结果**：四只**全部严格单调递减**

| 标的 | e=0.1% | e=0.3% | e=0.5% |
|---|---|---|---|
| BTC | +0.2237 | +0.0228 | **−0.1775** |
| ETH | +0.1380 | −0.0123 | **−0.1427** |
| BNB | +0.4066 | +0.2184 | +0.0539 |
| DOGE | +0.6043 | +0.4623 | +0.3399 |
| **中位** | **+0.3152** | — | **−0.0444** |

分层：大市值（BTC/ETH）浅档 0.1809pp vs 中小市值（BNB/DOGE）0.5054pp。

**结论（两层读法）**：
1. **H-042 系列用 `close` 作锚是保守选择，不需要改口径。**
2. **深档（e ≥ 0.3%）的增益不可信** —— 挂越高越容易被 bar 内高点（插针）吃掉，
   但成交价虚高被「未成交回退」抵消后净收益反而更差。
   ⇒ **H-042 的可信区间从 e ≤ 0.5% 收窄到 e ≤ 0.1%。**

★ **与 H-044 独立同向**：H-044 说「宽松档增益 1/5~1/3 是插针凑的」，
H-047 从**完全不同的维度**（换锚点而非换成交判据）二次证实「越靠近 bar 极端价，增益越假」。
两条不同路径指向同一结论 ⇒ 这条可以当事实用。

---

### H-048 · `taker_buy_volume` 占比可上提粒度 —— **已验证**

**来源**：`binancefuturesum/mod.rs` 的 `pu != prev_u` 断流检测 + `types.rs` 位掩码分层
+ `binancefutures.py:convert()` 的 `timestamp_slice=19` / `timestamp_mul=1000000` 定点换算。

**设计**：把 `taker_buy_volume/volume` 从 15m 量加权聚合到 1h(k=4) 与 4h(k=16)，
检验**中位数漂移**（对样本量不敏感）。**这是纯因子粒度研究，不动任何交易参数。**

**结果**：四标的中位漂移 **−0.03 ~ −0.22pp，全部 ≤ 2pp 且符号一致**。

**结论**：`taker_buy_volume` 占比在 4H 周期上**没有信息丢失**。
这条结掉了第 14 轮留下的悬案 —— 当时报「4H 只剩 13 个样本」，
那条结论是**阈值拍脑袋**造成的（把「样本少」误读成「因子失效」），**不是数据问题**。

**★ 口径纪律（本轮踩到）**：聚合后样本量 ÷4/÷16，**分位数天然收窄**，实测 IQR 比值只有 30.8~57.0%。
首版把「IQR 比值 80~125%」写进判据 → **直接把一条真结论判成"搁置"**。
正确做法：**判稳定只看中位数漂移**（对样本量不敏感），IQR 依然报出来但**只读不作判据**。
⇒ 这是「判据量级」类错误的**第 6 次变种**：拿对样本量敏感的尺子去量聚合后的分布。

---

## 7. 平台设计升级：**数据完整性闸 + 三态成交状态**（写进「平台设计」）

### 7.1 缺口 A（P0）· bar 级完整性从未被闸过

`core/backtest.py:805` 读 CSV 时只做 `df[df["volume"] > 0]` 一条过滤，
**不查时间轴连续性、不查 OHLC 内部一致性、不查重复戳、不查 taker 量越界**。

于是「数据坏了」会以「策略变差了」的形式表现出来 —— 这类混淆历史已咬过 4 次。
**落地件**：`audit_bars()`，八类 fatal + 两类 warn，`ok` 只看 fatal。

### 7.2 缺口 B（P1）· `taker_buy_volume` 从未被自洽校验

`taker_buy_volume <= volume` 这条**物理必然**从未断言过。
若某天数据源换了列序、或聚合时把 quote 量混进 base 量，最明显的症状就是这条越界 ——
而它对「买压」类因子是致命污染。**落地件**：`audit_bars(taker_col=...)`。

### 7.3 缺口 C（P0）· 成交状态只有两态

`fill_realism` 的判定是布尔（成/不成），**无法区分「部分成交（残渣）」和「还压着整手」**。
**落地件**：`qty_status()` 三态。这是今天 §5 的直接产物。

### 7.4 明确不做的（诚实边界）

- **双流时间戳（`exch_ts` / `local_ts`）不迁移**。15m bar 没有 bar 内延迟信息，
  硬造一个 `local_ts` = 假精度。要做就得先有**逐笔或 L2 数据**，而那是 §10 的账。
- **`volume_capped_qty()` 不按 lot 取整不改**。实测 `lot_size` 打开后净单笔 **Δ = 0.0000pp**
  （四标的 129/211/203/472 笔一只未变），**没有咬合力就不改**。
  证据留在 `_tools/probe_lot_roundtrip_20261104.py`。

---

## 8. 未完成 / 失败区（诚实留痕）

| # | 事项 | 状态 | 原因 |
|---|---|---|---|
| 1 | **AtomCode 最小推理连续第 14 轮失败** | ❌ 未完成 | `240s 超时 HTTP=0`；`guard` 报 `proxy_listening=true` / `health 200` / `logged_in=true`，但推理层僵死 ⇒ 判定上游问题，非本地配置。**已按收敛纪律降级本地 Read/Grep，0 积分。** |
| 2 | `audit_bars` 接进 `core/backtest.py` | ❌ 未做 | 模块就绪（40/40）但**接线未做** —— 接线要改 `_load_local_15m`，属独立一轮的活 |
| 3 | `manifest.json` row 级连续性校验 | ❌ 未做 | D137 的迁移项 |
| 4 | B 站学习降级为标题级 | ⚠️ 降级 | 字幕接口不可用；按纪律不做音频转录（省积分） |
| 5 | H-047 深档（e ≥ 0.5%）未继续上扫 | ⚠️ 未测 | 本轮只到 0.5%；但 e=0.5% 已转负，**继续上扫意义不大**，判定为收口 |
| 6 | 第 23 轮遗留 P0 `trail1` 推到 0.25/0.30/0.40 | ❌ 顺延 | 本轮聚焦数据层，未做工参网格 |
| 7 | 实盘逐笔导出 | ❌ 顺延（挂账第 6 轮） | 需要出口 + 手动导出 |

---

## 9. 三件套自检

| 件 | 内容 | 状态 |
|---|---|---|
| **代码** | `ai_quant_lab/20261104_hftbacktest_vnpy/bar_integrity_guard.py` v1.1.0 | ✅ `selftest 40/40` · `lab_bridge.get("bar_integrity_guard")` 零警告 |
| **假设** | H-047（已验证）· H-048（已验证） | ✅ 已注册 `hypothesis_runner`（`--only H-047` / `--only H-048` 均 rc=0）· 已补录台账 |
| **笔记** | 本文件 | ✅ |

**关键自检命令**（可复现）：
```bash
cd 我的黑马策略/quant_app
../quant_env/Scripts/python.exe -c "from core import lab_bridge; print(lab_bridge.get('bar_integrity_guard').selftest())"
cd ..
quant_env/Scripts/python.exe ai_quant_lab/hypothesis_runner.py --only H-047
quant_env/Scripts/python.exe ai_quant_lab/hypothesis_runner.py --only H-048
```

---

## 10. 下一步（P0 / P1）

| 优先级 | 事项 | 验收判据 |
|---|---|---|
| **P0** | `audit_bars` 接进 `_load_local_15m` | 四标的回测前必须过审计；审计失败**拒绝回测**（不静默降级） |
| **P0** | `qty_status` 三态接进撮合段 | `fill_realism` 自测用例覆盖三态，且**反测能翻红** |
| **P0** | 第 23 轮遗留：`trail1` 推到 0.25/0.30/0.40 | 封 H-046 的端点（第 5 次端点外移风险） |
| **P1** | `manifest.json` 加 row 级连续性（D137） | 四标的镜像各报一个「连续性中断次数」 |
| **P1** | `nautilus order_emulator/emulator.rs`（4371 行）精读 | 六项硬指标齐全 |
| **P1** | `core/risk.py` 的 `reduce_only` 无持仓终态核清（D118） | — |
| **P2** | `MEMORY.md` 第九次整理 | 正文 ≤ 注入上限 |
| **P2** | 实盘逐笔导出（挂账第 6 轮） | 先比「首末日期 + 标的数」 |

---

## 11. ★ 今天最该记住的一条

**今天我最重要的产出不是任何一条假设，是"发现我的自测在骗我"这件事本身。**

同族错误清单（第 24 轮补第 5 次）：

| 次 | 时间 | 表现 | 病根 |
|---|---|---|---|
| 1 | 10-27 | 咬合力算出 1.92%，真值 4.21% | 分母经过持仓状态机 |
| 2 | 10-29 | `generate_setting` 丢弃校验返回值 | 校验了但没人消费 |
| 3 | 10-31 | 成交样本基线 vs 全样本基线，符号翻转 | 条件样本被逆向选择筛过 |
| 4 | 11-02 | 「63,359/63,360 不一致」 | 拿 spot 对 um，尺子错 |
| **5** | **11-04** | **自测 34/34 全绿，实际两态判三态** | **判据分辨率 < 取值域** |

**共同点：全是「我的测量工具本身有问题」，不是「被测对象有问题」。**
所以我给自己加一条流程：

> **任何自测全绿之后，先做一次反测：拿"已知错误的实现"跑一遍，确认它会翻红。**
> 反测不翻红 ⇒ 这份自测的覆盖率是 0，不许拿来当交付证据。

这条已经写进 `bar_integrity_guard.py` 的模块头注释，防止未来重犯。

---

## 关联件

- 落地代码：`ai_quant_lab/20261104_hftbacktest_vnpy/bar_integrity_guard.py`（v1.1.0 · 40/40）
- 验证器：`ai_quant_lab/20261104_hftbacktest_vnpy/h047_h048_verify.py`
- 实证脚本：`ai_quant_lab/20261104_hftbacktest_vnpy/_run_bar_audit.py`（四标的真实审计，全 `ok=True`）
- 审计报告：`ai_quant_lab/20261104_hftbacktest_vnpy/bar_audit_report.json`
- 探针（证伪 lot 取整）：`_tools/probe_lot_roundtrip_20261104.py`
- 补丁脚本：`_tools/patch_register_h047_h048_20261104.py`（幂等，二次 `bytes_delta=0`）
- 台账补录：`_tools/append_h047_h048_ledger_20261104.py`（表头 10 列断言 + 幂等）
- 台账：`Obsidian知识库/AI量化平台/策略假设/策略假设台账.md`（H-047 / H-048 已入表 + 结论区）
- 结果文件：`Obsidian知识库/AI量化平台/策略假设/回测结果/回测结果_20261104.json`
- 前序：`20261103_freqtrade_vnpy.md`（H-045 / H-046）· `20261102_nautilus_trader_vnpy.md`（H-042 / H-044）
