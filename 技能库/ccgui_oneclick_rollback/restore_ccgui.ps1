# CCGUI 一键回滚恢复脚本
# 功能：终止CCGUI → 恢复settings.json/opencode.cmd → 重启CCGUI → 验证三引擎
# 版本：1.0
# 时间：2026-07-31 16:42

param(
    [switch]$DryRun,      # 仅检查不执行
    [switch]$SkipVerify   # 跳过引擎验证
)

$ErrorActionPreference = "Stop"

# ===== 路径配置 =====
$ccguiSettingsPath = "C:\Users\Administrator\AppData\Roaming\com.zhukunpenglinyutong.ccgui\settings.json"
$opencodeCmdPath    = "I:\npm\opencode.cmd"
$hqRollbackDir      = "E:\龙虾AI主控中心\我的AI分身\技能库\ccgui_orca_isolation\rollback_nodes"

$lastStable = @{
    settings = "$hqRollbackDir\settings_stable_20260731_164257.json"
    opencode = "$hqRollbackDir\opencode_cmd_clean_20260731_164257.cmd"
}

# ===== 前置检查 =====
Write-Host "========== CCGUI 一键回滚恢复 ==========" -ForegroundColor Cyan
Write-Host "时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host ""

# 检查源文件
foreach ($key in $lastStable.Keys) {
    if (-not (Test-Path $lastStable[$key])) {
        Write-Host "[错误] 源文件不存在: $($lastStable[$key])" -ForegroundColor Red
        exit 1
    }
}

if ($DryRun) {
    Write-Host "[DryRun] 将恢复以下文件:" -ForegroundColor Yellow
    Write-Host "  settings.json ← $($lastStable.settings)"
    Write-Host "  opencode.cmd  ← $($lastStable.opencode)"
    Write-Host "[DryRun] 跳过实际执行。"
    exit 0
}

# ===== Step 1: 终止 CCGUI =====
Write-Host "[Step 1/5] 终止 CCGUI 进程..." -ForegroundColor Yellow
$ccguiProcs = Get-Process -Name "CCGUI","com.zhukunpenglinyutong.ccgui" -ErrorAction SilentlyContinue
if ($ccguiProcs) {
    $ccguiProcs | Stop-Process -Force
    Start-Sleep -Seconds 3
    Write-Host "  已终止 $($ccguiProcs.Count) 个 CCGUI 进程"
} else {
    Write-Host "  CCGUI 未在运行"
}

# ===== Step 2: 恢复 settings.json =====
Write-Host "[Step 2/5] 恢复 settings.json..." -ForegroundColor Yellow
$settingsBackup = "$ccguiSettingsPath.rollback_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $ccguiSettingsPath $settingsBackup -Force -ErrorAction SilentlyContinue
Write-Host "  当前版本备份到: $settingsBackup"
Copy-Item $lastStable.settings $ccguiSettingsPath -Force
Write-Host "  已恢复 settings.json"

# ===== Step 3: 修复 opencode.cmd =====
Write-Host "[Step 3/5] 修复 opencode.cmd..." -ForegroundColor Yellow
Copy-Item $lastStable.opencode $opencodeCmdPath -Force
Write-Host "  已恢复 opencode.cmd (无 NUL 字节)"

# ===== Step 4: 清理 CCGUI 缓存 =====
Write-Host "[Step 4/5] 清理 CCGUI 运行时缓存..." -ForegroundColor Yellow
$cachePaths = @(
    "$env:LOCALAPPDATA\com.zhukunpenglinyutong.ccgui\Cache",
    "$env:LOCALAPPDATA\com.zhukunpenglinyutong.ccgui\Code Cache",
    "$env:LOCALAPPDATA\com.zhukunpenglinyutong.ccgui\GPUCache"
)
foreach ($p in $cachePaths) {
    if (Test-Path $p) {
        Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  清理: $p"
    }
}

# ===== Step 5: 重启 CCGUI =====
Write-Host "[Step 5/5] 重启 CCGUI..." -ForegroundColor Yellow
$ccguiExe = Get-ChildItem "$env:LOCALAPPDATA\com.zhukunpenglinyutong.ccgui" -Filter "*.exe" -Recurse -ErrorAction SilentlyContinue | 
    Where-Object { $_.Name -like "*CCGUI*" -or $_.Name -like "*ccgui*" } |
    Select-Object -First 1

if ($ccguiExe) {
    Start-Process $ccguiExe.FullName
    Write-Host "  CCGUI 已启动"
    Start-Sleep -Seconds 5
} else {
    Write-Host "  [警告] 未找到 CCGUI 可执行文件，请手动启动" -ForegroundColor Yellow
}

# ===== 验证 =====
if (-not $SkipVerify) {
    Write-Host ""
    Write-Host "========== 验证三引擎 ==========" -ForegroundColor Cyan
    
    # 验证 settings.json
    $settings = Get-Content $ccguiSettingsPath -Raw | ConvertFrom-Json
    $engines = $settings.lastComposerPrefsByEngine
    
    Write-Host ""
    Write-Host "settings.json 引擎配置:" -ForegroundColor Green
    Write-Host "  claude.modelId   = $($engines.claude.modelId)"
    Write-Host "  codex.modelId    = $($engines.codex.modelId)"
    Write-Host "  opencode.modelId = $($engines.opencode.modelId)"
    
    $allPro = ($engines.claude.modelId -eq "mimo-v2.5-pro") -and
              ($engines.codex.modelId -eq "mimo-v2.5-pro") -and
              ($engines.opencode.modelId -eq "mimo-v2.5-pro")
    
    if ($allPro) {
        Write-Host "  ✅ 三引擎 modelId 均为 mimo-v2.5-pro" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 存在非 Pro 引擎，请检查" -ForegroundColor Red
    }
    
    # 验证 opencode.cmd
    $bytes = [System.IO.File]::ReadAllBytes($opencodeCmdPath)
    $nulCount = ($bytes | Where-Object { $_ -eq 0 }).Count
    if ($nulCount -eq 0) {
        Write-Host "  ✅ opencode.cmd 无 NUL 字节" -ForegroundColor Green
    } else {
        Write-Host "  ❌ opencode.cmd 仍有 $nulCount 个 NUL 字节" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========== 回滚完成 ==========" -ForegroundColor Cyan
Write-Host "请在 CCGUI 中分别用三引擎发送「你是谁」验证。" -ForegroundColor White
Write-Host "预期回复:" -ForegroundColor White
Write-Host "  Claude   → 我是 Claude / Claude Code" -ForegroundColor White
Write-Host "  Codex    → 我是 Codex" -ForegroundColor White
Write-Host "  OpenCode → 我是 Hermes Agent" -ForegroundColor White
