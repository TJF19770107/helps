---
日期: 2026-10-20
仓库: vnpy/vnpy_binance
核心文件: portfolio_gateway.py（2146 行，组合保证金统一网关）
轮次: 第 10 轮
tags: [AI量化平台, 夜学, 代码拆解, 多市场路由, 订单生命周期, G2状态机]
---

# 20261020 · vnpy_binance · portfolio_gateway.py

## 0. 一句话结论

> **订单的「存在」必须早于「发送」；「网络异常」必须与「明确拒单」分开处理；持仓归零也必须推送。**
> 这三件事我在 `live.py` 里一条都没做到 —— 今天把第 1、3 条补上，第 2 条落到订单生命周期台账里。

---

## 1. 这个文件在系统里管什么（架构定位）

- **所属层**：**执行层**（网关层）—— 但它同时承担了**路由层**与**账户/持仓同步层**的职责。
- **它管的是一件事**：同一个组合保证金账户里，**USDT 本位永续（UM）+ 币本位永续（CM）+ 全仓杠杆（MARGIN）三种市场共用一个账户、一套持仓**，需要一个网关把「一个 vt_symbol」翻译成「三条不同的订单端点」。
- **上下游**：
  - 上游依赖 → `vnpy.trader.gateway.BaseGateway`、`RestClient`、`WebsocketClient`、`vnpy.trader.object.{OrderData,TradeData,PositionData,ContractData}`、`vnpy.trader.constant.{OrderType,Status,Direction,Exchange}`、`vnpy.trader.utility.round_to`
  - 下游被谁调用 → vnpy 主引擎（`MainEngine.send_order` → `gateway.send_order`）；事件由 `event_engine` 派发回策略层（`EVENT_ORDER` / `EVENT_TRADE` / `EVENT_POSITION`）
- **我方对照物**：`quant_app/core/live.py`（原 142 行，只有信号、**没有报单入口**）+ `core/risk.py`（876 行，八道闸）。

### ★ 白名单勘误（第 2 次了，必须写下来）
任务卡建议核心文件 `binance_gateway.py` —— **该文件在当前版本已不存在**。
仓库实际拆成四个：

| 文件 | 行数 | 市场 |
|---|---|---|
| `linear_gateway.py` | 1770 | U 本位永续（单市场） |
| `inverse_gateway.py` | 1699 | 币本位永续（单市场） |
| `spot_gateway.py` | 1523 | 现货 |
| **`portfolio_gateway.py`** | **2146（最大，前 9 轮从未读过）** | **三者合一（组合保证金）** |

→ 选最大且未读的那个，且它恰好是「多标的同账户」的真实形状（黑马策略 BTC/ETH/BNB/DOGE 同账户同向持仓）。
**结论：白名单里的「文件名」必须允许过期，但「选文件的原则」不能过期 —— 同层最大、从未读过、与当前痛点同形。**

---

## 2. 调用链（文字版时序图）

### 2.1 连接
```
connect(setting)
 → rest_api.connect(key, secret, server, proxy)     # :518
 → um_md_api / cm_md_api / margin_md_api .connect() # 三个行情 WS 分别连
 → event_engine.register(EVENT_TIMER, process_timer_event)
 → RestApi.query_time() → on_query_time            # 先校时（签名对时间敏感）
 → query_contract() ×3（um/cm/margin）→ on_query_*_contract → gateway.on_contract
 → query_account() ×3 → on_query_{um,cm,margin}_account
 → query_position() ×3 → on_query_*_position → gateway.on_position
 → start_user_stream() → POST /papi/v1/listenKey → on_start_user_stream
 → UserApi.connect(ws_url + listenKey)
```

### 2.2 报单（**这条链是本轮最大收获**）
```
strategy → gateway.send_order(req)                        # :283 转发到 rest_api
 → rest_api.send_order(req)                               # :690
   ① get_contract_by_symbol(req.symbol) → 拿不到就 return ""（**fail-closed**）
   ② orderid = prefix + str(++order_count)
   ③ order = req.create_order_data(orderid, gateway_name)
   ④ gateway.on_order(order)          ← ★ 先把 SUBMITTING 推给本地，**此时请求还没发**
   ⑤ params = {symbol: contract.name, side, quantity, newClientOrderId: orderid, ...}
   ⑥ path = /papi/v1/{um|cm|margin}/order   ← 按 get_market_type(symbol) 路由
   ⑦ add_request(POST, path, callback=on_send_order,
                 on_failed=on_send_order_failed, on_error=on_send_order_error)
 → 三种结局：
    on_send_order(data)              HTTP 200 → orderid 映射交易所 orderId
    on_send_order_failed(status_code) HTTP 4xx/5xx → **明确拒单**
    on_send_order_error(e)          网络异常/超时 → **状态未知**
```

### 2.3 成交回报（两套 schema，共用一条推送出口）
```
WS packet → UserApi.on_packet → 按 e 字段分派
 → "ORDER_TRADE_UPDATE" → on_order(packet)            # 期货（UM/CM）：o 里 s/S/q/z/l/L/t/T
 → "executionReport"    → on_execution_report(packet)# 杠杆：字段平铺，且 CANCELED 时用大写 C
 → 两者都：gateway.on_order(OrderData) + （若 l>0）round_to(l, min_volume) → gateway.on_trade(TradeData)
 → on_disconnected → 立刻 rest_api.start_user_stream() 重建 listenKey
```
**关键细节**：撤单回报的 `orderid` 在 MARGIN 通道用 `packet["C"]`（交易所 ID），其余用 `packet["c"]`（clientOrderId）。
→ 网关必须两边都落到**同一个本地 ID** 上，否则撤单事件的 key 与下单 key 不一致 → 台账出现幽灵订单。

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `MarketType(Enum)` | 枚举 | `UM` / `CM` / `MARGIN` | 与订单端点一一对应 |
| `get_market_type(symbol) -> MarketType` | 函数 | 由 **vt_symbol 后缀**判定市场 | `_SWAP_BINANCE` / `_SPOT_BINANCE` / `_BINANCE`；**默认 return UM（fail-open）** |
| `BinancePortfolioGateway(BaseGateway)` | 类 | 网关门面：`connect/subscribe/send_order/cancel_order/query_*` | `query_account/query_position` 是 `pass`（靠 WS 推送 + 定时查询） |
| `RestApi(RestClient)` | 类 | 全部 HTTP：签名、下单、撤单、查询、listenKey | `sign()` :470 处理 HMAC + 时间戳 |
| `send_order(req) -> str` | 方法 :690 | **先落库 → 再发请求** → 返回 vt_orderid | 找不到合约直接返回 `""`（fail-closed） |
| `cancel_order(req)` | 方法 :753 | 用 `origClientOrderId` 撤单 | 需先 `get_order()` 反查 symbol → 再查合约 → 再路由 |
| `on_send_order_failed(status_code, req)` | 回调 :1150 | HTTP 层拒单 | **可与 `on_send_order_error` 区别对待** |
| `on_send_order_error(exception, ...)` | 回调 :1162 | 网络异常 | **状态未知，不可归零** |
| `on_query_um_position(data)` | 回调 :887 | 持仓快照 → `PositionData(direction=Direction.NET)` | **`if position.volume:` 才推送 ← 上游真坑** |
| `UserApi.on_order(packet)` | 回调 :1425 | 期货订单/成交推送 | 一笔包可能同时含 order 更新 + 增量成交 |
| `UserApi.on_execution_report(packet)` | 回调 :1473 | 杠杆订单/成交推送 | CANCELED 时 orderid 换成 `packet["C"]` |
| `process_timer_event` → `keep_user_stream()` | 方法 :332/:803 | 每 N 秒续 listenKey | listenKey 有效期 30min，超时断流 |

---

## 4. 可迁移设计点（4 条，逐条写「为什么好」）

### D25 · 端点路由下沉到网关，策略层不许知道「市场」
`get_market_type()` 把「这个符号属于哪个市场」收敛成**一个纯函数**，`send_order` 只做一次 `if/elif` 选路径。
**为什么好**：策略/风控层只关心「标的 + 方向 + 数量」，一旦让策略层自己记 `"/papi/v1/um/order"`，换市场就要改策略代码 —— 而策略代码是**最难回归测试**的那部分。路由是**基础设施事实**，不是策略决策。
**我方现状**：`core/live.py` 完全没有路由概念（因为还没有真实 REST 适配器）。今天补的 `submit_order()` 只做到「过闸 + 占额度 + 返回指令」，路由字段留了 `client_order_id`，尚未含 `endpoint` —— **这是已知缺口，写在下面未完成区**。

### D26 · 先落库再发请求（submit-then-request）
`:704-711` 三行的顺序是 `create_order_data` → `on_order(SUBMITTING)` → `add_request()`。
**为什么好**：崩溃点如果落在「已经发出去、还没收到回报」这一瞬间，**本地必须有东西可对账**。
若等回报才创建订单对象，这一瞬间的订单在本地**不存在** → 重启后无法知道「我到底发没发出去」→ 只能靠人工翻交易所流水。
**这也是我方「在途态归零」铁律的另一面**：在途归零只能发生在**收到明确拒单/撤单确认**之后，网络异常时**恰恰不能归零**。

### D27 · 本地订单 ID 直接做交易所幂等键
`newClientOrderId = orderid`（下单）/ `origClientOrderId = req.orderid`（撤单）。
**为什么好**：不需要第二张「本地 ID ↔ 交易所 ID」映射表。映射表是典型**双写不一致**来源（本地有、交易所无；或反过来）。
**我方落地**：`live.submit_order()` 返回的 `order_id` 同时作为 `client_order_id` —— 第一版我把它写成「先 reserve 再 `_next_oid()`」，导致**返回 ID 与 `risk.pending` 的 key 是两个不同字符串**，`release_fill` 永远找不到在途单（额度锁死）。**这是今天自测抓到的真 bug**（见 §8）。

### D28 · 两类失败必须分开：拒单 vs 未知
`on_send_order_failed`（有 `status_code`）/ `on_send_order_error`（有 `exception`）。
**为什么好**：这两种事实的**信息量完全不同** —— 前者是「交易所说我不收」，后者是「我不知道交易所有没有收到」。
把「不确定」当「失败」处理（释放额度）→ 交易所里可能已经有一张活单，本地却认为没有 → **重复开仓**。
把「失败」当「不确定」处理（保留额度）→ 额度永不释放 → 平台把自己锁死。
**正确做法**：拒单 → 归零；未知 → 保留 + 置 `UNKNOWN` + **只能靠对账收口**（`OrderLifecycle.reconcile_missing`）。

### ★ D29（反向案例，从上游的坑学）· 持仓归零**必须**推送
`:920` 与 `:941` 都是 `if position.volume: self.gateway.on_position(position)` —— **平光仓位不推送**。
后果：订阅方持仓簿永远残留最后一笔非零仓位 → 组合敞口（R3）按**陈旧市值**计算 → 闸门越跑越松，且**不会自愈**（下一轮查询依然不推 0）。
**我方落地**：`PositionBook.apply_fill()` **无条件** append 一条 `{"flat": True, "qty": 0}` 事件（自测 `flat_pushed`）。

---

## 5. 可复用代码片段

### 5.1 先落库再发请求（骨架，去掉了交易所细节）
```python
# 来源：vnpy_binance/portfolio_gateway.py:704-742（send_order 前半段）
# 用途：任何「本地必须有订单对象」的报单入口
def send_order(self, req):
    contract = self.gateway.get_contract_by_symbol(req.symbol)
    if not contract:                       # fail-closed：不知道是什么合约就不发
        return ""
    self.order_count += 1
    orderid = self.order_prefix + str(self.order_count)
    order = req.create_order_data(orderid, self.gateway_name)
    self.gateway.on_order(order)           # ★ 先把 SUBMITTING 状态推到本地
    params = {"symbol": contract.name, "side": DIRECTION_VT2BINANCE[req.direction],
              "quantity": format_float(req.volume), "newClientOrderId": orderid}
    self.add_request(method="POST", path=ENDPOINTS[get_market_type(req.symbol)],
                     callback=self.on_send_order, params=params, extra=order,
                     on_failed=self.on_send_order_failed,
                     on_error=self.on_send_order_error)
    return order.vt_orderid
```

### 5.2 我方落地版（真实文件，已自测）
`quant_app/core/live.py` 新增：`submit_order()` / `on_order_fill()` / `on_order_cancel()` / `selftest_router()`（**4/4 通过**）。
`ai_quant_lab/20261020_vnpy_vnpy_binance/portfolio_gateway_patterns.py`：`MarketType/get_market_type/endpoint_for` + `OrderLifecycle`（7 态）+ `PositionBook`（净额 + 归零必推），**自测 13/13**，`lab_bridge` 零警告加载。

---

## 6. B站学习（本日 30% 权重）—— **★ 本轮把 W3 结案（永久降级）**

### 6.1 通路实测（4 个端点，各打一次）
| 端点 | 结果 | 说明 |
|---|---|---|
| `api.bilibili.com/x/web-interface/search/type` | **412** | 需要 WBI 签名（老结论复现） |
| `api.bilibili.com/x/web-interface/view?bvid=…` | **200** | 单视频元数据可拿（含 cid / 标题 / 时长） |
| `api.bilibili.com/x/player/v2?bvid=…&cid=…` | **200 但 `subtitles: []`** | 字幕列表**登录态**才非空 |
| `search.bilibili.com/all?keyword=…`（HTML） | **200 且服务端渲染** | ★ **这是新发现**：WebFetch 能拿到完整视频清单（标题+UP+BV+时长） |

### 6.2 结论（W3 正式结案，不再记为「未完成」）
- **能稳定拿到**：视频清单、标题、UP 主、BV 号、时长。
- **拿不到**：字幕文本（需登录 cookie，且零成本底线禁止音频转录）。
- **→ 永久降级为「标题 + 目录级笔记」**，并把降级原因写进蓝图 W3 结案行。**从今天起不再在「未完成」区重复记这一项**（连续 8 轮记同一条未完成本身就是纪律问题）。

### 6.3 今日选题（依据：与今天主题「执行层/可复现」同形）
| 视频 | UP | BV | 时长 | 为什么选它 |
|---|---|---|---|---|
| 回测数据预处理防泄漏指南 | 我是王者quant | BV1ZkJB6dEvW | 11:20 | 与我方 H-003（未闭合 K 线）同族 |
| 跑了几百次回测，结果复现不了怎么办？ | 千面学姐Sukey_量化版 | BV1DXnM6hE4c | 4:16 | 直指 W7（无 manifest） |
| VeighNa 免费回测框架详解 | 108度的蒸馏水 | BV1nQpJ6UEop | 05:11 | 与本轮 vnpy 主线同源 |
| 【零基础入门量化交易】15 天解锁 VNPY（上） | 纳米量化 | BV1To4y1k7p1 | **8:42:30** | 体系化长课，留作后续目录级索引 |

**蒸馏要点（仅凭标题/目录，**不当结论**）**：
- 「防泄漏」这个提法本身值得抄进纪律：**数据预处理与策略逻辑要分两处做，且预处理只能用截至当前时点的统计量**（与我方 H-016 的 rolling normalization 一致）。
- 「结果复现不了」被单独做成一期节目 → 说明这是**行业级痛点**，不是我方洁癖。→ 支持把 manifest（W7）从 P1 提到 P0。
- **存疑（待代码验证）**：视频标题暗示的「结果不可复现」是否主要来自**未固定随机种子/未固定数据快照**？我方回测是确定性的（无随机数），但 H-019 的 `_hash_keep` 是我自造的确定性散列 —— 需要确认「确定性 ≠ 可复现」（数据版本变了结果就变）。

---

## 7. 对黑马策略的启发（已落到具体动作）

| 动作 | 落在哪一行 | 验证方式 |
|---|---|---|
| **① `reduce_only` 白名单加持仓交叉校验**（AtomCode Q1 指出的真实绕过路径） | `core/risk.py` `pre_trade_check()` 的 `reducing` 判定处 | 新增自测 **`G2超量reduce_only不豁免`**：持仓 1.0 张却声明 `reduce_only=True` 卖 3.0 张 → rule 不得为「减仓放行」 |
| **② G2 四态状态机**（停机 → 恢复中 → 正常，禁止一步跳变） | `core/risk.py`：`RiskLevel.RECOVERING` / `begin_recovery()` / `_recover_scale_now()` / `on_trade_result()` | 新增 6 项自测，**16/16 → 22/22 → 24/24** |
| **③ `live.py` 报单入口**（原先根本没有） | `core/live.py` 新增 `submit_order/on_order_fill/on_order_cancel/selftest_router` | **4/4** 通过；`risk=None` 一律拒单（`NO-RISK`） |
| **④ 出场端极端档 A/B** | 假设 **H-020** | `exit_mode="let_run"` vs `tiered`，4 只 15m 全历史 → **0/4，已证伪** |
| **⑤ 成本端「真权衡」A/B** | 假设 **H-021** | maker 0.02% + 数据决定成交率 → **4/4 已验证，但咬合力 ≈ 0**（见 §8 的口径警告） |

### ★ H-020 的实证结论（本轮最重要的策略结论）
`let_run`（只在跌破 MA30 或 −5% 止损时离场）**不是「更松」，是「完全不卖」**：

| 标的 | 基线净额单笔% | let_run 净额单笔% | Δ |
|---|---|---|---|
| BTCUSDT | 1.8021 | **−0.2735** | −2.0756 |
| ETHUSDT | 2.1683 | **−0.2359** | −2.4042 |
| BNBUSDT | 2.1193 | **−0.2136** | −2.3329 |
| DOGEUSDT | 0.4726 | **−0.2317** | −0.7043 |

→ **推论（三条，都要记住）**：
1. **「越松越好」是错的**。H-018 的 15/12/8 有效，不代表「关掉止盈」更好 —— 说明 **tp_tiers 存在一个内部最优档**，而不是单调方向。
2. **三段止盈的贡献是「必须在趋势转坏之前落袋」**：let_run 让每笔都吃到 MA30 跌破，而 MA30 是**滞后的**（30 根均线），等它跌破时利润已被吃掉 2pp 以上。
3. **下一步该做的是敏感性扫描而不是继续放宽**：在 10/8/5（基线）与 15/12/8（H-018 已验证）之间、以及更紧一档（8/6/4）做扫描，找**内部最优**；并且必须**换样本外区间**验，否则就是在同一批数据上做参数寻优（H-013 的教训：同批样本内的选择效应）。

### ★ H-021 的实证结论（**必须带警告引用**）
4/4「不下降」，BTC 1.8021→1.9587（+0.157）等。**但这条不能当作「限价单取舍」的证据**：

| 标的 | 实际成交率（`low[t+1] ≤ close[t]`） |
|---|---|
| BTC / ETH / BNB | **100.00%** |
| DOGE | **99.79%** |

→ **咬合力≈0**。原因：挂单价取「信号当根收盘价」，而 15m 相邻两根的区间**几乎必然重叠**，次根最低价几乎总是下探到前根收盘之下。
→ 所以 H-021 的 +0.157pp 提升，**几乎全部来自费率 0.1%→0.02%（5 倍差）**，与「不追价的机会成本」无关。
→ **诚实结论**：`maker 降费率有效`（与 H-019 同源），**「限价单挂不上导致丢机会」在我这个模型下根本没有被测到**。
→ **修法（下轮）**：挂单价不能取当根收盘，必须取**更保守的价格**（如 `close × (1 − 0.1%)` 或 `min(low[t], close[t])`），才可能真正咬掉一批信号。**这条已写入下轮 P1。**

---

## 8. 未完成 / 失败区（诚实留痕）

1. **`live.py` 仍无真实 REST 适配器**。`submit_order()` 只到「过闸 + 占额度 + 返回可执行指令」，**没有真的发单**（需 API Key + 网络通路 + 签名）。不假装能下单。
2. **`portfolio_gateway` 的 `UmMdApi/CmMdApi/MarginMdApi` 只读了类结构，未逐行读**（约 500 行 WS 订阅与重连逻辑）。
3. **`_hash_keep` 式确定性 vs 真可复现**：manifest（W7）仍未落地 → 「结果复现不了」这条行业级痛点我方**同样没解**。
4. **H-021 的挂单价设计有缺陷**（咬合力≈0），结论只能引用为「降费率有效」，**不能引用为「限价单取舍已验证」**。已写进台账注。
5. **B站字幕永久放弃**（登录 cookie 不可得，零成本底线禁转录音频）。已结案，不再计入未完成。
6. **`recover_r_target = 1.0R` 是拍的**，没有回测支撑 —— 恢复期到底该用几 R 解锁，需要单独一条假设。
7. **AtomCode 首次调用失败**是我自己的 bug：`json.load()` 读了纯文本 prompt 文件（应为 `read_text()`）。已修，**记下来避免下次**。
8. **H-020 揭示「存在内部最优档」但本轮没做扫描**（怕在同一批样本上做过拟合），留给下轮 + 需样本外验证。

---

## 9. 三件套自检

- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘：
  - `ai_quant_lab/20261020_vnpy_vnpy_binance/portfolio_gateway_patterns.py`（**13/13**，`lab_bridge` 零警告）
  - 平台本体改动：`quant_app/core/risk.py`（**24/24**，G2 四态）、`quant_app/core/live.py`（**4/4**，报单路由）
- [x] ③ 策略假设已追加并结清：**H-020 = 已证伪**、**H-021 = 已验证（咬合力≈0，带警告）**；台账备份 `backup/策略假设台账_20261020_040715.md`；结果 `回测结果/回测结果_20261020.json`

## 10. 成本与技能

- **花费积分**：**0**（AtomCode 免费档 `glm5.3-flash`，probe 200 / 69.8s；交叉复核 200 / 122.9s）
- **用了哪些技能**：`ai-quant-open-source-nightly-learning`（夜学主流程 v1.1.7 → **v1.1.8**）
- **沉淀 / 迭代**：
  - `core/risk.py` 16/16 → **24/24**（G2 四态 + R 归一晋级 + 系数随深度 + reduce_only 交叉校验）
  - `core/live.py` 142 行 → 报单入口（**4/4**）
  - 技能 §3.10 新增 6 条（含「两类失败必须分开」「先落库再发请求」「咬合力为 100% 时结论只能是降费率」）
