---
日期: 2026-10-08
仓库: vnpy/vnpy_binance（主） + vnpy/vnpy_ctastrategy（副）
核心文件: vnpy_binance/linear_gateway.py（1770 行） · vnpy_ctastrategy/template.py（507 行）
轮次: 第 2 轮（轮转序号 #5/#4）
tags: [AI量化平台, 夜学, 代码拆解, 币安网关, CTA模板]
---

# 20261008 · vnpy/vnpy_binance · linear_gateway.py

## 0. 一句话结论
> 今天这个文件教会我：**实盘网关的价值 90% 不在「能下单」，而在「订单不丢、时间不错、断线能续、回测不偷看未来」**——这四条工程约束，每一条都能原样搬到黑马策略上，且不花一分钱、不承诺任何收益率。

---

## 1. 这个文件在系统里管什么（架构定位）

**主仓库 `linear_gateway.py`（U本位永续合约网关）**

- 所属层：**执行层**（连接 vnpy 事件层 ↔ 币安交易所）
- 上下游：
  - 上游依赖 → vnpy 核心 `BaseGateway` / `EventEngine` / `RestClient` / `WebsocketClient`；币安 REST + WS API
  - 下游被谁调用 → vnpy 的 `MainEngine` 注册为网关；CTA 策略引擎通过 `send_order/cancel_order/subscribe` 调用；`on_tick/on_order/on_trade` 事件推回事件引擎
- 同仓库 4 兄弟网关共用一个模式：`spot_gateway` / `linear_gateway`（U本位永续）/ `inverse_gateway`（币本位）/ `portfolio_gateway`（组合保证金）。**它们不是继承关系，而是同构复制**——因为三套 API 端点/字段不同（`/fapi` vs `/dapi` vs `/api`），vnpy 选择「复制模板 + 改差异」，而非抽象基类。这本身就是个设计取舍点（见 §4.4）。

**副仓库 `template.py`（CTA 策略模板）**

- 所属层：**策略层**（策略开发者继承的基类）
- 上游 → CTA 引擎 `engine.py`（把 tick/bar/order/trade 事件喂进策略）
- 下游 → 用户策略（继承 `CtaTemplate` 实现 `on_bar`/`on_tick`）；`TargetPosTemplate` 是内置的「目标仓位」子模板

---

## 2. 调用链（文字版时序图）

**A. 下单链路（linear_gateway.py）**
```
策略/引擎 send_order(OrderRequest)
  → Gateway.send_order()            [198]  门面转发
  → TradeApi.send_order()           [1546] WS 下单
      ① get_contract_by_symbol      [1561] 合约校验（拿 contract.name + min_volume 精度）
      ② orderid = 时间戳前缀+自增    [1567] 本地 clientOrderId（防订单归属丢失）
      ③ req.create_order_data()+on_order  [1571] 先推「提交中」事件，UI 立刻可见
      ④ 组 params（side/quantity/type）   [1578] STOP 单带 stopPrice
      ⑤ sign(params)                [1597] 写 timestamp + HMAC-SHA256 signature
      ⑥ reqid→on_send_order 注册     [1600]
      ⑦ send_packet({"method":"order.place"})
  → 交易所
  → 回报分两路：
     ├─ 请求响应 on_send_order [1680]：**只处理 error**（订单被拒 → status=REJECTED）
     └─ 用户流 on_order      [1042]：成交/状态变更，构 OrderData + TradeData 推事件
```

**B. 历史 K 线链路（query_history）**
```
策略 load_bar / 回测取数
  → Gateway.query_history()          [239] 转发
  → RestApi.query_history()          [818]
      while True: 组 params(limit=1500, startTime) → GET /fapi/v1/klines
        → 解析 BarData（含 bar.extra: trade_count / active_volume / active_turnover）
        → 最后一根的开盘 + 1周期 = 下一次 startTime
        → 收满一页 且 未到 end → 继续；否则 break
        → sleep(0.5)  限流
      ★ history.pop(-1)   [915] 剔除未闭合 K 线（防未来函数）
```

**C. 断线重连链路**
```
WS on_disconnected [1393/1103]
  → MdApi：on_connected 时遍历 self.ticks.keys() → resubscribe_market_channels() [1226]
  → UserApi：on_disconnected 直接 rest_api.start_user_stream() [1115] 重建 listenKey
  → Gateway.process_timer_event [264]：定时 keep_user_stream() + subscribe_new_channels()
```

**D. 副仓库：目标仓位调仓链路（template.py）**
```
策略 on_bar 算出信号 → set_target_pos(目标手数) [435]
  → trade() [440]
     ├─ 有活动委托？ → cancel_old_order() [447] 全撤（防重复下单）
     └─ 没有？        → send_new_order() [455]
           pos_change = target_pos - self.pos   [457] ★只交易「差额」
           买单挂 ask+tick_add / 卖单挂 bid-tick_add   [466-470] 主动保成交
```

---

## 3. 关键类 / 函数（签名 + 职责）

| 名称 | 类型 | 职责 | 备注 |
|---|---|---|---|
| `BinanceLinearGateway(BaseGateway)` | 类 | 网关门面：聚合 4 个 API 子对象，对外暴露标准接口 | `default_name="BINANCE_LINEAR"`；只支持全仓/单向持仓 |
| `RestApi.sign(request)` | 方法 | REST 签名：排序 params → 加 timestamp → HMAC-SHA256 | 时间偏移 `time_offset` 校正，防 -1021 |
| `TradeApi.send_order(req)` | 方法 | WS 下单：本地 clientOrderId + reqid 映射 + order.place | 支持 MARKET / STOP_MARKET / LIMIT |
| `UserApi.on_order(packet)` | 方法 | 订单/成交回报解析 → OrderData + TradeData | 三重过滤：订单类型白名单 / 合约存在 / traded 量 round_to |
| `MdApi.get_market_channels()` | 方法 | 生成行情通道（ticker/kline_1m/markPrice） | SWAP 才订阅 markPrice |
| `MdApi.resubscribe_market_channels()` | 方法 | 重连后按 `self.ticks.keys()` 重建订阅 | 防「重连了但没重订阅」静默丢行情 |
| `RestApi.query_history(req)` | 方法 | 历史 K 线分页拉取（limit 1500 + sleep 0.5） | ★`history.pop(-1)` 剔除未闭合 K 线 |
| `format_float(f)` / `generate_datetime(ts)` | 函数 | 精度格式化 / UTC 时间戳转 datetime | 精度错会被交易所拒单 |
| `CtaTemplate(ABC)` | 类 | CTA 策略基类：on_init/on_tick/on_bar/on_order/on_trade 钩子 | 副仓库 |
| `TargetPosTemplate(CtaTemplate)` | 类 | 目标仓位模板：只声明目标，模板自动算差额调仓 | 副仓库核心可迁移点 |

---

## 4. 可迁移设计点（逐条写「为什么好」）

**4.1 时间偏移校正（time_offset）—— 签名有效性的隐形地基**
- 出处：`linear_gateway.py:404-411`
- 设计：启动时 `query_time()` 拿服务器时间，算出 `time_offset`；每次签名 `timestamp` 按偏移修正。
- **为什么好**：本机时钟漂移 / 跨时区机器，会让签名 timestamp 超出交易所 `recvWindow`（默认 5000ms），下单被拒（-1021），而且**偶发**——白天没事半夜飘。vnpy 把它变成启动时一次性校正，成本 1 次请求。**黑马策略若走 API 下单，这是必须先上的第一道保险。**

**4.2 本地 clientOrderId + reqid→回调双映射 —— 订单不丢的唯一解**
- 出处：`455, 1567-1601`
- 设计：orderid = `启动时间戳 + 自增序号`；同时 `reqid_callback_map[reqid]=handler`、`reqid_order_map[reqid]=order`。
- **为什么好**：异步 WS 里，「请求已发、响应未回」是常态。本地 ID 让断线/超时后能对账；reqid 映射让响应回到正确处理器，不用 if/else 猜包。**没有这层，网络一抖就可能「下了单但不知道下没下」，实盘大忌。**

**4.3 重连后自动重订阅 —— 防「静默丢行情」**
- 出处：`1226-1250`
- 设计：用 `self.ticks.keys()` 当已订阅登记表，`on_connected` 时整体重订阅。
- **为什么好**：WS 断开重连后交易所不记得你订过什么。若只重连不重订阅，策略**不报错、只是再也收不到 tick**——最隐蔽的实盘故障。**黑马策略若接实时行情，必须自建订阅登记表。**

**4.4 同构复制 > 强行抽象（网关架构取舍）**
- 出处：4 个 gateway 文件并列，无公共基类
- 设计：币安 现货/合约/币本位/组合 四套 API 字段差异大，vnpy 选择「复制模板改差异」。
- **为什么好**：强行抽公共基类会得到一堆 `if 是现货 then...`，反而更难维护。**对黑马策略的启示**：多交易所/多品种接入时，「复制+改差异」往往比「过度抽象」更快更稳。**代价**是改 bug 要改 4 处——这是已知代价，工具（diff/sed）可缓解。

**4.5 【副仓库】TargetPosTemplate 目标仓位状态机 —— 仓位管理的最优范式**
- 出处：`template.py:435-472`
- 设计：策略只调 `set_target_pos(n)`；模板负责 `pos_change = target - pos` → 先撤旧单 → 只交易差额 → 买单挂 ask+tick_add 保成交。
- **为什么好**：把「仓位应该多少」和「怎么达成」彻底分离。策略层永远只回答前者，**天然幂等**——同一根 bar 重复算也不会重复下单。黑马策略当前是「事件驱动逐笔下单」，改成目标仓位驱动后，重复信号/断线重放都不会造成双开。

---

## 5. 可复用代码片段

**落盘位置（真实文件，已自测）：**
`E:\龙虾AI主控中心\我的AI分身\CODEX量化策略20260615\币安\我的黑马策略\ai_quant_lab\20261008_vnpy_vnpy_binance\`

| 文件 | 内容 | 自测 |
|---|---|---|
| `binance_gateway_patterns.py` | 5 个可迁移组件（时间偏移/订单ID工厂/reqid映射/K线翻页/重订阅登记表） | `_selftest.py` → **15/15 PASS** |
| `dark_horse_guard.py` | 黑马策略回测数据卫生守卫（剔未闭合K线+缺口检测+时区检查+taker因子） | 内置 `demo_selftest()` → 通过 |
| `_selftest.py` | 纯本地断言测试（不联网） | 退出码 0 |
| `bili/TOC.md`, `bili/*.json` | B站课程目录级素材 | — |

```python
# 来源：vnpy_binance/linear_gateway.py:404-423（时间偏移 + HMAC-SHA256 签名）
# 用途：任何需要签名鉴权的交易所 REST 请求，先校正时间再签名
import time, hmac, hashlib, urllib.parse

def sign_rest_query(secret: bytes, params: dict, time_offset_ms: int = 0) -> str:
    """按 key 排序 urlencode → 追加 timestamp → HMAC-SHA256。
    time_offset_ms = 启动时 server_time - local_time；不加校正会在时钟漂移时被拒(-1021)。"""
    params = dict(params)
    params["timestamp"] = int(time.time() * 1000) + time_offset_ms
    query = urllib.parse.urlencode(sorted(params.items()))
    sig = hmac.new(secret, query.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{query}&signature={sig}"
```

```python
# 来源：vnpy_binance/linear_gateway.py:913-915（剔除未闭合K线）
# 用途：★回测取数后必做，否则最后一根是「当前未收盘」bar = 用了未来数据
def drop_unclosed(bars: list) -> list:
    """砍掉最后一根未闭合 K 线，防 look-ahead bias。"""
    return bars[:-1] if bars else bars
```

```python
# 来源：vnpy_ctastrategy/template.py:455-472（目标仓位差量下单，副仓库）
# 用途：把黑马策略从「事件驱动逐笔下单」改成「目标仓位驱动」，天然幂等
class TargetPosTemplate:
    def send_new_order(self):
        pos_change = self.target_pos - self.pos      # ★只交易差额
        if not pos_change:
            return
        if pos_change > 0:
            price = self.last_tick.ask_price_1 + self.tick_add   # 主动保成交
            self.buy(price, abs(pos_change))
        else:
            price = self.last_tick.bid_price_1 - self.tick_add
            self.short(price, abs(pos_change))
```

> 说明：以上为**学习性摘录 + 指针**，非整段搬运源码（均 <80 行，附 `文件:行范围`）。完整可运行版见上面的落盘文件。

---

## 6. B站学习（本日 30% 权重）

**结果：降级为「标题 + 目录级」笔记**（字幕需登录态，未登录返回空 `subtitles: []`；遵守零成本底线**不做音频转录**）。

| 视频 | UP | 链接 | 分P | 字幕 |
|---|---|---|---|---|
| 【全298集】B站最用心最全的Python量化交易教程（2025） | 程序不打烊 | https://www.bilibili.com/video/BV1D52CBREpX | 69 | ❌ 未登录拿不到 |
| 【量化交易教程】全100集 python金融分析与量化实战 | 路飞学城Alex小助理 | https://www.bilibili.com/video/BV1Zi6AYjEG8 | 19 | ❌ 同上 |

**目录级蒸馏要点（从 69 集课程目录读出该课知识结构）：**
1. 基础篇（1-6P）：量化交易定义 / 开发流程 / 交易产品分类 / 盈利模式 / 策略信号分类
2. 股票概念篇（7-15P）：交易维度、行业分类、影响股价因素、基本选股与择时
3. 工具篇（16-20P）：Numpy 股价统计分析 → Pandas K线处理 → Matplotlib 技术分析
4. （后续分P目录）回测框架 / 策略实现 / 项目实战

**存疑处（待代码验证）：**
- 目录里「量化交易分类--盈利模式」「策略信号」两节的分类口径，与 vnpy 实际的策略模板（CtaTemplate/TargetPosTemplate）是否对得上？—— 待下轮拿到字幕后核对。
- 该课以**股票**为主，与黑马策略的 **加密永续 / XAUUSD** 在交易成本模型上差异大，**不能直接照搬**，只能取「指标计算 / 回测流程」骨架。

---

## 7. 对黑马策略的启发（必须落到具体动作）

**动作 1（工程 · 立即可做）— 回测数据卫生三步**
- 改哪：黑马策略回测取数入口，取完 K 线立即调用 `dark_horse_guard.guard_bars(bars, interval, now_ms)`。
- 加什么：① 剔除未闭合 K 线 ② 缺口检测（缺口 >1 周期时告警）③ 时区对齐检查（H4 开盘须落在 UTC 4h 边界）。
- 验什么：**剔除前后胜率差**——这就是 look-ahead bias 的量化值。若差 >5 个百分点，说明历史回测严重虚高。

**动作 2（结构 · 需改造）— 黑马 EA 仓位管理改「目标仓位驱动」**
- 改哪：EA 里「收到信号 → 直接下单」的逻辑，改为「收到信号 → 算出目标手数 → 比对当前持仓 → 只交易差额」。
- 加什么：活动委托队列 + 「有未完成委托时先撤再发」。
- 验什么：同一信号重复触发时，持仓不翻倍（幂等性测试）；断线重连重放信号后，持仓仍等于目标值。

**动作 3（因子 · 待数据）— 把 `bar.extra` 的主动买量用起来**
- 改哪：K 线取数时保留第 10 列（taker 主动买量），算 `taker_buy_volume / volume`。
- 加什么：作为 **H-002 假设**的入场条件（见台账）。
- 验什么：见台账 H-002 的待验指标。

---

## 8. 未完成 / 失败区（诚实留痕）

| # | 项 | 原因 | 处理 |
|---|---|---|---|
| 1 | **13460 代理未监听** | 实测 `netstat` 无 1081/7897/1080；curl socks5h:1081 → 000 | 降级纯本地 Read/Grep 精读，任务未中断（符合技能降级策略） |
| 2 | **AtomCode 推理不可用** | 任务卡载明：CodingPlan 免费额度 HTTP 403（账号级闸门），换模型也不行 | 未调用 AtomCode 推理；仅用其作为「已存在但本轮不用」的能力记录 |
| 3 | **git 全局代理指向死端口** | `http.proxy=127.0.0.1:7897` 未监听 → clone 失败 | 本次用 `git -c http.proxy= -c https.proxy=` 临时清空，走 ghproxy.net 镜像，**clone 成功** |
| 4 | **B站字幕抓不到** | 未登录，`player/v2` 返回 `subtitles: []` | 降级目录级笔记；明日待补（需登录 cookie 或换有公开 CC 的视频） |
| 5 | **副仓库仅 1 个** | 时间/通道预算；白名单剩余 nautilus_trader 体量大 | 今日副源取 `vnpy_ctastrategy`（与黑马 CTA 最相关）；nautilus_trader 待下轮 |
| 6 | **H-003 未实测** | 黑马策略现有回测是否含未闭合 K 线，需读其取数代码确认 | 守卫代码已备，**尚未挂到黑马回测上跑真实对比** —— 属「结论未验证项」 |

> ⚠️ 本笔记所有「可迁移设计点」均为**从源码读出的工程事实**；所有「对黑马策略的启发」均为**待验证假设**，不是结论。**本笔记不承诺任何收益率。**

---

## 9. 三件套自检
- [x] ① 拆解笔记已落盘（本文件）
- [x] ② 可复用代码落盘路径：`ai_quant_lab\20261008_vnpy_vnpy_binance\binance_gateway_patterns.py`（15/15 PASS）、`dark_horse_guard.py`（自测通过）
- [x] ③ 策略假设已追加进 [[策略假设台账]]（H-001 / H-002 / H-003）

## 10. 成本与技能
- 本次花费积分估算：**0**（全程免费档 + 本地 Read/Grep + 本地 Python 自测；未调用任何付费模型）
- 用了哪些技能：`ai-quant-open-source-nightly-learning`（夜学流程规范：白名单轮转 / 三件套验收 / 诚实边界 / 降级不中断）；`币安量化数据通路与黑马策略诊断`（币安数据通路知识：镜像通道判断）
- 沉淀 / 迭代了什么：新建可复用模块 2 个（见 §5）；台账新增 3 条假设（含首条工程性假设 H-003）；本轮**发现 ghproxy.net 镜像通道可作为 GitHub 克隆备用通路**（已写入收尾报告与记忆）
- 关联：[[AI量化平台架构蓝图]] · [[策略假设台账]] · [[_每日笔记模板]]
