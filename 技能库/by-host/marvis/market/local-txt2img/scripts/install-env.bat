@echo off
setlocal

for %%D in ("%~dp0..\bin") do set "UV_EXE=%%~fD\uv.exe"
for %%D in ("%~dp0..") do set "SKILL_ROOT=%%~fD"
set "REQUIREMENTS_FILE=%SKILL_ROOT%\requirements.txt"
set "VENDOR_DIR=%SKILL_ROOT%\vendor"
set "OPTIMUM_ONNX_WHEEL="
set "OPTIMUM_INTEL_WHEEL="

if not exist "%UV_EXE%" (
	echo Local UV was not found. Running scripts\install-uv.bat...
	call "%~dp0install-uv.bat"
	if errorlevel 1 exit /b 1
)

if not exist "%REQUIREMENTS_FILE%" (
	echo ERROR: requirements.txt was not found at "%REQUIREMENTS_FILE%".
	exit /b 1
)

set "VENV_PY=%USERPROFILE%\.openvino\venv\txt2img\Scripts\python.exe"
if not exist "%VENV_PY%" (
	echo ERROR: external venv not found at "%VENV_PY%".
	exit /b 1
)

if not exist "%VENDOR_DIR%" (
	echo ERROR: vendor directory was not found at "%VENDOR_DIR%".
	exit /b 1
)

for %%F in ("%VENDOR_DIR%\optimum_onnx-*.whl") do if exist "%%~fF" set "OPTIMUM_ONNX_WHEEL=%%~fF"
for %%F in ("%VENDOR_DIR%\optimum_intel-*.whl") do if exist "%%~fF" set "OPTIMUM_INTEL_WHEEL=%%~fF"

if not defined OPTIMUM_ONNX_WHEEL (
	echo ERROR: vendored optimum-onnx wheel was not found in "%VENDOR_DIR%".
	exit /b 1
)

if not defined OPTIMUM_INTEL_WHEEL (
	echo ERROR: vendored optimum-intel wheel was not found in "%VENDOR_DIR%".
	exit /b 1
)

echo Installing vendored optimum wheels into %VENV_PY% ...
"%UV_EXE%" pip install --python "%VENV_PY%" --no-deps "%OPTIMUM_ONNX_WHEEL%" "%OPTIMUM_INTEL_WHEEL%"
if errorlevel 1 exit /b %ERRORLEVEL%

echo Installing remaining txt2img requirements into %VENV_PY% ...
"%UV_EXE%" pip install --python "%VENV_PY%" --find-links "%VENDOR_DIR%" -r "%REQUIREMENTS_FILE%"
set "EXIT_CODE=%ERRORLEVEL%"

exit /b %EXIT_CODE%
