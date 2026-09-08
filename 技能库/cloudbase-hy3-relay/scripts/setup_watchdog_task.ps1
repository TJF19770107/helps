# setup_watchdog_task.ps1 — 注册 HY3 混元代理看门狗计划任务（登录时拉起 + 每5分钟自愈）
# 用法：powershell -ExecutionPolicy Bypass -File setup_watchdog_task.ps1
$ErrorActionPreference = "Stop"

$python   = "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$watchdog = "G:\龙虾AI主控中心\HY3混元代理\hy3_watchdog.py"
$taskName = "Hy3ProxyWatchdog"

$action = New-ScheduledTaskAction -Execute $python -Argument "`"$watchdog`""

$trigLogon  = New-ScheduledTaskTrigger -AtLogOn
$trigRepeat = New-ScheduledTaskTrigger -Once -At (Get-Date) `
    -RepetitionInterval (New-TimeSpan -Minutes 5) `
    -RepetitionDuration (New-TimeSpan -Days 248)

$principal = New-ScheduledTaskPrincipal -UserId "Administrator" `
    -LogonType ServiceAccount -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5) `
    -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger @($trigLogon, $trigRepeat) `
    -Principal $principal `
    -Settings $settings `
    -Description "HY3混元本地代理看门狗：登录拉起 + 每5分钟自愈，零手工干预" `
    -Force

Write-Host "已注册/更新计划任务: $taskName (Ready)"
Get-ScheduledTask -TaskName $taskName | Format-Table TaskName, State -AutoSize
