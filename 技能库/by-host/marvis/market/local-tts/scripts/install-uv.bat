@echo off
setlocal EnableExtensions

for %%D in ("%~dp0..\bin") do (
	set "SKILL_BIN=%%~fD"
	set "UV_EXE=%%~fD\uv.exe"
)

echo Checking UV installation...

call :EnsureUv
if errorlevel 1 goto fail

echo.
echo UV is available:
"%UV_EXE%" --version
if errorlevel 1 goto fail

echo.
echo Done. Scripts will use the local copy at "%UV_EXE%".
exit /b 0

:fail
set "EXIT_CODE=%ERRORLEVEL%"
if "%EXIT_CODE%"=="0" set "EXIT_CODE=1"
echo.
echo ERROR: Failed to install or verify UV.
exit /b %EXIT_CODE%

:EnsureUv
if exist "%UV_EXE%" exit /b 0

echo UV was not found at "%UV_EXE%". Checking PATH before downloading it...
call :InstallUv
if errorlevel 1 exit /b 1

if not exist "%UV_EXE%" (
	echo ERROR: UV was downloaded, but "%UV_EXE%" is missing.
	exit /b 1
)

exit /b 0

:InstallUv
if not exist "%SKILL_BIN%\" mkdir "%SKILL_BIN%"
if errorlevel 1 (
	echo ERROR: Failed to create "%SKILL_BIN%".
	exit /b 1
)

if exist "%UV_EXE%" del "%UV_EXE%" >nul 2>nul

call :CopyUvFromPath "%UV_EXE%"
set "COPY_RESULT=%ERRORLEVEL%"
if "%COPY_RESULT%"=="0" exit /b 0
if not "%COPY_RESULT%"=="2" (
	echo ERROR: Failed to reuse uv.exe from PATH.
	exit /b %COPY_RESULT%
)

echo Downloading UV to "%UV_EXE%"...
call :DownloadUv "%UV_EXE%"
if errorlevel 1 (
	if exist "%UV_EXE%" del "%UV_EXE%" >nul 2>nul
	echo ERROR: Failed to download uv.exe.
	exit /b 1
)

if not exist "%UV_EXE%" (
	echo ERROR: uv.exe was downloaded, but the file is missing.
	exit /b 1
)

exit /b 0

:CopyUvFromPath
set "TARGET_UV=%~1"
set "PATH_UV="
for /f "delims=" %%I in ('where uv.exe 2^>nul') do if not defined PATH_UV set "PATH_UV=%%~fI"

if not defined PATH_UV exit /b 2

echo Found uv.exe on PATH at "%PATH_UV%". Copying it to "%TARGET_UV%"...
copy /y "%PATH_UV%" "%TARGET_UV%" >nul
if errorlevel 1 (
	echo ERROR: Failed to copy "%PATH_UV%" to "%TARGET_UV%".
	exit /b 1
)

if not exist "%TARGET_UV%" (
	echo ERROR: Copied uv.exe is missing at "%TARGET_UV%".
	exit /b 1
)

exit /b 0

:DownloadUv
set "UV_EXE=%~1"
where curl.exe >nul 2>nul
if not errorlevel 1 (
	curl.exe -fL --ssl-no-revoke -o "%UV_EXE%" "https://gitcode.com/gcw_ggDjjkY3/kjfile/releases/download/download/uv.exe"
	if not errorlevel 1 exit /b 0
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing -Uri 'https://gitcode.com/gcw_ggDjjkY3/kjfile/releases/download/download/uv.exe' -OutFile $env:UV_EXE"
exit /b %ERRORLEVEL%
