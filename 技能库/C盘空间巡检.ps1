# C盘空间巡检脚本
# 版本: v1.0 | 用途: 每周自动检查C盘空间，低于阈值告警
# 调度: 建议通过Windows任务计划程序设置每周日03:00执行

$ErrorActionPreference = "SilentlyContinue"
$ThresholdGB = 5
$LogFile = "E:\龙虾AI主控中心\我的AI分身\技能库\space_check.log"

$DriveC = Get-PSDrive -Name C
$FreeGB = [math]::Round($DriveC.Free / 1GB, 2)
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 找出 Top 5 异常目录
$TopDirs = Get-ChildItem "$env:LOCALAPPDATA" -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Path=$_.Name; SizeMB=[math]::Round($size/1MB,2)}
} | Sort-Object SizeMB -Descending | Select-Object -First 5

$TopList = ($TopDirs | ForEach-Object { "$($_.Path): $($_.SizeMB)MB" }) -join " | "

if ($FreeGB -lt $ThresholdGB) {
    $Msg = "[$Timestamp] ⚠️ WARNING: C盘仅剩 ${FreeGB}GB (阈值 ${ThresholdGB}GB) | Top占用: $TopList"
}
else {
    $Msg = "[$Timestamp] ✅ OK: C盘可用 ${FreeGB}GB | Top占用: $TopList"
}

Add-Content -Path $LogFile -Value $Msg -Encoding UTF8

# 输出到控制台（任务计划程序可见）
Write-Output $Msg
