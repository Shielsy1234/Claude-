@echo off
setlocal EnableExtensions
title Daydream launcher
rem ------------------------------------------------------------------
rem  Daydream one-click start: starts Ollama and ComfyUI with the right
rem  settings, waits until they're ready, then opens the Daydream app.
rem  Change these if yours are different:
set "APP_URL=https://shielsy1234.github.io/Claude-/"
set "COMFY_PORT=8000"
set "OLLAMA_PORT=11434"
rem ------------------------------------------------------------------
set "HOME_DIR=%LOCALAPPDATA%\Daydream"
set "ORIGIN=https://shielsy1234.github.io"

echo.
echo   Daydream - starting your AI...
echo.

rem First run: keep a copy of this launcher and make Desktop + Start menu shortcuts.
if /i not "%~dp0"=="%HOME_DIR%\" call :install

rem ---------- Ollama (chat AI) ----------
reg query "HKCU\Environment" /v OLLAMA_ORIGINS >nul 2>&1 || (
  setx OLLAMA_ORIGINS "*" >nul
  echo   [ok] Allowed Daydream to talk to Ollama ^(one-time setting^).
)
set "OLLAMA_ORIGINS=*"
set "OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"
call :olcode
if "%OLCODE%"=="403" (
  echo   [..] Ollama is running with old settings - restarting it...
  taskkill /f /im "ollama app.exe" >nul 2>&1
  taskkill /f /im ollama.exe >nul 2>&1
  timeout /t 2 /nobreak >nul
  set "OLCODE=000"
)
if "%OLCODE%"=="200" (
  echo   [ok] Ollama is already running.
) else (
  if exist "%OLLAMA_EXE%" (
    echo   [..] Starting Ollama...
    start "" "%OLLAMA_EXE%"
    call :waitollama
  ) else (
    echo   [--] Ollama isn't installed ^(skip this if you don't use it^). Get it from https://ollama.com/download
  )
)

rem ---------- ComfyUI (images and video) ----------
call :comfyup
if defined COMFY_OK (
  echo   [ok] ComfyUI is already running on port %COMFY_PORT%.
) else (
  call :findcomfy
)
if not defined COMFY_OK if defined COMFY_EXE (
  echo   [..] Starting ComfyUI ^(the first start can take a minute^)...
  start "" "%COMFY_EXE%"
  call :waitcomfy
)
if not defined COMFY_OK if not defined COMFY_EXE echo   [--] Couldn't find ComfyUI Desktop. Start it yourself, or edit COMFY_EXE handling at the top of this file.

rem ---------- open the app ----------
echo   [..] Opening Daydream...
start "" msedge --app="%APP_URL%"
echo.
echo   Daydream is ready. You can close this window; everything keeps running.
echo   Or press S to shut down ComfyUI and Ollama ^(frees your graphics card^).
echo.
choice /c SX /n /m "  Press S to shut down, or X to close this window: "
if errorlevel 2 exit /b 0
echo   Shutting down...
taskkill /f /im "ollama app.exe" >nul 2>&1
taskkill /f /im ollama.exe >nul 2>&1
taskkill /f /t /im ComfyUI.exe >nul 2>&1
echo   Done.
timeout /t 2 /nobreak >nul
exit /b 0

rem ================= helpers =================
:olcode
set "OLCODE=000"
for /f %%c in ('curl -s -o nul -m 3 -w "%%{http_code}" -H "Origin: %ORIGIN%" http://127.0.0.1:%OLLAMA_PORT%/api/tags') do set "OLCODE=%%c"
exit /b 0

:waitollama
for /l %%i in (1,1,30) do (
  call :olcode
  call :olready && (echo   [ok] Ollama is ready. & exit /b 0)
  timeout /t 1 /nobreak >nul
)
echo   [!!] Ollama didn't answer. Open it from the Start menu, then try again.
exit /b 1
:olready
if "%OLCODE%"=="200" exit /b 0
exit /b 1

:comfyup
set "COMFY_OK="
curl -s -f -o nul -m 3 http://127.0.0.1:%COMFY_PORT%/system_stats && set "COMFY_OK=1" && exit /b 0
curl -s -f -o nul -m 3 http://127.0.0.1:8188/system_stats && set "COMFY_OK=1" && set "COMFY_PORT=8188"
exit /b 0

:waitcomfy
for /l %%i in (1,1,120) do (
  call :comfyup
  if defined COMFY_OK (echo   [ok] ComfyUI is ready on port %COMFY_PORT%. & exit /b 0)
  timeout /t 2 /nobreak >nul
)
echo   [!!] ComfyUI is taking a long time. Daydream will open anyway; press Check in the Video tab once ComfyUI has finished starting.
exit /b 1

:findcomfy
set "COMFY_EXE="
for %%p in ("%LOCALAPPDATA%\Programs\ComfyUI\ComfyUI.exe" "%LOCALAPPDATA%\Programs\@comfyorgcomfyui-electron\ComfyUI.exe" "%LOCALAPPDATA%\Programs\comfyui-electron\ComfyUI.exe" "%ProgramFiles%\ComfyUI\ComfyUI.exe") do (
  if not defined COMFY_EXE if exist "%%~p" set "COMFY_EXE=%%~p"
)
if not defined COMFY_EXE for /r "%APPDATA%\Microsoft\Windows\Start Menu\Programs" %%f in (ComfyUI*.lnk) do if not defined COMFY_EXE set "COMFY_EXE=%%f"
if not defined COMFY_EXE for /r "%ProgramData%\Microsoft\Windows\Start Menu\Programs" %%f in (ComfyUI*.lnk) do if not defined COMFY_EXE set "COMFY_EXE=%%f"
exit /b 0

:install
mkdir "%HOME_DIR%" 2>nul
copy /y "%~f0" "%HOME_DIR%\Start-Daydream.cmd" >nul
curl -s -f -o "%HOME_DIR%\daydream.ico" "%APP_URL%icons/daydream.ico"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; foreach($d in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))){ $s=$w.CreateShortcut((Join-Path $d 'Daydream.lnk')); $s.TargetPath=(Join-Path $env:LOCALAPPDATA 'Daydream\Start-Daydream.cmd'); $s.WorkingDirectory=(Join-Path $env:LOCALAPPDATA 'Daydream'); $s.IconLocation=(Join-Path $env:LOCALAPPDATA 'Daydream\daydream.ico'); $s.WindowStyle=1; $s.Description='Start Daydream'; $s.Save() }"
echo   [ok] Added a Daydream shortcut to your desktop and Start menu. Use that from now on.
exit /b 0
