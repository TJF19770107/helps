---
日期: 2026-10-22
仓库: freqtrade（#7 轮 · 二刷，改读撮合仿真层）
核心文件: freqtrade/optimize/backtesting.py（1977 行，撮合/成交价/撤单的唯一实现）
副文件: freqtrade/exchange/exchange.py（4380 行 · create_order / 滑点常数 1261 / 精度）
轮次: 第 12 轮
tags: [AI量化平台, 夜学, 代码拆解, 撮合回测, 部分成交, 跳空止损]
---

# 20261022 · freqtrade · optimize/backtesting.py

## 0. 一句话结论
> freqtrade 的撮合是**二元**的（`low ≤ rate ≤ high` 即全成，否则全不成），它自己**也不建模部分成交与排队**；
> 但它在两件我们一直忽略的事上比我们诚实：**止损按「开盘是否已穿越」定价（跳空）**、**撤单返回三态而不是布尔**。
> 本轮把这三件事搬进 `core/backtest.py`，并用 4 只标的 6 年全历史证明：**跳空风险在 15m/5% 止损下为 0（835 笔止损 0 次穿价）**
> —— 于是「我们回测乐观」的主因被彻底钉死在**执行成本假设**上，不是止损成交价。

## 1. 这个文件在系统里管什么（架构定位）
- 所属层：**撮合回测层**（唯一负责「信号→成交→资金」的那一层；策略判断在 `strategy/interface.py`，交易所交互在 `exchange/`）
- 上下游：
  - 上游依赖 → `IStrategy`（信号/ROI/止损参数）、`Wallets`（资金与下单量）、`PairLocks`（防重复开仓）、`exchange.get_min|max_pair_stake_amount`（最小名义额）
  - 下游被谁调用 → `commands/backtesting.py`（CLI）、`optimize/hyperopt.py`（**每个超参组合都调这个类**，所以 `backtest_loop` 被注释为「必须保持优化」）、`optimize/analysis`（产出 rejected signals 分析）

## 2. 调用链（文字版时序图）
```
backtest()                                   # 1772 装数据 + 建 Wallets
 └─ _time_pair_generator()                    # 1639 按「时间 → 各 pair」推进
     └─ backtest_loop(row, pair, ...)          # 1519 单根 K 线内的全部撮合
        ① manage_open_orders()                # 1330 挂单超时/改价
            ├─ check_order_cancel()           # 1377 三态：删单 / 撤单 / 保持
            └─ check_order_replace()          # 1408 adjust_order_price 改价 → 撤旧挂新
        ② _enter_trade()                      # 1122 建仓
            └─ get_valid_entry_price_and_stake()   # 1025 限价 clamp（买单 ≤ 当根 high）
        ③ _try_close_open_order()             # 802 入场单成交判定
            └─ _get_order_filled()            # 787 ★ 二元：low ≤ rate ≤ high
        ④ _check_trade_exit()                 # 980 出场判定 → _get_exit_for_signal 854
            └─ _get_close_rate()              # 574 出场价
                ├─ _get_close_rate_for_stoploss()   # 597 ★ 跳空：open 已穿越则按 open
                └─ _get_close_rate_for_roi()        # 651 ROI 夹回 [low, high]
        ⑤ _process_exit_order()               # 836 出场单成交 → 关单 → _run_funding_fees
```

## 3. 关键类 / 函数（签名 + 职责）
| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `_get_order_filled(rate, row)` | 方法 · 787 | `row[LOW] ≤ rate ≤ row[HIGH]` | **全部撮合逻辑就这一行**，无量能/排队/分批 |
| `_get_close_rate_for_stoploss(row, trade, exit_, trade_dur)` | 方法 · 597 | 止损成交价；同根触发时按「最坏路径」推算，且**开盘已穿越则按 open** | 夹回 `[low, high]`，注释明写 "worst realistic case" |
| `_get_close_rate_for_roi(...)` | 方法 · 651 | ROI 成交价；新 ROI 档生效当根按 open，其余 `min(max(close_rate, low), high)` | 处理「开仓当根就触发 ROI」的悖论（抛 ValueError 保护） |
| `get_valid_entry_price_and_stake(...)` | 方法 · 1025 | 限价 `custom_entry_price` 后 **clamp 到当根区间**（买 ≤ high / 卖 ≥ low） | 注释：高于 high 的买单在实盘等于 stop-limit，**实盘不支持** |
| `check_order_cancel(trade, order, current_time)` | 方法 · 1377 | 超时处置，返回 **True/False/None 三态** | True=删整笔交易；False=只撤这张；None=继续挂 |
| `_get_order_filled` 的调用方 `_try_close_open_order` | 方法 · 802 | 成交后 `close_bt_order` + 回调 `strategy.order_filled` | 成交回调是**策略唯一能感知成交的钩子** |
| `manage_open_orders` | 方法 · 1330 | 每根 K 线先处理「挂单生命周期」，再进新仓 | 顺序本身就是设计：**存量优先于增量** |

## 4. 可迁移设计点（本轮 D36~D40）
1. **D36 二元成交必须被显式承认是上限，而不是默认正确。**
   freqtrade 也没建模部分成交 —— 这说明「撮合保真度」不是某个框架的招牌能力，而是**每个平台自己必须交代的缺口**。
   我们以前把它当默认，结果 `PARTIALLY_FILLED` 在回测里从未出现过。**为什么更好**：承认缺口 → 才能给它加开关 → 才能量化「这个缺口值多少钱」。
2. **D37 止损成交价必须走「开盘穿越优先」，而不是止损价。**
   `_get_close_rate_for_stoploss` 先问「开盘是不是已经在 stop 之外」，是则按 open，再夹回当根区间。
   **为什么更好**：`sl_price×(1−slip)` 等于宣称「止损永远精确成交」，把尾部风险从回测里删掉了 —— 而尾部风险恰恰是唯一能打穿账户的东西。
3. **D38 限价报价必须夹在当根区间里。**
   回测允许挂在 `high` 之上的买单，实盘上它就是 stop-limit（语义变了、交易所行为也变了）。**回测允许、实盘不支持的参数，就是回测幻觉的源头**。
4. **D39 撤单必须三态**（删单 / 撤单 / 保持），压成布尔必然写错调用方。
   我们的 `OrderBook.on_canceled` 之前只用二值判断「是否关单」，freqtrade 用一个 `bool | None` 明确区分「整笔作废」与「只撤这一张」。
5. **D40 撮合约束必须自带「咬合力计数」。**
   这是本轮最硬的一条：加了约束却不知道约束有没有咬到，结论就既不能当验证也不能当证伪。
   → `core/backtest.py` 新增 `LAST_FILL_STATS`（rejected/partial/gap 三个计数 + `bite` 合计），**计数为 0 即宣告「本假设未被观测」**。

## 5. 可复用代码片段
```python
# 来源：freqtrade/optimize/backtesting.py:597-616（跳空穿损，逐行本地复刻）
# 用途：止损成交价现实化 —— 开盘已穿越 stop 则按 open 成交，再夹回当根区间

def gap_stop_price(open_px, high, low, stop_price, is_short=False) -> float:
    if is_short:
        raw = max(stop_price, open_px)
        return max(min(raw, high), low)      # 空头对称
    raw = min(stop_price, open_px)           # ★ 多头：open 更低就按 open
    return min(max(raw, low), high)
```
完整实现 + 24 项自测见 `ai_quant_lab/20261022_freqtrade_vnpy/fill_realism.py`
（`bar_fills_limit` / `gap_adjusted_stop_price` / `clamp_limit_price` / `volume_capped_qty` /
`deterministic_reject` / `timeout_decision` / `simulate_bar_fill`，与 `core.backtest` 逐点等价 **diff=0**）。

## 6. B站学习（本日 30% 权重）
- **状态**：按 2026-10-20 定案 **W3 结案** —— 字幕抓取恒空 → **永久降级为标题级**，本轮不再记「未完成」。
- 替代副源（本轮真做了）：去 freqtrade 自带测试里找**反例源**，结果本身就是一条发现 ——
  `tests/optimize/test_backtesting.py` **2956 行 / 49 个 test**，但
  `_get_order_filled` / `_get_close_rate*` / `_try_close_open_order` **被直接引用的次数 = 0**
  （只有 `custom_entry_price` 6 次、`stoploss` 12 次，全是**端到端回测结果**断言）。
  ⇒ **撮合细节连上游项目都没单元测试**，靠「整段回测的收益/笔数」间接钉住。
  这解释了两件事：①为什么改撮合逻辑极易静默出错；②为什么我们自己的 `selftest_fill_realism()` 必须存在 ——
  **别人不测的地方，就是我们要自己测的地方**（本轮 10 项断言里 F1「全关零退化」正是这个用途）。

## 7. 对黑马策略的启发（必须落到具体动作）
- **假设 H-024（已证伪）**：止损按跳空穿价成交后，4 只标的净额单笔均值应下降 ≥0.02pp。
- **怎么验**：同策略同费率，只切 `gap_stop` 一个开关；咬合力 = 跳空笔数 ÷ 止损笔数。
- **实测**：4 只标的 6 年全历史 **835 笔止损 / 0 笔跳空穿损 / Δ 全 +0.0000pp** → **已证伪**。
  ⇒ 台账里 H-010 那句预判成立：**「乐观偏差的主因是执行成本假设，不是止损成交价」**。
  这决定我们把有限时间继续投在**手续费/滑点/maker 成交率**上（H-021/H-022 那条线），不再纠结止损价。
- **改哪一行**：`core/backtest.py` 止损分支 → 新增 `gap_stop` 开关（默认关，零退化）；新增 `participation`（部分成交）、
  `reject_prob`（拒单）两个开关 + `selftest_fill_realism()` **10/10**。
- **H-023 补档（P0 结清）**：追加 `25/20/12`、`30/25/15` 两档重跑 → **4 只全选最松档 `30/25/15`（端点第二次外移）**，
  样本外 3/4 不下降（BTC 0.6028→1.7425 / ETH 0.8263→2.5727 / BNB 1.1740→1.2539 / **DOGE −0.9418→−1.2141 恶化**）。
  ⇒ 仍只能写「存在内部最优、方向偏松」，**不能写「越松越好」**；真实最优在 `30/25/15` 与 `let_run` 之间。

## 8. 未完成 / 失败区（诚实留痕）
- **AtomCode 通路连续第 2 轮失败**：`proxy_down` → 后台拉起 → `/health` 200 → 推理 **HTTP=0 / 240s 超时**；
  杀掉僵死 `atomcode.exe`（2 个 PID）后直接 curl 端点仍 **000 / 100s**、再试 **000 / 60s**。
  `logged_in=true`、到期 2026-10-26 → **非额度问题，是 CLI 串行锁/推理层僵死**；
  `~/.atomcode/` 下只有 `logs/ atomcode.log`（最后写入 2026-08-11），**无锁文件可删**。
  ⇒ 全程降级本地 Read/Grep，**0 积分，任务未中断**。下轮前置：先 `taskkill /IM atomcode.exe /F`，仍 000 则查 `atomcode.exe --version` 自检二进制是否损坏。
- **H-024 的观测是「真实零」而非「未观测」**：判据已在台账口径注解里写明（市场属性类 vs 模型参数类）。
  但**边界**：本轮只测 `5% 硬止损 + 15m`；换成 1m 或 2% 止损，跳空结论必须重测，不可外推。
- **H-023 最优点仍未定位**：端点第二次外移，说明 tp_tiers 单调性在 `30/25/15` 处**仍未触顶**；
  DOGE 反向恶化说明「单调」在低波动标的上不成立 → 下一轮需 `40/32/20` + 分标的结论。
- **P0 #3 未做**：`manifest_min` 尚未接进假设回测链（跑完自动落 manifest），仍是手工调用。
- **滑点系数仍未实盘标定**（挂账第 4 轮）：`p.slippage=0.05%` 是拍的，不是标定的。

## 9. 三件套自检
- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：`ai_quant_lab/20261022_freqtrade_vnpy/fill_realism.py`（自测 **24/24** + 与 core **diff=0**）
      · `quant_app/core/backtest.py`（`gap_stop`/`participation`/`reject_prob` + `selftest_fill_realism()` **10/10**）
      · lab_bridge 装载成功：`lab_bridge.get('fill_realism')` → module，零警告
- [x] ③ 策略假设已追加进 [[策略假设台账]]：**H-024 已证伪** + **H-023 补档 6 档**（读回确认，台账 144 行）

## 10. 成本与技能
- 本次花费积分估算：**0**（AtomCode 全程不可用 → 纯本地 Read/Grep + quant_env 本地运算）。
- 顺手修掉一个回写器真 bug：`hypothesis_runner.update_ledger` 原来用 `write_text("\n".join())` → **每次回写把 CRLF 刷成 LF**，
  已改为「先读字节判行尾 → 按原行尾写回」，并新增 `eol` / `bytes_delta` 回执（两次回写 `bytes_delta=0` 证幂等）。
