"""
Debug Firebase connection to find where kirana-ce28f is coming from
"""
import os
import sys
from dotenv import load_dotenv

print("="*60)
print("  DEBUGGING FIREBASE CONNECTION")
print("="*60)
print()

# Load environment
load_dotenv()

# Check ALL environment variables related to Google/Firebase
print("🔍 Checking ALL Google/Firebase environment variables:")
print()

env_vars = [
    'GOOGLE_APPLICATION_CREDENTIALS',
    'GOOGLE_CLOUD_PROJECT',
    'GCLOUD_PROJECT',
    'GCP_PROJECT',
    'FIREBASE_PROJECT_ID',
    'FIRESTORE_EMULATOR_HOST'
]

for var in env_vars:
    value = os.getenv(var)
    if value:
        print(f"   {var}: {value}")
    else:
        print(f"   {var}: (not set)")

print()

# Check the credentials file
print("📄 Checking credentials file:")
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
print(f"   Path: {creds_path}")

if creds_path and os.path.exists(creds_path):
    import json
    with open(creds_path, 'r') as f:
        creds = json.load(f)
        print(f"   ✅ File exists")
        print(f"   Project in file: {creds.get('project_id')}")
else:
    print(f"   ❌ File not found!")

print()

# Now try to initialize Firestore and see what happens
print("🔥 Attempting to initialize Firestore...")
print()

try:
    from google.cloud import firestore
    from google.oauth2 import service_account
    
    project_id = os.getenv('FIREBASE_PROJECT_ID')
    print(f"   Using project_id: {project_id}")
    
    credentials = service_account.Credentials.from_service_account_file(creds_path)
    print(f"   ✅ Credentials loaded")
    
    # Check what project the credentials think they're for
    print(f"   Credentials project_id: {credentials.project_id}")
    
    # Try to create client
    print(f"\n   Creating Firestore client with project: {project_id}")
    db = firestore.Client(credentials=credentials, project=project_id)
    
    print(f"   ✅ Client created")
    print(f"   Client project: {db.project}")
    
    # Try a simple operation
    print(f"\n   Testing database access...")
    test_ref = db.collection('test').document('test')
    test_ref.set({'test': 'value'})
    
    print(f"   ✅ Write successful!")
    
    # Clean up
    test_ref.delete()
    print(f"   ✅ Test document deleted")
    
    print()
    print("="*60)
    print("  ✅ FIREBASE CONNECTION SUCCESSFUL!")
    print(f"  📍 Connected to: {db.project}")
    print("="*60)
    
except Exception as e:
    print(f"\n   ❌ ERROR: {e}")
    print()
    
    # Check if error mentions kirana-ce28f
    error_str = str(e)
    if 'kirana-ce28f' in error_str:
        print("   🔍 ERROR MENTIONS: kirana-ce28f")
        print()
        print("   Possible causes:")
        print("   1. Credentials file has wrong project")
        print("   2. Environment variable GOOGLE_CLOUD_PROJECT is set")
        print("   3. gcloud CLI has default project set")
        print()
        
        # Check gcloud config
        print("   Checking gcloud config...")
        import subprocess
        try:
            result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                gcloud_project = result.stdout.strip()
                print(f"   gcloud default project: {gcloud_project}")
                if gcloud_project == 'kirana-ce28f':
                    print("   ⚠️  FOUND IT! gcloud is set to kirana-ce28f")
                    print()
                    print("   FIX: Run this command:")
                    print("   gcloud config set project kiranabuddy-55330")
        except:
            print("   (gcloud not installed or not in PATH)")
    
    import traceback
    print("\n   Full traceback:")
    traceback.print_exc()

