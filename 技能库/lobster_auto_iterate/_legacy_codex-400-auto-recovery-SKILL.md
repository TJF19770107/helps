---
name: "codex-400-auto-recovery"
description: "Codex++ 400/502/404 错误自动恢复技能。一键诊断+修复+校验，永久根除反复复发。覆盖gpt-5.5/502 Bad Gateway/v1/responses 404三大错误类型。基于龙虾五步法V2.6，含E/G盘健康检查、AI Code Switch(4567)拉起、cc-switch端点修复、server.pid清理、全链路curl验证。触发词：codex 400错误、codex 502、codex 404、gpt-5.5 unsupported model、codex修复、codex恢复、codex用不了、codex报错、reconnecting"
version: "1.3"
date: "2026-07-19"
author: "WorkBuddy AI ( lobster workflow )"
trigger_keywords:
  - "codex 400"
  - "codex 502"
  - "codex 404"
  - "gpt-5.5 unsupported"
  - "unsupported model"
  - "bad gateway"
  - "reconnecting"
  - "v1/responses"
  - "透传失败"
  - "codex修复"
  - "codex恢复"
  - "codex用不了"
  - "codex报错"
sync_mode: "forward"
primary_path: "E:\\龙虾AI主控中心\\我的AI分身\\技能库\\codex-400-auto-recovery\\SKILL.md"
---

# Codex++ 400/502/404 错误自动恢复技能 v1.1

## 支持的错误类型

| 错误 | HTTP码 | 现象 | 根因 |
|------|--------|------|------|
| **Type-A** | `400 Unsupported model gpt-5.5` | MiMO拒绝模型名 | cc-switch直连MiMO，绕过4567重写层 |
| **Type-B** | `502 Bad Gateway` | 连接4567失败 | AI Code Switch(4567)进程挂了/server.pid残留僵尸PID |
| **Type-C** | `404 Not Found` (on /v1/responses) | 端点不存在 | cc-switch端点URL带`/v1`或`/opencode/v1`错误路径后缀 |
| **Type-D** | `stream disconnected before completion` (截图报错) | 4567未监听 | AI Code Switch(4567)完全宕机需重新拉起 |

### 🔴🔴🔴 关键规则：URL 拼接逻辑（V1.3 核心发现）

**cc-switch 的路径拼接规则：**
```
cc-switch 转发路径 = provider.baseURL + API路径
```

| API格式 | cc-switch拼接的API路径 | baseURL必须为 | 最终正确URL |
|---------|----------------------|--------------|-----------|
| Responses (Codex++用) | `/responses` | `http://127.0.0.1:4567/**/v1**` | `http://127.0.0.1:4567/v1/responses` ✅ |
| Chat Completions | `/chat/completions` | `http://127.0.0.1:4567/**/v1**` | `http://127.0.0.1:4567/v1/chat/completions` ✅ |

**❌ 错误做法（V1.0-V1.2犯的错）：**
```
baseURL = http://127.0.0.1:4567  (无/v1)
→ 拼接后 = http://127.0.0.1:4567/responses → 404 Not Found!
```

**✅ 正确做法（V1.3修正）：**
```
baseURL = http://127.0.0.1:4567/v1  (带/v1)
→ 拼接后 = http://127.0.0.1:4567/v1/responses → 200 OK!
```

**需要修复的位置（全部都要带 /v1）：**
1. `providers` 表 → `xiaomimimo20260612` 的 `base_url` 字段 ⚠️ **Codex实际用这个！**
2. `providers` 表 → `aicodeswitch` 的 `options.baseURL` 字段
3. `provider_endpoints` 表 → id=15, id=21 的 `url` 字段

## 根因架构图

```
Codex++ 桌面版
├── GUI模型选择器 → gpt-5.5（硬编码，无法改）
│
└── 请求发出(两种API格式):
    ├── /v1/chat/completions (Chat格式) ──┐
    └── /v1/responses      (Responses格式) ──┤
                                              │
                              ┌────────────────▼──────────────┐
                              │     cc-switch :15721 (E盘程序)   │
                              │  从DB读取base_url → 转发请求      │
                              └──────────────┬──────────────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
          base_url=                      base_url=               base_url=
          xiaomimimo.com/v1           127.0.0.1:4567        127.0.0.1:4567
          (直连MiMO)              (正确✅)              (带/v1后缀❌)
                    │                        │                        │
                    ▼                        ▼                        ▼
              ┌──────────┐            ┌──────────────┐         ┌──────────┐
              │ Type-A   │            │   ✅ 正常     │         │ Type-C   │
              │ 400错误  │            │  4567重写模型 │         │ 404错误  │
              │(MiMO拒接)│            │  路径自动适配 │         │(路径拼接错)│
              └──────────┘            └──────┬───────┘         └──────────┘
                                            │
                                    ┌───────▼────────┐
                                    │ AI Code Switch │
                                    │    :4567 (G盘)  │
                                    │ Junction从E盘  │
                                    └───────┬────────┘
                                            │
                                    ┌───────▼────────┐
                                    │   MiMO 后端     │
                                    │  (支持两种格式) │
                                    └────────────────┘
```

---

## 一键自动恢复流程

### Phase 1: 快速诊断（30秒内完成）

```bash
# 1.1 检查端口
netstat -ano | grep -E ":15721|:4567"

# 1.2 检查磁盘空间
df -h /e /g

# 1.3 检查server.pid是否陈旧（导致启动失败）
cat /c/Users/Administrator/.aicodeswitch/server.pid 2>/dev/null
PID=$(cat /c/Users/Administrator/.aicodeswitch/server.pid 2>/dev/null)
tasklist | grep "$PID" || echo "[WARN] PID $PID 不存在! 需要删除server.pid"

# 1.4 三维链路测试
# Test A: 4567的chat/completions（基础能力）
curl -s --max-time 15 http://127.0.0.1:4567/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","messages":[{"role":"user","content":"test"}],"max_tokens":10}'

# Test B: 4567的/responses（Codex++实际用的！）
curl -s --max-time 15 http://127.0.0.1:4567/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","input":"test"}'

# Test C: 经15721的完整链路（最关键的测试）
curl -s --max-time 25 http://127.0.0.1:15721/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","input":"test"}'
```

**诊断决策矩阵：**

| Test A(4567 chat) | Test B(4567 resp) | Test C(15721 resp) | 诊断 | 进入Phase |
|-------------------|--------------------|---------------------|------|-----------|
| ❌ | ❌ | ❌ | 4567挂了 | **2B** |
| ✅ | ✅ | ❌ | cc-switch没路由到4567或路径错 | **2A** |
| ✅ | ✅ | ✅ | 全正常！问题在GUI缓存 | **2D** |
| ❌(E盘满) | — | — | E盘满导致4567崩溃 | **2C** |
| ✅ | ❌ | — | 4567不支持responses格式 | **2B**(升级) |

### Phase 2A: 修复 cc-switch DB（核心修复，解决Type-A/B/C）

```bash
export MSYS_NO_PATHCONV=1
LIVE_DB="E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db"
SQL="/c/ProgramData/chocolatey/bin/sqlite3"

# ⚠️ 必须先停止cc-switch才能让修改生效！
# 用 restart_ccswitch_fix.bat 或手动杀进程

# ======== 关键：所有URL必须是不带路径后缀的根地址 ========
# provider_endpoints: 去掉所有 /v1 后缀
"$SQL" "$LIVE_DB" "UPDATE provider_endpoints SET url = REPLACE(url, 'http://127.0.0.1:4567/v1', 'http://127.0.0.1:4567') WHERE url LIKE '%4567%';"

# providers.settings_config: 去掉 /v1 后缀（TOML和JSON两种格式都要处理）
"$SQL" "$LIVE_DB" "UPDATE providers SET settings_config = REPLACE(settings_config, '4567/v1', '4567') WHERE settings_config LIKE '%4567/v1%';"

# ⚠️ V1.2 新增：修复 aicodeswitch provider 的 /opencode/v1 后缀（根因！）
# 这个后缀导致 cc-switch 转发到 4567/opencode/v1/responses → 404
"$SQL" "$LIVE_DB" "UPDATE providers SET settings_config = REPLACE(settings_config, '4567/opencode/v1', '4567') WHERE id = 'aicodeswitch';"

# proxy_live_backup: 去掉 /v1 后缀
"$SQL" "$LIVE_DB" "UPDATE proxy_live_backup SET original_config = REPLACE(original_config, '4567/v1', '4567') WHERE original_config LIKE '%4567/v1%';"

# settings表: 如果有也要更新
"$SQL" "$LIVE_DB" "UPDATE settings SET value = REPLACE(value, '4567/v1', '4567') WHERE value LIKE '%4567/v1%';"

# 验证：不应再有 4567/v1 或 4567/opencode 的残留
"$SQL" "$LIVE_DB" "SELECT COUNT(*) as bad_urls FROM (
  SELECT url FROM provider_endpoints WHERE url LIKE '%4567/%'
  UNION ALL SELECT settings_config FROM providers WHERE settings_config LIKE '%4567/%'
  UNION ALL SELECT original_config FROM proxy_live_backup WHERE original_config LIKE '%4567/%'
);"
# 预期返回 0

# 重启cc-switch（必须！）
"E:/龙虾AI主控中心/CC-Switch/cc-switch.exe" &
```

### Phase 2B: 重启 AI Code Switch (4567)

```bash
export MSYS_NO_PATHCONV=1

# Step 1: 清理陈旧pid文件（关键前置步骤）
rm -f "/c/Users/Administrator/.aicodeswitch/server.pid"

# Step 2: 通过Junction启动（数据在G盘）
"/c/Program Files/nodejs/node.exe" "E:/aicodeswitch_v5/node_modules/aicodeswitch/bin/cli.js" start &

# Step 3: 等8秒验证
sleep 8
netstat -ano | grep ":4567.*LISTENING"
cat "/c/Users/Administrator/.aicodeswitch/server.pid"
```

**启动失败排查：**
- `EPERM: operation not permitted, unlink 'server.pid'` → 先手动删pid再启动
- `EACCES / ENOSPC` → E盘满，先执行 Phase 2C

### Phase 2C: E 盘空间紧急清理

```bash
# 安全清理候选（按优先级，已验证安全）:
rm -rf /e/aicodeswitch_v5_backup_pre_junction  # 16MB Junction旧备份
rm -rf /e/tmp/*                               # 2.5GB临时文件
# CC-Switch backups只保留最近2份
ls -t /e/龙虾AI主控中心/CC-Switch/.cc-switch/backups/* | tail -n +3 | xargs rm -f

df -h /e  # 确认释放后空间
```

### Phase 2D: Codex++ GUI 缓存清理

如果 Phase 1 全部通过但 Codex++ 仍报错：
1. **重启 Codex++**（最简单有效）
2. 如果还不行：删除 `AppData\Roaming\Codex\Local Storage\leveldb\` （⚠️ 会丢失对话历史）
3. 最后手段：右下角模型下拉框切换为 `mimo-v2.5-pro`

### Phase 3: 校验（修复后必须执行）

```bash
# 最终全链路测试（同时测试两种API格式）

echo "=== Chat Completions 格式 ==="
curl -s --max-time 30 http://127.0.0.1:15721/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","messages":[{"role":"user","content":"say OK"}],"max_tokens":15}'

echo ""
echo "=== Responses 格式(Codex++实际使用) ==="
curl -s --max-time 30 http://127.0.0.1:15721/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","input":"say OK"}'

# 两个都不含 error 字段 = ✅ 修复成功
```

---

## 一键重启脚本

### V2 完整版（推荐）：`codex_fullchain_fix_v2.bat`
覆盖全部错误类型，含DB修复+PID清理+4567拉起+全链路测试：
```bat
@echo off
:: 见 codex_fullchain_fix_v2.bat (龙虾五步法完整实现)
```

### V1 精简版：`restart_ccswitch_fix.bat`（仅重启cc-switch）

```bat
@echo off
chcp 65001 >nul
echo [Step 1] 停止cc-switch...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":15721.*LISTENING"') do taskkill /F /PID %%a >nul 2>&1
timeout /t 3 /nobreak >nul

echo [Step 2] 启动cc-switch...
start "" /B "E:\龙虾AI主控中心\CC-Switch\cc-switch.exe"
timeout /t 8 /nobreak >nul

echo [Step 3] 测试链路...
curl -s --max-time 30 http://127.0.0.1:15721/v1/responses -H "Content-Type: application/json" -d "{\"model\":\"gpt-5.5\",\"input\":\"ok\"}"
pause
```

---

## 备份策略

| 备份目标 | 位置 | 内容 | 频率 |
|---------|------|------|------|
| **全量快照** | `G:\龙虾AI主控中心\Codex备份\snapshots\<日期>\` | config.toml, cc-switch.db, aicodeswitch fs-db, Preferences, Local State | 每次修复前 |
| **cc-switch.db增量** | `.cc-switch/backups/` | cc-switch自动备份 | 自动 |
| **回滚副本** | 同快照目录 `_original/` | 修改前的原始文件 | 修改前cp一份 |

**重要：不要备份到C盘或E盘！统一落G盘。**

---

## 防复发检查清单

每次修复后逐项确认：

- [ ] **AI Code Switch 开机自启？** → Windows计划任务或Startup快捷方式
- [ ] **E/G Junction 存在且有效？** → `dir E:\aicodeswitch_v5` 应显示 `<JUNCTION>`
- [ ] **cc-switch DB 中无 4567/v1 残留？** → Phase 2A 的验证SQL返回0
- [ ] **cc-switch DB 中无 4567/opencode/v1 残留？（V1.2新增）** → `SELECT * FROM providers WHERE settings_config LIKE '%opencode%';` 返回空
- [ ] **server.pid 无陈旧值？** → pid文件中的PID对应活进程
- [ ] **磁盘空间余量 > 500MB？**
- [ ] **两种API格式都测过？** → chat/completions AND responses 都要测

---

## 回滚命令

```bash
# 1. 还原cc-switch数据库
BKUP="G:/龙虾AI主控中心/Codex备份/snapshots/<日期>/cc-switch.db"
LIVE="E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db"
cp "$BKUP" "$LIVE"

# 2. 删除Junction
Remove-Item "E:\aicodeswitch_v5" -Force
Rename-Item "E:\aicodeswitch_v5_backup_pre_junction" "aicodeswitch_v5"

# 3. 重启服务（cc-switch + AI Code Switch）
```

---

## 版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-07-18 | v1.0 | 初始版本。基于第4-6次复发经验，根治Type-A(400) |
| 2026-07-19 | v1.1 | 新增Type-B(502)、Type-C(/v1/responses 404)；server.pid清理；base_url去/v1后缀规则；一键重启脚本；G盘备份策略 |
| 2026-07-19 | v1.2 | **关键更新**：发现并修复Type-C真正根因 — `aicodeswitch` provider baseURL含`/opencode/v1`后缀导致404；新增Type-D(stream disconnected=4567宕机)；新增V2完整修复BAT脚本；cc-switch必须用`cmd /c "start /B"`启动才能正确绑定端口 |
| 2026-07-19 | v1.3 | **🔴颠覆性修正**：发现URL拼接逻辑真相！cc-switch的baseURL必须**带/v1后缀**（因为cc-switch只拼`/responses`不拼`/v1/responses`）。V1.0-V1.2全部在**删除**/v1，实际应该**保留/v1**。根因是`xiaomimimo20260612` provider（不是aicodeswitch）的`base_url`缺/v1。新增V2.1修复BAT脚本 |
