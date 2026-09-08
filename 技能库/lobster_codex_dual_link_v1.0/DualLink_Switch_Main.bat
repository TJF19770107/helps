@echo off
chcp 65001 >nul
title 龙虾双链路切换-主链路 v1.0
setlocal enabledelayedexpansion

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  切换到主链路 (AI Code Switch 直连)     ║
echo  ║  Codex → 4567(AICS) → MiMO API          ║
echo  ╚══════════════════════════════════════════╝
echo.

set CODEX_CONFIG="C:\Users\Administrator\.codex\config.toml"
set AICS_ACCESS="C:\Users\Administrator\.aicodeswitch\fs-db\access-keys.json"
set BACKUP_DIR="E:\龙虾AI主控中心\我的AI分身\技能库\lobster_codex_dual_link_v1.0\backups\%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"

:: 创建备份
echo [1/4] 备份当前配置...
mkdir "%BACKUP_DIR%" 2>nul
copy %CODEX_CONFIG% "%BACKUP_DIR%\codex_config.toml" /Y >nul
echo   ✅ 当前配置已备份到 %BACKUP_DIR%

:: 检查AICS是否运行
echo [2/4] 检查 AI Code Switch 状态...
netstat -ano 2>nul | findstr ":4567 " | findstr "LISTENING" >nul
if %errorlevel% neq 0 (
    echo   ⚠️  AI Code Switch 未运行，正在启动...
    call E:\aicodeswitch_v5\aicodeswitch.cmd start
    timeout /t 5 /nobreak >nul
    netstat -ano 2>nul | findstr ":4567 " | findstr "LISTENING" >nul
    if %errorlevel% neq 0 (
        echo   ❌ AI Code Switch 启动失败！请手动检查
        exit /b 1
    )
)
echo   ✅ AI Code Switch 已在运行 (端口4567)

:: 修改 Codex config.toml
echo [3/4] 修改 Codex config → 主链路 (4567直连)...
powershell -Command "(Get-Content %CODEX_CONFIG%) -replace 'base_url = \"http://127.0.0.1:15721/v1\"', 'base_url = \"http://127.0.0.1:4567/codex\"' | Set-Content %CODEX_CONFIG%"
echo   ✅ base_url 已切换为 http://127.0.0.1:4567/codex

:: 验证AICS access-keys
echo [4/4] 验证 AI Code Switch 密钥注册...
type %AICS_ACCESS% 2>nul | findstr "tp-cs3zbef" >nul
if %errorlevel% neq 0 (
    echo   ⚠️  access-keys.json 不包含当前密钥，正在注册...
    echo [{"key":"tp-cs3zbef7vhc75lcpsw9x7pau27mjftwhqnovn5zrq2d0puft","name":"Codex-MiMO-TokenPlan-Key","enabled":true,"clientType":"codex"}] > %AICS_ACCESS%
)
echo   ✅ 密钥已注册

:: 快速验证
echo.
echo  运行快速验证...
curl -s -o nul -w "  4567 连通性: HTTP %%{http_code}" http://127.0.0.1:4567/codex/responses
echo.
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ✅ 主链路切换完成！                   ║
echo  ║   Codex → 4567(AICS) → MiMO API          ║
echo  ║   当前: 纯对话编码模式                   ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  提示: 如需插件解锁，请运行 DualLink_Switch_Backup.bat
pause
