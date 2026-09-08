$ErrorActionPreference = "Stop"

function Get-NowStamp { (Get-Date).ToString("yyyyMMdd_HHmmss") }
function Ensure-Dir { param([Parameter(Mandatory = $true)][string]$Path) if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Path $Path | Out-Null } }

function Start-ProcessBg {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$ArgumentList,
        [Parameter(Mandatory = $true)][string]$StdoutPath,
        [Parameter(Mandatory = $true)][string]$StderrPath
    )
    $p = Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -PassThru -WindowStyle Hidden -RedirectStandardOutput $StdoutPath -RedirectStandardError $StderrPath
    @{ Pid = $p.Id; StdoutPath = $StdoutPath; StderrPath = $StderrPath }
}

function Stop-ProcessSafe { param([Parameter(Mandatory = $true)][int]$TargetPid) try { Stop-Process -Id $TargetPid -Force -ErrorAction SilentlyContinue } catch {} }

$skillRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$stateDir = Join-Path $skillRoot ".lobster_state"
$secureDir = Join-Path $stateDir "securecode"
$reportDir = Join-Path $stateDir "reports"
$stamp = Get-NowStamp
$reportPath = Join-Path $reportDir ("tunnel_env_mcp_report_" + $stamp + ".json")

Ensure-Dir $stateDir
Ensure-Dir $secureDir
Ensure-Dir $reportDir

. "$skillRoot\securecode_crypto.ps1"

$secretsPath = Join-Path $secureDir "secrets.dpapi"
$certPrefix = "LobsterSecureCodeMcp"
$handshakePath = Resolve-Path (Join-Path $skillRoot "..\..\..\.npc\handshake.json")

$dotnet = (Get-Command dotnet -ErrorAction SilentlyContinue).Source
if (-not $dotnet) { throw "dotnet not found" }

$cert = New-OrGet-SecureCodeMcpCertificate -FriendlyNamePrefix $certPrefix

if (-not (Test-Path $secretsPath)) {
    $toolProj = Join-Path $skillRoot "securecode_tool\SecureCodeTool.csproj"
    $toolBuildOut = Join-Path $stateDir ("securecode_tool_build_" + $stamp + ".log")
    & $dotnet build $toolProj -c Release | Out-File -Encoding utf8 $toolBuildOut
    $toolDll = Join-Path $skillRoot "securecode_tool\bin\Release\net8.0\securecode-tool.dll"
    if (-not (Test-Path $toolDll)) { throw "securecode-tool build output missing: $toolDll" }
    & $dotnet $toolDll --secrets-path $secretsPath --cert-thumbprint $cert.Thumbprint | Out-Null
    Set-FileAclCurrentUserOnly -Path $secretsPath
}

$secretsJson = Read-SecureCodeSecretsDpapiJson -SecretsPath $secretsPath
$secrets = $secretsJson | ConvertFrom-Json

[Environment]::SetEnvironmentVariable("SECURECODE_CERT_THUMBPRINT", [string]$secrets.certThumbprint, "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_MCP_BEARER_TOKEN", [string]$secrets.mcpBearerToken, "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_BIND_HOST", "127.0.0.1", "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_BIND_PORT", "19090", "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_HANDSHAKE_PATH", [string]$handshakePath, "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_WRITE_ENABLED", "1", "Process")

$proj = Join-Path $skillRoot "securecode_mcp\SecureCodeMcp.csproj"
$buildOut = Join-Path $stateDir ("securecode_mcp_build_" + $stamp + ".log")
$buildErr = $buildOut + ".err"
& $dotnet build $proj -c Release | Out-File -Encoding utf8 $buildOut

$dll = Join-Path $skillRoot "securecode_mcp\bin\Release\net8.0\securecode-mcp.dll"
if (-not (Test-Path $dll)) { throw "build output missing: $dll" }

$pidFile = Join-Path $stateDir "securecode_mcp.pid"
if (Test-Path $pidFile) {
    try {
        $oldPid = [int](Get-Content -Raw -Encoding ascii $pidFile).Trim()
        if ($oldPid -gt 0) { Stop-ProcessSafe -TargetPid $oldPid }
    } catch {
    }
}

$inUseAll = Get-NetTCPConnection -State Listen -LocalAddress 127.0.0.1 -LocalPort 19090 -ErrorAction SilentlyContinue
if ($inUseAll) {
    $pids = $inUseAll | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($p0 in $pids) {
        $p = Get-Process -Id $p0 -ErrorAction SilentlyContinue
        $name = if ($p) { [string]$p.ProcessName } else { "" }
        if ($name -match "python|dotnet") { Stop-ProcessSafe -TargetPid ([int]$p0) }
    }
    $deadlinePort = (Get-Date).AddSeconds(6)
    while ((Get-Date) -lt $deadlinePort) {
        $still = Get-NetTCPConnection -State Listen -LocalAddress 127.0.0.1 -LocalPort 19090 -ErrorAction SilentlyContinue
        if (-not $still) { break }
        Start-Sleep -Milliseconds 250
    }
    $still2 = Get-NetTCPConnection -State Listen -LocalAddress 127.0.0.1 -LocalPort 19090 -ErrorAction SilentlyContinue
    if ($still2) {
        $pid2 = ($still2 | Select-Object -First 1 -ExpandProperty OwningProcess)
        throw "Port 19090 already in use (PID=$pid2)"
    }
}

$srvOut = Join-Path $stateDir ("securecode_mcp_" + $stamp + ".log")
$srvErr = $srvOut + ".err"
$srv = Start-ProcessBg -FilePath $dotnet -ArgumentList @($dll) -StdoutPath $srvOut -StderrPath $srvErr
Set-Content -Encoding ascii -NoNewline -Path $pidFile -Value ([string]$srv.Pid)

$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
if (-not $python) { throw "python not found" }

$client = Join-Path $skillRoot "securecode_mcp_client_test.py"
$certSha256 = [string]$secrets.certSha256

$directOk = $false
$deadline = (Get-Date).AddSeconds(20)
while ((Get-Date) -lt $deadline) {
    try {
        $o = & $python $client --host 127.0.0.1 --port 19090 --cert-sha256 $certSha256 2>$null
        $t = ($o | Out-String)
        if ($t -match '"ok"\s*:\s*true') { $directOk = $true; break }
    } catch {
    }
    Start-Sleep -Milliseconds 350
}

$handshakeOk = $false
try {
    $json = Get-Content -Raw -Encoding utf8 $handshakePath
    $null = $json | ConvertFrom-Json
    $handshakeOk = $true
} catch {
    $handshakeOk = $false
}

$pass = ($directOk -and $handshakeOk)

$report = @{
    skill = "lobster_tunnel_env_mcp_universal_v1.1"
    timestamp = $stamp
    ports = @{
        securecodeMcpHttps = 19090
        forbidden = @("8000","18000","18091")
        hermesFixed = @("6060","8642")
    }
    secrets = @{
        store = "dpapi_file_current_user"
        path = $secretsPath
    }
    tls = @{
        certificateStore = "Cert:\\CurrentUser\\My"
        friendlyNamePrefix = $certPrefix
        sha256Fingerprint = $certSha256
    }
    securecodeMcp = @{
        endpoint = "https://127.0.0.1:19090/mcp"
        pid = [int]$srv.Pid
        logs = @{ stdout = $srvOut; stderr = $srvErr; build = $buildOut; buildErr = $buildErr }
    }
    handshake = @{
        path = [string]$handshakePath
        jsonValid = $handshakeOk
    }
    result = if ($pass) { "PASS" } else { "FAIL" }
}

($report | ConvertTo-Json -Depth 8) | Out-File -Encoding utf8 $reportPath
Write-Output ("REPORT=" + $reportPath)
Write-Output ("RESULT=" + $report.result)
