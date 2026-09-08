---
description: "Auto-generated skill"
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_53fc557b681a11f1a99c5254007bceed
    ReservedCode1: A/HTErkTxJ8kcI92vkjRMZHBLkiuBHAD5qKR2CL+WUUo8R7txo4QHRv3Da3yktGa4n6xfIqnXQKt5gIRx2BtS4bMOh7aQTSLoZLEkVn/54ooP6CedzLp3KzT5+PSaulsdJWKhNup6ZssVPo0Ype2v8woGMAS2JA4Mg4eIbeWsx4v6M6DH8ZN4Jh2Wts=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_53fc557b681a11f1a99c5254007bceed
    ReservedCode2: A/HTErkTxJ8kcI92vkjRMZHBLkiuBHAD5qKR2CL+WUUo8R7txo4QHRv3Da3yktGa4n6xfIqnXQKt5gIRx2BtS4bMOh7aQTSLoZLEkVn/54ooP6CedzLp3KzT5+PSaulsdJWKhNup6ZssVPo0Ype2v8woGMAS2JA4Mg4eIbeWsx4v6M6DH8ZN4Jh2Wts=
---



# 量化策略开发 (Quant Strategy Development)

基于 vnpy 4.4+ 框架的量化 CTA 策略开发全流程技能。

## 适用场景

- 用户要求开发、测试、优化量化交易策略
- 需要运行回测、分析回测结果
- 需要执行风控校验
- 需要将策略从开发环境迁移到生产环境

## 核心工作流

### 1. 策略设计

策略代码必须放置在 `strategies/dev/` 目录下，继承 vnpy CtaTemplate：

```python
from vnpy_ctastrategy import CtaTemplate
from vnpy.trader.constant import Direction, Offset

class MyStrategy(CtaTemplate):
    author = "Codex"
    
    def on_init(self):
        pass
    
    def on_start(self):
        pass
    
    def on_stop(self):
        pass
    
    def on_tick(self, tick):
        pass
    
    def on_bar(self, bar):
        pass
```

### 2. 回测验证

使用 vnpy-mcp 工具执行回测：

```
run_backtest(strategy_file, symbol, start_date, end_date, capital, interval)
```

回测要求：
- 至少 6 个月历史数据
- 初始资金 1,000,000
- 必须输出完整回测报告

### 3. 风控校验

回测完成后调用风险检查：

```
check_risk(backtest_report_file)
```

风控基线：
| 指标 | 阈值 | 动作 |
|------|------|------|
| 最大回撤 | < 20% | 不通过退回 dev |
| 单日最大亏损 | < 5% | 触发熔断 |
| 单一品种仓位 | < 30% | 减仓信号 |
| 夏普比率 | > 1.0 | 不达标标记观察 |
| 连续亏损 | < 5笔 | 策略冻结 |

### 4. 策略部署

校验通过后，将策略从 `dev/` 移至 `active/`：

```bash
move strategies\dev\my_strategy.py strategies\active\my_strategy.py
```

## 工作目录约束

- 所有写入操作限制在 `E:\龙虾AI主控中心\我的AI分身\Codex量化策略\`
- 主策略资产目录（父目录）只读，禁止修改
- 回测数据写入 `backtests/`
- 风控报告写入 `risk/`

## 工具链

- **vnpy-mcp**: 策略回测、代码验证、风险检查
- **doubao-proxy**: 市场分析、策略思路讨论
- **python_executor**: 辅助脚本运行
*（内容由AI生成，仅供参考）*
