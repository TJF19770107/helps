@echo off
chcp 65001 >nul
title Codex数据全量回滚 v1.0
setlocal enabledelayedexpansion

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   Codex 数据全量回滚 v1.0              ║
echo  ║   从备份恢复全部Codex数据              ║
echo  ╚══════════════════════════════════════════╝
echo.

set CODEX_DATA="C:\Users\Administrator\.codex"
set BACKUP_BASE="E:\龙虾AI主控中心\我的AI分身\技能库\lobster_codex_dual_link_v1.0\backups"

:: 列出可用的全量备份
echo 可用的全量备份:
echo.
set i=0
for /f "delims=" %%d in ('dir /b /ad "%BACKUP_BASE%\codex_full_*" 2^>nul') do (
    set /a i+=1
    echo   [!i!] %%d
)

if %i%==0 (
    echo   ❌ 没有找到任何全量备份！请先运行备份脚本。
    pause
    exit /b 1
)

echo.
set /p CHOICE="输入备份编号 (1-%i%): "

set j=0
for /f "delims=" %%d in ('dir /b /ad "%BACKUP_BASE%\codex_full_*" 2^>nul') do (
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
echo 备份内容:
dir "%RESTORE_DIR%" /b
echo.

echo ⚠️  警告：此操作将覆盖当前所有Codex数据！
echo     包括：对话历史、工作区配置、插件设置、技能库
set /p CONFIRM="确认回滚？(输入大写 YES 确认): "
if not "%CONFIRM%"=="YES" (
    echo 已取消
    pause
    exit /b 0
)

:: 先创建当前数据的紧急备份
echo.
echo [0/5] 创建当前数据紧急备份...
set EMERGENCY="%BACKUP_BASE%\emergency_before_rollback_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
mkdir "%EMERGENCY%" 2>nul
copy %CODEX_DATA%\*.toml "%EMERGENCY%\" /Y >nul 2>&1
copy %CODEX_DATA%\*.json "%EMERGENCY%\" /Y >nul 2>&1
copy %CODEX_DATA%\*.jsonl "%EMERGENCY%\" /Y >nul 2>&1
copy %CODEX_DATA%\*.sqlite "%EMERGENCY%\" /Y >nul 2>&1
echo   ✅ 紧急备份已保存到 %EMERGENCY%

:: 需要停止Codex才能还原数据库
echo [1/5] 检查Codex运行状态...
tasklist /fi "imagename eq codex.exe" 2>nul | findstr "codex.exe" >nul
if %errorlevel%==0 (
    echo   ⚠️  Codex正在运行！请手动关闭Codex后再执行回滚。
    pause
    exit /b 1
)
echo   ✅ Codex已停止

echo [2/5] 还原核心数据库...
copy "%RESTORE_DIR%\logs_2.sqlite" "%CODEX_DATA%\logs_2.sqlite" /Y >nul
copy "%RESTORE_DIR%\state_5.sqlite" "%CODEX_DATA%\state_5.sqlite" /Y >nul
copy "%RESTORE_DIR%\memories_1.sqlite" "%CODEX_DATA%\memories_1.sqlite" /Y >nul
copy "%RESTORE_DIR%\goals_1.sqlite" "%CODEX_DATA%\goals_1.sqlite" /Y >nul
echo   ✅ 数据库已还原

echo [3/5] 还原会话记录...
if exist "%RESTORE_DIR%\sessions" (
    rd /s /q "%CODEX_DATA%\sessions" 2>nul
    xcopy "%RESTORE_DIR%\sessions" "%CODEX_DATA%\sessions" /E /I /Y >nul
)
copy "%RESTORE_DIR%\session_index.jsonl" "%CODEX_DATA%\" /Y >nul
copy "%RESTORE_DIR%\history.jsonl" "%CODEX_DATA%\" /Y >nul
echo   ✅ 会话已还原

echo [4/5] 还原配置文件...
copy "%RESTORE_DIR%\config.toml" "%CODEX_DATA%\" /Y >nul
copy "%RESTORE_DIR%\codex.config.json" "%CODEX_DATA%\" /Y >nul
copy "%RESTORE_DIR%\auth.json" "%CODEX_DATA%\" /Y >nul
copy "%RESTORE_DIR%\mcp.json" "%CODEX_DATA%\" /Y >nul
copy "%RESTORE_DIR%\.codex-global-state.json" "%CODEX_DATA%\" /Y >nul
echo   ✅ 配置已还原

echo [5/5] 清理WAL日志...
del "%CODEX_DATA%\*.sqlite-wal" /Q 2>nul
del "%CODEX_DATA%\*.sqlite-shm" /Q 2>nul
echo   ✅ WAL已清理

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ✅ 回滚完成！                         ║
echo  ║   数据已从 %SEL% 恢复       ║
echo  ║   紧急备份: emergency_before_rollback    ║
echo  ╚══════════════════════════════════════════╝
echo.
echo   提示: 现在可以重新启动 Codex 了
pause
