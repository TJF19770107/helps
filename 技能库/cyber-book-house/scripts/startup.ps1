# 赛博书屋一键启动脚本
# v1.0 | 2026-08-05 | 龙虾五步法内置调用

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  赛博书屋（Cyber Book House）v1.0" -ForegroundColor Cyan
Write-Host "  龙虾五步法软链接内置子技能" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 路径常量
$SKILL_ROOT = "E:\龙虾AI主控中心\我的AI分身\技能库\cyber-book-house"
$LOBSTER_V3 = "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0"
$SYMLINK = "$LOBSTER_V3\cyber-book-house"

# Step1: 校验软链接
Write-Host "[Hermes] 校验软链接..." -ForegroundColor Yellow
if (Test-Path $SYMLINK) {
    $link = Get-Item $SYMLINK
    Write-Host "  ✅ 软链接存在: $($link.Target)" -ForegroundColor Green
} else {
    Write-Host "  ❌ 软链接不存在，正在创建..." -ForegroundColor Red
    New-Item -ItemType SymbolicLink -Path $SYMLINK -Target $SKILL_ROOT -Force
    Write-Host "  ✅ 软链接已创建" -ForegroundColor Green
}

# Step2: 磁盘空间校验
Write-Host "[Hermes] 磁盘空间校验..." -ForegroundColor Yellow
$disk = Get-PSDrive -Name E
$freePercent = [math]::Round(($disk.Free / $disk.Used + $disk.Free) * 100, 2)
Write-Host "  E盘剩余: $([math]::Round($disk.Free/1GB, 2))GB ($freePercent%)" -ForegroundColor White
if ($freePercent -lt 10) {
    Write-Host "  ❌ 磁盘空间不足10%，Hermes暂停萃取任务" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ 磁盘空间充足" -ForegroundColor Green

# Step3: 权限矩阵自检
Write-Host "[Hermes] 四层权限矩阵自检..." -ForegroundColor Yellow
$permFile = "$SKILL_ROOT\config\agent_permissions.json"
if (Test-Path $permFile) {
    $perms = Get-Content $permFile -Raw | ConvertFrom-Json
    Write-Host "  ✅ 权限配置加载成功" -ForegroundColor Green
    Write-Host "    四层架构: Hermes(L1) → Marius(L2) → Codex(L3) → Claude Code(L4)" -ForegroundColor White
} else {
    Write-Host "  ❌ 权限配置文件缺失" -ForegroundColor Red
    exit 1
}

# Step4: Obsidian输出目录就绪
Write-Host "[Marius] 输出目录就绪检查..." -ForegroundColor Yellow
$obsidianWiki = "E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋"
$categories = @("网盘课程", "B站视频", "GitHub仓库", "书籍笔记", "网页文章")
foreach ($cat in $categories) {
    $catPath = Join-Path $obsidianWiki $cat
    if (-not (Test-Path $catPath)) {
        New-Item -ItemType Directory -Path $catPath -Force | Out-Null
        Write-Host "  📁 创建: $catPath" -ForegroundColor Gray
    }
}
Write-Host "  ✅ Obsidian输出目录就绪" -ForegroundColor Green

# Step5: 状态汇总
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  赛博书屋 启动完成" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  软链接: $SYMLINK → $SKILL_ROOT" -ForegroundColor White
Write-Host "  磁盘: $([math]::Round($disk.Free/1GB, 2))GB / $([math]::Round(($disk.Used + $disk.Free)/1GB, 2))GB" -ForegroundColor White
Write-Host "  权限: 四层架构锁定" -ForegroundColor White
Write-Host "  状态: 等待Hermes调度" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "调用入口: 龙虾五步法任意环节 → 关键词触发 → 软链接唤起赛博书屋" -ForegroundColor Gray
Write-Host "触发词: 萃取/学习/网盘解析/B站视频/GitHub资料/资料入库/全网萃取" -ForegroundColor Gray
