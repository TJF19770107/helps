$ErrorActionPreference = "Stop"

if ($PSVersionTable.PSVersion.Major -lt 7) {
    $repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")
    $bundledPwsh = Join-Path $repoRoot "Clawith\7\pwsh.exe"
    if (Test-Path $bundledPwsh) {
        & $bundledPwsh -NoProfile -ExecutionPolicy Bypass -File $MyInvocation.MyCommand.Path @args
        exit $LASTEXITCODE
    }
    throw "PowerShell 7+ is required but 'pwsh' is not available. Expected bundled pwsh at: $bundledPwsh"
}

function Get-NowStamp {
    <#
    .SYNOPSIS
    Returns a filesystem-safe timestamp string.
    #>
    return (Get-Date).ToString("yyyyMMdd_HHmmss")
}

function Ensure-Dir {
    <#
    .SYNOPSIS
    Creates a directory if missing.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )
    if (-not (Test-Path $Path)) { New-Item -ItemType Directory -Path $Path | Out-Null }
}

function Test-TcpOpen {
    <#
    .SYNOPSIS
    Tests whether a TCP port is listening on a host.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$TargetHost,
        [Parameter(Mandatory = $true)]
        [int]$Port
    )
    try {
        $c = New-Object System.Net.Sockets.TcpClient
        $iar = $c.BeginConnect($TargetHost, $Port, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(800)
        if (-not $ok) { return $false }
        $c.EndConnect($iar)
        $c.Close()
        return $true
    } catch {
        return $false
    }
}

function Invoke-HttpsHealth {
    <#
    .SYNOPSIS
    Performs an HTTPS GET to /health with cert validation disabled (self-signed).
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$Url
    )
    try {
        $r = Invoke-WebRequest -UseBasicParsing -SkipCertificateCheck -TimeoutSec 3 -Uri $Url
        return ($r.StatusCode -ge 200 -and $r.StatusCode -lt 300)
    } catch {
        return $false
    }
}

function Start-SecureCodeMcpServer {
    <#
    .SYNOPSIS
    Starts SecureCode MCP HTTPS server in background and returns process info.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [string]$PythonExe,
        [Parameter(Mandatory = $true)]
        [string]$ServerScript,
        [Parameter(Mandatory = $true)]
        [string]$LogPath,
        [Parameter(Mandatory = $false)]
        [string]$ErrLogPath = "",
        [Parameter(Mandatory = $false)]
        [string]$BindHost = "127.0.0.1",
        [Parameter(Mandatory = $false)]
        [int]$Port = 19090
    )

    $args = @(
        "`"$ServerScript`"",
        "--host", $BindHost,
        "--port", "$Port"
    )

    $err = $ErrLogPath
    if (-not $err) { $err = ($LogPath + ".err") }
    $p = Start-Process -FilePath $PythonExe -ArgumentList $args -PassThru -WindowStyle Hidden -RedirectStandardOutput $LogPath -RedirectStandardError $err
    return @{
        Pid = $p.Id
        Host = $BindHost
        Port = $Port
        LogPath = $LogPath
        ErrLogPath = $err
    }
}

function Stop-ProcessSafe {
    <#
    .SYNOPSIS
    Stops a process by PID best-effort.
    #>
    param(
        [Parameter(Mandatory = $true)]
        [int]$TargetPid
    )
    try {
        $p = Get-Process -Id $TargetPid -ErrorAction SilentlyContinue
        if ($p) { Stop-Process -Id $TargetPid -Force -ErrorAction SilentlyContinue }
    } catch {
    }
}

$skillRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$stateDir = Join-Path $skillRoot ".lobster_state"
$secureDir = Join-Path $stateDir "securecode"
$tlsOutDir = Join-Path $env:LOCALAPPDATA "LobsterSecureCode\tls"
$secretsPath = Join-Path $secureDir "secrets.dpapi"
$reportDir = Join-Path $stateDir "reports"
$stamp = Get-NowStamp
$reportPath = Join-Path $reportDir ("tunnel_env_mcp_report_" + $stamp + ".json")

Ensure-Dir $stateDir
Ensure-Dir $secureDir
Ensure-Dir $reportDir
Ensure-Dir $tlsOutDir

. "$skillRoot\securecode_crypto.ps1"

$created = $false
if (-not (Test-Path $secretsPath)) {
    Save-SecureCodeSecretsDpapi -SecretsPath $secretsPath | Out-Null
    Set-FileAclCurrentUserOnly -Path $secretsPath
    $created = $true
}

$secretsJson = Read-SecureCodeSecretsDpapiJson -SecretsPath $secretsPath
$secrets = $secretsJson | ConvertFrom-Json

$certText = [string]$secrets.tlsCertPem
$keyText = [string]$secrets.tlsKeyPem
if (-not ($certText -match "BEGIN CERTIFICATE") -or -not ($keyText -match "BEGIN (RSA |EC |)PRIVATE KEY")) {
    Save-SecureCodeSecretsDpapi -SecretsPath $secretsPath | Out-Null
    Set-FileAclCurrentUserOnly -Path $secretsPath
    $created = $true
    $secretsJson = Read-SecureCodeSecretsDpapiJson -SecretsPath $secretsPath
    $secrets = $secretsJson | ConvertFrom-Json
    $certText = [string]$secrets.tlsCertPem
    $keyText = [string]$secrets.tlsKeyPem
}

$tlsCertPath = Join-Path $tlsOutDir "securecode_mcp_cert.pem"
$tlsKeyPath = Join-Path $tlsOutDir "securecode_mcp_key.pem"
[System.IO.File]::WriteAllText($tlsCertPath, $certText, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText($tlsKeyPath, $keyText, [System.Text.Encoding]::UTF8)
Set-FileAclCurrentUserOnly -Path $tlsCertPath
Set-FileAclCurrentUserOnly -Path $tlsKeyPath

[Environment]::SetEnvironmentVariable("SECURECODE_TLS_CERT_PATH", $tlsCertPath, "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_TLS_KEY_PATH", $tlsKeyPath, "Process")
[Environment]::SetEnvironmentVariable("SECURECODE_MCP_BEARER_TOKEN", [string]$secrets.mcpBearerToken, "Process")

$pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonExe) { $pythonExe = (Get-Command python3 -ErrorAction SilentlyContinue).Source }
if (-not $pythonExe) { throw "Python not found in PATH. Install Python or run from an environment that provides python." }

$serverLog = Join-Path $stateDir ("securecode_mcp_" + $stamp + ".log")
$server = Start-SecureCodeMcpServer -PythonExe $pythonExe -ServerScript (Join-Path $skillRoot "securecode_mcp_server.py") -LogPath $serverLog

$clientScript = Join-Path $skillRoot "securecode_mcp_client_test.py"
$directOk = $false
$deadline = (Get-Date).AddSeconds(15)
while ((Get-Date) -lt $deadline) {
    try {
        $o = & $pythonExe $clientScript --url "https://127.0.0.1:19090/mcp" 2>$null
        $oText = ($o | Out-String)
        if ($oText -match '"ok"\s*:\s*true') { $directOk = $true; break }
    } catch {
    }
    Start-Sleep -Milliseconds 300
}

$dockerExe = (Get-Command docker -ErrorAction SilentlyContinue).Source
$frpStarted = $false
$frpNote = ""
if ($dockerExe) {
    try {
        Push-Location $skillRoot
        & $dockerExe compose -f .\docker-compose.frp.local.yml up -d --force-recreate | Out-Null
        Pop-Location
        $frpStarted = $true
    } catch {
        try { Pop-Location } catch {}
        $frpNote = "FRP docker-compose start failed"
    }
} else {
    $frpNote = "Docker not found; skipped FRP local simulation"
}

$testDirect = $directOk
$testViaFrp = $false

if ($frpStarted) {
    $deadline2 = (Get-Date).AddSeconds(8)
    while ((Get-Date) -lt $deadline2) {
        if (Test-TcpOpen -TargetHost "127.0.0.1" -Port 19100) { break }
        Start-Sleep -Milliseconds 300
    }
    try {
        $out2 = & $pythonExe $clientScript --url "https://127.0.0.1:19100/mcp" 2>$null
        $out2Text = ($out2 | Out-String)
        $testViaFrp = $out2Text -match '"ok"\s*:\s*true'
    } catch {
        $testViaFrp = $false
    }
}

$frpReconnectPass = $true
$frpBurstPass = $true
if ($frpStarted) {
    try {
        Push-Location $skillRoot
        & $dockerExe compose -f .\docker-compose.frp.local.yml stop frpc frps | Out-Null
        Start-Sleep -Seconds 2
        & $dockerExe compose -f .\docker-compose.frp.local.yml start frps frpc | Out-Null
        Pop-Location
    } catch {
        try { Pop-Location } catch {}
        $frpReconnectPass = $false
    }

    if ($frpReconnectPass) {
        $deadlineR = (Get-Date).AddSeconds(25)
        while ((Get-Date) -lt $deadlineR) {
            if (Test-TcpOpen -TargetHost "127.0.0.1" -Port 19100) { break }
            Start-Sleep -Milliseconds 300
        }
        try {
            $rr = & $pythonExe $clientScript --url "https://127.0.0.1:19100/mcp" 2>$null
            $rrText = ($rr | Out-String)
            $frpReconnectPass = ($rrText -match '"ok"\s*:\s*true')
        } catch {
            $frpReconnectPass = $false
        }
    }

    if ($frpReconnectPass) {
        for ($k = 0; $k -lt 3; $k++) {
            try {
                $bb = & $pythonExe $clientScript --url "https://127.0.0.1:19100/mcp" 2>$null
                $bbText = ($bb | Out-String)
                if (-not ($bbText -match '"ok"\s*:\s*true')) { $frpBurstPass = $false; break }
            } catch {
                $frpBurstPass = $false
                break
            }
        }
    }
}

$restartPass = $true
for ($i = 0; $i -lt 2; $i++) {
    Stop-ProcessSafe -TargetPid ([int]$server.Pid)
    Start-Sleep -Milliseconds 300
    $serverLog2 = Join-Path $stateDir ("securecode_mcp_restart_" + $stamp + "_$i.log")
    $server = Start-SecureCodeMcpServer -PythonExe $pythonExe -ServerScript (Join-Path $skillRoot "securecode_mcp_server.py") -LogPath $serverLog2

    $ready = $false
    $deadline3 = (Get-Date).AddSeconds(12)
    while ((Get-Date) -lt $deadline3) {
        try {
            $oo = & $pythonExe $clientScript --url "https://127.0.0.1:19090/mcp" 2>$null
            $ooText = ($oo | Out-String)
            if ($ooText -match '"ok"\s*:\s*true') { $ready = $true; break }
        } catch {
        }
        Start-Sleep -Milliseconds 300
    }
    if (-not $ready) { $restartPass = $false; break }
    try {
        $out3 = & $pythonExe $clientScript --url "https://127.0.0.1:19090/mcp" 2>$null
        $out3Text = ($out3 | Out-String)
        if (-not ($out3Text -match '"ok"\s*:\s*true')) { $restartPass = $false; break }
    } catch {
        $restartPass = $false
        break
    }
}

$pass = ($directOk -and $testDirect -and $restartPass -and ((-not $frpStarted) -or ($testViaFrp -and $frpReconnectPass -and $frpBurstPass)))

$report = @{
    skill = "lobster_tunnel_env_mcp_universal_v1.0"
    timestamp = $stamp
    secrets = @{
        store = "dpapi_file_current_user"
        path = $secretsPath
        createdThisRun = $created
    }
    securecodeMcp = @{
        https = @{
            direct = "https://127.0.0.1:19090/mcp"
            viaFrp = "https://127.0.0.1:19100/mcp"
        }
        health = @{
            direct = $directOk
        }
        pid = [int]$server.Pid
        logPath = $server.LogPath
    }
    frp = @{
        simulatedLocal = $frpStarted
        note = $frpNote
        remotePort = 19100
    }
    tests = @{
        directMcp = $testDirect
        frpMcp = $testViaFrp
        frpReconnect = $frpReconnectPass
        frpBurst = $frpBurstPass
        restart = $restartPass
    }
    result = if ($pass) { "PASS" } else { "FAIL" }
}

($report | ConvertTo-Json -Depth 8) | Out-File -Encoding utf8 $reportPath

Write-Output ("REPORT=" + $reportPath)
Write-Output ("RESULT=" + $report.result)
