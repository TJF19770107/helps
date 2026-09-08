@echo off
setlocal EnableDelayedExpansion

call :InitLog
call :Log "client.bat started with arguments: %*"

if "%~1"=="" (
	call :Log "No prompt argument provided."
	echo Usage: scripts\client.bat "<prompt>" [--voice ^<name^>] [--language ^<lang^>] [--ref-audio ^<path^> --ref-text ^<text^>] [--output ^<wav^>]
	echo        scripts\client.bat --continue
	exit /b 1
)

set "USER_PROMPT=%~1"

if /i "!USER_PROMPT!"=="--continue" (
	echo Resuming pending request ...
) else (
	echo Received prompt: !USER_PROMPT!
)

set "PLATFORM_EXE=%~dp0..\bin\platform.exe"
call :Log "Resolved PLATFORM_EXE=%PLATFORM_EXE%"
if not exist "%PLATFORM_EXE%" (
	call :Log "platform.exe was not found; skipping AIPC check (dev mode)."
	echo WARN: bin\platform.exe missing; skipping AIPC check.
	goto :afterUltraCheck
)

for /f "usebackq delims=" %%I in (`"%PLATFORM_EXE%" --is-aipc`) do set "IS_AIPC=%%I"
call :Log "platform --is-aipc returned %IS_AIPC%"
if not "%IS_AIPC%"=="1" (
	call :Log "This machine is not an Intel AIPC platform."
	echo This skill requires an Intel AIPC platform.
	exit /b 1
)

:afterUltraCheck

rem Build REST_ARGS = all args after the first one, preserving quoting as best as cmd.exe allows.
set "REST_ARGS="
set "SKIP_FIRST=1"
for %%A in (%*) do (
	if defined SKIP_FIRST (
		set "SKIP_FIRST="
	) else (
		if defined REST_ARGS (
			set "REST_ARGS=!REST_ARGS! %%A"
		) else (
			set "REST_ARGS=%%A"
		)
	)
)
call :Log "Resolved REST_ARGS=!REST_ARGS!"

pushd "%~dp0.." >nul
if errorlevel 1 (
	call :Log "Failed to change working directory to %~dp0.."
	exit /b 1
)
call :Log "Changed working directory to %CD%"

for %%D in ("%~dp0..\bin") do set "UV_EXE=%%~fD\uv.exe"
call :Log "Resolved UV_EXE=%UV_EXE%"

set "VENV_DIR=%USERPROFILE%\.openvino\venv\tts"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
call :Log "Resolved VENV_PY=%VENV_PY%"

call :EnsureUv
if errorlevel 1 goto fail
call :Log "EnsureUv completed successfully."
echo UV is available. Continuing ...

if not exist "%VENV_PY%" (
	call :Log "External venv not found at %VENV_DIR%. Creating it."
	echo Creating Python virtual environment at %VENV_DIR% ...
	"%UV_EXE%" venv --python 3.11 "%VENV_DIR%"
	if errorlevel 1 goto fail
	call :Log "Python virtual environment created."

	call :Log "Running scripts\install-env.bat."
	echo Installing Python environment...
	call scripts\install-env.bat
	if errorlevel 1 goto fail
	call :Log "scripts\install-env.bat completed successfully."
)

if exist "%VENV_PY%" call :Log "Python environment is available."

if not exist "%VENV_PY%" (
	call :Log "Python environment was not created."
	echo ERROR: Python environment was not created.
	goto fail
)

echo Python environment is ready. Launching client.py (first run may need one or more --continue commands while the model downloads).

if /i "!USER_PROMPT!"=="--continue" (
	call :Log "Launching scripts\client.py --continue."
	"%VENV_PY%" scripts\client.py --continue
) else (
	call :Log "Launching scripts\client.py -i \"!USER_PROMPT!\" !REST_ARGS!"
	"%VENV_PY%" scripts\client.py -i "!USER_PROMPT!" !REST_ARGS!
)
set "EXIT_CODE=!ERRORLEVEL!"
call :Log "scripts\client.py exited with code %EXIT_CODE%"
popd >nul
exit /b %EXIT_CODE%

:fail
set "EXIT_CODE=%ERRORLEVEL%"
if "%EXIT_CODE%"=="0" set "EXIT_CODE=1"
call :Log "Failure path reached with exit code %EXIT_CODE%"
popd >nul
exit /b %EXIT_CODE%

:EnsureUv
call :Log "Checking for local UV at %UV_EXE%"
if exist "%UV_EXE%" exit /b 0

call :Log "Local UV was not found. Running scripts\install-uv.bat."
echo Local UV was not found. Running scripts\install-uv.bat...
call scripts\install-uv.bat
if errorlevel 1 exit /b 1

if not exist "%UV_EXE%" (
	call :Log "UV installation reported success, but uv.exe is still missing."
	echo ERROR: UV was installed, but "%UV_EXE%" is still missing.
	exit /b 1
)

call :Log "Local UV is available."
exit /b 0

:InitLog
set "LOG_DIR=%USERPROFILE%\.openvino\log"
if not exist "%LOG_DIR%\" mkdir "%LOG_DIR%" >nul 2>nul

for /f "usebackq delims=" %%I in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Date -Format 'yyyyMMdd-HHmmss'"`) do set "LOG_TIMESTAMP=%%I"
if not defined LOG_TIMESTAMP set "LOG_TIMESTAMP=unknown"

set "LOG_FILE=%LOG_DIR%\tts-client-%LOG_TIMESTAMP%.log"
>> "%LOG_FILE%" echo [%DATE% %TIME%] Log initialized.
exit /b 0

:Log
>> "%LOG_FILE%" echo [%DATE% %TIME%] %~1
exit /b 0
