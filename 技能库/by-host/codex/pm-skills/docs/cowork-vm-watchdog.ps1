# CC Switch Cowork VM Watchdog - pm-skills deployment
# Purpose: Monitor and auto-repair VM service to prevent startup crashes

$ServiceNames = @("Cowork*", "Hyper-V*", "vmcompute", "vmms")
$LogFile = "C:\Users\Administrator\.cc-switch\logs\cowork_watchdog.log"
$MaxLogSize = 5MB

function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp [WATCHDOG] $Message" | Out-File -Append -FilePath $LogFile -Encoding UTF8
    # Rotate log if too large
    if ((Get-Item $LogFile -ErrorAction SilentlyContinue).Length -gt $MaxLogSize) {
        $archive = $LogFile -replace '\.log$', "_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
        Move-Item $LogFile $archive -Force
    }
}

try {
    Write-Log "Watchdog cycle started"
    
    foreach ($pattern in $ServiceNames) {
        $svcs = Get-Service -Name $pattern -ErrorAction SilentlyContinue
        if (-not $svcs) { continue }
        foreach ($svc in $svcs) {
            if ($svc.Status -ne "Running" -and $svc.StartType -ne "Disabled") {
                Write-Log "Service $($svc.Name) is $($svc.Status), attempting restart..."
                try {
                    Start-Service -Name $svc.Name -ErrorAction Stop
                    Write-Log "Service $($svc.Name) started successfully"
                } catch {
                    Write-Log "FAILED to start $($svc.Name): $_"
                }
            }
        }
    }
    Write-Log "Watchdog cycle completed"
} catch {
    Write-Log "FATAL: $_"
}
