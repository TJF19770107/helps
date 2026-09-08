# MCP 迁移清单
# 基准节点: base_20260619_0424_initial_success
# 迁移时间: 2026-06-19
# 目标路径: E:\龙虾AI主控中心\我的AI分身\技能库\MCP

## 存量 MCP 组件迁移

| # | 源路径 | 类型 | 目标分类 | 状态 |
|---|--------|------|---------|------|
| 1 | ~/.cc-switch/backups/hermes/hermes_*.yaml | hermes 备份 | exchange_mcp | 存量归档 |
| 2 | ~/.cc-switch/backups/lobster_fix_final_*/cc-switch.config.json | 配置快照 | common_mcp | 存量归档 |
| 3 | ~/.cc-switch/backups/lobster_fix_final_*/cc-switch.settings.json | 设置快照 | common_mcp | 存量归档 |
| 4 | ~/.cc-switch/skills/global-stock-data/skill_config.yaml | 技能配置 | stock_mcp | 源仓保留 |
| 5 | ~/.cc-switch/skills/collector_five_in_one_v*/ | 数据采集器 | exchange_mcp | 源仓保留 |
| 6 | ~/.cc-switch/skills/gstack/ (MCP SDK 依赖) | SDK | common_mcp | 源仓保留 |

## 存量迁移策略

CC Switch 内部 MCP 相关文件采用「源仓保留 + 索引映射」策略：
- .cc-switch/skills/ 目录是 CC Switch 的技能注册表，保留原位置不动
- 通过 CC Switch config.json 中的 `mcp_servers.scan_paths` 指向技能库 MCP 目录实现双路径扫描
- 存量备份文件 (backups/) 作为历史节点保留，不做物理迁移

## 本次新建 MCP 组件

| # | 名称 | 文件 | 分类目录 | 状态 |
|---|------|------|---------|------|
| 1 | binance_spot_mcp.yaml | 币安现货交易 | exchange_mcp | ✅ 新建 |
| 2 | binance_market_data_mcp.yaml | 币安行情数据 | exchange_mcp | ✅ 新建 |
| 3 | sentiment_fng_mcp.yaml | 情绪数据 | sentiment_mcp | ✅ 新建 |
| 4 | onchain_glassnode_mcp.yaml | 链上数据(预留) | onchain_mcp | ✅ 新建 |
| 5 | defi_llama_mcp.yaml | DeFi 生态数据 | defi_mcp | ✅ 新建 |
| 6 | global_stock_data_mcp.yaml | 美股/港股数据 | stock_mcp | ✅ 新建 |
| 7 | vibe_trading_orchestrator_mcp.yaml | Vibe-Trading 调度 | common_mcp | ✅ 新建 |

## CC Switch 配置变更

- 文件: ~/.cc-switch/config.json
- 变更: mcp_servers 新增 scan_paths、auto_scan、scan_interval_seconds
- 挂载路径: E:\龙虾AI主控中心\我的AI分身\技能库\MCP
- 自动扫描: 已启用，扫描间隔 300 秒

## 迁移统计

- 存量 MCP 相关文件: 6 组（源仓保留，不做物理迁移）
- 本次新建 MCP: 7 套
- 总 MCP 组件: 7 套（新建）+ 存量映射
