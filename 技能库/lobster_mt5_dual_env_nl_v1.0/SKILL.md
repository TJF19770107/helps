---
name: "lobster_mt5_dual_env_nl_v1.0"
description: "MT5双环境隔离+自然语言调用+Claude代理兼容全流程实战。涵盖：MT5模拟/实盘双环境隔离配置、自然语言调用MT5 MCP标准化模板、Claude Code代理兼容替代方案（含claude-proxy.bat）、sim/real两套.env和mcp.json样板、Codex自然语言指令示例。"
version: "1.0"
merged_from: ["MT5双环境隔离部署实战", "MT5三大问题答疑报告_20260629", "Codex_MT5_NL_Commands自然语言指令清单", "龙虾MT5双AI量化MCP对接运维(lobster_mt5_quant_mcp_deploy_v1.0)"]
date: "2026-06-29"
sync_mode: "bidirectional"
primary_path: "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_mt5_dual_env_nl_v1.0\SKILL.md"
backup_path: "G:\龙虾AI主控中心\我的AI分身\技能库\backup\"
---

# 龙虾MT5双环境隔离+自然语言调用+Claude代理兼容 全流程实战技能

技能名称：龙虾MT5双环境隔离+自然语言调用+Claude代理兼容全流程实战
技能标识：lobster_mt5_dual_env_nl_v1.0
适用范围：MT5量化交易双环境部署运维 / 自然语言调用MT5标准化 / Claude Code代理兼容替代 / Codex NL指令开发
执行口径：严格按双环境隔离架构执行，模拟盘与实盘物理隔离，实盘硬锁定 readonly
版本号：v1.0（首发版，基于V2.4架构锁定版五步法执行沉淀）
更新时间：2026-06-29
生效范围：全域 / 永久 / Codex + Claude Code + Hermes 统一

---

## 一、MT5双环境隔离架构总览

### 1.1 架构图

```
                    ┌──────────────┐
                    │  用户自然语言  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         Claude Code     Codex       Hermes
         (STDIO模式)   (HTTP模式)   (辅助分析)
              │            │            │
              ▼            ▼            ▼
    ┌─────────────┐ ┌─────────────┐ ┌──────────┐
    │ sim/        │ │ real/       │ │ 行情分析  │
    │ .env        │ │ .env        │ │ 回测报告  │
    │ mcp_sim.json│ │ mcp_real.json│ │          │
    └──────┬──────┘ └──────┬──────┘ └──────────┘
           │               │
           ▼               ▼
    ┌──────────┐    ┌──────────┐
    │ MT5 Demo │    │ MT5 Live │
    │ 模拟账户  │    │ 实盘账户  │
    │ (完整权限)│    │ (只读锁定)│
    └──────────┘    └──────────┘
```

### 1.2 双环境对照表

| 维度 | 方案A（模拟盘） | 方案B（实盘） |
|------|---------------|--------------|
| **技能标识** | lobster_mt5_dual_env_nl_v1.0 / sim | lobster_mt5_dual_env_nl_v1.0 / real |
| **AI引擎** | Claude Code | Codex |
| **MCP传输** | STDIO（stdio） | HTTP API |
| **监听地址** | 本地进程标准输入输出 | 0.0.0.0:8000 |
| **配置路径** | `MT5-MCP-Server/sim/` | `MT5-MCP-Server/real/` |
| **配置文件** | `sim/.env` + `sim/mcp_sim.json` | `real/.env` + `real/mcp_real.json` |
| **账户类型** | 模拟账户（Demo） | 实盘账户（Live） |
| **操作权限** | 完整策略执行 / 模拟开仓平仓 | 仅行情查询 / 回测 / 禁用下单 |
| **环境变量控制** | 无限制 | `MT5_TRADE_MODE=readonly` |
| **风险等级** | 零资金风险 | 实盘资金，硬锁定保护 |

---

## 二、sim/ 模拟盘环境配置流程

### 2.1 .env 配置模板

文件路径：`E:\龙虾AI主控中心\MT5-MCP-Server\sim\.env`

```ini
# ============================================================
# MT5 MCP Server - 模拟盘 (SIM) 环境变量配置
# 方案A：Claude Code + MCP STDIO 模式，绑定模拟账户
# ============================================================
# ⚠️ 请将下方占位符替换为您的MT5模拟账户信息
# ⚠️ 模拟账户可从MT5客户端「开设模拟账户」获取
# ============================================================

# MT5模拟账户登录号
LOGIN=SIM_LOGIN_PLACEHOLDER

# MT5模拟账户密码
PASSWORD=SIM_PASSWORD_PLACEHOLDER

# MT5模拟账户服务器名（如 FOREX.com-Demo）
SERVER=SIM_SERVER_PLACEHOLDER

# MT5终端程序路径（虚拟盘/模拟盘共用同一终端）
MT5_PATH=C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe
```

### 2.2 mcp_sim.json 配置模板

文件路径：`E:\龙虾AI主控中心\MT5-MCP-Server\sim\mcp_sim.json`

```json
{
  "mcpServers": {
    "metatrader-sim": {
      "command": "metatrader-mcp-server",
      "args": [
        "--login", "SIM_LOGIN_PLACEHOLDER",
        "--password", "SIM_PASSWORD_PLACEHOLDER",
        "--server", "SIM_SERVER_PLACEHOLDER",
        "--transport", "stdio",
        "--path", "C:\\Program Files\\MT5 by FOREX.com Global CN\\terminal64.exe"
      ],
      "env": {
        "MT5_ENV_FILE": "E:\\龙虾AI主控中心\\MT5-MCP-Server\\sim\\.env"
      },
      "description": "MT5模拟盘 MCP Server - 方案A (STDIO模式)，仅绑定模拟账户，允许完整策略执行/模拟开仓平仓"
    }
  }
}
```

### 2.3 部署步骤

```powershell
# 1. 编辑 .env 填入模拟账户信息
# 2. 编辑 mcp_sim.json 将占位符替换为对应值
# 3. 在 Claude Code 中加载此 MCP 配置
claude mcp add --from-file E:\龙虾AI主控中心\MT5-MCP-Server\sim\mcp_sim.json
```

### 2.4 允许的操作清单

- ✅ 完整策略执行（加载/初始化/运行）
- ✅ 模拟开仓 / 平仓
- ✅ 挂单（限价单/止损单/止盈单）
- ✅ 修改持仓止损止盈
- ✅ 行情数据订阅
- ✅ 技术指标计算
- ✅ 历史数据回测
- ✅ 账户信息查询

### 2.5 禁止的操作

- ❌ 严禁在此环境下配置实盘账户凭据
- ❌ 严禁将 mcp_sim.json 中的占位符替换为实盘账号密码

---

## 三、real/ 实盘环境配置流程

### 3.1 .env 配置模板

文件路径：`E:\龙虾AI主控中心\MT5-MCP-Server\real\.env`

```ini
# ============================================================
# MT5 MCP Server - 实盘 (REAL) 环境变量配置
# 方案B：Codex + MT5 HTTP API 模式，绑定实盘账户
# ============================================================
# ⚠️ 高敏配置：请谨慎填写，切勿提交到版本控制
# ⚠️ 实盘操作接口默认关闭，仅开放行情查询与回测
# ============================================================

# MT5实盘账户登录号
LOGIN=REAL_LOGIN_PLACEHOLDER

# MT5实盘账户密码
PASSWORD=REAL_PASSWORD_PLACEHOLDER

# MT5实盘服务器名（如 FOREX.com-Real）
SERVER=REAL_SERVER_PLACEHOLDER

# MT5终端程序路径
MT5_PATH=C:\Program Files\MT5 by FOREX.com Global CN\terminal64.exe

# HTTP API 监听配置（方案B专用）
API_HOST=0.0.0.0
API_PORT=8000
```

### 3.2 mcp_real.json 配置模板

文件路径：`E:\龙虾AI主控中心\MT5-MCP-Server\real\mcp_real.json`

```json
{
  "mcpServers": {
    "metatrader-real": {
      "command": "metatrader-mcp-server",
      "args": [
        "--login", "REAL_LOGIN_PLACEHOLDER",
        "--password", "REAL_PASSWORD_PLACEHOLDER",
        "--server", "REAL_SERVER_PLACEHOLDER",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "env": {
        "MT5_ENV_FILE": "E:\\龙虾AI主控中心\\MT5-MCP-Server\\real\\.env",
        "MT5_TRADE_MODE": "readonly"
      },
      "description": "MT5实盘 MCP Server - 方案B (HTTP API模式)，仅开放行情查询/回测，已屏蔽自动下单接口"
    }
  }
}
```

### 3.3 部署步骤

```powershell
# 1. 编辑 .env 填入实盘账户信息（极端谨慎）
# 2. 编辑 mcp_real.json 将占位符替换为对应值
# 3. 启动 HTTP API 服务
metatrader-mcp-server --host 0.0.0.0 --port 8000 --env E:\龙虾AI主控中心\MT5-MCP-Server\real\.env

# 4. 在 Codex 中加载此 MCP 配置
```

### 3.4 允许的操作清单

- ✅ 行情数据读取（实时报价/历史K线）
- ✅ 技术指标计算
- ✅ 账户信息查询（余额/净值/保证金）
- ✅ 持仓查询
- ✅ 历史订单查询
- ✅ 回测分析

### 3.5 禁止的操作

- ❌ 已屏蔽 自动下单接口（市价单/挂单/修改订单）
- ❌ 已屏蔽 平仓操作
- ❌ 已屏蔽 止损止盈修改
- ❌ 严禁将 `MT5_TRADE_MODE` 改为 `readwrite`

---

## 四、自然语言调用MT5 MCP标准化模板

### 4.1 Codex 内置 MT5 MCP 函数集

Codex通过 `mcp_real.json` 加载MT5 MCP Server后，内置函数集自动注册为可调用工具。

| 函数域 | 典型函数 | 说明 |
|--------|---------|------|
| **行情** | `get_symbol_price` `get_symbol_spread` `get_ticks` | 实时报价/点差/Tick数据 |
| **K线** | `get_candles` `get_ohlc` | 历史K线数据 |
| **账户** | `get_account_info` `get_balance` `get_equity` | 账户信息查询 |
| **持仓** | `get_positions` `get_open_orders` | 持仓/挂单查询 |
| **回测** | `run_backtest` `get_backtest_report` | 历史回测引擎 |
| **指标** | `calculate_ma` `calculate_macd` `calculate_rsi` | 技术指标计算 |

### 4.2 Marvis自然语言中转调度逻辑

```
用户自然语言指令
       │
       ▼
  ┌─ Marvis (自然语言理解) ─┐
  │  1. 意图识别             │
  │  2. 槽位填充             │
  │  3. 风险判定             │
  │  4. 路由分发             │
  └─────────┬───────────────┘
            │
   ┌────────┼────────┐
   ▼        ▼        ▼
Claude     Codex    Hermes
(模拟盘)   (实盘)   (辅助)
```

调度逻辑规则：

| 关键词 | 路由 | 附加检查 |
|--------|------|----------|
| 模拟 / 测试 / 演练 | 方案A (Claude Code STDIO) | 无 |
| 实盘 / 正式 / 上线 | 方案B (Codex HTTP) | 强制只读检查 |
| 行情 / 查询 / 回测 | 优先方案B | 实盘数据更准确 |
| 开仓 / 平仓 / 下单（未明确模拟） | 阻断并垂询确认 | 安全拦截 |

### 4.3 标准化调用模板

调用模板四要素：

```
[操作前缀] [品种] [参数] [风控条件]

示例：
- "模拟买入 0.01手 EURUSD 止损20点"     → 方案A执行
- "查询 XAUUSD 实时行情"                 → 方案B执行
- "回测 EURUSD MA5×MA20策略 近3个月H1"   → 方案B执行
```

---

## 五、Claude Code代理兼容替代方案

### 5.1 Claude Code境外网络依赖

| 依赖项 | 域名/IP | 用途 | 不可用影响 |
|--------|---------|------|-----------|
| Anthropic API | `api.anthropic.com` | 模型推理 | Claude Code完全不可用 |
| npm registry | `registry.npmjs.org` | MCP包安装 | `metatrader-mcp-server` 无法安装/更新 |
| GitHub | `github.com` | 源码/更新 | MCP Server版本更新受阻 |

**结论**：Claude Code对境外网络有**硬依赖**，无代理环境下无法运行。

### 5.2 claude-proxy.bat 代理启动脚本

文件建议路径：`E:\龙虾AI主控中心\MT5-MCP-Server\scripts\claude-proxy.bat`

```batch
@echo off
REM ============================================================
REM Claude Code 4567 代理兼容启动脚本
REM 适用于：Claude Code / npm / git 等境外依赖工具
REM ============================================================

set PROXY_HOST=127.0.0.1
set PROXY_PORT=4567
set PROXY_URL=http://%PROXY_HOST%:%PROXY_PORT%

REM 设置当前会话环境变量
set HTTP_PROXY=%PROXY_URL%
set HTTPS_PROXY=%PROXY_URL%
set NO_PROXY=localhost,127.0.0.1,.local,.cn

REM npm代理
call npm config set proxy %PROXY_URL%
call npm config set https-proxy %PROXY_URL%

REM git代理
call git config --global http.proxy %PROXY_URL%
call git config --global https.proxy %PROXY_URL%

REM 启动 Claude Code
echo ============================================================
echo Claude Code 已通过 4567 代理启动
echo HTTP_PROXY  = %HTTP_PROXY%
echo HTTPS_PROXY = %HTTPS_PROXY%
echo ============================================================

claude
```

### 5.3 MIMO V2.5 Pro 本地替代方案

当Claude Code不可用时，降级到本地替代链：

| 组件 | Claude Code链路 | MIMO V2.5 替代链路 |
|------|----------------|-------------------|
| AI引擎 | Anthropic Claude | MIMO V2.5 Pro (本地LLM) |
| MCP传输 | STDIO | 本地管道或HTTP localhost |
| MT5连接 | metatrader-mcp-server (npm) | MIMO内置MT5 Connector |
| 策略执行 | Claude Code技能库 | MIMO策略引擎 |
| 网络要求 | 必须境外代理 | **完全离线可用** |

MIMO V2.5 Pro优势：
- 零境外网络依赖
- 全本地推理，数据不出本机
- 内置MT5桥接组件
- 支持Python策略脚本直接执行

---

## 六、Codex自然语言指令示例

详见 `E:\龙虾AI主控中心\MT5-MCP-Server\Codex_MT5_NL_Commands.md`。以下列出核心分类：

### 6.1 行情查询类
```
读取黄金实时行情
显示欧元兑美元当前点差
查询XAUUSD买价和卖价
列出所有外汇主要货币对的实时报价
```

### 6.2 策略生成类
```
生成模拟均线交易策略，参数MA5上穿MA20做多
基于MACD交叉设计突破策略，DIF上穿DEA做多
设计RSI超买超卖+布林带突破组合策略
```

### 6.3 回测类
```
回测近30天欧元兑美元数据，周期H1
验证双均线策略过去3个月胜率
对MACD策略进行2026年1月至今的回测，输出夏普比率和最大回撤
```

### 6.4 风控类
```
计算当前持仓风险敞口
设置最大回撤10%预警
检查是否有超过总资金2%风险的单笔持仓
```

### 6.5 模拟交易类
```
模拟买入0.01手EURUSD
模拟做空0.02手XAUUSD，止损设在1950
模拟平仓所有盈利头寸
模拟将所有持仓止损调整至盈亏平衡点
```

### 6.6 账户与统计类
```
显示当前账户余额、净值和浮动盈亏
生成本周交易统计报表，包含胜率和盈亏比
分析EURUSD近期波动率和平均真实波幅ATR
```

---

## 七、文件结构总览

```
E:\龙虾AI主控中心\MT5-MCP-Server\
├── .env                          ← 原始配置（已备份）
├── sim/
│   ├── .env                      ← 模拟盘环境变量
│   ├── mcp_sim.json              ← Claude Code STDIO MCP配置
│   └── README.md                 ← 方案A说明文档
├── real/
│   ├── .env                      ← 实盘环境变量（含 MT5_TRADE_MODE=readonly）
│   ├── mcp_real.json             ← Codex HTTP API MCP配置
│   └── README.md                 ← 方案B说明文档
├── scripts/
│   ├── claude-proxy.bat          ← Claude Code 代理启动脚本
│   └── 4567_proxy_setup.ps1      ← 4567代理配置脚本
└── Codex_MT5_NL_Commands.md     ← Codex自然语言指令清单

E:\龙虾AI主控中心\我的AI分身\技能库\
├── lobster_mt5_dual_env_nl_v1.0\
│   └── SKILL.md                  ← 本技能文件（当前文件）
├── MT5三大问题答疑报告_20260629.md
├── MT5双AI量化链路可行性分析报告_20260629.md
└── backup\
    └── mt5_config_snapshot_20260629\
```

---

## 八、安全守则（最高优先级）

1. **实盘硬锁定**：方案B（real/）环境 `MT5_TRADE_MODE` 必须保持 `readonly`，任何情况下不得改为 `readwrite`
2. **凭据保护**：`.env` 文件中的 LOGIN/PASSWORD/SERVER 为最高敏信息，严禁提交版本控制、严禁日志回显、严禁截图分享
3. **双环境隔离**：sim/ 和 real/ 的配置文件物理分离，互不引用，互不穿透
4. **审计追踪**：所有实盘配置变更必须纳入 `backup/` 快照管理
5. **指令拦截**：涉及「开仓/平仓/下单」且未明确标注「模拟」的自然语言指令，必须在 Marvis 层阻断并垂询确认

---

## 九、关联技能

- lobster_task_standard_workflow_v2.3_locked V2.5（龙虾五步法，本技能遵循其五大步骤沉淀）
- lobster_mt5_quant_mcp_deploy_v1.0（MT5双AI量化MCP对接运维，环境诊断→组件部署→链路配置→服务巡检）
- lobster_codex_dual_link_v1.0（Codex双链路架构，端口身份地图+主备链路隔离+一键切换）
- direct-network-recovery-rollback v1.0（直连网络恢复，全域9大程序通用兜底）
- workbuddy-recovery-rollback v1.0（WorkBuddy网络故障诊断与修复）

---

## 十、版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-06-29 | 首发版，基于V2.4架构锁定期MT5双环境隔离部署实战沉淀 |

*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
