# watchdog_tangxiaolong.ps1 - 汤小龙崩溃自动重启（防失忆防掉线）
# 用法: powershell -File watchdog_tangxiaolong.ps1
$ErrorActionPreference = "SilentlyContinue"
$ent = "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体"
$py  = "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$running = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*$ent*启动我的AI分身*" }
if ($running) {
    Write-Output "汤小龙进程存活 (PID $($running.ProcessId))"
} else {
    Write-Output "汤小龙进程不在，自动拉起..."
    Start-Process -WindowStyle Hidden -FilePath $py -ArgumentList "`"$ent\启动我的AI分身.py`""
    Start-Sleep -Seconds 3
    $alive = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*$ent*启动我的AI分身*" }
    if ($alive) { Write-Output "已重启 (PID $($alive.ProcessId))" } else { Write-Output "重启失败" }
}