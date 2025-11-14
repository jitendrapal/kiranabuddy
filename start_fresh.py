"""
Start app with fresh configuration - no cache
"""
import sys
import os
import shutil

print("="*60)
print("  STARTING FRESH - CLEARING ALL CACHE")
print("="*60)
print()

# Step 1: Clear Python cache
print("1️⃣ Clearing Python cache...")
cache_dirs = ['__pycache__', '.pytest_cache']
for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print(f"   ✅ Removed {cache_dir}")

# Remove .pyc files
import glob
for pyc_file in glob.glob('**/*.pyc', recursive=True):
    os.remove(pyc_file)
    print(f"   ✅ Removed {pyc_file}")

print()

# Step 2: Verify configuration
print("2️⃣ Verifying configuration...")
from dotenv import load_dotenv
load_dotenv()

project_id = os.getenv('FIREBASE_PROJECT_ID')
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

print(f"   Project ID: {project_id}")
print(f"   Credentials: {creds_path}")

if project_id != "kiranabuddy-55330":
    print(f"\n   ❌ ERROR: Wrong project ID!")
    print(f"   Expected: kiranabuddy-55330")
    print(f"   Got: {project_id}")
    sys.exit(1)

print("   ✅ Configuration correct!")
print()

# Step 3: Import and start app
print("3️⃣ Starting Flask app...")
print()

# Force reload of all modules
if 'app' in sys.modules:
    del sys.modules['app']
if 'config' in sys.modules:
    del sys.modules['config']
if 'database' in sys.modules:
    del sys.modules['database']

from app import app

port = int(os.getenv("PORT", 5000))

print("="*60)
print(f"🚀 SERVER STARTING")
print("="*60)
print(f"\n📍 URL: http://localhost:{port}")
print(f"📍 Test: http://localhost:{port}/test")
print(f"📍 Project: {project_id}")
print(f"\nPress CTRL+C to stop\n")
print("="*60)
print()

app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)

