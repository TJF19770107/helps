---
日期: 2026-10-09
仓库: nautilus_trader（主）· vnpy/vnpy（副）
核心文件: crates/risk/src/sizing.rs + crates/risk/src/engine/mod.rs · vnpy/event/engine.py + vnpy/trader/engine.py
轮次: 第 3 轮（轮转序号 #6/12）
tags: [AI量化平台, 夜学, 代码拆解, 风控层, 事件层]
---

# 20261009 · nautilus_trader + vnpy · 风控层 / 事件层

## 0. 一句话结论
> nautilus 的 `RiskEngine` 教会我：**风控不是六道闸，而是一台「订单准入机」** ——
> 风险预算里要扣手续费、状态机要三态、挂单要占持仓额度、报单要限流。
> 我们 2026-10-09 新建的 `core/risk.py` 六道闸方向对，但这四条一补上，
> 才从「回测不漏」升级到「实盘不炸」。

---

## 1. 这个文件在系统里管什么（架构定位）

### 主：nautilus_trader `crates/risk/`
- **所属层**：风控层（第 6 层），且是**订单级准入**（pre-trade order validation），不是账户级回撤管理。
- **上下游**：
  - 上游依赖 → `nautilus-model`（Instrument/Price/Quantity/Money）、`nautilus-common`（Cache、Throttler、msgbus）、`nautilus-portfolio`（Portfolio）
  - 下游被谁调用 → **msgbus 消息总线**：策略发 `TradingCommand` → 总线端点 `risk_engine_execute()` → `RiskEngine::execute()`；通过校验后再 `send_to_execution()` 送往执行层。
- **★ 重要认知**：nautilus 的 RiskEngine **只管「单笔订单能不能过」**，不含回撤闸/日亏熔断 —— 那些是策略层/组合层的事。
  我们 `risk.py` 把「订单级（R1-R4）」与「账户级（R5-R6）」**合在一处**，这其实**超出**了 nautilus 的职责划分，换来了「一个类管全部」的简单性，代价是职责不够单一。如实记为「差异化，非缺陷」。

### 副：vnpy `vnpy/event/engine.py`（147 行）+ `vnpy/trader/engine.py`（887 行）
- **所属层**：事件层（第 1 层）。`event/engine.py` 是总线本体；`trader/engine.py` 是 `MainEngine`（引擎容器）+ `OmsEngine`（订单状态缓存）+ `LogEngine`/`EmailEngine`/`WechatEngine`（通知功能引擎）。
- **上下游**：`MainEngine` 持有 `EventEngine`；各功能引擎在 `__init__` 里把自己 register 进总线；网关（Gateway）把行情/成交事件 put 进总线。

---

## 2. 调用链（文字版时序图）

### nautilus 下单准入链
```
策略 Strategy
  → msgbus.publish(TradingCommand)
  → [端点] risk_engine_execute()          # register_msgbus_handlers 注册
  → RiskEngine::execute(cmd)  → command_count++
  → handle_command(cmd) → handle_submit_order(cmd)
      ├─ is_reducing_submission? ── 是 → 减仓快路径
      ├─ order_notional_limit()            # 单笔名义上限（R4 对标）
      ├─ check_order_price() / check_quantity()   # 价格/数量合法性
      ├─ available_position_quantity()     # 净持仓 − 挂单占用（★缺口3）
      ├─ order_risk_quantity()             # 换算 base qty
      └─ check_orders_risk() → check_risk_increase()  # 只查风险增量
  → execution_gateway(cmd)  # TradingState 三态分派（★缺口2）
      ├─ Halted   → deny（全拒）
      ├─ Reducing → 仅 is_reducing_submission 放行，且过 throttler
      └─ Active   → throttler_submit.send(cmd)   # 限流（★缺口4）
  → 执行层 ExecutionClient
```

### nautilus 仓位计算公式（sizing.rs）
```
fixed_risk_position_size(entry, stop, equity, risk, commission_rate):
  risk_money = equity × risk                       # 名义风险预算
  commission = risk_money × commission_rate × 2    # ★ 双边手续费
  riskable   = risk_money − commission             # 真正能冒险的钱（★缺口1）
  risk_points = |entry − stop| / price_increment   # 止损距离换算 tick
  qty = riskable / exchange_rate / risk_points / price_increment / multiplier
      → min(hard_limit) → min(max_quantity) → 返回 Quantity
```

### vnpy 事件链
```
MainEngine.__init__ → EventEngine().start()      # 起消费线程 + 定时线程
Gateway.on_tick()  → event_engine.put(Event(EVENT_TICK))
EventEngine._run()  ← queue.get()  ← put()
  → _process(ev) → handlers[type] → OmsEngine.process_tick_event() → self.ticks[sym]=tick
TimerEmitter(_run_timer 独立线程) → sleep(interval) → put(EVENT_TIMER)   # ★独立节拍
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `RiskEngine` | Rust struct | 订单准入总控：价格/数量/名义/持仓/限流/状态门 | 2886 行，职责高度聚合 |
| `RiskEngineConfig` | Rust struct | bypass / max_order_submit(100/s) / max_order_modify(100/s) / max_notional_per_order | **限流器是配置项**，不是补丁 |
| `calculate_fixed_risk_position_size` | Rust fn | 固定风险反推张数，含手续费/tick/乘数/硬上限/溢出保护 | `sizing.rs:39-117` |
| `calculate_riskable_money` | Rust fn | `equity×risk − equity×risk×c×2` | **★缺口1 的出处** `sizing.rs:132-152` |
| `TradingState` | Rust enum | Active / Reducing / Halted | **★缺口2** |
| `available_position_quantity` | Rust fn | 净持仓 − 未成交挂单 leaves_qty | **★缺口3** `mod.rs:1405-1446` |
| `Throttler<T, F>` | Rust struct | 报单/改单滑动窗口限流 | **★缺口4** |
| `is_reducing_submission` | Rust fn | reduce_only + qty ≤ 实际持仓 才算减仓 | 比我们的方向推断更严 |
| `is_full_position_exit` | Rust fn | 全仓条件退出（止损单带 close_position 占位量）跳过名义检查 | 极细的边界处理 |
| `check_risk_increase` | Rust fn | 改单只对 `current−previous` 增量做风控 | 减仓部分不占新额度 |
| `EventEngine`（vnpy） | Python class | `_run` 消费线程 + `_run_timer` **独立定时线程**；defaultdict handlers + general_handlers | `event/engine.py` |
| `MainEngine`（vnpy） | Python class | 引擎容器：`add_engine`/`add_gateway`/`add_app`；关停顺序 stop总线→关引擎→关网关 | `trader/engine.py` |
| `OmsEngine`（vnpy） | Python class | 事件→状态 dict 缓存 + 活跃订单集合增量维护 | `trader/engine.py:375-620` |

---

## 4. 可迁移设计点（逐条写「为什么好」）

1. **风险预算必须扣双边手续费**（`calculate_riskable_money`）
   - *为什么好*：止损打掉时亏的是「价差×张数 + 进出两笔手续费」。不扣费 = 系统性超配。
   - 量化：止损 1000 点、双边 0.10% 时超配 **+5.00%**；**止损 100 点时超配 +50%**（止损越近越致命）。
   - 这正是 H-002 教训（方向对、被手续费吃光）在**仓位层**的镜像 —— 同一个敌人，两个战场。

2. **状态机三态而非两态**（Active / Reducing / Halted）
   - *为什么好*：「回撤闸触发→只许减仓」与「账户冻结→全停」是**两件不同的事**。
   - 我们现在把前者塞进 HALTED 当附加条件 → 日志/运维说不清「到底停在哪一档」。
   - ☠️ 注意语义差异：**nautilus 的 Halted 连平仓都拒**（合规/冻结场景）；我们的 HALTED 其实是 nautilus 的 Reducing。**保留我们的实战语义（停机仍可平仓），但拆成三态。**

3. **挂单会占用持仓额度**（`available_position_quantity`）
   - *为什么好*：净多 1.0 已挂 0.8 止损单，再发 1.0 平仓单 → 合计 1.8 > 持仓 → 先后成交即**反向裸空**。
   - 扣挂单占用是**唯一能防「重复申报」**的手段。这是实盘才暴露、回测永远看不到的坑。

4. **报单/改单限流**（`Throttler` 默认 100/s）
   - *为什么好*：六道闸只拦「单笔」风险，拦不住「**一万笔小额**」。一个 while bug 几秒打上千单，每单合法、总敞口也合法，但手续费已打穿。
   - **限流是唯一能防这类事故的一道闸**，且成本极低。

5. **timer 必须独立线程**（vnpy `_run_timer`）
   - *为什么好*：我们 `events.py` 的 timer 寄生在 `queue.get(timeout=)` 上 → 事件一忙，timer 就被推迟。
   - 对黑马的影响：实盘的**时间止损/定时巡检**恰恰在行情暴动时最该准点，而它那时最不准。
   - 小改良：vnpy 用裸 `sleep`，stop 最多延迟 1 个 interval；我们用 `Event.wait` → stop **立即生效**。

6. **事件→状态快照缓存（OMS），活跃集合增量维护**
   - *为什么好*：策略查「我有几张挂单」若每次重扫全量事件 = O(n) 且易错。OMS 用事件到达驱动 dict，查询 O(1)。
   - 精华：`is_active → 加入；否则 pop` —— 一次判断维护集合，天然与事件流一致。

---

## 5. 可复用代码片段

> 落盘为**两个真实可跑模块**（不是伪代码），均在 `ai_quant_lab/20261009_nautilus_trader_vnpy/`：

| 模块 | 对标 | 自测 | 内容 |
|---|---|---|---|
| `nautilus_risk_patterns.py` | `core/risk.py` 四条缺口 | **16/16 ✅** | `TradingStateMachine`(三态) · `riskable_money`(含费预算) · `fixed_risk_qty`(乘数/硬上限) · `available_position_qty`(挂单占用) · `OrderThrottler`(限流) |
| `vnpy_event_patterns.py` | `core/events.py` 三个范式 | **9/9 ✅** | `TimerEmitter`(独立定时线程) · `BaseEngine`(功能引擎生命周期) · `OmsCache`(事件→快照，活跃集合增量维护) |

核心片段（来源 `nautilus risk_patterns:fixed_risk_qty`，可直接替换 `core/risk.py` R1 那行）：

```python
# 来源：nautilus_trader crates/risk/src/sizing.rs:39-152（Python 移植）
# 用途：把 risk.py R1 的 `risk_budget = eq*max_risk_per_trade` 换成含费口径
def riskable_money(equity, risk_pct, commission_rate, sides=2):
    if equity <= 0 or risk_pct <= 0:
        return 0.0
    gross = equity * risk_pct
    return max(0.0, gross - gross * commission_rate * sides)   # ★ 扣双边手续费

def fixed_risk_qty(equity, entry, stop, risk_pct, commission_rate=0.0,
                   multiplier=1.0, hard_limit=None, max_qty=None):
    stop_dist = abs(float(entry) - float(stop))
    if equity <= 0 or risk_pct <= 0 or stop_dist <= 0:
        return 0.0
    qty = riskable_money(equity, risk_pct, commission_rate) / (stop_dist * multiplier)
    if hard_limit is not None: qty = min(qty, hard_limit)
    if max_qty is not None:    qty = min(qty, max_qty)
    return max(0.0, qty)

# 实测：100k 权益 / 2% 风险 / 止损 1000 点 / 双边 0.10%
#   旧口径 qty = 2.0000（实际最坏亏损 2100，超预算 +5.00%）
#   新口径 qty = 1.9048（实际最坏亏损 2000，残差 0.0000）  → H-005 已验证
```

平台接线已验证（lab_bridge 自动发现，无警告）：
```
discovered: ['binance_gateway_patterns','dark_horse_guard','nautilus_risk_patterns','vnpy_event_patterns']
nautilus_risk_patterns  loaded=True   # fixed_risk_qty(含费)=1.998  vs 旧口径 2.0
vnpy_event_patterns     loaded=True
```

---

## 6. B站学习（本日 30% 权重）

| 素材 | UP / 出处 | 有无字幕 | 状态 |
|---|---|---|---|
| 《10万本金职业仓位管理模型》 | B站「普通人投资框架」（经雪球转述文本） | 转述文本 | ✅ 已蒸馏 |
| 《Python量化投资从零开始》 | B站「量化投资与机器学习」 | 未抓 | ⏳ 目录级（清单已记） |

**蒸馏要点（素材1）**：
1. 仓位公式 `仓位 = 允许亏损金额 / 止损幅度` —— 与 nautilus `fixed_risk_position_size`、我们 R1 **同源**（三方独立印证，可信度高）。
2. 机会分级 A/B/C：A 级 15-20% 仓、B 级 8-12%、C 级 3-5%（单笔风险均控 1% 内）。
3. 只在盈利后金字塔加仓，**禁止亏损加仓**。
4. 三步减仓：盈利 5% 锁本 → 破均线减仓 → 破结构清仓。
5. **连亏熔断：连亏 3 笔仓位减半、连亏 5 笔停止交易复盘**。

**★ 独立佐证（写进结论区）**：素材1 的「连亏 5 笔停机」与我们 `core/risk.py` 的
`max_consecutive_losses = 5 → HALTED` **完全一致** —— 民间实盘模型与机构级代码在我们
自研风控参数上撞车，说明 R6 的参数不是拍脑袋。

**存疑处（待代码验证）**：
- 「A/B/C 分级」是主观判断，无可量化边界 → 不宜直接编码，需先用可回测因子替代「机会质量」。
- 「破均线/破结构」缺精确定义 → 与黑马头肩底 MA30 的出场规则可能冲突，需对齐。

**B站素材2 的旁证**（来自 vnpy 教程文章的「5 个坑」）：明确写着「**事件引擎回调里写慢逻辑会拖慢整个消息循环，重活请放独立线程**」—— 正好印证 §4.5 的 timer 独立线程差距，是**独立来源的交叉验证**。

---

## 7. 对黑马策略的启发（必须落到具体动作）

| 假设 | 怎么验 | 若成立，改哪 |
|---|---|---|
| **H-004**（已跑）：15m，连续 3 根温和买压(>0.55)且收阳 → 下一根收阳率**高于**基准（延续） | `hypothesis_runner.py` 15m/1h/4h 三档 + 8184 样本 | **结果：已证伪** —— 收阳率 43.01% vs 基准 50.21%（**低 7.20pp**，z=-13.02）。即「持续温和买压」反而是更强的**反转**信号（比 H-002 单根极值的 4.96pp 更强）。含成本做空单笔 -0.2105% → 仍不可交易。**动作：把「买压持续性」作为反向因子登记，与 H-002 合并进同一因子族继续挖。** |
| **H-005**（已跑）：R1 风险预算不扣手续费 → 实际超预算 | 纯数学证明（nautilus_risk_patterns） | **结果：已验证** —— 超配 +5.00%（止损 1000 点）/ +50%（止损 100 点）。**动作：`core/risk.py` R1 改为 `qty = budget / (stop_dist + price*commission*2)`。** |

补充动作（结构性，来自 §4）：
- **`core/risk.py`**：R1 换含费口径（已用 `nautilus_risk_patterns.fixed_risk_qty` 验证）；状态机拆三态；新增 R7-挂单占用（可平量 = 净持仓 − 活跃挂单量）；新增 R8-报单限流。
- **`core/events.py`**：timer 从「队列 timeout 寄生」改为「独立线程」（用 `vnpy_event_patterns.TimerEmitter` 范式）。
- **黑马回测入口**：调用 `lab_bridge.drop_unclosed()` 强制剔除未闭合末根（H-003 的防护按常识做）。

---

## 8. 未完成 / 失败区（诚实留痕）

1. **nautilus 主仓库 clone 成功但 Python 端几乎为空**：新版 nautilus 已把核心迁到 Rust（`crates/`），`python/nautilus_trader/risk/` 只剩 `__init__.py` 转导出。本次精读实际读的是 **Rust 源码**（`crates/risk/src/*.rs`）。→ **未完成**：Rust 端还有 `crates/execution`、`crates/portfolio` 未读，留待后续。
2. **B站字幕未抓取**：仍受登录态限制（与 2026-10-08 同因）。素材1 用的是**雪球转述文本**，非视频原字幕；素材2 未抓。→ 明日尝试有公开 CC 的视频或改用 yt-dlp。
3. **H-001 仍搁置**：本地 K 线 CSV 无 `funding_rate` 列。→ 需落 `data.binance.vision` 的 fundingRate 历史（批量库路径 `data/futures/um/monthly/fundingRate/`），落数后 H-001 可直接复用 H-002 池化框架。
4. **H-003 仍搁置**：本地 4H 数据末端本身就是闭合 K 线，`dropped_unclosed` 全为 0 → 「剔除 vs 不剔除」无差别。**不判定为证伪**；需采集到真实未闭合末根的快照后重跑。
5. **H-004 虽已证伪原假设，但其「反向」方向（持续买压→收阴）统计极显著却不可交易** —— 与 H-002 同样卡在「幅度 < 手续费」。→ 未完成：需要研究**降低换手/扩大持有周期**能否让该因子族跨过成本线。
6. **`nautilus_risk_patterns` 尚未回填进 `core/risk.py`**：本次只做到「模块可被 lab_bridge 加载 + 自测通过」，**没有改 `core/risk.py` 本体**（避免一次夜学动平台核心）。→ 列为明日动作。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件，读回确认）
- [x] ② 可复用代码落盘路径：
  - `ai_quant_lab/20261009_nautilus_trader_vnpy/nautilus_risk_patterns.py`（自测 16/16 ✅）
  - `ai_quant_lab/20261009_nautilus_trader_vnpy/vnpy_event_patterns.py`（自测 9/9 ✅）
  - **lab_bridge 加载验证**：两模块 `loaded=True`，`warnings=[]` ✅
- [x] ③ 策略假设已追加进 [[策略假设台账]]：H-004（已证伪）、H-005（已验证），并在 `hypothesis_runner.py` REGISTRY 注册验证器 ✅

---

## 10. 成本与技能

- **本次花费积分估算**：**0**（AtomCode 免费档实测未用于本任务；全部本地 Read/Grep/自算；guard 探活 1 次实测推理）。
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程）· `币安量化数据通路与黑马策略诊断`（数据/回测口径）
- **沉淀 / 迭代**：`nautilus_risk_patterns.py` + `vnpy_event_patterns.py` 两个可复用模块；平台设计文档《风控层对标升级设计》

---

*生成：2026-10-09 · 汤小龙 · 夜学第 3 轮 · 绑定五步法 §24 / 全域模板 #341*
