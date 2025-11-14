"""
Check what configuration is being loaded
"""
import os
from dotenv import load_dotenv

print("="*60)
print("  CHECKING CONFIGURATION")
print("="*60)
print()

# Load .env
print("📂 Loading .env file...")
load_dotenv()
print("✅ .env loaded")
print()

# Check environment variables
print("🔍 Environment Variables:")
print(f"   FIREBASE_PROJECT_ID: {os.getenv('FIREBASE_PROJECT_ID')}")
print(f"   GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
print()

# Check if credentials file exists
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if creds_path and os.path.exists(creds_path):
    print(f"✅ Credentials file exists: {creds_path}")
    
    # Read the project ID from the file
    import json
    with open(creds_path, 'r') as f:
        creds_data = json.load(f)
        print(f"   Project ID in file: {creds_data.get('project_id')}")
else:
    print(f"❌ Credentials file NOT found: {creds_path}")

print()

# Now check what Config class loads
print("🔧 Checking Config class...")
from config import Config

print(f"   Config.FIREBASE_PROJECT_ID: {Config.FIREBASE_PROJECT_ID}")
print(f"   Config.GOOGLE_APPLICATION_CREDENTIALS: {Config.GOOGLE_APPLICATION_CREDENTIALS}")
print()

# Check if they match
env_project = os.getenv('FIREBASE_PROJECT_ID')
config_project = Config.FIREBASE_PROJECT_ID

if env_project == config_project:
    print(f"✅ Config matches .env: {config_project}")
else:
    print(f"❌ MISMATCH!")
    print(f"   .env says: {env_project}")
    print(f"   Config says: {config_project}")

print()
print("="*60)

