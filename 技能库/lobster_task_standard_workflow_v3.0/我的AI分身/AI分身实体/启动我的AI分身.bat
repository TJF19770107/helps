chcp 65001>nul
@echo off
REM 一键启动我的AI分身（全量加载版）
cd /d "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体"
"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe" 启动我的AI分身.py %*
pause
