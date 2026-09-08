#Requires -RunAsAdministrator
<#
.SYNOPSIS
    查找磁盘空间元凶：Top20大目录和大文件
.DESCRIPTION
    对指定路径进行递归扫描，输出Top20大目录、Top20大文件、可清理项清单
.PARAMETER Path
    扫描路径，默认为C:\
.PARAMETER TopN
    输出数量，默认20
.EXAMPLE
    .\find_space_hogs.ps1 -Path E:\
    .\find_space_hogs.ps1 -Path C:\Users\Administrator -TopN 30
#>
param(
    [string]$Path = "C:\",
    [int]$TopN = 20
)

Write-Host "正在扫描 $Path ，请耐心等待..." -ForegroundColor Cyan

# 获取所有文件和目录大小
$items = Get-ChildItem $Path -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }

# TopN大文件
$topFiles = $items | Sort-Object Length -Descending | Select-Object -First $TopN | ForEach-Object {
    [PSCustomObject]@{
        Path = $_.FullName
        SizeGB = [math]::Round($_.Length / 1GB, 2)
        Modified = $_.LastWriteTime.ToString("yyyy-MM-dd")
    }
}

# 按目录聚合
$dirSizes = @{}
foreach ($file in $items) {
    $dir = $file.DirectoryName
    if (-not $dirSizes.ContainsKey($dir)) { $dirSizes[$dir] = 0 }
    $dirSizes[$dir] += $file.Length
}
$topDirs = $dirSizes.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First $TopN | ForEach-Object {
    [PSCustomObject]@{
        Path = $_.Key
        SizeGB = [math]::Round($_.Value / 1GB, 2)
    }
}

# 输出Markdown
$report = @()
$report += "# 空间元凶扫描报告"
$report += "扫描路径：$Path"
$report += "扫描时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$report += ""

$report += "## Top${TopN}大目录"
$report += "| 路径 | 大小(GB) |"
$report += "|------|---------|"
foreach ($d in $topDirs) { $report += "| $($d.Path) | $($d.SizeGB) |" }
$report += ""

$report += "## Top${TopN}大文件"
$report += "| 路径 | 大小(GB) | 修改时间 |"
$report += "|------|---------|----------|"
foreach ($f in $topFiles) { $report += "| $($f.Path) | $($f.SizeGB) | $($f.Modified) |" }
$report += ""

# 可清理项（基于路径关键词）
$report += "## 可清理项清单（🟢安全 🟡建议确认 🔴禁止自动删除）"
$report += "| 路径 | 大小(GB) | 风险等级 | 说明 |"
$report += "|------|---------|----------|------|"
$cleanable = $items | Where-Object {
    $_.FullName -match '\\Temp\\|\\temp\\|\\Downloads\\|\\logs\\|\\Log\\|\\Cache\\|\\cache\\|\.tmp$|\.log$|\\SoftwareDistribution\\Download\\|\\Recycle\\.Bin' -and
    $_.FullName -notmatch '\\Windows\\System32|\\Program Files|\\ProgramData\\Microsoft'
} | Sort-Object Length -Descending | Select-Object -First $TopN | ForEach-Object {
    $risk = if ($_.FullName -match '\\Temp\\|\\temp\\|\.tmp$|\\SoftwareDistribution\\Download') { "🟢 安全" }
            elseif ($_.FullName -match '\\logs\\|\\Log\\|\.log$|\\Cache\\|\\cache\\') { "🟡 建议确认" }
            else { "🟡 建议确认" }
    [PSCustomObject]@{
        Path = $_.FullName
        SizeGB = [math]::Round($_.Length / 1GB, 2)
        Risk = $risk
        Note = "手动确认后再删除"
    }
}
foreach ($c in $cleanable) { $report += "| $($c.Path) | $($c.SizeGB) | $($c.Risk) | $($c.Note) |" }

Write-Host ($report -join "`n")
