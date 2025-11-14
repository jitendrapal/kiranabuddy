"""
Test Firebase write operations
"""
from google.cloud import firestore
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def test_firebase_write():
    """Test if we can write to Firebase"""
    
    print("="*60)
    print("  TESTING FIREBASE WRITE")
    print("="*60)
    print()
    
    try:
        # Get credentials
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        project_id = os.getenv('FIREBASE_PROJECT_ID')
        
        print(f"📍 Project ID: {project_id}")
        print(f"📄 Credentials: {creds_path}")
        print()
        
        # Check if file exists
        if not os.path.exists(creds_path):
            print(f"❌ Credentials file not found: {creds_path}")
            return False
        
        print("✅ Credentials file found")
        print()
        
        # Initialize Firestore
        print("📡 Connecting to Firestore...")
        credentials = service_account.Credentials.from_service_account_file(creds_path)
        db = firestore.Client(credentials=credentials, project=project_id)
        print("✅ Connected to Firestore!")
        print()
        
        # Try to write a test document
        print("📝 Writing test document...")
        test_data = {
            'test_field': 'Hello from Kirana App!',
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'testing'
        }
        
        doc_ref = db.collection('test_collection').document('test_doc')
        doc_ref.set(test_data)
        print("✅ Test document written!")
        print()
        
        # Try to read it back
        print("📖 Reading test document...")
        doc = doc_ref.get()
        
        if doc.exists:
            print("✅ Test document read successfully!")
            print(f"   Data: {doc.to_dict()}")
            print()
            
            # Delete test document
            print("🗑️  Deleting test document...")
            doc_ref.delete()
            print("✅ Test document deleted!")
            print()
            
            print("="*60)
            print("  ✅ FIREBASE WRITE TEST PASSED!")
            print("="*60)
            print()
            print("Firebase is working correctly!")
            print("You can now create real data.")
            print()
            return True
        else:
            print("❌ Could not read test document")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_existing_data():
    """Check if there's any existing data"""
    
    print("="*60)
    print("  CHECKING EXISTING DATA")
    print("="*60)
    print()
    
    try:
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        project_id = os.getenv('FIREBASE_PROJECT_ID')
        
        credentials = service_account.Credentials.from_service_account_file(creds_path)
        db = firestore.Client(credentials=credentials, project=project_id)
        
        collections = ['shops', 'users', 'products', 'transactions']
        
        for collection_name in collections:
            print(f"📁 Checking '{collection_name}' collection...")
            docs = list(db.collection(collection_name).limit(5).stream())
            
            if docs:
                print(f"   ✅ Found {len(docs)} document(s)")
                for doc in docs:
                    print(f"      - {doc.id}")
            else:
                print(f"   ⚠️  No documents found")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🔥 FIREBASE DIAGNOSTIC TEST\n")
    
    # Test 1: Check if we can write
    if test_firebase_write():
        print("\n" + "="*60)
        print()
        
        # Test 2: Check existing data
        check_existing_data()
        
        print("="*60)
        print()
        print("Next steps:")
        print("1. If test passed, run: python setup_first_shop.py")
        print("2. Then check Firebase Console")
        print("3. Refresh the page to see collections")
        print()
    else:
        print("\n❌ Firebase write test failed!")
        print()
        print("Possible issues:")
        print("1. Firestore database not created in Firebase Console")
        print("2. Security rules blocking writes")
        print("3. Service account doesn't have permissions")
        print()
        print("Solutions:")
        print("1. Go to: https://console.firebase.google.com/project/kirana-ce28f/firestore")
        print("2. Create Firestore database if not exists")
        print("3. Update security rules to allow writes")
        print()

