# CCGUI 一键恢复启动器
# 用途：修复 CCGUI 启动时的 settings.json 回写问题，确保三引擎始终可用
# 时间：2026-07-31 16:55
# 故障根因：CCGUI 启动后会重写 lastComposerPrefsByEngine，仅保留当前活跃引擎，删除其余引擎配置

param(
    [switch]$Monitor,    # 持续监控模式，检测到回写自动恢复
    [switch]$Kill        # 先强制终止所有 CCGUI 进程再启动
)

$ErrorActionPreference = "Stop"

# === 路径定义 ===
$settingsPath = "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json"
$backupDir = "E:\龙虾AI主控中心\我的AI分身\技能库\ccgui_oneclick_rollback\rollback_nodes"
$stableBackup = "$backupDir\settings_stable_20260731_164257.json"
$opencodeCmdPath = "I:\npm\opencode.cmd"
$opencodeCmdBackup = "$backupDir\opencode_cmd_clean_20260731_164257.cmd"
$ccguiExe = "$env:LOCALAPPDATA\ccgui\cc-gui.exe"

# === 稳定配置模板（三引擎锁定 Pro） ===
$stableEngines = @"
{
    "claude":  { "accessMode": null, "collaborationModeId": null, "effort": null, "modelId": "mimo-v2.5-pro" },
    "codex":   { "accessMode": null, "collaborationModeId": null, "effort": "medium", "modelId": "mimo-v2.5-pro" },
    "opencode":{ "accessMode": null, "collaborationModeId": null, "effort": null, "modelId": "mimo-v2.5-pro" }
}
"@

function Restore-Config {
    Write-Host "[$(Get-Date -Format HH:mm:ss)] 恢复 settings.json ..." -ForegroundColor Yellow
    
    $json = Get-Content $settingsPath -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json -ErrorAction SilentlyContinue
    if (-not $json) { 
        Write-Host "  settings.json 无效，从备份完全覆盖" -ForegroundColor Red
        Copy-Item $stableBackup $settingsPath -Force
        return $true
    }
    
    # 检查三引擎是否存在
    $engines = $json.lastComposerPrefsByEngine
    $needFix = $false
    
    if (-not $engines.claude) { $engines | Add-Member -NotePropertyName "claude" -NotePropertyValue (@{accessMode=$null;collaborationModeId=$null;effort=$null;modelId="mimo-v2.5-pro"}) -Force; $needFix=$true; Write-Host "  + 补回 claude" }
    if (-not $engines.codex)  { $engines | Add-Member -NotePropertyName "codex"  -NotePropertyValue (@{accessMode=$null;collaborationModeId=$null;effort="medium";modelId="mimo-v2.5-pro"}) -Force; $needFix=$true; Write-Host "  + 补回 codex" }
    if (-not $engines.opencode){ $engines | Add-Member -NotePropertyName "opencode"-NotePropertyValue (@{accessMode=$null;collaborationModeId=$null;effort=$null;modelId="mimo-v2.5-pro"}) -Force; $needFix=$true; Write-Host "  + 补回 opencode" }
    
    # 确保 modelId 正确
    if ($engines.claude.modelId -ne "mimo-v2.5-pro")   { $engines.claude.modelId="mimo-v2.5-pro"; $needFix=$true; Write-Host "  ! claude modelId 修正" }
    if ($engines.codex.modelId -ne "mimo-v2.5-pro")    { $engines.codex.modelId="mimo-v2.5-pro"; $needFix=$true; Write-Host "  ! codex modelId 修正" }
    if ($engines.opencode.modelId -ne "mimo-v2.5-pro") { $engines.opencode.modelId="mimo-v2.5-pro"; $needFix=$true; Write-Host "  ! opencode modelId 修正" }
    
    if ($needFix) {
        # 备份当前损坏的配置
        $ts = Get-Date -Format "yyyyMMdd_HHmmss"
        Copy-Item $settingsPath "$backupDir\settings_corrupted_$ts.json" -Force
        
        # 写入修复后的配置
        $json | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
        Write-Host "  配置已修复并保存" -ForegroundColor Green
        
        # 同时设置只读防止立即回写（CCGUI 关闭时恢复可写）
        Set-ItemProperty $settingsPath -Name IsReadOnly -Value $false
    } else {
        Write-Host "  配置正常，无需修复" -ForegroundColor Green
    }
    
    # 确保 opencode.cmd 干净
    $bytes = [System.IO.File]::ReadAllBytes($opencodeCmdPath)
    $nulCount = ($bytes | Where-Object { $_ -eq 0 }).Count
    if ($nulCount -gt 0) {
        Write-Host "  ! opencode.cmd 含 $nulCount 个 NUL 字节，从备份恢复" -ForegroundColor Red
        Copy-Item $opencodeCmdBackup $opencodeCmdPath -Force
    }
    
    return $needFix
}

# === 终止 CCGUI ===
if ($Kill) {
    Write-Host "终止所有 CCGUI 进程..." -ForegroundColor Cyan
    Get-Process -Name "cc-gui" -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
}

# === 恢复配置 ===
$fixed = Restore-Config

# === 启动 CCGUI ===
if (Test-Path $ccguiExe) {
    Write-Host "启动 CCGUI..." -ForegroundColor Cyan
    Start-Process $ccguiExe
    
    if ($Monitor) {
        Write-Host "进入守护模式，每 10 秒检测 settings.json ..." -ForegroundColor Magenta
        Write-Host "按 Ctrl+C 停止监控" -ForegroundColor Gray
        
        Start-Sleep -Seconds 15  # 等 CCGUI 完全加载
        
        while ($true) {
            $ccguiRunning = Get-Process -Name "cc-gui" -ErrorAction SilentlyContinue
            if (-not $ccguiRunning) {
                Write-Host "[$(Get-Date -Format HH:mm:ss)] CCGUI 已退出，停止守护" -ForegroundColor Gray
                break
            }
            
            $json = Get-Content $settingsPath -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json -ErrorAction SilentlyContinue
            if ($json) {
                $engines = $json.lastComposerPrefsByEngine
                $count = ($engines.PSObject.Properties | Measure-Object).Count
                if ($count -lt 3) {
                    Write-Host "[$(Get-Date -Format HH:mm:ss)] 检测到引擎回写（仅 $count 个），自动修复..." -ForegroundColor Red
                    Restore-Config
                }
                # 检查 modelId
                foreach ($e in @('claude','codex','opencode')) {
                    if ($engines.$e -and $engines.$e.modelId -ne "mimo-v2.5-pro") {
                        Write-Host "[$(Get-Date -Format HH:mm:ss)] $e modelId 异常: $($engines.$e.modelId)，自动修复..." -ForegroundColor Red
                        Restore-Config
                        break
                    }
                }
            }
            
            Start-Sleep -Seconds 10
        }
    }
} else {
    Write-Host "错误：找不到 CCGUI 可执行文件 $ccguiExe" -ForegroundColor Red
    exit 1
}
