@echo off
REM KiranaBuddy POS - Full Kiosk Mode for Windows
REM This script starts the app and opens browser in full-screen kiosk mode

echo ========================================
echo   KiranaBuddy POS - Kiosk Mode
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/3] Starting Flask server...
start /B python app.py

echo [2/3] Waiting for server to start...
timeout /t 8 /nobreak >nul

echo [3/3] Opening browser in kiosk mode...
echo.
echo Press Alt+F4 to exit kiosk mode
echo ========================================
echo.

REM Try Chrome first, then Edge, then default browser
where chrome >nul 2>&1
if %errorlevel% equ 0 (
    start chrome --kiosk --app=http://localhost:5000 --disable-pinch --overscroll-history-navigation=0
    goto :end
)

where msedge >nul 2>&1
if %errorlevel% equ 0 (
    start msedge --kiosk --app=http://localhost:5000
    goto :end
)

REM Fallback to default browser
start http://localhost:5000

:end
echo Kiosk mode started!
REM Keep server running
pause

