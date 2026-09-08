param(
    [string]$HermesHost = "127.0.0.1",
    [int]$HermesPort = 18080,
    [string]$DoubaoHost = "127.0.0.1",
    [int]$DoubaoPort = 18000,
    [string]$TraeHost = "127.0.0.1",
    [int]$TraePort = 0,
    [string]$HermesBaseUrl = "",
    [string]$DoubaoBaseUrl = "",
    [string]$TraeBaseUrl = "",
    [string]$StateDir = "",
    [int]$Repair = 0
)

$ErrorActionPreference = "Stop"

function NowIso() {
    return (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffK")
}

function Resolve-RepoRoot([string]$scriptRoot) {
    try {
        return (Resolve-Path (Join-Path $scriptRoot "..\..\..")).Path
    } catch {
        return (Get-Location).Path
    }
}

function Ensure-Dir([string]$p) {
    if (-not $p) { return }
    if (-not (Test-Path -LiteralPath $p)) {
        New-Item -ItemType Directory -Path $p -Force | Out-Null
    }
}

function Test-Tcp([string]$nodeHost, [int]$port) {
    if ($port -le 0) {
        return @{ ok = $true; mode = "LOCAL"; host = $nodeHost; port = $port }
    }
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $iar = $client.BeginConnect($nodeHost, $port, $null, $null)
        $ok = $iar.AsyncWaitHandle.WaitOne(800)
        if (-not $ok) {
            try { $client.Close() } catch { }
            return @{ ok = $false; mode = "TCP"; host = $nodeHost; port = $port; error = "TIMEOUT" }
        }
        $client.EndConnect($iar) | Out-Null
        try { $client.Close() } catch { }
        return @{ ok = $true; mode = "TCP"; host = $nodeHost; port = $port }
    } catch {
        try {
            if ($client) { $client.Close() }
        } catch { }
        return @{ ok = $false; mode = "TCP"; host = $nodeHost; port = $port; error = $_.Exception.GetType().FullName }
    }
}

function Normalize-BaseUrl([string]$nodeHost, [int]$port, [string]$baseUrl) {
    if ($baseUrl) { return $baseUrl.TrimEnd("/") }
    if ($port -le 0) { return "" }
    return ("http://{0}:{1}" -f $nodeHost, $port)
}

function Probe-Http([string]$baseUrl, [hashtable]$headers) {
    if (-not $baseUrl) {
        return @{ ok = $true; mode = "LOCAL"; url = ""; status = $null; path = "" }
    }
    $paths = @("/health", "/healthz", "/api/health", "/v1/health", "/v1/models", "/openapi.json", "/")

    $curl = $null
    try { $curl = Get-Command curl.exe -ErrorAction SilentlyContinue } catch { $curl = $null }
    if ($curl) {
        foreach ($p in $paths) {
            $u = ($baseUrl.TrimEnd("/") + $p)
            try {
                $args = @("-sS", "-m", "2", "-o", "NUL", "-w", "%{http_code}")
                if ($headers) {
                    foreach ($k in $headers.Keys) {
                        $args += @("-H", ("{0}: {1}" -f $k, $headers[$k]))
                    }
                }
                $args += $u
                $code = (& $curl.Source @args) 2>$null
                if ($code -match '^\d{3}$' -and $code -ne "000") {
                    return @{ ok = $true; mode = "HTTP"; url = $u; status = [int]$code; path = $p }
                }
            } catch {
                continue
            }
        }
        return @{ ok = $false; mode = "HTTP"; url = $baseUrl; status = $null; path = "" }
    }

    $client = $null
    try {
        $client = New-Object System.Net.Http.HttpClient
        $client.Timeout = [TimeSpan]::FromMilliseconds(1800)
        if ($headers) {
            foreach ($k in $headers.Keys) {
                try { $client.DefaultRequestHeaders.Remove($k) | Out-Null } catch { }
                try { $client.DefaultRequestHeaders.Add($k, [string]$headers[$k]) } catch { }
            }
        }
        foreach ($p in $paths) {
            $u = ($baseUrl.TrimEnd("/") + $p)
            try {
                $resp = $client.GetAsync($u).GetAwaiter().GetResult()
                return @{ ok = $true; mode = "HTTP"; url = $u; status = [int]$resp.StatusCode; path = $p }
            } catch {
                continue
            }
        }
    } catch {
        return @{ ok = $false; mode = "HTTP"; url = $baseUrl; status = $null; path = "" }
    } finally {
        try { if ($client) { $client.Dispose() } } catch { }
    }
    return @{ ok = $false; mode = "HTTP"; url = $baseUrl; status = $null; path = "" }
}

function Env-Flag([string]$name) {
    $v = [Environment]::GetEnvironmentVariable($name)
    if ($v) { return "SET" }
    return "EMPTY"
}

function Read-TextSafe([string]$path) {
    try {
        return (Get-Content -LiteralPath $path -Raw -Encoding UTF8 -ErrorAction Stop)
    } catch {
        return ""
    }
}

function Find-FirstFile([string]$root, [string]$fileName) {
    try {
        foreach ($p in [System.IO.Directory]::EnumerateFiles($root, $fileName, [System.IO.SearchOption]::AllDirectories)) {
            return $p
        }
    } catch { }
    return ""
}

function Extract-Version([string]$text) {
    if (-not $text) { return "" }
    $m = [regex]::Match($text, "版本号：\s*(v[0-9]+(\.[0-9]+)*)")
    if ($m.Success) { return $m.Groups[1].Value }
    $m2 = [regex]::Match($text, "\bv[0-9]+(\.[0-9]+)*\b")
    if ($m2.Success) { return $m2.Value }
    return ""
}

function Find-IndexEntry([string]$indexPath, [string]$name) {
    if (-not $indexPath) { return $null }
    if (-not (Test-Path -LiteralPath $indexPath)) { return $null }
    try {
        foreach ($line in Get-Content -LiteralPath $indexPath -Encoding UTF8 -ErrorAction Stop) {
            if (-not $line) { continue }
            $obj = $null
            try { $obj = ($line | ConvertFrom-Json -ErrorAction Stop) } catch { $obj = $null }
            if ($null -ne $obj -and $obj.name -eq $name -and $obj.file) {
                return [string]$obj.file
            }
        }
    } catch { }
    return $null
}

$scriptRoot = $PSScriptRoot
$repoRoot = Resolve-RepoRoot $scriptRoot

if (-not $StateDir) {
    if ($env:LOBSTER_STATE_DIR) {
        $StateDir = $env:LOBSTER_STATE_DIR
    } else {
        $StateDir = Join-Path $env:TEMP "lobster_state\\tripartite_handshake"
    }
}
Ensure-Dir $StateDir

$hermesApiTokenHeader = $env:HERMES_API_TOKEN_HEADER
if (-not $hermesApiTokenHeader) { $hermesApiTokenHeader = "X-API-Token" }
$hermesLocalKeyHeader = $env:HERMES_LOCAL_KEY_HEADER
if (-not $hermesLocalKeyHeader) { $hermesLocalKeyHeader = "X-Local-Key" }

$hermesUrl = Normalize-BaseUrl $HermesHost $HermesPort $HermesBaseUrl
$doubaoUrl = Normalize-BaseUrl $DoubaoHost $DoubaoPort $DoubaoBaseUrl
$traeUrl = Normalize-BaseUrl $TraeHost $TraePort $TraeBaseUrl

$nodes = @(
    @{ name = "Hermes"; host = $HermesHost; port = $HermesPort; baseUrl = $hermesUrl },
    @{ name = "Doubao"; host = $DoubaoHost; port = $DoubaoPort; baseUrl = $doubaoUrl },
    @{ name = "Trae"; host = $TraeHost; port = $TraePort; baseUrl = $traeUrl }
)

$nodeReports = @()
foreach ($n in $nodes) {
    $tcp = Test-Tcp $n.host ([int]$n.port)
    $comm = @{ ok = $false; mode = "SKIP" }
    if ($tcp.ok) {
        $headers = @{}
        if ($n.name -eq "Hermes") {
            if ($env:HERMES_API_TOKEN) {
                $headers[$hermesApiTokenHeader] = $env:HERMES_API_TOKEN
            }
            if ($env:HERMES_LOCAL_KEY) {
                $headers[$hermesLocalKeyHeader] = $env:HERMES_LOCAL_KEY
            }
        }
        $comm = Probe-Http $n.baseUrl $headers
    }
    $nodeReports += @{
        name = $n.name
        physical = $tcp
        comm = $comm
        online = [bool]($tcp.ok -and $comm.ok)
        baseUrl = $n.baseUrl
    }
}

$indexPath = Find-FirstFile $repoRoot "INDEX.jsonl"
$skills = @(
    @{ id = "lobster_tripartite_handshake_v1.0"; expected = "v1.0" },
    @{ id = "lobster_self_learning_iteration_skill_v1.0"; expected = "v1.0" },
    @{ id = "lobster_claude_mem_gstack_bridge_v1.0"; expected = "" }
)

$skillReports = @()
foreach ($s in $skills) {
    $localPath = Join-Path $repoRoot (".trae\skills\{0}\SKILL.md" -f $s.id)
    $localText = Read-TextSafe $localPath
    $localVer = Extract-Version $localText

    $sharedPath = Find-IndexEntry $indexPath $s.id
    $sharedText = Read-TextSafe $sharedPath
    $sharedVer = Extract-Version $sharedText
    $sharedPathStr = ""
    if ($sharedPath) { $sharedPathStr = [string]$sharedPath }

    $skillReports += @{
        id = $s.id
        expected = $s.expected
        localSkillDoc = @{ path = $localPath; exists = (Test-Path -LiteralPath $localPath); version = $localVer }
        sharedDoc = @{ path = $sharedPathStr; exists = [bool]($sharedPath -and (Test-Path -LiteralPath $sharedPath)); version = $sharedVer }
    }
}

$versionOk = $true
foreach ($sr in $skillReports) {
    if (-not $sr.expected) { continue }
    if ($sr.localSkillDoc.exists -and $sr.localSkillDoc.version -and ($sr.localSkillDoc.version -ne $sr.expected)) { $versionOk = $false }
    if ($sr.sharedDoc.exists -and $sr.sharedDoc.version -and ($sr.sharedDoc.version -ne $sr.expected)) { $versionOk = $false }
}

$allLocalExist = ($skillReports | Where-Object { -not $_.localSkillDoc.exists }).Count -eq 0
$requiresSync = -not ([bool]($indexPath -and (Test-Path -LiteralPath $indexPath)) -and $allLocalExist -and $versionOk)

$onlineNodes = @($nodeReports | Where-Object { $_.online })
$onlineCount = $onlineNodes.Count
$offlineNodes = @($nodeReports | Where-Object { -not $_.online } | ForEach-Object { $_.name })

$overall = "OK"
if ($onlineCount -lt 2) { $overall = "DEGRADED" }
if ($onlineCount -eq 0) { $overall = "OFFLINE" }
if ($requiresSync -and $overall -eq "OK") { $overall = "DEGRADED" }

$report = @{
    skill = "lobster_tripartite_handshake_v1.0"
    version = "v1.0"
    ts = (NowIso)
    repoRoot = $repoRoot
    nodes = $nodeReports
    app = @{
        skills = $skillReports
        index = @{ path = $indexPath; exists = [bool]($indexPath -and (Test-Path -LiteralPath $indexPath)) }
        tokens = @{
            LOBSTER_MASTER_TOKEN = (Env-Flag "LOBSTER_MASTER_TOKEN")
            HERMES_API_TOKEN = (Env-Flag "HERMES_API_TOKEN")
            HERMES_LOCAL_KEY = (Env-Flag "HERMES_LOCAL_KEY")
            TRAE_TOKEN = (Env-Flag "TRAE_TOKEN")
        }
    }
    requiresSync = [bool]$requiresSync
    overall = $overall
    offlineNodes = $offlineNodes
}

$linkPath = Join-Path $StateDir "tripartite_handshake_link.json"
$reportPath = Join-Path $StateDir "tripartite_handshake_last_report.json"
$pendingSyncPath = Join-Path $StateDir "tripartite_pending_sync.json"

$reportJson = ($report | ConvertTo-Json -Depth 12)
Set-Content -LiteralPath $reportPath -Value $reportJson -Encoding UTF8

if ($onlineCount -ge 2 -and -not $requiresSync) {
    $link = @{
        ts = $report.ts
        nodes = ($nodeReports | ForEach-Object {
            @{
                name = $_.name
                baseUrl = $_.baseUrl
                host = $_.physical.host
                port = $_.physical.port
                online = $_.online
            }
        })
    }
    $linkJson = ($link | ConvertTo-Json -Depth 8)
    Set-Content -LiteralPath $linkPath -Value $linkJson -Encoding UTF8
} else {
    try {
        if (Test-Path -LiteralPath $linkPath) {
            Remove-Item -LiteralPath $linkPath -Force
        }
    } catch { }
}

if ($requiresSync) {
    $pending = @{
        ts = $report.ts
        reason = "VERSION_OR_INDEX_OR_DOC_MISMATCH"
        indexExists = [bool]($indexPath -and (Test-Path -LiteralPath $indexPath))
        skills = ($skillReports | ForEach-Object {
            @{
                id = $_.id
                expected = $_.expected
                localExists = $_.localSkillDoc.exists
                localVersion = $_.localSkillDoc.version
                sharedExists = $_.sharedDoc.exists
                sharedVersion = $_.sharedDoc.version
            }
        })
    }
    $pendingJson = ($pending | ConvertTo-Json -Depth 6)
    Set-Content -LiteralPath $pendingSyncPath -Value $pendingJson -Encoding UTF8
} else {
    try {
        if (Test-Path -LiteralPath $pendingSyncPath) {
            Remove-Item -LiteralPath $pendingSyncPath -Force
        }
    } catch { }
}

Write-Output $reportJson

if ($overall -eq "OFFLINE") { exit 2 }
if ($requiresSync) { exit 3 }
if ($overall -eq "DEGRADED") { exit 1 }
exit 0
