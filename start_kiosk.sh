#!/bin/bash
# KiranaBuddy POS - Full Kiosk Mode for Linux
# This script starts the app and opens browser in full-screen kiosk mode

echo "========================================"
echo "  KiranaBuddy POS - Kiosk Mode"
echo "========================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

echo "[1/4] Starting Flask server..."
# Activate virtual environment if exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Start Flask in background
python3 app.py &
SERVER_PID=$!
echo "Server started (PID: $SERVER_PID)"

echo "[2/4] Waiting for server to start..."
sleep 8

echo "[3/4] Hiding mouse cursor..."
# Hide mouse cursor (install: sudo apt install unclutter)
if command -v unclutter &> /dev/null; then
    unclutter -idle 0.1 -root &
fi

echo "[4/4] Opening browser in kiosk mode..."
echo ""
echo "Press Alt+F4 or Ctrl+W to exit kiosk mode"
echo "========================================"
echo ""

# Disable screen blanking
if command -v xset &> /dev/null; then
    xset s off
    xset -dpms
    xset s noblank
fi

# Try Chromium first, then Firefox, then default
if command -v chromium-browser &> /dev/null; then
    chromium-browser \
        --kiosk \
        --app=http://localhost:5000 \
        --disable-pinch \
        --overscroll-history-navigation=0 \
        --disable-features=TranslateUI \
        --noerrdialogs \
        --disable-infobars \
        --check-for-update-interval=31536000
elif command -v firefox &> /dev/null; then
    firefox --kiosk http://localhost:5000
else
    xdg-open http://localhost:5000
fi

# When browser closes, kill server
kill $SERVER_PID

