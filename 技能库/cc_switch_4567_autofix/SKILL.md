---
name: "cc_switch_4567_autofix"
description: "cc-switch→AI Code Switch(4567)→MiMO 全链路 404/400/502/断连故障一键修复技能。根因：cc-switch 的 provider baseURL 缺 /v1 前缀(拼接出 4567/responses 而非 4567/v1/responses) 或 4567 进程宕机(server.pid 僵尸)。覆盖 gpt-5.5 模型名重写、/opencode/v1 错误后缀、E盘满导致4567崩溃。触发词：cc-switch 404、127.0.0.1:4567转发、baseURL缺失/v1前缀、provider_endpoints数据库路由错误、Codex++报错、stream disconnected、gpt-5.5 unsupported、reconnecting"
version: "1.0"
date: "2026-07-19"
author: "WorkBuddy (lobster workflow)"
sync_mode: "forward"
primary_path: "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\cc_switch_4567_autofix\\SKILL.md"
depends_on: ["lobster_auto_iterate", "lobster_task_standard_workflow_v2.7"]
---

# cc-switch → 4567 → MiMO 全链路修复技能 V1.0

## 链路架构（权威定义，禁止再推翻）

```
Codex++ 桌面版 (GUI, 模型选择器锁定 gpt-5.5)
        │  POST /v1/responses
        ▼
cc-switch :15721  (E:\龙虾AI主控中心\CC-Switch\cc-switch.exe)
        │  从 providers 表读 base_url 转发
        │  ⚠️ 拼接逻辑: base_url + "/responses"  (不带 /v1 前缀!)
        ▼
AI Code Switch :4567  (E:\aicodeswitch_v5 → G盘 Junction)
        │  模型名重写 gpt-5.5 → mimo-v2.5-pro
        │  路径适配 /v1/responses
        ▼
MiMO 后端 (token-plan-cn.xiaomimimo.com/v1)
```

**关键拼接规则（V1.3 颠覆性修正，此前 V1.0-V1.2 全部做反）：**
```
base_url 必须是 http://127.0.0.1:4567/v1  (带 /v1)
→ cc-switch 拼出 http://127.0.0.1:4567/v1/responses  ✅ 200

❌ 错误: base_url = http://127.0.0.1:4567 (无 /v1)
→ 拼出 http://127.0.0.1:4567/responses  → 404 Not Found
```

---

## 错误类型与根因

| 类型 | 报错现象 | 根因 | 修复入口 |
|------|---------|------|---------|
| A | `400 Unsupported model gpt-5.5` | cc-switch 直连 MiMO 绕过4567重写层 | 改 provider 走 4567 |
| B | `502 Bad Gateway` | 4567 进程挂了/server.pid 僵尸 | 清 pid + 重启4567 |
| C | `404 Not Found` on /responses | base_url 缺 /v1 前缀 (本技能核心!) | DB 补 /v1 |
| D | `stream disconnected before completion` | 4567 完全宕机未监听 | 启动4567 |
| E | `404 /opencode/v1/responses` | base_url 含 /opencode/v1 错误后缀 | DB 去 /opencode |

---

## 一键修复（首选）

**双击 `codex_fullchain_fix_v2.1.bat`**（位于 `我的AI分身\技能库\cc_switch_4567_autofix\`），自动完成：
强杀 cc-switch → 修 DB(/v1前缀) → 清理僵尸 pid → 启动 4567 → 启动 cc-switch → 全链路测试

---

## 手动修复流程

### 1. 端口诊断
```bash
netstat -ano | grep -E ":15721|:4567"
```
- 4567 不在 → 进步骤2
- 15721 不在 → 强杀后重启动 cc-switch

### 2. 启动 AI Code Switch 4567
```bash
# 清理僵尸 pid (关键!)
del /F C:\Users\Administrator\.aicodeswitch\server.pid
# 通过 Junction 启动 (数据在G盘)
cd /d E:\aicodeswitch_v5
node node_modules\aicodeswitch\bin\cli.js start --port 4567
```

### 3. DB 修复（核心，cc-switch 必须停止时执行）
```bash
# ※ 必须先杀 cc-switch 释放 DB 锁
taskkill /F /IM cc-switch.exe

LIVE_DB="E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db"

# Fix A: xiaomimimo20260612 (Codex实际用的 provider!) 补 /v1
sqlite3 "$LIVE_DB" "UPDATE providers SET settings_config =
  REPLACE(settings_config, 'base_url\":\"http://127.0.0.1:4567\"',
                       'base_url\":\"http://127.0.0.1:4567/v1\"')
  WHERE id='xiaomimimo20260612';"

# Fix B: aicodeswitch provider 补 /v1
sqlite3 "$LIVE_DB" "UPDATE providers SET settings_config =
  REPLACE(settings_config, 'baseURL\":\"http://127.0.0.1:4567\"',
                       'baseURL\":\"http://127.0.0.1:4567/v1\"')
  WHERE id='aicodeswitch';"

# Fix C: provider_endpoints id=15,21 补 /v1
sqlite3 "$LIVE_DB" "UPDATE provider_endpoints SET url='http://127.0.0.1:4567/v1' WHERE id IN (15,21);"

# Fix D: 清理 /opencode/v1 错误后缀
sqlite3 "$LIVE_DB" "UPDATE providers SET settings_config =
  REPLACE(settings_config, '4567/opencode/v1', '4567/v1') WHERE id='aicodeswitch';"

# Fix E: 确保不直连 MiMO
sqlite3 "$LIVE_DB" "UPDATE providers SET settings_config =
  REPLACE(settings_config, 'token-plan-cn.xiaomimimo.com', 'http://127.0.0.1:4567/v1')
  WHERE id LIKE 'xiaomimimo%';"

# Fix F: 🔴 兜底! 所有 providers 中 4567 缺/v1 一律补齐 (实测曾漏掉 d240abd2-... Codex provider)
sqlite3 "$LIVE_DB" "UPDATE providers SET settings_config =
  REPLACE(settings_config, 'http://127.0.0.1:4567\"', 'http://127.0.0.1:4567/v1\"')
  WHERE settings_config LIKE '%127.0.0.1:4567\"%' AND settings_config NOT LIKE '%127.0.0.1:4567/v1%';"
```

### 4. 验证（修复后必须执行）
```bash
# 直接测 4567
curl -s http://127.0.0.1:4567/v1/responses -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","input":"hi"}'   # 应返回 MiMO 响应

# 经 15721 全链路
curl -s http://127.0.0.1:15721/v1/responses -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","input":"hi"}'   # 不应含 error 字段
```

### 5. 重启 cc-switch（必须用 start 窗口模式）
```bash
# 杀干净
taskkill /F /IM cc-switch.exe
# 等端口释放
# 启动 (窗口模式，确保绑定)
start "" "E:\龙虾AI主控中心\CC-Switch\cc-switch.exe"
```

---

## 回滚预案
```bash
# 还原 cc-switch.db 到快照
BKUP="G:/龙虾AI主控中心/Codex备份/snapshots/<日期>/cc-switch.db.pre-fix.db"
cp "$BKUP" "E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db"
```

## 防复发清单
- [ ] 所有 4567 URL 带 /v1 前缀（xiaomimimo20260612 / aicodeswitch / provider_endpoints）
- [ ] 无 /opencode/v1 残留
- [ ] server.pid 无僵尸 PID
- [ ] E/G Junction 有效
- [ ] 启动前跑 `cc_switch_precheck` 自动校验

---

## 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-07-19 | v1.0 | 从 cc-switch 404 反复故障中沉淀。明确 URL 拼接需 /v1 前缀；封装一键 BAT；定义回滚与防复发清单 |
