@echo off
setlocal

for %%D in ("%~dp0..\bin") do set "UV_EXE=%%~fD\uv.exe"
for %%D in ("%~dp0..") do set "SKILL_ROOT=%%~fD"
set "ASSETS_DIR=%SKILL_ROOT%\assets"
if not exist "%UV_EXE%" (
	echo Local UV was not found. Running scripts\install-uv.bat...
	call "%~dp0install-uv.bat"
	if errorlevel 1 exit /b 1
)

if not exist "%ASSETS_DIR%\*.whl" (
	echo ERROR: No wheel file found in "%ASSETS_DIR%".
	exit /b 1
)

set "WHEEL_FILE="
for %%F in ("%ASSETS_DIR%\*.whl") do (
	set "WHEEL_FILE=%%~nxF"
	goto install
)

echo ERROR: No wheel file found in "%ASSETS_DIR%".
exit /b 1

:install
set "VENV_PY=%USERPROFILE%\.openvino\venv\computer-use\Scripts\python.exe"
if not exist "%VENV_PY%" (
	echo ERROR: external venv not found at "%VENV_PY%".
	exit /b 1
)
echo Installing %WHEEL_FILE% into %VENV_PY% ...
"%UV_EXE%" pip install --python "%VENV_PY%" "%ASSETS_DIR%\%WHEEL_FILE%"
set "EXIT_CODE=%ERRORLEVEL%"

exit /b %EXIT_CODE%
