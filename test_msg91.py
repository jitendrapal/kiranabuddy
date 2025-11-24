"""
Quick test script for MSG91 OTP integration
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_msg91_api():
    """Test MSG91 API directly"""
    print("\n" + "="*60)
    print("  🧪 Testing MSG91 API")
    print("="*60 + "\n")
    
    auth_key = os.getenv('MSG91_AUTH_KEY', '')
    
    if not auth_key:
        print("❌ MSG91_AUTH_KEY not found in .env")
        return
    
    print(f"📋 Auth Key: {auth_key[:10]}...{auth_key[-4:]}")
    
    # Test phone number
    test_phone = input("\nEnter phone number to test (10 digits, e.g., 9876543210): ").strip()
    
    if not test_phone:
        print("❌ No phone number provided")
        return
    
    # Clean phone number
    test_phone = test_phone.replace('+91', '').replace('+', '').replace(' ', '').replace('-', '')
    
    if len(test_phone) != 10:
        print(f"❌ Invalid phone number. Must be 10 digits. Got: {test_phone}")
        return
    
    print(f"\n📱 Testing with phone: {test_phone}")
    
    # Generate test OTP
    test_otp = "123456"
    
    print(f"🔑 Test OTP: {test_otp}")
    print("\n⏳ Sending SMS via MSG91...")
    
    # Try simple sendotp API (works without template)
    try:
        url = f"https://api.msg91.com/api/sendotp.php"
        
        params = {
            "authkey": auth_key,
            "mobile": test_phone,
            "otp": test_otp,
            "message": f"Your OTP is {test_otp}. Valid for 5 minutes. Do not share with anyone."
        }
        
        print(f"\n📤 Request URL: {url}")
        print(f"📤 Params: mobile={test_phone}, otp={test_otp}")
        
        response = requests.get(url, params=params)
        
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"📥 Response Body: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            
            if response_data.get('type') == 'success':
                print("\n✅ SUCCESS! SMS sent via MSG91")
                print(f"   Message: {response_data.get('message')}")
                print(f"\n📱 Check phone {test_phone} for OTP: {test_otp}")
            else:
                print(f"\n❌ Failed: {response_data.get('message')}")
                print("\n🔍 Possible issues:")
                print("1. Invalid auth key")
                print("2. No credits in account")
                print("3. Account not verified")
                print("4. DLT registration required (India)")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60)
    
    print("\n📝 Next Steps:")
    print("1. If SMS was sent successfully, your MSG91 is configured!")
    print("2. Restart Flask app: python app.py")
    print("3. Test login at: http://localhost:5000/login")
    print("4. You'll receive REAL SMS with OTP")

if __name__ == '__main__':
    test_msg91_api()

