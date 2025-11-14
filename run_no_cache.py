"""
Run Flask app with NO CACHE and correct configuration
"""
import os
import sys

# FORCE production mode (no reloader, no cache)
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# Clear any cached modules
modules_to_clear = ['app', 'config', 'database', 'ai_service', 'whatsapp_service', 'command_processor', 'models']
for module in modules_to_clear:
    if module in sys.modules:
        del sys.modules[module]

print("="*60)
print("  STARTING APP - NO CACHE MODE")
print("="*60)
print()

# Verify configuration BEFORE importing app
from dotenv import load_dotenv
load_dotenv()

project_id = os.getenv('FIREBASE_PROJECT_ID')
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

print(f"✅ Configuration:")
print(f"   Project ID: {project_id}")
print(f"   Credentials: {creds_path}")
print()

if project_id != 'kiranabuddy-55330':
    print(f"❌ ERROR: Wrong project!")
    print(f"   Expected: kiranabuddy-55330")
    print(f"   Got: {project_id}")
    sys.exit(1)

# Verify credentials file
if not os.path.exists(creds_path):
    print(f"❌ ERROR: Credentials file not found!")
    print(f"   Path: {creds_path}")
    sys.exit(1)

import json
with open(creds_path) as f:
    creds = json.load(f)
    if creds.get('project_id') != 'kiranabuddy-55330':
        print(f"❌ ERROR: Credentials file has wrong project!")
        print(f"   Expected: kiranabuddy-55330")
        print(f"   Got: {creds.get('project_id')}")
        sys.exit(1)

print("✅ All checks passed!")
print()

# NOW import and run app
print("🚀 Starting Flask app...")
print()

from app import app

port = int(os.getenv("PORT", 5000))

print("="*60)
print(f"  SERVER RUNNING - NO CACHE MODE")
print("="*60)
print()
print(f"📍 URL: http://localhost:{port}")
print(f"📍 Test: http://localhost:{port}/test")
print(f"📍 Project: {project_id}")
print()
print("⚠️  Debug mode: OFF (no reloader)")
print("⚠️  This prevents caching issues")
print()
print("Press CTRL+C to stop")
print("="*60)
print()

# Run WITHOUT reloader
app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

