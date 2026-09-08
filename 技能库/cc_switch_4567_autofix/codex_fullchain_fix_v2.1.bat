@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ════════════════════════════════════════════════════════
echo   Codex++ 全链路修复工具 V2.1
echo   龙虾五步法: 备份-修复-校验-回滚-沉淀
echo   覆盖错误: 400/502/404/断连/stream disconnected
echo   ⚠️ 关键规则: 所有4567 URL 必须带 /v1 后缀!
echo ════════════════════════════════════════════════════════
echo.

:: ========== Step 0: 快照备份 ==========
set SNAPSHOT_DIR=G:\龙虾AI主控中心\Codex备份\snapshots\%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%_auto_fix
mkdir "%SNAPSHOT_DIR%" 2>nul
echo [Step 0] 快照备份 → %SNAPSHOT_DIR%
copy "E:\龙虾AI主控中心\CC-Switch\.cc-switch\cc-switch.db" "%SNAPSHOT_DIR%\" >nul 2>&1
copy "C:\Users\Administrator\.aicodeswitch\fs-db\routes.json" "%SNAPSHOT_DIR%\" >nul 2>&1
echo   ✅ 快照完成
echo.

:: ========== Step 1: 强杀所有 cc-switch ==========
echo [Step 1] 强制终止 cc-switch...
taskkill /F /IM cc-switch.exe >nul 2>&1
timeout /t 2 /nobreak >nul
:: 再杀一次确保干净
taskkill /F /IM cc-switch.exe >nul 2>&1
timeout /t 2 /nobreak >nul
:: 确认端口释放
netstat -ano | findstr ":15721.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ❌ 15721仍被占用，尝试按PID杀...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":15721.*LISTENING"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 3 /nobreak >nul
) else (
    echo   ✅ 15721已释放
)

:: ========== Step 2: 清理僵尸PID + 启动 4567 ==========
echo.
echo [Step 2] AI Code Switch (4567)...
if exist "C:\Users\Administrator\.aicodeswitch\server.pid" (
    del /F "C:\Users\Administrator\.aicodeswitch\server.pid" >nul 2>&1
    echo   ✅ 清除残留server.pid
)

netstat -ano | findstr ":4567.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ 4567 已运行
) else (
    echo   正在启动 4567...
    start /B cmd /c "cd /d E:\aicodeswitch_v5 && node node_modules\aicodeswitch\bin\cli.js start --port 4567"
    timeout /t 8 /nobreak >nul
    netstat -ano | findstr ":4567.*LISTENING" >nul 2>&1
    if !errorlevel! equ 0 (
        echo   ✅ 4567 已启动
    ) else (
        echo   ❌ 4567启动失败!
    )
)

:: ========== Step 3: DB修复 (核心!) ==========
echo.
echo [Step 3] 修复 cc-switch DB...
set CC_DB=E:\龙虾AI主控中心\CC-Switch\.cc-switch\cc-switch.db

:: 🔴🔴🔴 核心规则: cc-switch 拼接路径逻辑是 baseURL + "/responses"
::         所以 baseURL 必须是 http://127.0.0.1:4567/v1
::         最终转发路径 = http://127.0.0.1:4567/v1/responses ✅
::
:: ❌ 错误: baseURL = http://127.0.0.1:4567
::    结果路径 = http://127.0.0.1:4567/responses → 404!

echo.
echo   Fix A: xiaomimimo20260612 provider (Codex实际用的!)
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'base_url\":\"http://127.0.0.1:4567\"', 'base_url\":\"http://127.0.0.1:4567/v1\"') WHERE id='xiaomimimo20260612';" >nul 2>&1
echo   ✅ xiaomimimo base_url → 4567/v1

echo   Fix B: aicodeswitch provider baseURL
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'baseURL\":\"http://127.0.0.1:4567\"', 'baseURL\":\"http://127.0.0.1:4567/v1\"') WHERE id='aicodeswitch';" >nul 2>&1
echo   ✅ aicodeswitch baseURL → 4567/v1

echo   Fix C: provider_endpoints 表 (id=15,21)
sqlite3 "%CC_DB%" "UPDATE provider_endpoints SET url = 'http://127.0.0.1:4567/v1' WHERE id IN (15,21) AND url NOT LIKE '%%/v1';" >nul 2>&1
:: 如果上面没匹配(已经有其他值)，强制更新
sqlite3 "%CC_DB%" "UPDATE provider_endpoints SET url = 'http://127.0.0.1:4567/v1' WHERE id IN (15,21);" >nul 2>&1
echo   ✅ endpoints → 4567/v1

echo   Fix D: 清理 /opencode/v1 错误后缀
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, '4567/opencode/v1', '4567/v1') WHERE id='aicodeswitch';" >nul 2>&1
echo   ✅ 清理 /opencode/v1

echo   Fix E: 确保 xiaomimimo 不直连MiMO
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'token-plan-cn.xiaomimimo.com', 'http://127.0.0.1:4567/v1') WHERE id LIKE 'xiaomimimo%%';" >nul 2>&1
sqlite3 "%CC_DB%" "UPDATE provider_endpoints SET url = 'http://127.0.0.1:4567/v1' WHERE url LIKE '%%xiaomimimo%%';" >nul 2>&1
echo   ✅ xiaomimimo → 经4567中转

echo   Fix F: 🔴 兜底! 所有 providers 中 4567 地址缺/v1 一律补齐 (覆盖 d240abd2 等漏网provider)
sqlite3 "%CC_DB%" "UPDATE providers SET settings_config = REPLACE(settings_config, 'http://127.0.0.1:4567\"', 'http://127.0.0.1:4567/v1\"') WHERE settings_config LIKE '%%127.0.0.1:4567\"%%' AND settings_config NOT LIKE '%%127.0.0.1:4567/v1%%';" >nul 2>&1
echo   ✅ 兜底补全所有 4567 地址 /v1 前缀

echo.
echo   验证DB配置...
sqlite3 "%CC_DB%" "SELECT '  xiaomimimo: ' || substr(json_extract(settings_config,'$.base_url'),1,40) FROM providers WHERE id='xiaomimimo20260612';"
sqlite3 "%CC_DB%" "SELECT '  aicodeswitch: ' || substr(json_extract(settings_config,'$.options.baseURL'),1,40) FROM providers WHERE id='aicodeswitch';"
sqlite3 "%CC_DB%" "SELECT '  endpoint#15: ' || url FROM provider_endpoints WHERE id=15;"
sqlite3 "%CC_DB%" "SELECT '  endpoint#21: ' || url FROM provider_endpoints WHERE id=21;"

:: ========== Step 4: 启动 cc-switch ==========
echo.
echo [Step 4] 启动 cc-switch...
start "" "E:\龙虾AI主控中心\CC-Switch\cc-switch.exe"
timeout /t 15 /nobreak >nul

netstat -ano | findstr ":15721.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ cc-switch 已启动 (15721)
) else (
    echo   ⚠️ 15721未就绪，等待中...
    timeout /t 10 /nobreak >nul
    netstat -ano | findstr ":15721.*LISTENING" >nul 2>&1
    if !errorlevel! equ 0 (
        echo   ✅ cc-switch 已启动 (延迟绑定)
    ) else (
        echo   ❌ 15721启动失败
    )
)

:: ========== Step 5: 全链路测试 ==========
echo.
echo [Step 5] 全链路测试...
echo.
echo   测试: Codex++ ^-> 15721 ^-> 4567 ^-> MiMO
curl -s --max-time 30 http://127.0.0.1:15721/v1/responses -H "Content-Type: application/json" -d "{\"model\":\"gpt-5.5\",\"input\":\"say OK\"}" >"%SNAPSHOT_DIR%\test_result.txt" 2>&1
type "%SNAPSHOT_DIR%\test_result.txt" | find /i "error" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ❌ 测试失败! 详情:
    type "%SNAPSHOT_DIR%\test_result.txt"
) else (
    echo   ✅ 全链路测试通过!
    type "%SNAPSHOT_DIR%\test_result.txt"
)

echo.
echo   ┌──────────┬────────┬──────────────┐
echo   │   端口    │ 状态  │     PID      │
echo   ├──────────┼────────┼──────────────┤
netstat -ano | findstr ":4567.*LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":4567.*LISTENING"') do echo   │  4567    │  OK   │  PID %%p     │
) else (
    echo   │  4567    │ FAIL  │  -           │
)
netstat -ano | findstr ":15721.*LISTENING" >nul 2>&1
if %errorlevel! equ 0 (
    for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":15721.*LISTENING"') do echo   │  15721   │  OK   │  PID %%p     │
) else (
    echo   │  15721   │ FAIL  │  -           │
)
echo   └──────────┴────────┴──────────────┘
echo.
echo ════════════════════════════════════════════════════════
echo   修复完成! 请在 Codex++ 中发送消息测试
echo   快照: %SNAPSHOT_DIR%
echo ════════════════════════════════════════════════════════
pause
