# VNPY量化框架源码研读笔记

> 来源：GitHub vnpy/vnpy (44K+ Stars) + 51bitquant/course_codes
> 提取时间：2026-08-01
> 版本：VeighNa 4.0+

---

## 一、项目基本信息

- **项目名**：VeighNa (原vnpy)
- **GitHub**: https://github.com/vnpy/vnpy
- **Stars**: 44,086 | **Forks**: 12,293
- **License**: MIT | **创建**: 2015-03-02
- **Python**: 推荐3.13，支持3.10+（64位）
- **支持系统**: Windows 11+ / Ubuntu 22.04 LTS+

---

## 二、源码目录结构

```
vnpy/
├── alpha/              # 4.0新增：AI量化策略模块
│   ├── dataset/        # 因子特征工程
│   │   ├── cs_function.py    # 截面因子函数
│   │   ├── ts_function.py    # 时序因子函数
│   │   ├── ta_function.py    # 技术分析函数
│   │   ├── math_function.py  # 数学函数
│   │   ├── processor.py      # 数据处理器
│   │   └── template.py       # 数据集模板
│   ├── model/          # ML模型训练
│   │   ├── models/           # 具体模型实现
│   │   └── template.py       # 模型模板
│   └── strategy/       # 策略投研
│       ├── strategies/       # 具体策略实现
│       ├── backtesting.py    # Alpha回测引擎
│       └── template.py       # 策略模板
├── chart/              # K线图表
├── event/              # 事件驱动引擎
│   └── engine.py       # EventEngine核心
├── rpc/                # 分布式RPC通讯
└── trader/             # 交易核心模块
    ├── engine.py       # MainEngine主引擎
    ├── gateway.py      # BaseGateway接口基类
    ├── object.py       # 核心数据结构定义
    ├── constant.py     # 常量枚举定义
    ├── converter.py    # 持仓转换器
    ├── database.py     # 数据库适配器
    ├── datafeed.py     # 数据服务适配器
    ├── optimize.py     # 参数优化工具
    ├── utility.py      # 工具函数
    ├── setting.py      # 全局设置
    ├── logger.py       # 日志系统
    ├── app.py          # App基类
    ├── wechat.py       # 微信通知
    └── ui/             # GUI界面
```

---

## 三、核心数据结构 (object.py)

### 3.1 行情数据

**TickData（实时Tick）**
- 必填：`symbol`, `exchange`, `datetime`
- 价格：`last_price`, `open_price`, `high_price`, `low_price`, `pre_close`, `limit_up`, `limit_down`
- 盘口：`bid_price_1~5`, `ask_price_1~5`, `bid_volume_1~5`, `ask_volume_1~5`
- 统计：`volume`, `turnover`, `open_interest`
- 自动生成：`vt_symbol = f"{symbol}.{exchange.value}"`

**BarData（K线）**
- 必填：`symbol`, `exchange`, `datetime`, `interval`
- OHLCV：`open_price`, `high_price`, `low_price`, `close_price`, `volume`

### 3.2 订单管理

**OrderData（订单）**
- 必填：`symbol`, `exchange`, `orderid`
- 字段：`type`, `direction`, `offset`, `price`, `volume`, `traded`, `status`
- 关键方法：`is_active()`, `create_cancel_request()`
- 自动生成：`vt_symbol`, `vt_orderid`

**TradeData（成交）**
- 必填：`symbol`, `exchange`, `orderid`, `tradeid`
- 一个Order可能对应多个Trade

### 3.3 账户持仓

**PositionData（持仓）**
- 必填：`symbol`, `exchange`, `direction`
- 字段：`volume`, `frozen`, `price`, `pnl`, `yd_volume`

**AccountData（账户）**
- 必填：`accountid`
- 字段：`balance`, `frozen`
- 自动计算：`available = balance - frozen`

### 3.4 请求对象

| 请求类 | 用途 | 关键字段 |
|--------|------|----------|
| `SubscribeRequest` | 订阅行情 | symbol, exchange |
| `OrderRequest` | 下单 | symbol, exchange, direction, type, volume, price, offset |
| `CancelRequest` | 撤单 | orderid, symbol, exchange |
| `HistoryRequest` | 历史数据 | symbol, exchange, start, end, interval |
| `QuoteRequest` | 双边报价 | bid_price, ask_price, bid_volume, ask_volume |

---

## 四、事件驱动引擎 (event/engine.py)

### 4.1 设计模式

核心采用 **观察者模式（Observer Pattern）**：

```python
class Event:
    def __init__(self, type: str, data: Any = None):
        self.type = type    # 事件类型字符串
        self.data = data    # 事件携带的数据

class EventEngine:
    _handlers: defaultdict(list)     # type -> [handler1, handler2, ...]
    _general_handlers: list          # 监听所有事件的处理器
    _queue: Queue                    # 线程安全事件队列
```

### 4.2 工作机制

1. **事件产生**：Gateway/Timer产生Event，`put()`放入Queue
2. **事件分发**：`_run()`线程从Queue取Event，调用`_process()`
3. **事件处理**：先调用type-specific handlers，再调用general handlers
4. **定时器**：默认每1秒产生`EVENT_TIMER`事件

### 4.3 事件类型

| 事件类型 | 触发场景 | 特定事件后缀 |
|----------|----------|--------------|
| `EVENT_TICK` | Tick行情更新 | `tick.vt_symbol` |
| `EVENT_ORDER` | 订单状态变化 | `order.vt_orderid` |
| `EVENT_TRADE` | 成交回报 | `trade.vt_symbol` |
| `EVENT_POSITION` | 持仓变化 | `position.vt_symbol` |
| `EVENT_ACCOUNT` | 账户变化 | `account.vt_accountid` |
| `EVENT_CONTRACT` | 合约信息 | 无 |
| `EVENT_LOG` | 日志 | 无 |
| `EVENT_TIMER` | 定时器 | 无 |

### 4.4 注册与注销

```python
# 注册特定事件处理器
event_engine.register(EVENT_TICK, on_tick_handler)

# 注册通用事件处理器（监听所有事件）
event_engine.register_general(on_all_handler)

# 注销
event_engine.unregister(EVENT_TICK, on_tick_handler)
```

---

## 五、MainEngine 主引擎 (trader/engine.py)

### 5.1 架构设计

```
MainEngine (中央协调器)
├── EventEngine (事件引擎)
├── Gateways (交易所连接)
│   ├── CtpGateway
│   ├── XtpGateway
│   └── ...
├── Apps (策略应用)
│   ├── CtaStrategyApp
│   ├── SpreadTradingApp
│   └── ...
└── Engines (功能引擎)
    ├── LogEngine (日志)
    ├── OmsEngine (订单管理)
    ├── EmailEngine (邮件通知)
    └── WechatEngine (微信通知)
```

### 5.2 OmsEngine（订单管理系统）

**中央数据仓库**，存储所有交易数据：

```python
self.ticks: dict[str, TickData] = {}
self.orders: dict[str, OrderData] = {}
self.trades: dict[str, TradeData] = {}
self.positions: dict[str, PositionData] = {}
self.accounts: dict[str, AccountData] = {}
self.contracts: dict[str, ContractData] = {}
self.quotes: dict[str, QuoteData] = {}
self.active_orders: dict[str, OrderData] = {}   # 活跃订单单独跟踪
self.active_quotes: dict[str, QuoteData] = {}
```

### 5.3 启动流程

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp
from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp

def main():
    qapp = create_qapp()                    # 1. 创建Qt应用
    event_engine = EventEngine()            # 2. 创建事件引擎
    main_engine = MainEngine(event_engine)  # 3. 创建主引擎
    main_engine.add_gateway(CtpGateway)     # 4. 添加交易接口
    main_engine.add_app(CtaStrategyApp)     # 5. 添加策略应用
    main_window = MainWindow(main_engine, event_engine)  # 6. 创建GUI
    main_window.showMaximized()
    qapp.exec()                             # 7. 启动事件循环
```

### 5.4 关闭流程

1. 停止EventEngine（阻止新事件）
2. 按顺序关闭所有Engine
3. 关闭所有Gateway

---

## 六、BaseGateway 交易接口 (trader/gateway.py)

### 6.1 设计规范

- **线程安全**：所有方法必须线程安全
- **非阻塞**：所有方法必须非阻塞
- **自动重连**：连接断开后必须自动重连
- **数据不可变**：传给回调的Data对象不可修改，缓存时用`copy.copy`

### 6.2 必须实现的方法

```python
class BaseGateway(ABC):
    @abstractmethod
    def connect(self, setting: dict) -> None: ...
    
    @abstractmethod
    def close(self) -> None: ...
    
    @abstractmethod
    def subscribe(self, req: SubscribeRequest) -> None: ...
    
    @abstractmethod
    def send_order(self, req: OrderRequest) -> str: ...  # 返回vt_orderid
    
    @abstractmethod
    def cancel_order(self, req: CancelRequest) -> None: ...
    
    @abstractmethod
    def query_account(self) -> None: ...
    
    @abstractmethod
    def query_position(self) -> None: ...
```

### 6.3 回调方法

```python
def on_tick(self, tick: TickData) -> None     # 行情推送
def on_order(self, order: OrderData) -> None  # 订单状态
def on_trade(self, trade: TradeData) -> None  # 成交回报
def on_position(self, pos: PositionData) -> None  # 持仓
def on_account(self, account: AccountData) -> None  # 账户
def on_contract(self, contract: ContractData) -> None  # 合约
def on_quote(self, quote: QuoteData) -> None  # 报价
def on_log(self, log: LogData) -> None        # 日志
```

### 6.4 支持的交易接口

**国内**：CTP/Mini/CTP证券、中泰XTP、华鑫奇点、飞马、易盛等
**海外**：Interactive Brokers、易盛9.0外盘等
**数据**：RQData、迅投研

---

## 七、CTA策略模板 (vnpy_ctastrategy)

### 7.1 CtaTemplate 基类

```python
class CtaTemplate(ABC):
    author: str = ""
    parameters: list = []   # 策略参数（可优化）
    variables: list = []    # 策略变量（可观测）
    
    # 核心状态
    inited: bool = False    # 是否已初始化
    trading: bool = False   # 是否允许交易
    pos: float = 0          # 当前持仓
```

### 7.2 生命周期回调

```python
@abstractmethod
def on_init(self) -> None:      # 策略初始化（必须实现）
def on_start(self) -> None:     # 策略启动
def on_stop(self) -> None:      # 策略停止
def on_tick(self, tick) -> None:  # Tick回调
def on_bar(self, bar) -> None:    # K线回调
def on_trade(self, trade) -> None:  # 成交回调
def on_order(self, order) -> None:  # 订单回调
def on_stop_order(self, stop_order) -> None:  # 停止单回调
```

### 7.3 交易方法

```python
def buy(self, price, volume, stop=False, lock=False, net=False) -> list:
    """买入开多"""

def sell(self, price, volume, stop=False, lock=False, net=False) -> list:
    """卖出平多"""

def short(self, price, volume, stop=False, lock=False, net=False) -> list:
    """卖出开空"""

def cover(self, price, volume, stop=False, lock=False, net=False) -> list:
    """买入平空"""

def cancel_all(self) -> None:
    """撤销所有活动委托"""
```

### 7.4 工具方法

```python
def load_bar(self, days, interval=Interval.MINUTE, callback=None, use_database=False):
    """加载历史K线用于初始化"""

def load_tick(self, days):
    """加载历史Tick用于初始化"""

def get_pricetick(self) -> float:  # 最小变动价位
def get_size(self) -> int:         # 合约乘数
def write_log(self, msg) -> None:  # 写日志
def put_event(self) -> None:       # 触发UI更新
def sync_data(self) -> None:       # 持久化策略变量
```

### 7.5 三种策略模板

1. **CtaTemplate**：标准模板，手动管理下单
2. **CtaSignal**：轻量信号生成器，只输出信号位置（-1, 0, 1）
3. **TargetPosTemplate**：目标持仓模板，自动计算并执行调仓

---

## 八、回测引擎 (vnpy_ctastrategy/backtesting.py)

### 8.1 核心参数

```python
BacktestingEngine(
    vt_symbol,           # 交易品种
    interval,            # K线周期
    start,               # 回测开始时间
    rate=0,              # 手续费率
    slippage=0,          # 滑点
    size=1,              # 合约乘数
    pricetick=0,         # 最小变动价位
    capital=1_000_000,   # 初始资金
    risk_free=0,         # 无风险利率
    annual_days=240,     # 年交易日
    half_life=120,       # EWM半衰期
)
```

### 8.2 回测流程

```
1. set_parameters()    → 设置回测参数
2. add_strategy()      → 添加策略类和参数
3. load_data()         → 从数据库加载数据（按30天分批）
4. run_backtesting()   → 执行回测
   ├── on_init()       → 策略初始化
   ├── on_start()      → 策略启动
   └── new_bar/tick()  → 逐根K线/Tick推送
5. calculate_result()  → 计算每日盈亏
6. calculate_statistics() → 计算绩效指标
7. show_chart()        → 可视化展示
```

### 8.3 订单撮合逻辑

**限价单撮合（BAR模式）**：
- 买入：`bar.low_price <= order.price`，以`min(bar.open_price, order.price)`成交
- 卖出：`bar.high_price >= order.price`，以`max(bar.open_price, order.price)`成交

**停止单撮合（BAR模式）**：
- 买入：`bar.high_price >= stop_price`，以`stop_price`成交
- 卖出：`bar.low_price <= stop_price`，以`stop_price`成交

### 8.4 每日盈亏计算

```python
class DailyResult:
    holding_pnl = start_pos * (close_price - pre_close) * size  # 持仓盈亏
    trading_pnl = pos_change * (close_price - trade_price) * size  # 交易盈亏
    turnover = volume * size * trade_price  # 成交额
    commission = turnover * rate  # 手续费
    slippage = volume * size * slippage  # 滑点成本
    net_pnl = holding_pnl + trading_pnl - commission - slippage  # 净盈亏
```

### 8.5 绩效指标

| 指标 | 计算方式 |
|------|----------|
| 总收益率 | `(end_capital - capital) / capital` |
| 年化收益率 | `(1 + total_return) ^ (annual_days / total_days) - 1` |
| 最大回撤 | 峰到谷的最大百分比跌幅 |
| Sharpe Ratio | `(daily_return - risk_free) / return_std * √annual_days` |
| EWM Sharpe | 指数加权移动平均Sharpe |
| 收益回撤比 | `-total_return / max_drawdown_percent` |
| RGR Ratio | `(gain * stability * skew * kurt) / combined_risk` |

### 8.6 参数优化

```python
# 暴力搜索优化
engine.run_bf_optimization(target_name="sharpe_ratio")

# 遗传算法优化（pop_size=100, ngen=30, cxpb=0.95）
engine.run_ga_optimization(target_name="sharpe_ratio")
```

---

## 九、AI量化模块 (vnpy/alpha) — 4.0新增

### 9.1 模块架构

```
alpha/
├── dataset/        # 因子特征工程
│   ├── cs_function.py    # 截面因子（Cross-Sectional）
│   ├── ts_function.py    # 时序因子（Time-Series）
│   ├── ta_function.py    # 技术分析因子
│   ├── math_function.py  # 数学变换
│   ├── processor.py      # 数据预处理
│   └── template.py       # 数据集模板
├── model/          # ML模型
│   ├── models/           # Lasso、LightGBM、MLP等
│   └── template.py       # 模型模板
└── strategy/       # 策略
    ├── strategies/       # 截面/时序策略
    ├── backtesting.py    # Alpha回测
    └── template.py       # 策略模板
```

### 9.2 因子工程

- **Alpha 158特征集**：经典的158个量化因子
- **截面因子**：跨品种横截面比较
- **时序因子**：单品种时间序列特征
- **技术因子**：传统技术指标

### 9.3 模型集成

- **Lasso**：线性正则化
- **LightGBM**：梯度提升树
- **MLP**：多层感知机深度学习

---

## 十、数据库与数据源适配

### 10.1 数据库支持

| 类型 | 适配器 |
|------|--------|
| SQL | SQLite（默认）、MySQL、PostgreSQL |
| NoSQL | QuestDB、TDengine、MongoDB、DolphinDB |

### 10.2 数据源支持

- 迅投研、RQData、TuShare、Wind、iFinD
- 支持股票、期货、期权、基金、债券等

---

## 十一、策略应用模块

| 模块 | 功能 |
|------|------|
| `cta_strategy` | CTA策略引擎，支持细粒度委托控制 |
| `cta_backtester` | CTA策略回测 |
| `spread_trading` | 价差交易（套利） |
| `option_master` | 期权交易 |
| `portfolio_strategy` | 多合约组合策略 |
| `algo_trading` | 算法交易（TWAP、Sniper等） |
| `paper_account` | 本地仿真 |
| `risk_manager` | 风险管理 |
| `data_manager` | 数据管理 |
| `data_recorder` | 行情记录 |

---

## 十二、51bitquant课程结构

课程：VNPY数字货币量化交易从零到实盘
- 27节课（class_01 ~ class_27 + class_33）
- 基于howtrader（vnpy数字货币分支）
- B站/YouTube/网易云课堂免费公开

---

## 十三、关键设计模式总结

1. **事件驱动**：所有数据流通过EventEngine，解耦生产者和消费者
2. **模板方法**：BaseGateway/CtaTemplate定义骨架，子类实现细节
3. **观察者模式**：register/unregister动态注册事件处理器
4. **策略模式**：不同Gateway/Strategy可插拔替换
5. **单例模式**：MainEngine作为全局协调器
6. **工厂模式**：add_gateway/add_app动态创建实例
7. **延迟初始化**：Email/WeChat引擎首次使用时才启动
