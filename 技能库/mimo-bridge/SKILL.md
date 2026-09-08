---
name: "mimo-bridge"
description: "让 WorkBuddy / 任意 Agent 直接调用小米 MiMO V2.5 Pro API 做推理，绕过 Hy3 积分消耗。适用于需要低成本长程推理、量化代码生成、Agent 自主多步执行的场景。当用户说'用 MiMO 跑/分析/生成'时激活。"
version: "1.0"
date: "2026-07-14"
author: "WorkBuddy + 龙虾AI主控中心"
tags: ["mimo", "bridge", "省钱", "api", "量化"]
primary_path: "~/.workbuddy/skills/mimo-bridge/SKILL.md"
shared_path: "E:/龙虾AI主控中心/我的AI分身/技能库/mimo-bridge/SKILL.md (待镜像)"
---

# MiMO Bridge — 直连小米 MiMO V2.5 Pro

> **目的**：把"重推理"从 WorkBuddy(Hy3) 的积分账单上摘下来，改走你已付费的 MiMO Token Plan。
> **核心引擎**：MiMO V2.5 Pro | **端点**：`https://token-plan-cn.xiaomimimo.com/v1` | **模型**：`mimo-v2.5-pro`

---

## 一、何时激活本技能

- 用户明确要求"用 MiMO 跑 / 分析 / 生成 / 回测"，而不是消耗 WorkBuddy 积分
- 任务需要 **长上下文(1M)**、**低成本 Token**、**Agent 自主多步工具调用**
- MiMO 链路健康（CC-Switch:15721 → AI Code Switch:4567 → MiMO:18808 通）

---

## 二、端点与鉴权

| 项 | 值 |
|----|----|
| Base URL | `https://token-plan-cn.xiaomimimo.com/v1` |
| 模型名 | `mimo-v2.5-pro` |
| 本地代理端口 | `18808`（CC-Switch 中转后） |
| 鉴权头 | `Authorization: Bearer $MIMO_API_KEY` |

**获取 API Key（不要硬编码到脚本）**：
- 从你的 CC-Switch / AI Code Switch 配置文件读取
- 或设置环境变量 `MIMO_API_KEY`（推荐）
- 位置参考：`E:\龙虾AI主控中心\我的AI分身\CODEX量化策略20260615\嘉盛\黄金黑马策略\Doc\` 下的链路排障报告

---

## 三、调用示例（curl）

```bash
curl https://token-plan-cn.xiaomimimo.com/v1/chat/completions \
  -H "Authorization: Bearer $MIMO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mimo-v2.5-pro",
    "messages": [{"role":"user","content":"帮我写一个双均线黄金策略回测代码"}],
    "max_tokens": 4096,
    "temperature": 0.3
  }'
```

## 四、调用示例（Python，推荐用托管运行时）

```python
import os, requests
resp = requests.post(
    "https://token-plan-cn.xiaomimimo.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['MIMO_API_KEY']}"},
    json={"model":"mimo-v2.5-pro",
          "messages":[{"role":"user","content":"总结这段回测日志并给优化建议"}],
          "max_tokens":4096},
    timeout=120,
)
print(resp.json()["choices"][0]["message"]["content"])
```

---

## 五、成本参考（为什么要用它省积分）

| 维度 | MiMO V2.5 Pro | WorkBuddy(Hy3) 积分 |
|------|---------------|---------------------|
| 计费 | 输入 ¥1/百万 + 输出 ¥4/百万（缓存低至 ¥0.25） | 消耗 CodeBuddy 积分 |
| 长程 Agent 任务 | 极便宜（Token 效率高 40-60%） | 积分消耗可观 |
| 结论 | **重推理首选 MiMO** | 仅用于对话/编排/文档 |

---

## 六、失败回退链

```
MiMO 不可达？
  ├─ 检查 CC-Switch:15721 / AI Code Switch:4567 / MiMO:18808 是否在跑
  ├─ 检查 MIMO_API_KEY 是否过期（今晚8点后续费）
  └─ 仍不行 → 切本地 Ollama（见 ollama-bridge 技能，免费热备）
       仍不行 → 提示用户检查端口/续费，不要静默失败
```

---

## 七、关联技能

| 技能 | 关系 |
|------|------|
| `ollama-bridge` | 本地免费后备 |
| `多智能体舰队编排` | 整体舰队架构与路由 |
| `龙虾五步法` | 变更前备份规范 |
