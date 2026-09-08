# ============================================================
# C盘空间一键清理脚本
# 版本: v1.0 | 创建: 2026-07-07
# 用途: 清理已知安全可删的占用项，释放C盘空间
# 风险: 🟡 中风险——仅清理临时/缓存/残留文件，不触碰系统文件
# ============================================================

$ErrorActionPreference = "Stop"
$TotalFreed = 0

function Write-Step {
    param([string]$Message)
    Write-Host "`n[$([DateTime]::Now.ToString('HH:mm:ss'))] $Message" -ForegroundColor Cyan
}

function Write-Done {
    param([string]$Message, [long]$Bytes)
    $MB = [math]::Round($Bytes / 1MB, 2)
    Write-Host "  ✅ $Message (释放: ${MB}MB)" -ForegroundColor Green
    $script:TotalFreed += $Bytes
}

function Write-Skip {
    param([string]$Reason)
    Write-Host "  ⏭️ 跳过: $Reason" -ForegroundColor Yellow
}

function Safe-Remove {
    param([string]$Path, [string]$Description)
    if (Test-Path $Path) {
        $size = (Get-ChildItem -Path $Path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Remove-Item -Path $Path -Recurse -Force -ErrorAction SilentlyContinue
        if (-not (Test-Path $Path)) { Write-Done -Message $Description -Bytes $size }
        else { Write-Host "  ⚠️ 部分删除失败: $Path" -ForegroundColor Red }
    }
    else { Write-Skip "$Description (路径不存在)" }
}

# ============================================================
# 阶段 1: Docker Desktop 升级残留
# ============================================================
Write-Step "阶段 1/5: 清理 Docker Desktop 升级残留"

$DockerWslOld = "$env:LOCALAPPDATA\Docker\wsl_old"
$DockerLog = "$env:LOCALAPPDATA\Docker\log"

if (Test-Path $DockerWslOld) {
    $wslOldSize = (Get-ChildItem -Path $DockerWslOld -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "  Docker wsl_old 大小: $([math]::Round($wslOldSize / 1GB, 2)) GB"
    $confirm = Read-Host "  是否删除 Docker wsl_old？(y/n)"
    if ($confirm -eq 'y') {
        Safe-Remove -Path $DockerWslOld -Description "Docker wsl_old (升级残留)"
    }
    else { Write-Skip "用户选择保留 Docker wsl_old" }
}
else { Write-Skip "Docker wsl_old 不存在，已清理" }

# Docker 日志
Safe-Remove -Path $DockerLog -Description "Docker 日志"

# ============================================================
# 阶段 2: Marvis Workspace 临时残留
# ============================================================
Write-Step "阶段 2/5: 清理 Marvis Workspace 临时残留"

$MarvisBase = "$env:APPDATA\Tencent\Marvis\User"

# 遍历所有账号目录
if (Test-Path $MarvisBase) {
    Get-ChildItem -Path $MarvisBase -Directory | ForEach-Object {
        $accountDir = $_.FullName
        $tempDir = Join-Path $accountDir "temp"
        if (Test-Path $tempDir) {
            # 清理 base_fingerprint.txt
            $fingerprint = Join-Path $tempDir "base_fingerprint.txt"
            if (Test-Path $fingerprint) {
                Remove-Item -Path $fingerprint -Force -ErrorAction SilentlyContinue
                Write-Done -Message "临时指纹文件: $fingerprint" -Bytes (Get-Item $fingerprint).Length
            }

            # 清理 codex_backup_extract
            $codexBackup = Join-Path $tempDir "codex_backup_extract"
            Safe-Remove -Path $codexBackup -Description "Codex 备份解压临时文件"

            # 清理 .tool-results
            $toolResults = Join-Path $tempDir ".tool-results"
            Safe-Remove -Path $toolResults -Description "工具结果缓存"
        }
    }
}
else { Write-Skip "Marvis 目录不存在" }

# ============================================================
# 阶段 3: Codex / Ollama / 其他工具缓存
# ============================================================
Write-Step "阶段 3/5: 清理第三方工具缓存"

# Codex Logs
$CodexLogs = "$env:LOCALAPPDATA\Codex\Logs"
Safe-Remove -Path $CodexLogs -Description "Codex 日志"

# Ollama 更新缓存
$OllamaUpdates = "$env:LOCALAPPDATA\Ollama\updates_v2"
Safe-Remove -Path $OllamaUpdates -Description "Ollama 更新缓存"

# hermes-agent 日志缓存
$HermesAgent = "$env:LOCALAPPDATA\hermes\hermes-agent"
if (Test-Path $HermesAgent) {
    $hermesSize = (Get-ChildItem -Path $HermesAgent -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $confirm = Read-Host "  Hermes Agent 目录 ($([math]::Round($hermesSize / 1MB, 2)) MB)，是否清理？(y/n)"
    if ($confirm -eq 'y') {
        Safe-Remove -Path $HermesAgent -Description "Hermes Agent 缓存"
    }
}

# 浏览器缓存（CEF）
$CEFCache = "$env:APPDATA\Tencent\Marvis\cef\Cache\Cache_Data"
if (Test-Path $CEFCache) {
    $cefSize = (Get-ChildItem -Path $CEFCache -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $confirm = Read-Host "  Marvis CEF 浏览器缓存 ($([math]::Round($cefSize / 1MB, 2)) MB)，是否清理？(y/n)"
    if ($confirm -eq 'y') {
        Safe-Remove -Path $CEFCache -Description "Marvis CEF 浏览器缓存"
    }
}

# ============================================================
# 阶段 4: 系统临时文件
# ============================================================
Write-Step "阶段 4/5: 清理系统临时文件"

# 系统 TEMP
$SystemTemp = "C:\Windows\TEMP"
if (Test-Path $SystemTemp) {
    $sysTempSize = (Get-ChildItem -Path $SystemTemp -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    if ($sysTempSize -gt 50MB) {
        $confirm = Read-Host "  系统 TEMP 目录 ($([math]::Round($sysTempSize / 1MB, 2)) MB)，是否清理？(y/n)"
        if ($confirm -eq 'y') {
            Get-ChildItem -Path $SystemTemp -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
            Write-Done -Message "系统 TEMP 文件" -Bytes $sysTempSize
        }
    }
    else { Write-Skip "系统 TEMP 目录占用极小 (< 50MB)" }
}

# ============================================================
# 阶段 5: 报告与建议
# ============================================================
Write-Step "阶段 5/5: 生成清理报告"

$DriveC = Get-PSDrive -Name C
$FreeGB = [math]::Round($DriveC.Free / 1GB, 2)
$TotalGB = [math]::Round($DriveC.Used / 1GB, 2) + $FreeGB
$FreedGB = [math]::Round($TotalFreed / 1GB, 2)

Write-Host "`n============================================" -ForegroundColor White
Write-Host "  清理完成报告" -ForegroundColor White
Write-Host "============================================" -ForegroundColor White
Write-Host "  本次释放空间: ${FreedGB} GB" -ForegroundColor Green
Write-Host "  C 盘当前可用: ${FreeGB} GB / ${TotalGB} GB" -ForegroundColor Yellow
Write-Host "============================================`n" -ForegroundColor White

# 待处理建议
Write-Host "⚠️ 以下项目需要手工处理或 Marvis 自身优化：" -ForegroundColor Yellow
Write-Host "  1. Marvis data.db ($env:APPDATA\Tencent\Marvis\User\*\database\data.db)" -ForegroundColor White
Write-Host "     → 建议: 在 Marvis 设置中启用数据库定期压缩/归档" -ForegroundColor Gray
Write-Host "  2. Marvis memory.db ($env:APPDATA\Tencent\Marvis\User\*\database\memory.db)" -ForegroundColor White
Write-Host "     → 建议: 定期清理过期记忆数据" -ForegroundColor Gray
Write-Host "  3. MT4/MT5 市场数据 ($env:APPDATA\MetaQuotes\Terminal\*\Community\)" -ForegroundColor White
Write-Host "     → 建议: 限制历史数据下载范围" -ForegroundColor Gray

Read-Host "`n按 Enter 键退出..."
