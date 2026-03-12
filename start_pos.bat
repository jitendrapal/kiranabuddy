@echo off
REM KiranaBuddy POS Auto-Start Script for Windows
REM This script starts the Flask app and opens it in browser

echo ========================================
echo   KiranaBuddy POS System Starting...
echo ========================================
echo.

REM Change to the directory where this script is located
cd /d "%~dp0"

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/4] Activating virtual environment (if exists)...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found, using system Python
)
echo.

echo [3/4] Starting Flask server...
echo Server will run on http://localhost:5000
echo.
echo To stop the server, close this window or press Ctrl+C
echo ========================================
echo.

REM Start Flask app in background
start /B python app.py

REM Wait 5 seconds for server to start
timeout /t 5 /nobreak >nul

echo [4/4] Opening browser...
start http://localhost:5000

echo.
echo ========================================
echo   POS System is now running!
echo   Browser should open automatically
echo   Keep this window open
echo ========================================
echo.

REM Keep the window open
pause

