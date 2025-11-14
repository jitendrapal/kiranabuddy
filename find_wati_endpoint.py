"""
Find the correct WATI endpoint and base URL
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_wati_endpoints():
    """Test different WATI endpoints to find the correct one"""
    
    print("="*60)
    print("  FINDING CORRECT WATI ENDPOINT")
    print("="*60)
    print()
    
    api_key = os.getenv('WATI_API_KEY')
    
    if not api_key:
        print("❌ No API key found in .env")
        return
    
    print(f"API Key: {api_key[:30]}...")
    print()
    
    # Different base URLs to try
    base_urls = [
        "https://live-eu-server.wati.io",
        "https://eu-app-api.wati.io",
        "https://live-server.wati.io",
        "https://live-us-server.wati.io",
        "https://app-server.wati.io",
    ]
    
    # Different endpoints to try
    endpoints = [
        "/api/v1/getAccountDetails",
        "/api/v1/getContacts",
        "/api/v1/getMessages",
        "/api/v2/getAccountDetails",
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Testing different combinations...\n")
    
    for base_url in base_urls:
        print(f"📍 Testing: {base_url}")
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            
            try:
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    print(f"   ✅ SUCCESS: {endpoint}")
                    print(f"      Status: {response.status_code}")
                    print(f"      Response: {response.json()}")
                    print()
                    print("="*60)
                    print(f"  ✅ FOUND WORKING ENDPOINT!")
                    print("="*60)
                    print()
                    print(f"Base URL: {base_url}")
                    print(f"Endpoint: {endpoint}")
                    print()
                    print("Update your .env file:")
                    print(f"WATI_BASE_URL={base_url}")
                    return
                    
                elif response.status_code == 401:
                    print(f"   🔑 Auth Error: {endpoint} (API key might be invalid)")
                    
                elif response.status_code == 404:
                    print(f"   ❌ Not Found: {endpoint}")
                    
                else:
                    print(f"   ⚠️  {response.status_code}: {endpoint}")
                    
            except requests.exceptions.Timeout:
                print(f"   ⏱️  Timeout: {endpoint}")
            except requests.exceptions.ConnectionError:
                print(f"   🔌 Connection Error: {endpoint}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print()
    
    print("="*60)
    print("  ❌ NO WORKING ENDPOINT FOUND")
    print("="*60)
    print()
    print("💡 Suggestions:")
    print("1. Check if your WATI trial is active")
    print("2. Login to WATI dashboard and check API docs")
    print("3. Contact WATI support for correct endpoint")

if __name__ == "__main__":
    test_wati_endpoints()

