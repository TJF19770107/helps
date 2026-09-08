# ============================================================
# Agent-Reach Windows 安装脚本
# 自动检测环境、安装依赖、配置代理
# 版本: 1.0.0 | 日期: 2026-06-14
# ============================================================

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$LogDir = Join-Path $ScriptDir "logs"
$DoctorLog = Join-Path $ScriptDir "doctor-log.txt"

# 创建日志目录
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# 日志函数
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path (Join-Path $LogDir "install-$(Get-Date -Format 'yyyyMMdd').log") -Value $LogEntry
}

function Test-Command {
    param([string]$Command)
    return (Get-Command $Command -ErrorAction SilentlyContinue) -ne $null
}

Write-Log "=== Agent-Reach 安装脚本启动 ==="
Write-Log "项目根目录: $ProjectRoot"

# ============================================================
# 步骤1: 检查 Python 3.10+ 环境
# ============================================================
Write-Log "步骤1: 检查 Python 环境..."

$PythonCmd = $null
if (Test-Command "python3") {
    $PythonCmd = "python3"
} elseif (Test-Command "python") {
    $PythonCmd = "python"
} else {
    Write-Log "未找到 Python，请先安装 Python 3.10+" -Level "ERROR"
    Write-Host "错误: 未找到 Python，请从 https://www.python.org/downloads/ 安装 Python 3.10+"
    exit 1
}

$PythonVersion = & $PythonCmd --version 2>&1
Write-Log "Python 版本: $PythonVersion"

# 解析版本号
$VersionMatch = [regex]::Match($PythonVersion, '(\d+)\.(\d+)')
if (-not $VersionMatch.Success) {
    Write-Log "无法解析 Python 版本号" -Level "ERROR"
    exit 1
}
$Major = [int]$VersionMatch.Groups[1].Value
$Minor = [int]$VersionMatch.Groups[2].Value
if ($Major -lt 3 -or ($Major -eq 3 -and $Minor -lt 10)) {
    Write-Log "Python 版本不满足要求（需要 3.10+），当前: $PythonVersion" -Level "ERROR"
    exit 1
}
Write-Log "Python 版本检查通过"

# ============================================================
# 步骤2: 升级 pip 并安装 agent-reach
# ============================================================
Write-Log "步骤2: 安装 agent-reach..."

& $PythonCmd -m pip install --upgrade pip 2>&1 | ForEach-Object { Write-Log "pip upgrade: $_" }

$InstallResult = & $PythonCmd -m pip install agent-reach 2>&1
$InstallResult | ForEach-Object { Write-Log "pip install: $_" }

if ($LASTEXITCODE -ne 0) {
    Write-Log "agent-reach 安装失败，尝试从 GitHub 直接安装..." -Level "WARN"
    & $PythonCmd -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip 2>&1 | ForEach-Object { Write-Log "pip github: $_" }
    if ($LASTEXITCODE -ne 0) {
        Write-Log "agent-reach 安装失败" -Level "ERROR"
        exit 1
    }
}
Write-Log "agent-reach 安装完成"

# ============================================================
# 步骤3: 执行 agent-reach doctor 并保存日志
# ============================================================
Write-Log "步骤3: 执行 agent-reach doctor..."

try {
    & $PythonCmd -m agent_reach doctor 2>&1 | Tee-Object -FilePath $DoctorLog
    Write-Log "doctor 日志已保存至: $DoctorLog"
} catch {
    Write-Log "agent-reach doctor 执行异常: $_" -Level "WARN"
    # 尝试直接调用
    try {
        agent-reach doctor 2>&1 | Tee-Object -FilePath $DoctorLog
    } catch {
        Write-Log "agent-reach doctor 失败，可能命令未注册到 PATH" -Level "WARN"
    }
}

# ============================================================
# 步骤4: 执行 agent-reach install --env=auto
# ============================================================
Write-Log "步骤4: 执行 agent-reach install --env=auto..."

try {
    & $PythonCmd -m agent_reach install --env=auto 2>&1 | ForEach-Object { Write-Log "install: $_" }
} catch {
    try {
        agent-reach install --env=auto 2>&1 | ForEach-Object { Write-Log "install: $_" }
    } catch {
        Write-Log "agent-reach install 失败" -Level "ERROR"
        exit 1
    }
}
Write-Log "agent-reach install 完成"

# ============================================================
# 步骤5: 配置代理
# ============================================================
Write-Log "步骤5: 配置代理 (127.0.0.1:6738 青云梯)..."

try {
    & $PythonCmd -m agent_reach config set proxy.http "http://127.0.0.1:6738" 2>&1 | ForEach-Object { Write-Log "proxy config: $_" }
    & $PythonCmd -m agent_reach config set proxy.https "http://127.0.0.1:6738" 2>&1 | ForEach-Object { Write-Log "proxy config: $_" }
} catch {
    try {
        agent-reach config set proxy.http "http://127.0.0.1:6738" 2>&1 | ForEach-Object { Write-Log "proxy config: $_" }
        agent-reach config set proxy.https "http://127.0.0.1:6738" 2>&1 | ForEach-Object { Write-Log "proxy config: $_" }
    } catch {
        Write-Log "代理配置失败，请手动执行: agent-reach config set proxy.http 'http://127.0.0.1:6738'" -Level "WARN"
    }
}

# ============================================================
# 步骤6: 验证安装
# ============================================================
Write-Log "步骤6: 验证安装..."

try {
    $Version = & $PythonCmd -m agent_reach --version 2>&1
    Write-Log "agent-reach 版本: $Version"
} catch {
    try {
        $Version = agent-reach --version 2>&1
        Write-Log "agent-reach 版本: $Version"
    } catch {
        Write-Log "无法获取版本号，但安装流程已完成" -Level "WARN"
    }
}

# ============================================================
# 完成
# ============================================================
Write-Log "=== Agent-Reach 安装脚本完成 ==="
Write-Host ""
Write-Host "========================================"
Write-Host "  Agent-Reach 安装完成！"
Write-Host "========================================"
Write-Host "  Doctor 日志: $DoctorLog"
Write-Host "  安装日志: $LogDir"
Write-Host "  下一步: 配置各平台 Cookie/Token"
Write-Host "  参考: 项目根目录 README.md"
Write-Host "========================================"
