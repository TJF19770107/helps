@echo off
chcp 65001>nul
rem NVIDIA_API_KEY 已迁到环境变量
set NVIDIA_PROXY_PORT=13331
start /min "NVIDIAFree" "C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe" "E:\龙虾AI主控中心\我的AI分身\技能库\lobster_task_standard_workflow_v3.0\我的AI分身\AI分身实体\nvidia_free_proxy.py"
echo 已启动英伟达免费模型代理 @ 127.0.0.1:13331
pause
