---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: cf54d54c59baa0ada35a5ecb7c73a584_6774315879bb11f1a8895254002afed2
    ReservedCode1: I1glMg5UedbTSURFGRy+qVb22r0v6VgcpS4UiDDhAUIN2xRiGqi9yMbiTxjPdD+TXq5o0cEuI2ilK8FpUpLaFZhYDbhVz/VXOpnXpQMk5H09IivTeGea2uw0yhTgHH0jbb22vUVU/Q42FqGjp7zHUrY9dI7XssdokYVYUUjKDkv9xxL0tKhyckj41tw=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: cf54d54c59baa0ada35a5ecb7c73a584_6774315879bb11f1a8895254002afed2
    ReservedCode2: I1glMg5UedbTSURFGRy+qVb22r0v6VgcpS4UiDDhAUIN2xRiGqi9yMbiTxjPdD+TXq5o0cEuI2ilK8FpUpLaFZhYDbhVz/VXOpnXpQMk5H09IivTeGea2uw0yhTgHH0jbb22vUVU/Q42FqGjp7zHUrY9dI7XssdokYVYUUjKDkv9xxL0tKhyckj41tw=
---

# C盘空间健康管控 技能包

> 版本: v1.0 | 创建: 2026-07-07 | 归档位置: E:\龙虾AI主控中心\我的AI分身\技能库

---

## 一、技能概述

**核心能力**：自动排查C盘关键目录空间占用，一键清理可安全删除的垃圾文件，强制实施零冗余存储铁律，内置定时巡检防止空间回滚。

**适用场景**：
- C盘可用空间频繁回滚到不足 1GB
- 排查未知的空间占用源
- 部署新项目前确认磁盘健康状态
- 定期维护（建议每周执行一次）

---

## 二、排查流程（标准化步骤）

### Step 1: 全局空间快照
```powershell
Get-PSDrive -PSProvider FileSystem | Format-Table Name, Used, Free, @{N='Used%';E={[math]::Round($_.Used/($_.Used+$_.Free)*100,1)}}
```

### Step 2: 定位 C 盘 Top 占用目录
```powershell
# AppData\Local 前20大
Get-ChildItem "$env:LOCALAPPDATA" -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Path=$_.Name; SizeMB=[math]::Round($size/1MB,2)}
} | Sort-Object SizeMB -Descending | Select-Object -First 20 | Format-Table

# AppData\Roaming 大于100MB的单文件
Get-ChildItem "$env:APPDATA" -Recurse -File -ErrorAction SilentlyContinue | Where-Object Length -gt 100MB | Sort-Object Length -Descending | Format-Table Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,2)}}, DirectoryName
```

### Step 3: 检查已知膨胀源
| 检查项 | 路径 | 正常阈值 | 异常处理 |
|---|---|---|---|
| Marvis 数据库 | `%APPDATA%\Tencent\Marvis\User\*\database\data.db` | <2GB | 联系 Marvis 支持启用定期压缩 |
| Marvis 记忆库 | `%APPDATA%\Tencent\Marvis\User\*\database\memory.db` | <500MB | 清理过期记忆 |
| Marvis WAL 日志 | `%APPDATA%\Tencent\Marvis\User\*\database\*.db-wal` | <100MB | 正常关闭 Marvis 后自动合并 |
| Docker wsl_old | `%LOCALAPPDATA%\Docker\wsl_old` | 不应存在 | 立即删除 |
| Codex Logs | `%LOCALAPPDATA%\Codex\Logs` | <200MB | 删除旧日志 |
| Ollama updates | `%LOCALAPPDATA%\Ollama\updates_v2` | <500MB | 删除过期更新包 |
| MT5 市场数据 | `%APPDATA%\MetaQuotes\Terminal\*\Community\` | <500MB | 限制历史数据范围 |

### Step 4: 系统层面排查
```powershell
# 系统还原点
vssadmin list shadows
vssadmin list shadowstorage

# 定时任务（关注备份/清理类）
Get-ScheduledTask | Where-Object {$_.TaskPath -match 'Cleanup|Backup|Update|Maintenance'} | Format-Table TaskName, State

# Windows 更新缓存
Get-ChildItem "C:\Windows\SoftwareDistribution\Download" -Recurse | Measure-Object Length -Sum
```

---

## 三、清理脚本

**脚本位置**：`E:\龙虾AI主控中心\我的AI分身\技能库\C盘空间清理脚本.ps1`

**执行方式**：
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& "E:\龙虾AI主控中心\我的AI分身\技能库\C盘空间清理脚本.ps1"
```

**清理项目清单**：

| 阶段 | 清理目标 | 预估释放 | 风险等级 |
|---|---|---|---|
| 1 | Docker wsl_old 升级残留 | ~14 GB | 🟢 安全（需确认） |
| 2 | Marvis workspace 临时残留 | ~2 GB | 🟢 安全 |
| 3 | Codex/Ollama/Hermes 缓存 | ~5 GB | 🟡 需确认 |
| 4 | 系统 TEMP 临时文件 | 不定 | 🟡 需确认 |
| 5 | 生成清理报告 | — | — |

---

## 四、零冗余存储铁律

> **所有项目文件（量化EA、快照、日志、模型）必须部署至 E 盘**，C 盘仅保留：
> - Windows 操作系统文件
> - 必需的驱动和系统服务
> - Marvis 运行所需的数据库（由 Marvis 自行管理）

### 强制迁移清单

| 项目 | 当前路径（C盘） | 目标路径（E盘） |
|---|---|---|
| Docker 数据 | `%LOCALAPPDATA%\Docker\wsl` | Docker 设置中更改数据目录 |
| Codex 日志 | `%LOCALAPPDATA%\Codex\Logs` | 配置 CODE_LOG_DIR 环境变量 |
| Ollama 模型 | `%LOCALAPPDATA%\Ollama\` | 设置 OLLAMA_MODELS 环境变量 |
| 用户临时文件 | 已迁移 ✅ | `E:\tmp` / `E:\temp` |
| MT5/MT4 安装 | `C:\Program Files\MetaTrader*` | 重装至 E 盘 |
| 量化策略代码 | — | `E:\龙虾AI主控中心\CODEX量化策略*` |

---

## 五、定时巡检配置

### 方案 A：Windows 任务计划程序（推荐）

```powershell
# 创建每周日 03:00 执行的空间巡检任务
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -WindowStyle Hidden -File `"E:\龙虾AI主控中心\我的AI分身\技能库\C盘空间巡检.ps1`""
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 03:00
$Principal = New-ScheduledTaskPrincipal -UserId "Administrator" -RunLevel Highest
Register-ScheduledTask -TaskName "C盘空间健康巡检" -Action $Action -Trigger $Trigger -Principal $Principal -Description "每周自动检查C盘空间，低于5GB时告警"
```

### 巡检脚本（C盘空间巡检.ps1）

另存为 `E:\龙虾AI主控中心\我的AI分身\技能库\C盘空间巡检.ps1`：

```powershell
$DriveC = Get-PSDrive -Name C
$FreeGB = [math]::Round($DriveC.Free / 1GB, 2)
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$LogFile = "E:\龙虾AI主控中心\我的AI分身\技能库\space_check.log"

if ($FreeGB -lt 5) {
    $Msg = "[$Timestamp] ⚠️ 告警: C盘仅剩 ${FreeGB}GB，建议立即执行清理脚本"
    Add-Content -Path $LogFile -Value $Msg
    # 可选: 发送桌面通知
    # msg * "C盘空间不足: ${FreeGB}GB"
}
else {
    $Msg = "[$Timestamp] ✅ 正常: C盘可用 ${FreeGB}GB"
    Add-Content -Path $LogFile -Value $Msg
}
```

---

## 六、空间使用报告模板

每次巡检/排查完成后，输出以下结构化报告：

| 指标 | 数值 | 上次值 | 趋势 |
|---|---|---|---|
| C盘总容量 | — | — | — |
| C盘可用空间 | — | — | ↑/↓/→ |
| C盘使用率 | — | — | — |
| Marvis data.db | — | — | — |
| Docker 残留 | — | — | — |
| 临时文件总量 | — | — | — |
| Top 异常目录 | — | — | — |

---

## 七、已知根因库（持续更新）

| 发现时间 | 根因 | 占用 | 修复方案 | 状态 |
|---|---|---|---|---|
| 2026-07-07 | Docker Desktop 升级残留 wsl_old | 14.37 GB | 删除 wsl_old 目录 | ✅ 已修复 |
| 2026-07-07 | Marvis 双账号数据库 data.db | ~23 GB | 待 Marvis 优化数据库管理 | ⚠️ 监控中 |
| 2026-07-07 | Marvis workspace 临时残留 | ~1.9 GB | 清理 temp 目录 | ✅ 已修复 |
| 2026-07-07 | Codex Logs 累积 | 1.37 GB | 删除旧日志，限制日志轮转 | ✅ 已修复 |
| 2026-07-07 | Ollama 更新缓存 | 1.37 GB | 删除 updates_v2 | ✅ 已修复 |

---

## 八、禁止事项

- ❌ 禁止在 C 盘创建大型项目目录（>1GB）
- ❌ 禁止关闭 Marvis 数据库文件（会导致数据损坏）
- ❌ 禁止手动删除 `data.db-wal` 和 `data.db-shm` 文件（应在 Marvis 正常关闭状态下操作）
- ❌ 禁止在 C 盘剩余空间 <5GB 时启动大型编译/容器任务
- ❌ 禁止将 Docker 镜像/容器数据存放在 C 盘

---

*技能包维护人: Marvis | 最后更新: 2026-07-07*
*（内容由AI生成，仅供参考）*
