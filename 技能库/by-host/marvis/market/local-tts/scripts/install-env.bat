@echo off
setlocal

for %%D in ("%~dp0..\bin") do set "UV_EXE=%%~fD\uv.exe"
for %%D in ("%~dp0..") do set "SKILL_ROOT=%%~fD"
set "REQUIREMENTS_FILE=%SKILL_ROOT%\requirements.txt"

if not exist "%UV_EXE%" (
	echo Local UV was not found. Running scripts\install-uv.bat...
	call "%~dp0install-uv.bat"
	if errorlevel 1 exit /b 1
)

if not exist "%REQUIREMENTS_FILE%" (
	echo ERROR: requirements.txt was not found at "%REQUIREMENTS_FILE%".
	exit /b 1
)

set "VENV_PY=%USERPROFILE%\.openvino\venv\tts\Scripts\python.exe"
if not exist "%VENV_PY%" (
	echo ERROR: external venv not found at "%VENV_PY%".
	exit /b 1
)

echo Installing tts requirements via Tsinghua mirror ...
"%UV_EXE%" pip install --python "%VENV_PY%" -r "%REQUIREMENTS_FILE%" --index-url https://pypi.tuna.tsinghua.edu.cn/simple --upgrade
if errorlevel 1 (
	echo Tsinghua mirror failed, retrying from official PyPI ...
	"%UV_EXE%" pip install --python "%VENV_PY%" -r "%REQUIREMENTS_FILE%" --upgrade
	if errorlevel 1 exit /b %ERRORLEVEL%
)

exit /b 0
