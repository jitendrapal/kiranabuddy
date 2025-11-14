@echo off
echo ============================================================
echo   CLEARING CACHE AND STARTING FRESH
echo ============================================================
echo.

echo 1. Clearing Python cache...
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo    Cleared __pycache__
)

if exist .pytest_cache (
    rmdir /s /q .pytest_cache
    echo    Cleared .pytest_cache
)

for /d %%i in (*.pyc) do del /q %%i
echo    Cleared .pyc files
echo.

echo 2. Checking configuration...
python check_config.py
echo.

echo 3. Starting app...
echo ============================================================
echo.
python app.py

