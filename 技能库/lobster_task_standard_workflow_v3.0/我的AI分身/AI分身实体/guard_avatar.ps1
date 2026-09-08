# guard_avatar.ps1 · P0 守护自愈
# 每30分钟检测分身进程，挂了自动拉起。用法: powershell -File guard_avatar.ps1
$ErrorActionPreference = "SilentlyContinue"
$ent = "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体"
$py  = "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*$ent*" -and ($_.CommandLine -like "*nvidia_avatar*" -or $_.CommandLine -like "*启动我的AI分身*") }
if ($procs) {
    "OK: 分身进程存活 ($($procs.Count))"
} else {
    "DOWN: 分身进程不在，准备拉起..."
    Start-Process -WindowStyle Hidden -FilePath $py -ArgumentList "`"$ent\nvidia_avatar.py`""
    Start-Sleep -Seconds 3
    $alive = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*$ent*nvidia_avatar*" }
    if ($alive) { "RESTARTED: 分身已拉起" } else { "RESTART_FAIL: 拉起失败" }
}