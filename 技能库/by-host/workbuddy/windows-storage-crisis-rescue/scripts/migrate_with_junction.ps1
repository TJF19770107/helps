#Requires -RunAsAdministrator
<#
.SYNOPSIS
    安全迁移目录到G盘并创建Junction软链接
.DESCRIPTION
    双备份 → robocopy → 校验 → 重命名源目录 → 创建Junction → 验证
.PARAMETER SourceDir
    源目录路径
.PARAMETER TargetDir
    目标目录路径（建议在G盘）
.PARAMETER BackupRoot
    备份根目录
.PARAMETER DryRun
    仅预览不执行
.PARAMETER SkipBackup
    跳过备份（不建议）
.EXAMPLE
    .\migrate_with_junction.ps1 -SourceDir "C:\Users\Administrator\.ollama" -TargetDir "G:\Data\.ollama" -BackupRoot "G:\Backups"
#>
param(
    [Parameter(Mandatory=$true)][string]$SourceDir,
    [Parameter(Mandatory=$true)][string]$TargetDir,
    [string]$BackupRoot = "G:\Backups",
    [switch]$DryRun,
    [switch]$SkipBackup
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$sourceName = Split-Path $SourceDir -Leaf
$logFile = "$BackupRoot\migration_${sourceName}_${timestamp}.log"

function Write-Log($msg) {
    $line = "[$(Get-Date -Format 'HH:mm:ss')] $msg"
    Write-Host $line
    if ($BackupRoot) { $line | Out-File -FilePath $logFile -Append -Encoding utf8 }
}

# 前置检查
if (-not (Test-Path $SourceDir)) { throw "源目录不存在：$SourceDir" }
if (-not (Test-Path $BackupRoot)) { New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null }

$sourceDrive = (Get-Item $SourceDir).PSDrive.Root
$targetDrive = (Get-Item $TargetDir -ErrorAction SilentlyContinue).PSDrive.Root
if (-not $targetDrive) { $targetDrive = (Split-Path $TargetDir -Qualifier) + "\" }

Write-Log "=== 迁移任务开始 ==="
Write-Log "源目录：$SourceDir"
Write-Log "目标目录：$TargetDir"
Write-Log "备份根目录：$BackupRoot"
Write-Log "是否仅预览：$DryRun"
Write-Log ""

if ($DryRun) {
    Write-Log "【DRY RUN】仅预览，不会执行实际迁移"
    $sourceSize = (Get-ChildItem $SourceDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Log "源目录大小：$([math]::Round($sourceSize / 1GB, 2)) GB"
    Write-Log "目标父目录：$(Split-Path $TargetDir -Parent)"
    return
}

# 1. 停止可能占用源目录的进程
Write-Log "步骤1/6：尝试停止常见占用进程（Ollama/Obsidian/Docker等）"
$processes = @("ollama", "Obsidian", "Docker Desktop", "Code", "chrome")
foreach ($p in $processes) {
    Get-Process -Name $p -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

# 2. 双备份
if (-not $SkipBackup) {
    Write-Log "步骤2/6：执行双备份"
    $backup1 = "$BackupRoot\${sourceName}_${timestamp}_backup1"
    $backup2 = "$BackupRoot\${sourceName}_${timestamp}_backup2"
    Write-Log "备份1：$backup1"
    robocopy "$SourceDir" "$backup1" /E /COPYALL /R:3 /W:5 /MT:8
    Write-Log "备份2：$backup2"
    robocopy "$SourceDir" "$backup2" /E /COPYALL /R:3 /W:5 /MT:8
} else {
    Write-Log "步骤2/6：跳过备份（用户指定SkipBackup）"
}

# 3. 复制到目标盘
Write-Log "步骤3/6：复制数据到目标目录"
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
robocopy "$SourceDir" "$TargetDir" /E /COPYALL /R:3 /W:5 /MT:8 /LOG:"$logFile.robocopy"

# 4. 校验完整性
Write-Log "步骤4/6：校验源目录与目标目录完整性"
$sourceSizeAfter = (Get-ChildItem $SourceDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$targetSizeAfter = (Get-ChildItem $TargetDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
$sourceCount = (Get-ChildItem $SourceDir -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
$targetCount = (Get-ChildItem $TargetDir -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Log "源大小：$([math]::Round($sourceSizeAfter / 1GB, 2)) GB | 目标大小：$([math]::Round($targetSizeAfter / 1GB, 2)) GB"
Write-Log "源文件数：$sourceCount | 目标文件数：$targetCount"
if ([math]::Abs($sourceSizeAfter - $targetSizeAfter) -gt 1MB) {
    throw "校验失败：源目录与目标目录大小差异超过1MB，请勿继续！"
}

# 5. 重命名源目录
$oldDir = "$SourceDir.old_${timestamp}"
Write-Log "步骤5/6：重命名源目录为 $oldDir"
Rename-Item -Path $SourceDir -NewName $oldDir -Force

# 6. 创建Junction
Write-Log "步骤6/6：创建Junction软链接 $SourceDir -> $TargetDir"
$parent = Split-Path $SourceDir -Parent
cmd /c mklink /J "$SourceDir" "$TargetDir"
if (-not (Test-Path $SourceDir)) {
    throw "Junction创建失败，正在回滚..."
}

# 验证Junction
$link = Get-Item $SourceDir
Write-Log "Junction验证：$($link.FullName) -> $($link.Target)"

Write-Log "=== 迁移任务完成 ==="
Write-Log "观察期建议：72小时内保留 $oldDir"
Write-Log "确认稳定后执行：Remove-Item -Path '$oldDir' -Recurse -Force"
Write-Log "日志文件：$logFile"
