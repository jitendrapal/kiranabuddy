"""
Quick test script for Fast2SMS OTP integration
"""
import os
from dotenv import load_dotenv
from database import FirestoreDB
from otp_service import OTPService
from config import Config

# Load environment variables
load_dotenv()

def test_fast2sms_setup():
    """Test Fast2SMS configuration"""
    print("\n" + "="*60)
    print("  🧪 Testing Fast2SMS OTP Setup")
    print("="*60 + "\n")
    
    # Check environment variables
    print("📋 Checking Configuration:")
    print(f"   OTP_DEV_MODE: {os.getenv('OTP_DEV_MODE')}")
    print(f"   SMS_PROVIDER: {os.getenv('SMS_PROVIDER')}")
    
    api_key = os.getenv('FAST2SMS_API_KEY', '')
    if api_key:
        print(f"   FAST2SMS_API_KEY: {api_key[:10]}...{api_key[-4:]} ✅")
    else:
        print(f"   FAST2SMS_API_KEY: Not configured ❌")
        return
    
    print()
    
    # Initialize database
    try:
        print("🔧 Initializing Database...")
        db = FirestoreDB(
            credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
            project_id=Config.FIREBASE_PROJECT_ID
        )
        print("✅ Database connected\n")
    except Exception as e:
        print(f"❌ Database error: {e}\n")
        return
    
    # Initialize OTP service
    try:
        print("📱 Initializing OTP Service...")
        otp_service = OTPService(db.db)
        print(f"✅ OTP Service initialized")
        print(f"   Provider: {otp_service.sms_provider}")
        print(f"   Dev Mode: {otp_service.dev_mode}")
        print(f"   API Key: {otp_service.fast2sms_api_key[:10]}...{otp_service.fast2sms_api_key[-4:]}")
        print()
    except Exception as e:
        print(f"❌ OTP Service error: {e}\n")
        return
    
    # Test OTP generation
    print("🔑 Testing OTP Generation...")
    test_otp = otp_service.generate_otp()
    print(f"✅ Generated OTP: {test_otp}")
    print()
    
    # Ask user if they want to send a test SMS
    print("="*60)
    print("⚠️  WARNING: This will send a REAL SMS and consume credits!")
    print("="*60)
    test_phone = input("\nEnter your phone number to test (or press Enter to skip): ").strip()
    
    if not test_phone:
        print("\n⏭️  Skipped SMS test")
        print("\n✅ Configuration is correct!")
        print("\n📝 Next steps:")
        print("1. Start your Flask app: python app.py")
        print("2. Visit: http://localhost:5000/login")
        print("3. Enter your phone number")
        print("4. You'll receive a REAL SMS with OTP!")
        return
    
    # Clean phone number
    test_phone = test_phone.replace(' ', '').replace('-', '')
    if not test_phone.startswith('+'):
        if test_phone.startswith('91'):
            test_phone = '+' + test_phone
        else:
            test_phone = '+91' + test_phone
    
    print(f"\n📱 Sending test OTP to: {test_phone}")
    print("⏳ Please wait...")
    
    # Create OTP
    try:
        result = otp_service.create_otp(test_phone)
        
        if not result['success']:
            print(f"\n❌ Failed to create OTP: {result['message']}")
            return
        
        otp = result['otp']
        otp_code = result['otp_code']
        
        print(f"✅ OTP created: {otp_code}")
        print(f"   OTP ID: {otp.otp_id}")
        print(f"   Expires in: {otp_service.otp_validity_minutes} minutes")
        print()
        
        # Send SMS
        print("📤 Sending SMS via Fast2SMS...")
        send_result = otp_service.send_otp(test_phone, otp_code)
        
        if send_result['success']:
            print(f"\n✅ SUCCESS! SMS sent to {test_phone}")
            print(f"   Provider: {send_result['provider']}")
            print(f"   Message: {send_result['message']}")
            print(f"\n📱 Check your phone for OTP: {otp_code}")
            print()
            
            # Test verification
            verify_input = input("Enter the OTP you received to verify (or press Enter to skip): ").strip()
            
            if verify_input:
                verify_result = otp_service.verify_otp(test_phone, verify_input)
                
                if verify_result['success']:
                    print("\n✅ OTP VERIFIED SUCCESSFULLY! 🎉")
                    print("\n🎊 Your Fast2SMS integration is working perfectly!")
                else:
                    print(f"\n❌ Verification failed: {verify_result['message']}")
            else:
                print("\n⏭️  Skipped verification test")
        else:
            print(f"\n❌ Failed to send SMS: {send_result['message']}")
            print("\n🔍 Troubleshooting:")
            print("1. Check if your Fast2SMS API key is correct")
            print("2. Check if you have sufficient credits")
            print("3. Visit Fast2SMS dashboard: https://www.fast2sms.com/")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60)

if __name__ == '__main__':
    test_fast2sms_setup()

