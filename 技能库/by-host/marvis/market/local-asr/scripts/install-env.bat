@echo off
setlocal EnableExtensions

for %%D in ("%~dp0..\bin") do set "UV_EXE=%%~fD\uv.exe"
for %%D in ("%~dp0..") do set "SKILL_ROOT=%%~fD"
set "WHEELS_DIR=%SKILL_ROOT%\wheels"

if not exist "%UV_EXE%" (
	echo Local UV was not found. Running scripts\install-uv.bat...
	call "%~dp0install-uv.bat"
	if errorlevel 1 exit /b 1
)

set "VENV_DIR=%USERPROFILE%\.openvino\venv\asr"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
if not exist "%VENV_PY%" (
	echo ERROR: external venv not found at "%VENV_PY%".
	exit /b 1
)

echo Installing ASR runtime packages into %VENV_PY% ...
"%UV_EXE%" pip install --python "%VENV_PY%" ^
	"openvino>=2025.4" ^
	"numpy<2.0" ^
	"soundfile" ^
	"scipy" ^
	"librosa" ^
	"modelscope" ^
	"moviepy"
if errorlevel 1 (
	echo ERROR: failed to install base ASR packages.
	exit /b 1
)

set "QWEN_WHEEL="
for %%W in ("%WHEELS_DIR%\qwen_asr-*.whl") do set "QWEN_WHEEL=%%~fW"
if not defined QWEN_WHEEL (
	echo ERROR: qwen_asr wheel not found under "%WHEELS_DIR%".
	exit /b 1
)

echo Installing qwen_asr from "%QWEN_WHEEL%" ...
"%UV_EXE%" pip install --python "%VENV_PY%" "%QWEN_WHEEL%"
set "EXIT_CODE=%ERRORLEVEL%"

exit /b %EXIT_CODE%
