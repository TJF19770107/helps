# CCGUI-ORCA 环境自检脚本 v1.0
# 用途：每次CCGUI启动前/后执行基础环境校验
# 2026-07-31

param(
    [switch]$PreLaunch,  # 启动前检查
    [switch]$PostLaunch  # 启动后检查
)

$ErrorActionPreference = "Continue"
$CCGUI_CONFIG = "$env:APPDATA\com.zhukunpenglinyutong.ccgui\settings.json"
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Status($label, $ok, $detail) {
    $mark = if ($ok) { "✓" } else { "✗" }
    Write-Output "[$mark] $label : $detail"
}

Write-Output "========================================"
Write-Output " CCGUI-ORCA 环境自检  $TIMESTAMP"
Write-Output "========================================"

# ==========================================
# SECTION 1: 文件与路径检查
# ==========================================
Write-Output "`n--- 文件与路径 ---"

$cfgExists = Test-Path $CCGUI_CONFIG
Write-Status "settings.json" $cfgExists $(if ($cfgExists) { $CCGUI_CONFIG } else { "文件不存在!" })

if ($cfgExists) {
    try {
        $json = Get-Content $CCGUI_CONFIG -Raw | ConvertFrom-Json
        Write-Status "JSON语法" $true "通过"

        $claudeOk = $json.claudeBin -ne $null
        Write-Status "claudeBin" $claudeOk $(if ($claudeOk) { $json.claudeBin } else { "null - 未配置!" })

        $claudeExists = Test-Path $json.claudeBin
        Write-Status "Claude二进制" $claudeExists $(if ($claudeExists) { $json.claudeBin } else { "路径不存在!" })

        $codexExists = Test-Path $json.codexBin
        Write-Status "Codex二进制" $codexExists $(if ($codexExists) { $json.codexBin } else { "路径不存在!" })

        $opencodeExists = Test-Path $json.opencodeBin
        Write-Status "OpenCode二进制" $opencodeExists $(if ($opencodeExists) { $json.opencodeBin } else { "路径不存在!" })

        Write-Status "OpenCode通道" $json.opencodeEnabled "Hermes代理已启用"

        Write-Status "默认模型" ($json.lastComposerModelId -eq "mimo-v2.5-pro") $json.lastComposerModelId

        # 引擎绑定检查
        $engines = $json.lastComposerPrefsByEngine
        $requiredEngines = @("codex", "claude", "opencode")
        foreach ($e in $requiredEngines) {
            $bound = $engines.PSObject.Properties.Name -contains $e
            $model = if ($bound) { $engines.$e.modelId } else { "未绑定!" }
            $ok = $bound -and ($model -eq "mimo-v2.5-pro")
            Write-Status "$e 绑定" $ok $model
        }
    } catch {
        Write-Status "JSON语法" $false "解析失败: $_"
    }
}

# ==========================================
# SECTION 2: 端口检查
# ==========================================
Write-Output "`n--- 端口占用 ---"

$targetPorts = @(3080, 4732)
foreach ($port in $targetPorts) {
    $inUse = netstat -ano 2>$null | Select-String ":$port " | Select-String "LISTENING"
    if ($inUse) {
        Write-Status "端口 $port" $false "已被占用"
    } else {
        Write-Status "端口 $port" $true "空闲"
    }
}

# ==========================================
# SECTION 3: ORCA基座进程（只读参考）
# ==========================================
Write-Output "`n--- ORCA基座进程（参考） ---"

$orcaEngines = @("codex", "claude", "hermes")
foreach ($engine in $orcaEngines) {
    $procs = Get-Process -Name $engine -ErrorAction SilentlyContinue
    if ($procs) {
        $pids = ($procs | ForEach-Object { $_.Id }) -join ", "
        Write-Status "ORCA $engine" $true "运行中 PID=$pids"
    } else {
        Write-Status "ORCA $engine" $false "未运行"
    }
}

# ==========================================
# SECTION 4: CCGUI进程检查
# ==========================================
if ($PostLaunch) {
    Write-Output "`n--- CCGUI进程状态 ---"
    $ccProcs = Get-Process -Name "cc-gui" -ErrorAction SilentlyContinue
    if ($ccProcs) {
        $pids = ($ccProcs | ForEach-Object { $_.Id }) -join ", "
        Write-Status "CCGUI" $true "运行中 PID=$pids"
    } else {
        Write-Status "CCGUI" $false "未检测到进程"
    }
}

Write-Output "`n========================================"
Write-Output " 自检完成"
Write-Output "========================================"
