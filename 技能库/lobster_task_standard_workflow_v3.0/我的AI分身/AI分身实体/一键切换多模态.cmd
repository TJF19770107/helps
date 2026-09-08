@echo off
chcp 65001>nul
rem 一键切换 Codex 到多模态模型（重启后贴图即可识别）
echo 选择要切换的模型：
echo  1) GLM-5.3-flash（智谱，视觉）
echo  2) NVIDIA llama-vision（免费视觉）
set /p c="输入 1 或 2: "
if "%c%"=="1" (
  echo model_provider = "glm_free" ^| model = "glm-5.3-flash" > "C:\tmp\switch_model.txt"
)
if "%c%"=="2" (
  echo model_provider = "nvidia_free" ^| model = "meta/llama-3.2-11b-vision-instruct" > "C:\tmp\switch_model.txt"
)
echo 已生成切换标记 C:\tmp\switch_model.txt
echo 请在 Codex 配置中按标记改 model_provider/model，然后重启 Codex。
echo 记忆不会丢（读 HANDOFF_恢复文档.md 即可接回）。
pause