@echo off
setlocal EnableExtensions

call :InitLog
call :Log "client.bat started with arguments: %*"

if "%~1"=="" (
	call :Log "No audio path argument provided."
	echo Usage: scripts\client.bat "<audio_or_video_path^|glob^|list>" [language]
	echo        Example: scripts\client.bat "C:\audio\*.wav" [language]
	echo        Example: scripts\client.bat "C:\audio\1.wav;C:\audio\2.wav" [language]
	echo        scripts\client.bat --continue
	exit /b 1
)

if /i "%~1"=="--continue" (
	echo Resuming pending ASR request ...
) else (
	echo Received audio input: %~1
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

echo Intel AIPC platform detected. Continuing ...

set "AUDIO_PATH=%~1"
set "LANGUAGE=%~2"
if not defined LANGUAGE set "LANGUAGE=auto"

pushd "%~dp0.." >nul
if errorlevel 1 (
	call :Log "Failed to change working directory to %~dp0.."
	exit /b 1
)
call :Log "Changed working directory to %CD%"

for %%D in ("%~dp0..\bin") do set "UV_EXE=%%~fD\uv.exe"
call :Log "Resolved UV_EXE=%UV_EXE%"

set "VENV_DIR=%USERPROFILE%\.openvino\venv\asr"
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

echo Python environment is ready. Launching client.py ^(supports single files, globs, and semicolon-separated lists; first run downloads the Qwen3-ASR model, ~2 GB; the call may exit early with --continue^).

if /i "%AUDIO_PATH%"=="--continue" (
	call :Log "Launching scripts\client.py --continue."
	"%VENV_PY%" scripts\client.py --continue --log "%LOG_FILE%"
) else (
	call :Log "Launching scripts\client.py --audio ""%AUDIO_PATH%"" --language %LANGUAGE%."
	"%VENV_PY%" scripts\client.py --audio "%AUDIO_PATH%" --language "%LANGUAGE%" --log "%LOG_FILE%"
)
set "EXIT_CODE=%ERRORLEVEL%"
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

set "LOG_FILE=%LOG_DIR%\asr-client-%LOG_TIMESTAMP%.log"
>> "%LOG_FILE%" echo [%DATE% %TIME%] Log initialized.
exit /b 0

:Log
>> "%LOG_FILE%" echo [%DATE% %TIME%] %~1
exit /b 0
