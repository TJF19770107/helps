@echo off
chcp 65001 >nul
title 龙虾双链路一键回滚 v1.0
setlocal enabledelayedexpansion

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   龙虾Codex双链路一键回滚 v1.0          ║
echo  ║   从备份恢复全部配置                    ║
echo  ╚══════════════════════════════════════════╝
echo.

set BACKUP_BASE="E:\龙虾AI主控中心\我的AI分身\技能库\lobster_codex_dual_link_v1.0\backups"

:: 列出可用的备份
echo 可用的备份版本:
echo.
set i=0
for /f "delims=" %%d in ('dir /b /ad "%BACKUP_BASE%" 2^>nul') do (
    set /a i+=1
    echo   [!i!] %%d
)

if %i%==0 (
    echo   ❌ 没有找到任何备份！
    pause
    exit /b 1
)

:: 选择备份
echo.
set /p CHOICE="输入备份编号 (1-%i%): "

set j=0
for /f "delims=" %%d in ('dir /b /ad "%BACKUP_BASE%" 2^>nul') do (
    set /a j+=1
    if !j!==%CHOICE% set SEL=%%d
)

if not defined SEL (
    echo ❌ 无效选择！
    pause
    exit /b 1
)

set RESTORE_DIR="%BACKUP_BASE%\%SEL%"

echo.
echo 将从此备份恢复: %SEL%
echo.

:: 确认
set /p CONFIRM="确认回滚？这将覆盖当前所有配置！(y/N): "
if /i not "%CONFIRM%"=="y" (
    echo 已取消
    pause
    exit /b 0
)

echo.
echo [1/4] 恢复 Codex 配置...
copy "%RESTORE_DIR%\codex_config.toml" "C:\Users\Administrator\.codex\config.toml" /Y >nul
copy "%RESTORE_DIR%\codex_auth.json" "C:\Users\Administrator\.codex\auth.json" /Y >nul
echo   ✅ Codex 配置已恢复

echo [2/4] 恢复 AI Code Switch 配置...
copy "%RESTORE_DIR%\aics_routes.json" "C:\Users\Administrator\.aicodeswitch\fs-db\routes.json" /Y >nul
copy "%RESTORE_DIR%\aics_vendors.json" "C:\Users\Administrator\.aicodeswitch\fs-db\vendors.json" /Y >nul
copy "%RESTORE_DIR%\aics_access_keys.json" "C:\Users\Administrator\.aicodeswitch\fs-db\access-keys.json" /Y >nul
copy "%RESTORE_DIR%\aics_api_path_bindings.json" "C:\Users\Administrator\.aicodeswitch\fs-db\api-path-bindings.json" /Y >nul
copy "%RESTORE_DIR%\aics_config.json" "C:\Users\Administrator\.aicodeswitch\fs-db\config.json" /Y >nul
echo   ✅ AICS 配置已恢复

echo [3/4] 恢复 CC-Switch 数据库...
copy "%RESTORE_DIR%\cc_switch.db" "C:\Users\Administrator\.cc-switch\cc-switch.db" /Y >nul
echo   ✅ CC-Switch 数据库已恢复

echo [4/4] 重启服务...
echo   ⚠️  请手动重启以下服务:
echo      - AI Code Switch: E:\aicodeswitch_v5\aicodeswitch.cmd restart
echo      - CC-Switch: 重新启动 cc-switch.exe
echo      - Codex++: 重新启动 codex-plus-plus.exe

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ✅ 回滚完成！                         ║
echo  ║   配置文件已从 %SEL% 恢复         ║
echo  ╚══════════════════════════════════════════╝
pause
