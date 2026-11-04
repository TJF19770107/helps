---
日期: 2026-10-11
仓库: hftbacktest（主·#8/12 · nkaz001）· B站（副·降级：无字幕可抓）
核心文件: hftbacktest/src/backtest/evs.rs（事件集）· backtest/mod.rs（主循环）· backtest/order.rs（OrderBus）· backtest/models/latency.rs · backtest/models/fee.rs（Rust 核心）· py-hftbacktest/hftbacktest/stats/metrics.py（Python 指标）
轮次: 第 5 轮
tags: [AI量化平台, 夜学, 代码拆解, hftbacktest, 延迟建模, 回测真实性]
---

# 20261011 · hftbacktest · 撮合/延迟/成交口径（Rust 核心）

## 0. 一句话结论

> **hftbacktest 把「延迟」当成架构，而不是参数。**
> 它给每个资产开 **4 条带时间戳的事件流**（本地行情 / 本地订单 / 交易所行情 / 交易所订单），
> 主循环每次取**时间戳最早**的事件处理 —— 事件之间的**时间差本身就是延迟**，
> 无需在策略代码里到处写「打个折」。配套三条同样干净的设计：
> **① 拒单用「负延迟」表达**（与正常成交走同一通道，不是散落的 if-else 错误分支）；
> **② 手续费毛/净两套账**（`equity_wo_fee - fee`），让「收益来自 alpha 还是幸存于费率」一眼可见；
> **③ 「回测-实盘差距」本身就是要交付的东西**（README：既不许过度悲观，也不许过度乐观）。
>
> 我们 `core/backtest.py` 默认 `entry_on="close"`（信号当根收盘价成交）= **零延迟穿越**，
> 且滑点是**拍脑袋常数** —— 正是它批判的对象。本轮把这个差距**量化并归因**。

---

## 1. 这个文件在系统里管什么（架构定位）

| 项 | 结论 |
|---|---|
| 仓库结构 | **Rust 核心（`hftbacktest/src/`）+ Python 绑定（`py-hftbacktest/`，Numba JIT）+ 连接器（Binance Futures / Bybit）** 三层 |
| 所属层 | **撮合回测层（成交仿真 + 延迟/费用建模）**；`live/` 兼执行层 |
| 本质 | 用 tick-by-tick 级 L2/L3 盘口做「你的单真的成交得到吗」的成交考验 |
| 上游依赖 | 历史订单簿（L2 Market-By-Price / L3 Market-By-Order）+ 逐笔成交；`LatencyModel` / `FeeModel` / `QueueModel` 可插拔 |
| 下游调用者 | `backtest/mod.rs::Backtest`（Python 侧 `hbt.elapse/submit/cancel/wait_order_response`）；`live/bot.rs` 把**同一套算法**接实盘 |
| 本次主攻文件 | `evs.rs`（62 行，事件集）· `mod.rs`（主循环，约 1900 行）· `order.rs`（订单总线）· `models/latency.rs`（延迟模型）· `models/fee.rs`（费用模型）· `stats/metrics.py`（指标） |
| 同类对标 | vnpy 事件引擎（单队列、即时投递）；nautilus（消息总线 + 时钟）；freqtrade（bar 级、无延迟概念）。**hftbacktest 的差异点：延迟与队列位置是一等公民** |

---

## 2. 调用链（文字版时序图）

**主循环（`mod.rs::goto`，约 755-863）**
```
hbt.elapse(duration)
  → goto(target_time, side)
      loop:
        ┌─ 取「下一个最早事件」：min(本地行情流, 本地订单流, 交易所行情流, 交易所订单流)
        │   （每条流各自按时间戳有序；取最早 = 时间戳最小的那一条）
        ├─ 若事件时间 > target_time → 停（时钟推进到目标时刻）
        ├─ 分发事件：
        │    · 交易所行情  → 更新盘口/价格、撮合 resting 订单（含队列位置）
        │    · 交易所订单  → 订单确认/成交/拒单回报（此路径的到达时刻 = 本地时间 + 下单延迟）
        │    · 本地行情/订单 → 策略可见的事件
        └─ 循环
```
**延迟如何涌现**：
```
策略在「本地时间 T」发单
  → 订单带时间戳 T 进入 OrderBus
  → 交易所实际收到于 T' = T + order_entry_latency
  → 成交回报于 T'' = T' + order_response_latency
  → 策略在 T'' 才看得到「成交」事件
★ 延迟 = 这几条流的**时间戳之差**，被主循环取最早事件的顺序**自动**兑现，
   不需要在策略里写「time.sleep(latency)」。
```

**拒单（`order.rs::OrderBus`）**
```
submit(order) → 若模型判定被拒 → 仍作为一条「订单事件」投递，但延迟为**负值**
  （|负延迟| = 收到拒单通知的延迟）→ 与正常成交回报走**同一条**消费路径
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `EventSet` / `Event` | struct | 每资产 4 条事件流 + 时间戳；`evs.rs:7-63` | 本地/交易所**时间分离**的载体 |
| `Backtest::goto` | fn | 时钟推进到目标时刻，多流按时间戳合并处理 | `mod.rs:755-863`，核心循环 |
| `Backtest::submit_order` / `cancel` | fn | 发单/撤单，写入 OrderBus | 带本地时间戳 |
| `OrderBus` | struct | 订单在总线上按到达时间投递 | `order.rs` |
| `trait LatencyModel` | trait | 延迟可插拔：`ConstantLatency` / `IntensityLatency` / 自定义 | `models/latency.rs:14-20` |
| `FeeModel` / maker-taker | trait/enum | 按名义/数量/笔计费，maker/taker + 方向性 | `models/fee.rs:47-153` |
| `Stats` 指标插件 | struct | 逐笔 record，插件式指标；**费用单独记账** | `stats/metrics.py:43,96,185` |
| `feed_order_latency` | py helper | 由行情延迟推断下单延迟 | `data/utils/feed_order_latency.py` |

---

## 4. 可迁移设计点（逐条写「为什么好」）

1. **延迟是架构层的时间戳算术，不是事后打折。**
   为什么好：延迟一旦退化成「在收益上乘个 0.999」，就再也无法区分
   「是滑点吃掉了收益，还是时点错了、还是根本没成交」。放进事件流里，
   **每个成因都能被单独归因** —— 这正是我们 `ablation_report` 能拆出
   「入场时点 / 出场时点 / 跳空 / 动态滑点」四笔账的原因。

2. **拒单走同一通道（负延迟），而非错误分支。**
   为什么好：真实世界里「没成交」是**常态**而不是异常。把它做成错误分支，
   就会诱导开发者在回测里「当作没发生」，从而系统性高估成交率。我们落成
   **「执行根成交量门槛 → 本次不入场」**（`min_volume_ratio`），语义等价。

3. **手续费毛/净两套账（`equity_wo_fee - fee`）。**
   为什么好：黑马策略胜率仅 16~21%、换手高 —— 费率是净收益最大敏感项。
   不拆毛净，永远不知道收益来自 alpha 还是「幸存于低费率假设」。

4. **可插拔的费用/延迟模型（maker/taker + 方向性）。**
   为什么好：一套接口覆盖现货、期货、股票（印花税）；换交易所/换品种只换模型，
   不动主循环。我们落成 `FeeSchedule` / `SlippageModel` 两个可替换数据类。

5. **「量化回测-实盘差距」是第一性目标，且差距必须可归因。**
   为什么好（本轮最大收获）：它把「回测可信度」从**口号**变成**可交付物**。
   我们没有 tick/盘口，但**同一哲学在 bar 级仍成立**：把结构性时点（无自由参数，
   可当事实）与执行成本假设（有自由参数，只能报区间）**分层报告**，
   不许用「未标定的系数」冒充既成事实。

> **搬不动、如实记录的部分**：`depth/*.rs`（L2/L3 盘口重建，`fuse.rs` 1361 行）、
> `models/queue.rs`（1366 行，队列位置成交模型）—— 这是它的核心竞争力，
> 但**我们只有 15m OHLCV，没有盘口**，现阶段做不了。不假装能做。

---

## 5. 可复用代码片段

**A. 转义感知的 markdown 表格行切分（本轮真事故的修复，普适）**
```python
# 来源：本平台 ai_quant_lab/hypothesis_runner.py（2026-10-11 修复）
# 用途：回写台账时，单元格内的 markdown 转义竖线 `\|`（如 `\|Δ\|`）
#       不能被当作列分隔符，否则列号顶偏 → 状态被静默写进「止损」列。
import re

_ROW_SEP = re.compile(r"(?<!\\)\|")   # 只切「未被反斜杠转义」的竖线

def split_row(ln: str) -> list[str]:
    return _ROW_SEP.split(ln)          # 往返幂等：'|'.join(split_row(x)) == x
# 安全闸：写回前断言列数 == 表头列数+2，异常行**大声跳过**而非静默错位
```

**B. 延迟的现实化「浮动滑点」（bar 级近似，来源 hftbacktest 的自适应滑点思想）**
```python
# 来源：本平台 ai_quant_lab/20261011_hftbacktest_vnpy/latency_fill_model.py
# 用途：用「波幅 + 相对成交量」给每根 bar 算一个滑点 bps，替代常数滑点。
#       系数未标定 → 只用于**相对归因**，绝对值必须报区间。
def slippage_bps(high, low, close, vol, med_vol, side, taker_buy):
    volatility = (high - low) / close                 # 当根相对波幅
    liq = 1.0 if med_vol <= 0 else (vol / med_vol)    # 相对成交量
    imbalance = 0.5 if taker_buy is None else taker_buy  # 主动买占比（方向性）
    base = base_bps
    extra = k_vol * volatility * 1e4 * (1.0 + k_liq / max(liq, 1e-9))
    # 卖出更差（-），买入更差（+），方向性修正
    return base + extra * (1.0 + (2 * imbalance - 1) * (1 if side == "buy" else -1))
```

---

## 6. B站学习（本日 30% 权重 · 本轮降级）

- **状态：降级为「标题 + 目录级 + 外部资料」，未取得可抓字幕的 B 站视频。**
  原因：无登录态 / 无字幕 API，B 站视频页无法在零成本前提下抓到 CC 文本。**不做音频转录**（零成本底线）。
- **可核验的外部素材（已实测可达，非 B 站）**：
  - `opensourceprojects.dev`《The Backtesting Problem Nobody Talks About: Your Orders Don't Fill Instantly》
    —— 明确复述 hftbacktest 哲学：「**回测必须既不过度悲观也不过度乐观**」「**验证先于优化**：
    先能重放一段实盘期并与之吻合，再谈过拟合」。★ 本句已直接进平台设计的诚实边界。
  - CSDN《HftBacktest 实战案例：基于订单簿不平衡的做市策略》—— 列出三类延迟
    （行情延迟 / 订单进入延迟 / 订单响应延迟）与我读到的 `models/latency.rs` 一致，可交叉印证。
  - GitHub `cognenzo/hftbacktest` 镜像 README —— 给出最小示例
    `hbt.elapse(100_000)` + `submit_sell_order(... GTX)` + `wait_order_response(...)`，
    印证「**所有订单请求视为同一时刻发出 → wait_order_response 等到回报收到**」这一时序语义。
- **蒸馏要点（待代码验证，暂列）**：做市策略的年化/夏普/回撤数字（CSDN 引用 15-25% / 夏普 1.5-2.5）
  **一律当假设**，与我们无关（我们不做市、无盘口），**不得进结论区**。
- **明日补**：若接上 B 站登录态，优先抓「vnpy 事件引擎」「量化回测滑点/延迟」两类有 CC 的视频。

---

## 7. 对黑马策略的启发（已落成具体动作）

| 假设 | 怎么验 | 结论 |
|---|---|---|
| **H-009**：成交口径从「信号当根收盘价」改为「次根开盘 + 延迟 1 根 + 自适应滑点 + 跳空穿越止损 + 信号出场延迟 → 次开」后，含成本总收益与单笔均值**显著下降** | `latency_fill_model.run_policy_backtest(OPTIMISTIC_CLOSE vs REALISTIC)`，4 只 15m 全历史 | **已验证**：4/4 总收益下降。BTC 219.3%→116.3%（−103.0pp）、单笔 2.006%→1.655% |
| **H-010**：**跳空穿越止损**（开盘已破止损价 → 按开盘价成交）是系统性低估的成本项，占比 ≥5% | 标记 `gap_through`，统计止损单中占比（4 只全历史） | **已证伪**：占比 **0.00%（0/840）**。15m 加密单根跳空 >5% 概率极低 → 「止损按 bar 边界价成交」的乐观化**可忽略** |
| **H-011**：回测乐观偏差的**主因**是「执行成本假设」（滑点），**不是**「成交时点延迟」 | `ablation_report` 阶梯消融：结构性项（无自由参数）vs 成本项（k_vol）之比 | **已验证**：3/4 满足「结构 ≤100pp 且成本 ≥3×结构」。BTC 成本 ×344、BNB ×3.7 → **主因是滑点，不是时点** |

**落到具体动作**：
- **P0**：`core/backtest.py` 增 `fill_policy` 入参，默认从 `OPTIMISTIC_CLOSE` 改 **`NEXT_OPEN`**
  —— 一行默认值就能消掉「零延迟穿越」，等价性自测已就位（diff=0）。
- **P0**：`core/report.py` 双列输出**毛收益 / 净收益 / 费率占比**（对标 L3）。
- **P1**：用**实盘成交日志**标定 `k_vol` —— 这是把「区间」收敛成「点估计」的唯一途径。
- **不做什么**：盘口级成交仿真（无 tick 数据）；不做市。

---

## 8. 未完成 / 失败区（诚实留痕）

1. **B 站字幕未取得**（无登录态/无字幕 API）→ 已按纪律降级为「标题 + 目录级 + 外部资料」，明日补。
2. **`k_vol` / `base_bps` 未经实盘成交标定** → D/E 两栏绝对值**不可当事实**，只报区间与相对归因。
3. **无 tick/盘口数据** → 队列位置成交仿真（hftbacktest 核心）**做不了**，明确不做。
4. **H-010 被证伪** —— 这是**硬信息而非失败**：它把「乐观偏差的主因」从「止损成交价」正确地
   排除掉，指向「执行成本假设」。（本行按纪律保留，反直觉结论本身就是价值。）
5. **DOGE 系统性亏损**（各口径皆负）→ 泛化性存疑，不为学习进度而掩盖。
6. **本轮修复了一个真 bug**：台账回写器按未转义 `|` 切列 → H-011 列错位（`已验证` 被写进「止损」列）。
   已修：改**转义感知切分 + 列数断言（异常行大声跳过）**，并重建 H-011 行、补幂等自测。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：
  - `ai_quant_lab/20261011_hftbacktest_vnpy/latency_fill_model.py`（自测全通过，含与 `core.backtest` 等价性 diff=0）
  - `ai_quant_lab/20261011_hftbacktest_vnpy/_ablation_study.py`（消融脚本）
  - `ai_quant_lab/hypothesis_runner.py`（回写器转义感知修复）
  - `lab_bridge.get("latency_fill_model")` **加载成功、零警告**
- [x] ③ 策略假设已追加进 [[策略假设台账]]：H-009（已验证）· H-010（已证伪）· H-011（已验证）

---

## 10. 成本与技能

- **花费积分**：**0**（第零步 AtomCode guard=healthy，实测推理走免费档 glm5.3-flash；回测纯本地）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程）；`币安量化数据通路与黑马策略诊断`（本地数据口径 / 回测铁律）
- **没用哪个技能及原因**：B 站相关抓取技能（无字幕可抓，降级）；盘口/队列模型（无数据）
- **沉淀 / 迭代**：修复 `hypothesis_runner.py` 回写器（转义感知 + 列数闸）；新增 `latency_fill_model.py`；平台设计新增 [[AI量化平台_成交现实化层对标hftbacktest设计_20261011]]

---

*建立：2026-10-11 · 汤小龙 · 夜学第 5 轮 · 对标 hftbacktest*
*关联：[[AI量化平台_成交现实化层对标hftbacktest设计_20261011]] · [[20261010_freqtrade_vnpy]] · [[策略假设台账]]*
