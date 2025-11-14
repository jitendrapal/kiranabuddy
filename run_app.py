"""
Simple script to run the Flask app
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the app
from app import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Starting Kirana Shop Management App on port {port}...")
    print(f"📍 Server will be available at: http://localhost:{port}")
    print(f"📍 Health check: http://localhost:{port}/")
    print(f"📍 Webhook: http://localhost:{port}/webhook")
    print("\nPress CTRL+C to stop the server\n")
    app.run(host="0.0.0.0", port=port, debug=True)

