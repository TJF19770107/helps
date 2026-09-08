---
name: "lobster_fleet_tencent_hy3_cloud_bridge"
description: "腾讯云混元3(hy3-preview)云函数中转穿透方案：解决10亿免费Token仅限小程序SDK/云函数调用的硬性限制，通过云函数中转实现本地Agent免费调用hy3，含双模型额度隔离监控、一键回滚、分阶段SOP。"
version: "1.0.0"
date: "2026-07-19"
updated: "2026-07-19 (首次创建，基于CloudBase控制台截图实证)"
merged_from: ["lobster_fleet_hy3_integration v1.0", "混元hy3接入与额度对比方案 v2.0"]
sync_mode: "bidirectional"
primary_path: "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_fleet_tencent_hy3_cloud_bridge\SKILL.md"
---

# 技能：腾讯云 hy3 云函数中转穿透（免费额度方案）

## 触发条件
当任务涉及以下场景时，自动激活本技能：
- 提及「hy3 免费 Token」或「小程序成长计划」
- 需要将 hy3/hy3-preview 接入多 Agent 舰队但担心付费风险
- CloudBase 控制台显示「仅允许 SDK/云函数消耗」
- 需要双模型（hy3 + Qwen2.5）额度隔离监控
- 需要执行 hy3 → Qwen2.5 一键回滚

## 核心发现（铁律 · 截图实证 2026-07-19）

| 限制项 | 详情 | 应对 |
|--------|------|------|
| **免费Token使用范围** | 仅允许「小程序SDK」+「云函数调用」消耗 | 部署 `hy3-relay-proxy` 云函数 |
| **本地直调后果** | 走**付费计费通道**，不扣免费额度 | **禁止**本地直连 hy3 API |
| **MiniMax-M2.5 下线** | 2026-08-07 | hy3 或 kimi-k2.6 替代 |
| **高负载下可用周期** | 10亿Token ≈ **17~33天**（三Agent全速） | 分阶段灰度 + 限流 + 监控 |

## 两套方案

### 方案 A：云函数中转（推荐 · 主力）
```
本地Agent(15731) → 云函数(hy3-relay-proxy) → hy3 API (免费抵扣)
```
- 本地代理：`hy3_cloud_relay_client.py --mode serve`
- 端口 15731（与 MiMO 桥接 15721 分离）
- 内置用量统计 + 50%/80%/95% 三级告警

### 方案 B：本地降级（必备兜底）
```
所有Agent → Qwen2.5(MiMO/Ollama) → 零成本
```
- 一键回滚：`rollback_to_qwen.ps1`
- 秒级切换，零风险

## 快速操作指南

```bash
# 1) 测试连通性（需先部署云函数）
python hy3_cloud_relay_client.py --mode test

# 2) 启动本地代理
python hy3_cloud_relay_client.py --mode serve

# 3) 查看用量
python hy3_cloud_relay_client.py --status

# 4) 双模型监控
python hy3_qwen_dual_monitor.py --check

# 5) 回滚到Qwen2.5
powershell -ExecutionPolicy Bypass -File rollback_to_qwen.ps1
```

## 配置模板

### Claude Code（云中转模式）
```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:15731",
    "DISABLE_AUTOUPDATE": "1"
  }
}
```

### Codex（云中转模式，双文件！）
```toml
[api]
base_url = "http://127.0.0.1:15731/v1"
model_provider = "custom"
requires_openai_auth = false
env_key = "OPENAI_API_KEY"
wire_api = "chat_completions"
```

## 四阶段落地

| Phase | 内容 | 时长 | 通过标准 |
|-------|------|------|---------|
| 0 | 前置准备（EnvID/Secret/备份） | 2h | 凭证就位 |
| 1 | 部署云函数 + 连通验证 | 1~2天 | test模式3次PASS + 免费扣减确认 |
| 2 | Codex单Agent灰度7天 | 7天 | 日均<5000万tokens + 质量≥3分 |
| 3 | 全舰队分批切换 | 15天 | 每阶段48h异常率<5% |
| 4 | 长期配额管理 | 持续 | 月度≤3亿tokens + 双监控守护 |

## 关键文件索引

| 文件 | 路径 |
|------|------|
| 主方案文档 | `E:\...\docs\多Agent舰队编排\混元hy3接入与额度对比方案.md` |
| 云函数源码(index.js) | 待部署至 CloudBase 控制台 |
| 本地中转代理 | `E:\...\scripts\hy3_cloud_relay_client.py` |
| 双模型监控 | `E:\...\scripts\hy3_qwen_dual_monitor.py` |
| 一键回滚脚本 | `E:\...\scripts\rollback_to_qwen.ps1` |

## 关联技能/协议

| 关联项 | 说明 |
|--------|------|
| `lobster_fleet_hy3_integration` | 上版技能（假设无限制的直连方案） |
| `orca-agent-connection-fix` v1.2.0 | 协议桥修复（15721端口管理） |
| 全域模板 #293.8 | 免费额度穿透规范 |
| 五步法V2.7 | 新增「第三方云端免费额度前置校验」步骤 |

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-07-19 | 初始版本，基于CloudBase控制台截图实证 |
