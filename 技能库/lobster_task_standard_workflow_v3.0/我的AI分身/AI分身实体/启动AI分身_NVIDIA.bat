chcp 65001>nul
@echo off
REM 启动我的AI分身（NVIDIA 免费大脑版）
cd /d "E:\龙虾AI主控中心\我的AI分身\AI分身实体"
"C:\Users\Administrator\.workbuddy\binaries\python\versions\3.13.12\python.exe" nvidia_avatar.py %*
pause
