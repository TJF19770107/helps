@echo off
chcp 65001 >nul
:: 赛博书屋快速自检脚本
:: v1.0 | 2026-08-05

echo ========================================
echo   赛博书屋 快速自检
echo ========================================
echo.

set SKILL_ROOT=E:\龙虾AI主控中心\我的AI分身\技能库\cyber-book-house
set LOBSTER_V3=E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0
set SYMLINK=%LOBSTER_V3%\cyber-book-house

echo [软链接检查]
if exist "%SYMLINK%" (
    echo   [OK] 软链接存在
    dir "%SYMLINK%" 2>nul | findstr "SYMLINK" >nul && echo   [OK] 为符号链接 || echo   [WARN] 不是符号链接
) else (
    echo   [FAIL] 软链接不存在
)

echo.
echo [核心文件检查]
if exist "%SKILL_ROOT%\SKILL.md" (echo   [OK] SKILL.md) else (echo   [FAIL] SKILL.md缺失)
if exist "%SKILL_ROOT%\config\agent_permissions.json" (echo   [OK] agent_permissions.json) else (echo   [FAIL] agent_permissions.json缺失)
if exist "%SKILL_ROOT%\src\cyber_ingest.py" (echo   [OK] cyber_ingest.py) else (echo   [FAIL] cyber_ingest.py缺失)
if exist "%SKILL_ROOT%\scripts\orca_bridge.py" (echo   [OK] orca_bridge.py) else (echo   [FAIL] orca_bridge.py缺失)
if exist "%SKILL_ROOT%\scripts\startup.ps1" (echo   [OK] startup.ps1) else (echo   [FAIL] startup.ps1缺失)
if exist "%SKILL_ROOT%\tests\claude_review_template.md" (echo   [OK] claude_review_template.md) else (echo   [FAIL] claude_review_template.md缺失)

echo.
echo [权限配置文件校验]
python -c "import json; json.load(open(r'%SKILL_ROOT%\config\agent_permissions.json','r',encoding='utf-8')); print('  [OK] JSON格式正确')" 2>nul || echo   [FAIL] JSON格式错误

echo.
echo [Obsidian输出目录检查]
if exist "E:\龙虾AI主控中心\Obsidian\wiki\赛博书屋" (echo   [OK] Obsidian赛博书屋目录) else (echo   [WARN] Obsidian赛博书屋目录未创建 - 首次运行startup.ps1自动创建)

echo.
echo ========================================
echo   自检完成
echo ========================================
pause
