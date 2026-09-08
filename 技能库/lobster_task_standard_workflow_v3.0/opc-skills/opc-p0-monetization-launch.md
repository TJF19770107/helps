---
name: opc-p0-monetization-launch
title: OPC P0 变现启动包生成器
version: 1.0.0
date: 2026-08-19
author: OPC 庄家团 / opc-orchestrator
cost: 0 积分（本地产出，不联网不派子Agent）
triggers: [一人公司变现, P0服务包, 落地页, 报价单, 接单剧本, 跑通首笔, monetization launch, opc p0]
depends:
  - agency-agents/one-person-company/monetization-architect.md
  - agency-agents/one-person-company/pricing-strategist.md
  - agency-agents/one-person-company/private-domain-closer.md
  - opc-doc/outputs/07-conversion-loop/conversion-loop.md
  - opc-doc/outputs/08-asset-ops/asset-ops.md
---

# OPC P0 变现启动包生成器（四化蒸馏技能）

> 把「一人公司启动规划」九阶段产出，一键蒸馏为可直接拿去卖的 P0 服务包成品。
> 遵循龙虾五步法 V3.6（检查→分析→修复→迭代→沉淀）+ 全域模板 + 仓颉 RIA-TV++。

## 适用场景
用户已完成 OPC 阶段01~09，需要"跑通首笔真实变现"，但缺可直接面向客户的物料。

## 四化映射（本技能自身）
- **智能化**：自动识别"变现启动"意图，调度变现铁三角（monetization-architect + pricing-strategist + private-domain-closer）。
- **定制化**：套用龙虾本地路径 `E:/龙虾AI主控中心/我的AI分身/opc-doc/outputs/10-monetization-launch/`，兼容 CNB/企微。
- **全自动化**：九阶段产出 → P0 包（文案/落地页/报价单/剧本）→ 四化蒸馏 → CNB 同步，一气呵成。
- **自我进化**：每次成交后回灌客户台账与案例，强化报价锚点与话术。

## 执行 SOP（0 积分）
1. **检查**：读取阶段07转化闭环（报价体系）与阶段08资产沉淀（P0 定义）。
2. **分析**：确定三档价格锚点（轻启动¥1,980 / 标准¥4,980 / 全案¥9,800），对齐已有 bracket。
3. **生成**：并行写 4 份成品到 `10-monetization-launch/`：
   - `service-package-copy.md`（文案，套全域模板）
   - `landing-page.html`（light 主题，自包含）
   - `quote-sheet.html`（可打印，里程碑付款）
   - `seed-customer-playbook.md`（私域 SOP）
4. **蒸馏**：更新 `sihua-index.md` 阶段10 条目 + 本技能文件注入技能池。
5. **同步**：copy 到 `企业微信群定制接单项目/.cnb/` 对应目录，git commit + push CNB（用 CNB_TOKEN oauth2 认证）。

## 价格锚点（不要偏离）
| 档位 | 价格 | 主推 |
|------|------|------|
| 轻启动版 | ¥1,980 | 低门槛 |
| 标准版 | ¥4,980 | ✅ 推荐 |
| 全案陪跑版 | ¥9,800 | 高意向 |

## 真实性边界（重要）
本技能只生成"可自动化的物料"——**真实客户与真实收款必须由用户在现实世界完成**。
生成后可提示用户：用接单剧本找 1 个种子客户，按里程碑付款跑通首笔 ≥¥1,000 收款，即验证阶段07→09。

## 成本约束
- 预算积分：0 ｜ 实际：0
- 禁止：派发子 Agent、联网、触发云端构建、重复读取已读文件。
