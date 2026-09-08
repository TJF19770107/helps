#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Windows磁盘空间快照诊断脚本
.DESCRIPTION
    输出所有盘符容量、根目录Top10、用户目录Top15、回收站、临时目录大小
.PARAMETER OutputPath
    报告输出路径，默认输出到控制台
.EXAMPLE
    .\storage_snapshot.ps1
    .\storage_snapshot.ps1 -OutputPath G:\storage_report_20260825.md
#>
param(
    [string]$OutputPath = ""
)

$report = @()
$report += "# Windows磁盘空间快照报告"
$report += "生成时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$report += ""

# 1. 盘符容量
$report += "## 盘符容量概览"
$report += "| 盘符 | 总容量(GB) | 已用(GB) | 可用(GB) | 可用率 | 状态 |"
$report += "|------|-----------|---------|---------|--------|------|"
$disks = Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 }
foreach ($disk in $disks) {
    $total = [math]::Round($disk.Size / 1GB, 2)
    $free = [math]::Round($disk.FreeSpace / 1GB, 2)
    $used = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 2)
    $pct = if ($disk.Size -gt 0) { [math]::Round(($disk.FreeSpace / $disk.Size) * 100, 1) } else { 0 }
    $status = if ($pct -lt 5 -or $free -lt 2) { "🔴 危险" } elseif ($pct -lt 15) { "🟡 警告" } else { "🟢 正常" }
    $report += "| $($disk.DeviceID) | $total | $used | $free | ${pct}% | $status |"
}
$report += ""

# 2. C盘根目录Top10
$report += "## C盘根目录Top10"
$report += "| 路径 | 大小(GB) |"
$report += "|------|---------|"
$cDirs = Get-ChildItem C:\ -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{ Path = $_.FullName; SizeGB = [math]::Round($size / 1GB, 2) }
} | Sort-Object SizeGB -Descending | Select-Object -First 10
foreach ($d in $cDirs) { $report += "| $($d.Path) | $($d.SizeGB) |" }
$report += ""

# 3. 用户目录Top15
$report += "## 用户目录Top15 ($env:USERPROFILE)"
$report += "| 路径 | 大小(GB) |"
$report += "|------|---------|"
$userDirs = Get-ChildItem $env:USERPROFILE -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{ Path = $_.FullName; SizeGB = [math]::Round($size / 1GB, 2) }
} | Sort-Object SizeGB -Descending | Select-Object -First 15
foreach ($d in $userDirs) { $report += "| $($d.Path) | $($d.SizeGB) |" }
$report += ""

# 4. 回收站和临时目录
$report += "## 可回收空间估算"
$recycle = (Get-ChildItem "C:\`$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$temp = (Get-ChildItem $env:TEMP -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$winTemp = (Get-ChildItem "C:\Windows\Temp" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$report += "| 项目 | 大小(GB) |"
$report += "|------|---------|"
$report += "| 回收站 | $([math]::Round($recycle / 1GB, 2)) |"
$report += "| 用户Temp | $([math]::Round($temp / 1GB, 2)) |"
$report += "| Windows Temp | $([math]::Round($winTemp / 1GB, 2)) |"
$report += ""

$output = $report -join "`n"
if ($OutputPath) {
    $output | Out-File -FilePath $OutputPath -Encoding utf8
    Write-Host "报告已保存到：$OutputPath" -ForegroundColor Green
} else {
    Write-Host $output
}
