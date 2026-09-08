# Codex++ 400 错误修复回滚预案

> 日期: 2026-07-18 18:xx
> 方案: 龙虾五步法 V2.6
> 状态: ✅ 已完成修复 + E→G 迁移

---

## 一、变更清单

### 变更 #1: AI Code Switch E→G 迁移（Junction 软连接）

| 项目 | 原始值 | 当前值 |
|------|--------|--------|
| **AI Code Switch 安装位置** | `E:\aicodeswitch_v5\` (16MB, 物理文件) | `G:\龙虾AI主控中心\数据迁移\aicodeswitch_v5\` (物理) |
| **E 盘访问路径** | `E:\aicodeswitch_v5\` (物理目录) | `E:\aicodeswitch_v5\` (**Junction** → G 盘) |
| **原始备份位置** | — | `E:\aicodeswitch_v5_backup_pre_junction\` |

**Junction 命令（已执行）:**
```powershell
New-Item -Path "E:\aicodeswitch_v5" -ItemType Junction `
  -Target "G:\龙虾AI主控中心\数据迁移\aicodeswitch_v5"
```

**回滚命令:**
```powershell
# 删除 Junction
Remove-Item "E:\aicodeswitch_v5" -Force
# 还原原名
Rename-Item "E:\aicodeswitch_v5_backup_pre_junction" "aicodeswitch_v5"
```

---

### 变更 #2: cc-switch 数据库端点重定向（4 处修改）

**数据库:** `E:\龙虾AI主控中心\CC-Switch\.cc-switch\cc-switch.db` (45MB)

| # | 表名 | 字段 | 原始值 | 新值 |
|---|------|------|--------|------|
| 1 | `provider_endpoints` | `url` (id=21) | `https://token-plan-cn.xiaomimimo.com/v1/chat/completions` | `http://127.0.0.1:4567/v1/chat/completions` |
| 2 | `providers` | `settings_config` (id=d240abd2) | `base_url = "https://token-plan-cn.xiaomimimo.com/v1"` | `base_url = "http://127.0.0.1:4567/v1"` |
| 3 | `proxy_live_backup` | `original_config` (app_type=codex) | 同上 | `http://127.0.0.1:4567/v1` |
| 4 | `settings` | `value` (key=common_config_codex) | 含 xiaomimomo URL | 已替换为 4567 |

**完整 SQL 回滚（一键还原）:**
```bash
export MSYS_NO_PATHCONV=1
DB="E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db"
SQL="/c/ProgramData/chocolatey/bin/sqlite3"

# 先停止 cc-switch！
# PowerShell: Stop-Process -Id (Get-NetTCPConnection -LocalPort 15721).OwningProcess -Force

# 从备份还原
BKUP_DB="C:/Users/Administrator/AppData/Local/Temp/codex400_backup_20260718/cc-switch.db"
cp "$BKUP_DB" "$DB"

# 重启 cc-switch
"E:/龙虾AI主控中心/CC-Switch/cc-switch.exe" &
```

---

### 变更 #3: CC-Switch 数据目录 E→G 迁移（进行中/可选）

| 项目 | 原始值 | 目标值 |
|------|--------|--------|
| **`.cc-switch/` 数据目录** | `E:\龙虾AI主控中心\CC-Switch\.cc-switch\` (656MB) | `G:\龙虾AI主控中心\数据迁移\CC-Switch-data\.cc-switch\` |
| **E 盘访问路径** | 物理目录 | Junction → G 盘 |

**状态**: 后台复制中（656MB），完成后创建 Junction。

---

## 二、备份位置

所有备份统一存放在：
```
C:\Users\Administrator\AppData\Local\Temp\codex400_backup_20260718\
```

| 文件 | 大小 | 说明 |
|------|------|------|
| `config.toml` | 1.4KB | Codex CLI 配置 |
| `auth.json` | 39B | 认证信息 |
| `cc-switch-model-catalog.json` | 47KB | 模型目录 |
| `.codex-global-state.json` | 122KB | 全局状态（含历史诊断记录）|
| `aicodeswitch_fs-db/` | ~50KB | AI Code Switch 配置 |
| `cc-switch.db` | **46.9MB** | cc-switch 完整数据库 |
| `cc-switch-config.json` | 2.8KB | CC-Switch 根配置 |
| `cc-switch-settings.json` | 1KB | CC-Switch 设置 |
| `Codex-Preferences` | 122B | Codex GUI 偏好 |
| `Codex-LocalState` | 490B | Codex GUI 本地状态 |
| **总计** | **~156MB** | 全量备份 |

---

## 三、服务状态（修复后）

| 服务 | 端口 | PID | 状态 |
|------|------|-----|------|
| cc-switch | 15721 | 运行中 | ✅ 上游已改为 4567 |
| AI Code Switch | 4567 | 1033744 | ✅ 通过 Junction 运行在 G 盘 |
| MiMO 后端 | 443 (云端) | — | ✅ 正常 |

**验证测试结果:**
- `gpt-5.5` → 15721 → 4567 → MiMO = ✅ **200 OK**
- `mimo-v2.5-pro` → 15721 → 4567 → MiMO = ✅ **200 OK**

---

## 四、紧急联系/恢复步骤

### 如果 Codex++ 再次报 400：

1. 调用本技能：`codex-400-auto-recovery`
2. 执行 Phase 1 诊断（30秒）
3. 按 Phase 对应方案修复
4. Phase 3 校验确认

### 如果完全无法修复：

```bash
# 一键还原到修复前状态
# 1. 还原数据库
cp C:/Users/Administrator/AppData/Local/Temp/codex400_backup_20260718/cc-switch.db \
   E:/龙虾AI主控中心/CC-Switch/.cc-switch/cc-switch.db

# 2. 删除 Junction
# PowerShell: Remove-Item "E:\aicodeswitch_v5" -Force
# Rename-Item "E:\aicodeswitch_v5_backup_pre_junction" "aicodeswitch_v5"

# 3. 重启全部服务
```
