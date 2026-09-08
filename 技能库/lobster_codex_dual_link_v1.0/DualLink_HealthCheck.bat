@echo off
chcp 65001 >nul
title 龙虾双链路健康检测 v1.0
setlocal enabledelayedexpansion

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   龙虾Codex双链路健康检测 v1.0         ║
echo  ║   检测时间: %date% %time%         ║
echo  ╚══════════════════════════════════════════╝
echo.

set FAIL=0
set PASS=0

:: ============================================
:: 检测1: 端口15721 (CC-Switch总网关)
:: ============================================
echo [检测1/8] 端口 15721 - CC-Switch 总网关
netstat -ano 2>nul | findstr ":15721 " | findstr "LISTENING" >nul
if %errorlevel%==0 (
    for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":15721 " ^| findstr "LISTENING"') do set PID=%%a
    echo   ✅ 端口 15721 存活 → PID !PID!
    set /a PASS+=1
) else (
    echo   ❌ 端口 15721 未监听！
    set /a FAIL+=1
)

:: ============================================
:: 检测2: 端口4567 (AI Code Switch)
:: ============================================
echo [检测2/8] 端口 4567 - AI Code Switch
netstat -ano 2>nul | findstr ":4567 " | findstr "LISTENING" >nul
if %errorlevel%==0 (
    for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":4567 " ^| findstr "LISTENING"') do set PID=%%a
    echo   ✅ 端口 4567 存活 → PID !PID!
    set /a PASS+=1
) else (
    echo   ❌ 端口 4567 未监听！
    set /a FAIL+=1
)

:: ============================================
:: 检测3: 端口57321 (Codex++)
:: ============================================
echo [检测3/8] 端口 57321 - Codex++
netstat -ano 2>nul | findstr ":57321 " | findstr "LISTENING" >nul
if %errorlevel%==0 (
    for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":57321 " ^| findstr "LISTENING"') do set PID=%%a
    echo   ✅ 端口 57321 存活 → PID !PID!
    set /a PASS+=1
) else (
    echo   ⚠️  端口 57321 未监听 (Codex++可能未启动)
    set /a FAIL+=1
)

:: ============================================
:: 检测4: HTTP 15721/v1/models
:: ============================================
echo [检测4/8] HTTP 连通性: 15721/v1/models
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:15721/v1/models >nul 2>&1
if %errorlevel%==0 (
    for /f %%a in ('curl -s -o nul -w "%%{http_code}" http://127.0.0.1:15721/v1/models 2^>nul') do set CODE=%%a
    echo   ✅ 15721 HTTP !CODE!
    set /a PASS+=1
) else (
    echo   ❌ 15721 无响应
    set /a FAIL+=1
)

:: ============================================
:: 检测5: HTTP 4567/codex/responses
:: ============================================
echo [检测5/8] HTTP 连通性: 4567/codex/responses
curl -s -o nul -w "%%{http_code}" http://127.0.0.1:4567/codex/responses >nul 2>&1
if %errorlevel%==0 (
    for /f %%a in ('curl -s -o nul -w "%%{http_code}" http://127.0.0.1:4567/codex/responses 2^>nul') do set CODE=%%a
    echo   ✅ 4567 HTTP !CODE!
    set /a PASS+=1
) else (
    echo   ❌ 4567 无响应
    set /a FAIL+=1
)

:: ============================================
:: 检测6: 主链路穿透测试 (4567→MiMO)
:: ============================================
echo [检测6/8] 主链路穿透测试 (4567→MiMO)
curl -s -X POST http://127.0.0.1:4567/codex/responses -H "Content-Type: application/json" -d "{\"model\":\"mimo-v2.5-pro\",\"input\":\"hi\",\"max_output_tokens\":5}" 2>nul | findstr "output" >nul
if %errorlevel%==0 (
    echo   ✅ 主链路穿透成功
    set /a PASS+=1
) else (
    echo   ❌ 主链路穿透失败
    set /a FAIL+=1
)

:: ============================================
:: 检测7: 备用链路穿透测试 (15721→4567→MiMO)
:: ============================================
echo [检测7/8] 备用链路穿透测试 (15721→4567→MiMO)
curl -s -X POST http://127.0.0.1:15721/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\":\"mimo-v2.5-pro\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":5}" 2>nul | findstr "content" >nul
if %errorlevel%==0 (
    echo   ✅ 备用链路穿透成功
    set /a PASS+=1
) else (
    echo   ❌ 备用链路穿透失败
    set /a FAIL+=1
)

:: ============================================
:: 检测8: MiMO API直连
:: ============================================
echo [检测8/8] MiMO API 直连测试
curl -s -o nul -w "%%{http_code}" https://token-plan-cn.xiaomimimo.com/v1/chat/completions >nul 2>&1
if %errorlevel%==0 (
    for /f %%a in ('curl -s -o nul -w "%%{http_code}" https://token-plan-cn.xiaomimimo.com/v1/chat/completions 2^>nul') do set CODE=%%a
    echo   ✅ MiMO API HTTP !CODE!
    set /a PASS+=1
) else (
    echo   ❌ MiMO API 不可达
    set /a FAIL+=1
)

:: ============================================
:: 汇总报告
:: ============================================
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   健康检测报告                          ║
echo  ╠══════════════════════════════════════════╣
echo  ║   通过: !PASS!/8                         ║
echo  ║   失败: !FAIL!/8                         ║
echo  ╚══════════════════════════════════════════╝
echo.

if !FAIL! gtr 0 (
    echo  ❌ 检测未通过，请根据上方失败项排查！
    exit /b 1
) else (
    echo  ✅ 双链路全部健康，可以正常使用！
    exit /b 0
)
