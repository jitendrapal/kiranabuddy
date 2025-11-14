"""
Start the app with debug mode and better error messages
"""
import os
import sys

print("="*60)
print("  STARTING KIRANA SHOP MANAGEMENT APP")
print("="*60)
print()

# Check environment
print("🔍 Checking environment...")
from dotenv import load_dotenv
load_dotenv()

required_vars = ['OPENAI_API_KEY', 'FIREBASE_PROJECT_ID', 'GOOGLE_APPLICATION_CREDENTIALS']
missing = []

for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"   ✅ {var}: Set")
    else:
        print(f"   ❌ {var}: NOT SET")
        missing.append(var)

if missing:
    print(f"\n❌ Missing environment variables: {', '.join(missing)}")
    print("Please check your .env file")
    sys.exit(1)

print()

# Try to import and start app
print("📦 Loading application...")

try:
    from app import app
    print("   ✅ App imported successfully")
    print()
    
    port = int(os.getenv("PORT", 5000))
    
    print("="*60)
    print(f"🚀 Starting server on port {port}...")
    print("="*60)
    print()
    print(f"📍 Server: http://localhost:{port}")
    print(f"📍 Test Interface: http://localhost:{port}/test")
    print(f"📍 Health Check: http://localhost:{port}/")
    print()
    print("Press CTRL+C to stop")
    print("="*60)
    print()
    
    app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)
    
except Exception as e:
    print(f"\n❌ ERROR starting app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

