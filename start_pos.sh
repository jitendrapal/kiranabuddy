#!/bin/bash
# KiranaBuddy POS Auto-Start Script for Linux/Mac
# This script starts the Flask app and opens it in browser

echo "========================================"
echo "  KiranaBuddy POS System Starting..."
echo "========================================"
echo ""

# Change to the directory where this script is located
cd "$(dirname "$0")"

echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3"
    exit 1
fi
echo "Python found: $(python3 --version)"
echo ""

echo "[2/4] Activating virtual environment (if exists)..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
else
    echo "No virtual environment found, using system Python"
fi
echo ""

echo "[3/4] Starting Flask server..."
echo "Server will run on http://localhost:5000"
echo ""
echo "To stop the server, press Ctrl+C"
echo "========================================"
echo ""

# Start Flask app in background
python3 app.py &
SERVER_PID=$!

# Wait 5 seconds for server to start
sleep 5

echo "[4/4] Opening browser..."

# Detect OS and open browser
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5000
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser --kiosk http://localhost:5000 &
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:5000
fi

echo ""
echo "========================================"
echo "  POS System is now running!"
echo "  Browser should open automatically"
echo "  Server PID: $SERVER_PID"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"

# Wait for server process
wait $SERVER_PID

