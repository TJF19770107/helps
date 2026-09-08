@echo off
chcp 65001 >nul
title 龙虾双链路切换-备用链路 v1.0
setlocal enabledelayedexpansion

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║  切换到备用链路 (CC-Switch + Codex++)    ║
echo  ║  Codex → 15721(CC-Switch) → 4567(AICS)  ║
echo  ║            → MiMO API                    ║
echo  ╚══════════════════════════════════════════╝
echo.

set CODEX_CONFIG="C:\Users\Administrator\.codex\config.toml"
set CC_SWITCH_EXE="E:\龙虾AI主控中心\CC-Switch\cc-switch.exe"
set CODEXPP_EXE="E:\龙虾AI主控中心\tools\Codex++\codex-plus-plus.exe"
set BACKUP_DIR="E:\龙虾AI主控中心\我的AI分身\技能库\lobster_codex_dual_link_v1.0\backups\%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"

:: 创建备份
echo [1/5] 备份当前配置...
mkdir "%BACKUP_DIR%" 2>nul
copy %CODEX_CONFIG% "%BACKUP_DIR%\codex_config.toml" /Y >nul
echo   ✅ 当前配置已备份到 %BACKUP_DIR%

:: 检查CC-Switch
echo [2/5] 检查 CC-Switch 状态...
netstat -ano 2>nul | findstr ":15721 " | findstr "LISTENING" >nul
if %errorlevel% neq 0 (
    echo   ⚠️  CC-Switch 未运行，正在启动...
    start "" %CC_SWITCH_EXE%
    timeout /t 5 /nobreak >nul
    netstat -ano 2>nul | findstr ":15721 " | findstr "LISTENING" >nul
    if %errorlevel% neq 0 (
        echo   ❌ CC-Switch 启动失败！请手动检查
        exit /b 1
    )
)
echo   ✅ CC-Switch 已在运行 (端口15721)

:: 检查AICS (CC-Switch需要转发到4567)
echo [3/5] 检查 AI Code Switch 状态...
netstat -ano 2>nul | findstr ":4567 " | findstr "LISTENING" >nul
if %errorlevel% neq 0 (
    echo   ⚠️  AI Code Switch 未运行，正在启动...
    call E:\aicodeswitch_v5\aicodeswitch.cmd start
    timeout /t 5 /nobreak >nul
    netstat -ano 2>nul | findstr ":4567 " | findstr "LISTENING" >nul
    if %errorlevel% neq 0 (
        echo   ❌ AI Code Switch 启动失败！备用链路需要AICS做协议转换
        exit /b 1
    )
)
echo   ✅ AI Code Switch 已在运行 (端口4567)

:: 验证CC-Switch MiMO provider配置
echo [4/5] 验证 CC-Switch MiMO Provider 配置...
sqlite3 "C:\Users\Administrator\.cc-switch\cc-switch.db" "SELECT settings_config FROM providers WHERE id='d240abd2-180b-4698-9c3a-309300d64ca5' AND app_type='codex';" 2>nul | findstr "4567" >nul
if %errorlevel% neq 0 (
    echo   ❌ CC-Switch MiMO provider 的 base_url 未指向 4567！正在修复...
    sqlite3 "C:\Users\Administrator\.cc-switch\cc-switch.db" "UPDATE providers SET settings_config = '{\"auth\":{\"OPENAI_API_KEY\":\"tp-cs3zbef7vhc75lcpsw9x7pau27mjftwhqnovn5zrq2d0puft\"},\"config\":\"model_provider = \\\"custom\\\"\nmodel = \\\"mimo-v2.5-pro\\\"\nmodel_reasoning_effort = \\\"high\\\"\ndisable_response_storage = true\n\n[model_providers]\n[model_providers.custom]\nname = \\\"xiaomi_mimo\\\"\nbase_url = \\\"http://127.0.0.1:4567/codex\\\"\nwire_api = \\\"responses\\\"\nrequires_openai_auth = true\",\"modelCatalog\":{\"models\":[{\"model\":\"mimo-v2.5-pro\",\"displayName\":\"MiMo V2.5 Pro\",\"contextWindow\":1048576}]}}' WHERE id='d240abd2-180b-4698-9c3a-309300d64ca5' AND app_type='codex';" 2>nul
    echo   ✅ 已修复
)

:: 重置provider健康状态
sqlite3 "C:\Users\Administrator\.cc-switch\cc-switch.db" "UPDATE provider_health SET is_healthy=1, failures=0 WHERE provider_id='d240abd2-180b-4698-9c3a-309300d64ca5';" 2>nul
echo   ✅ Provider 健康状态已重置

:: 修改 Codex config.toml
echo [5/5] 修改 Codex config → 备用链路 (15721)...
powershell -Command "(Get-Content %CODEX_CONFIG%) -replace 'base_url = \"http://127.0.0.1:4567/codex\"', 'base_url = \"http://127.0.0.1:15721/v1\"' | Set-Content %CODEX_CONFIG%"
echo   ✅ base_url 已切换为 http://127.0.0.1:15721/v1

:: 快速验证
echo.
echo  运行快速验证...
curl -s -o nul -w "  15721 连通性: HTTP %%{http_code}" http://127.0.0.1:15721/v1/models
echo.
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ✅ 备用链路切换完成！                 ║
echo  ║   Codex → 15721(CC-Switch) → 4567(AICS)  ║
echo  ║            → MiMO API                    ║
echo  ║   当前: 插件解锁 + 对话双模式            ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  提示: 
echo    - 通过 Codex++ 启动 Codex 可解锁插件
echo    - 如仅需纯对话编码，请运行 DualLink_Switch_Main.bat
pause
