<#
  mirror_skill.ps1 — cloudbase-hy3-relay 技能一键镜像（备份 + 同步 + 校验）
  用法（在受管目录放行后，于本机以 Administrator 运行）：
    powershell -ExecutionPolicy Bypass -File "C:\Users\Administrator\.workbuddy\skills\cloudbase-hy3-relay\scripts\mirror_skill.ps1"
  说明：本脚本由 WorkBuddy 生成，供用户在沙箱外执行；沙箱内对该目录的写入已被硬拦截。
#>
$ErrorActionPreference = 'Stop'
$src = "C:\Users\Administrator\.workbuddy\skills\cloudbase-hy3-relay"
$dst = "E:\龙虾AI主控中心\我的AI分身\技能库\cloudbase-hy3-relay"
$ts  = Get-Date -Format 'yyyyMMdd-HHmmss'

# 1) 备份现有共享版本（支持回滚）
if (Test-Path $dst) {
    $bak = "E:\龙虾AI主控中心\我的AI分身\技能库\.bak_cloudbase-hy3-relay_$ts"
    Write-Host ("[1/3] 备份现有版本 -> {0}" -f $bak)
    Copy-Item -Recurse $dst $bak
} else {
    Write-Host "[1/3] 目标不存在，跳过备份"
}

# 2) 递归镜像
Write-Host ("[2/3] 镜像 {0} -> {1}" -f $src, $dst)
Copy-Item -Recurse -Force $src $dst

# 3) 校验
$srcFiles = (Get-ChildItem -Recurse -File $src).Count
$dstFiles = (Get-ChildItem -Recurse -File $dst).Count
Write-Host ("[3/3] 校验：源文件数={0} 目标文件数={1}" -f $srcFiles, $dstFiles)
if ($srcFiles -eq $dstFiles) {
    Write-Host "OK 镜像成功，文件数一致。技能已同步至舰队共享技能库。"
} else {
    Write-Host "WARN 文件数不一致，请检查。" -ForegroundColor Yellow
    exit 1
}
