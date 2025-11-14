"""
Test script to verify setup and configuration
"""
import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are set"""
    print("🔍 Testing Environment Configuration...\n")
    
    load_dotenv()
    
    required_vars = [
        'OPENAI_API_KEY',
        'FIREBASE_PROJECT_ID'
    ]
    
    optional_vars = [
        'WATI_API_KEY',
        'WHATSAPP_ACCESS_TOKEN',
        'GOOGLE_APPLICATION_CREDENTIALS'
    ]
    
    all_good = True
    
    print("Required Variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {'*' * 10} (set)")
        else:
            print(f"  ❌ {var}: NOT SET")
            all_good = False
    
    print("\nOptional Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {'*' * 10} (set)")
        else:
            print(f"  ⚠️  {var}: not set")
    
    # Check WhatsApp provider
    has_wati = os.getenv('WATI_API_KEY')
    has_whatsapp = os.getenv('WHATSAPP_ACCESS_TOKEN')
    
    print("\nWhatsApp Provider:")
    if has_wati:
        print("  ✅ WATI configured")
    elif has_whatsapp:
        print("  ✅ WhatsApp Cloud API configured")
    else:
        print("  ❌ No WhatsApp provider configured")
        all_good = False
    
    return all_good


def test_imports():
    """Test if all required packages are installed"""
    print("\n🔍 Testing Package Imports...\n")
    
    packages = [
        ('flask', 'Flask'),
        ('openai', 'OpenAI'),
        ('google.cloud.firestore', 'Firestore'),
        ('requests', 'Requests'),
        ('dotenv', 'python-dotenv')
    ]
    
    all_good = True
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            all_good = False
    
    return all_good


def test_openai_connection():
    """Test OpenAI API connection"""
    print("\n🔍 Testing OpenAI Connection...\n")
    
    try:
        from openai import OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("  ❌ OPENAI_API_KEY not set")
            return False
        
        client = OpenAI(api_key=api_key)
        
        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=5
        )
        
        print("  ✅ OpenAI API connection successful")
        print(f"  ✅ Model: gpt-4o-mini")
        return True
        
    except Exception as e:
        print(f"  ❌ OpenAI connection failed: {e}")
        return False


def test_firebase_connection():
    """Test Firebase connection"""
    print("\n🔍 Testing Firebase Connection...\n")
    
    try:
        from google.cloud import firestore
        from google.oauth2 import service_account
        
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        project_id = os.getenv('FIREBASE_PROJECT_ID')
        
        if not project_id:
            print("  ❌ FIREBASE_PROJECT_ID not set")
            return False
        
        if creds_path and os.path.exists(creds_path):
            credentials = service_account.Credentials.from_service_account_file(creds_path)
            db = firestore.Client(credentials=credentials, project=project_id)
            print(f"  ✅ Firebase connected with service account")
        else:
            db = firestore.Client(project=project_id)
            print(f"  ✅ Firebase connected with default credentials")
        
        print(f"  ✅ Project ID: {project_id}")
        return True
        
    except Exception as e:
        print(f"  ❌ Firebase connection failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("  KIRANA SHOP MANAGEMENT - SETUP TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Environment", test_environment()))
    results.append(("Imports", test_imports()))
    results.append(("OpenAI", test_openai_connection()))
    results.append(("Firebase", test_firebase_connection()))
    
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("  🎉 ALL TESTS PASSED! You're ready to go!")
    else:
        print("  ⚠️  Some tests failed. Please fix the issues above.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

