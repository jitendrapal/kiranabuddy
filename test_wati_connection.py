"""
Test WATI connection and API credentials
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_wati_connection():
    """Test if WATI credentials are working"""
    
    print("="*60)
    print("  TESTING WATI CONNECTION")
    print("="*60)
    print()
    
    # Get credentials from .env
    api_key = os.getenv('WATI_API_KEY')
    base_url = os.getenv('WATI_BASE_URL')
    
    print("📋 Configuration:")
    print(f"   API Key: {api_key[:20]}..." if api_key and len(api_key) > 20 else f"   API Key: {api_key}")
    print(f"   Base URL: {base_url}")
    print()
    
    # Check if credentials are set
    if not api_key or api_key == 'your-wati-api-key' or api_key == 'your-wati-api-key-here':
        print("❌ ERROR: WATI_API_KEY not set!")
        print()
        print("💡 How to fix:")
        print("   1. Login to https://app.wati.io")
        print("   2. Go to Settings → API Access")
        print("   3. Copy your API key")
        print("   4. Update .env file:")
        print("      WATI_API_KEY=your-actual-api-key")
        print()
        return False
    
    if not base_url or base_url == 'https://live-server.wati.io':
        print("⚠️  WARNING: Using default base URL")
        print("   Make sure this matches your WATI region!")
        print()
    
    # Test API connection
    print("🔍 Testing API connection...")
    print()
    
    try:
        # Test endpoint: Get account info
        url = f"{base_url}/api/v1/getAccountDetails"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        print(f"   Calling: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! WATI connection working!")
            print()
            
            data = response.json()
            print("📊 Account Details:")
            
            if 'phoneNumber' in data:
                print(f"   WhatsApp Number: {data['phoneNumber']}")
            if 'businessName' in data:
                print(f"   Business Name: {data['businessName']}")
            if 'accountStatus' in data:
                print(f"   Account Status: {data['accountStatus']}")
            
            print()
            print("🎉 Your WATI integration is ready to use!")
            return True
            
        elif response.status_code == 401:
            print("❌ AUTHENTICATION FAILED!")
            print()
            print("   Your API key is invalid or expired.")
            print()
            print("💡 How to fix:")
            print("   1. Login to https://app.wati.io")
            print("   2. Go to Settings → API Access")
            print("   3. Generate a new API key")
            print("   4. Update .env file with new key")
            return False
            
        elif response.status_code == 404:
            print("❌ ENDPOINT NOT FOUND!")
            print()
            print("   Your base URL might be wrong.")
            print()
            print("💡 Try these base URLs:")
            print("   India: https://live-server.wati.io")
            print("   USA: https://live-us-server.wati.io")
            print("   Europe: https://live-eu-server.wati.io")
            return False
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print()
        print("   Cannot connect to WATI server.")
        print()
        print("💡 Check:")
        print("   1. Internet connection")
        print("   2. Base URL is correct")
        print("   3. Firewall settings")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wati_connection()
    
    print()
    print("="*60)
    
    if success:
        print("  ✅ WATI SETUP COMPLETE!")
        print("="*60)
        print()
        print("Next steps:")
        print("1. Setup webhook to receive messages")
        print("2. Test sending a message")
        print("3. Run: python test_wati_send_message.py")
    else:
        print("  ❌ WATI SETUP INCOMPLETE")
        print("="*60)
        print()
        print("Please fix the errors above and try again.")
    
    print()

