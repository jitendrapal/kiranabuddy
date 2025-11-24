"""
Setup script for OTP verification
Helps configure SMS provider and test OTP functionality
"""
import os
from dotenv import load_dotenv, set_key

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def setup_development_mode():
    """Setup development mode with console OTP"""
    print_header("🔧 Setting Up Development Mode")
    
    env_file = '.env'
    
    # Check if .env exists
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("# OTP Configuration\n")
    
    # Set development mode
    set_key(env_file, 'OTP_DEV_MODE', 'true')
    set_key(env_file, 'SMS_PROVIDER', 'console')
    
    print("✅ Development mode configured!")
    print("\n📋 Configuration:")
    print("   OTP_DEV_MODE=true")
    print("   SMS_PROVIDER=console")
    print("\n🔑 Hardcoded OTP: 123456")
    print("\n💡 OTP will be printed to console when requested")

def setup_msg91():
    """Setup MSG91 SMS provider"""
    print_header("📱 Setting Up MSG91 (India)")
    
    print("To use MSG91, you need:")
    print("1. MSG91 account (https://msg91.com/)")
    print("2. Auth Key from dashboard")
    print("3. DLT Template ID")
    print()
    
    auth_key = input("Enter MSG91 Auth Key (or press Enter to skip): ").strip()
    
    if not auth_key:
        print("⏭️  Skipped MSG91 setup")
        return
    
    template_id = input("Enter MSG91 Template ID: ").strip()
    sender_id = input("Enter Sender ID (default: KIRANA): ").strip() or "KIRANA"
    
    env_file = '.env'
    
    set_key(env_file, 'OTP_DEV_MODE', 'false')
    set_key(env_file, 'SMS_PROVIDER', 'msg91')
    set_key(env_file, 'MSG91_AUTH_KEY', auth_key)
    set_key(env_file, 'MSG91_TEMPLATE_ID', template_id)
    set_key(env_file, 'MSG91_SENDER_ID', sender_id)
    
    print("\n✅ MSG91 configured!")
    print("\n📋 Configuration:")
    print(f"   SMS_PROVIDER=msg91")
    print(f"   MSG91_AUTH_KEY={auth_key[:10]}...")
    print(f"   MSG91_TEMPLATE_ID={template_id}")
    print(f"   MSG91_SENDER_ID={sender_id}")
    print("\n💰 Cost: ₹0.20 per SMS")

def setup_twilio():
    """Setup Twilio SMS provider"""
    print_header("🌍 Setting Up Twilio (Global)")
    
    print("To use Twilio, you need:")
    print("1. Twilio account (https://www.twilio.com/)")
    print("2. Account SID")
    print("3. Auth Token")
    print("4. Twilio Phone Number")
    print()
    
    account_sid = input("Enter Twilio Account SID (or press Enter to skip): ").strip()
    
    if not account_sid:
        print("⏭️  Skipped Twilio setup")
        return
    
    auth_token = input("Enter Twilio Auth Token: ").strip()
    phone_number = input("Enter Twilio Phone Number (e.g., +1234567890): ").strip()
    
    env_file = '.env'
    
    set_key(env_file, 'OTP_DEV_MODE', 'false')
    set_key(env_file, 'SMS_PROVIDER', 'twilio')
    set_key(env_file, 'TWILIO_ACCOUNT_SID', account_sid)
    set_key(env_file, 'TWILIO_AUTH_TOKEN', auth_token)
    set_key(env_file, 'TWILIO_PHONE_NUMBER', phone_number)
    
    print("\n✅ Twilio configured!")
    print("\n📋 Configuration:")
    print(f"   SMS_PROVIDER=twilio")
    print(f"   TWILIO_ACCOUNT_SID={account_sid[:10]}...")
    print(f"   TWILIO_PHONE_NUMBER={phone_number}")
    print("\n💰 Cost: ₹1.00 per SMS")

def setup_fast2sms():
    """Setup Fast2SMS provider"""
    print_header("⚡ Setting Up Fast2SMS (India)")
    
    print("To use Fast2SMS, you need:")
    print("1. Fast2SMS account (https://www.fast2sms.com/)")
    print("2. API Key from dashboard")
    print()
    
    api_key = input("Enter Fast2SMS API Key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⏭️  Skipped Fast2SMS setup")
        return
    
    env_file = '.env'
    
    set_key(env_file, 'OTP_DEV_MODE', 'false')
    set_key(env_file, 'SMS_PROVIDER', 'fast2sms')
    set_key(env_file, 'FAST2SMS_API_KEY', api_key)
    
    print("\n✅ Fast2SMS configured!")
    print("\n📋 Configuration:")
    print(f"   SMS_PROVIDER=fast2sms")
    print(f"   FAST2SMS_API_KEY={api_key[:10]}...")
    print("\n💰 Cost: ₹0.15 per SMS")

def test_otp_service():
    """Test OTP service"""
    print_header("🧪 Testing OTP Service")
    
    try:
        from database import FirestoreDB
        from otp_service import OTPService
        from config import Config
        
        # Initialize database
        db = FirestoreDB(
            credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
            project_id=Config.FIREBASE_PROJECT_ID
        )
        
        # Initialize OTP service
        otp_service = OTPService(db.db)
        
        print(f"✅ OTP Service initialized")
        print(f"   Provider: {otp_service.sms_provider}")
        print(f"   Dev Mode: {otp_service.dev_mode}")
        print(f"   OTP Length: {otp_service.otp_length}")
        print(f"   Validity: {otp_service.otp_validity_minutes} minutes")
        print(f"   Max Attempts: {otp_service.max_attempts}")
        
        # Test OTP generation
        test_otp = otp_service.generate_otp()
        print(f"\n🔑 Generated OTP: {test_otp}")
        
        print("\n✅ OTP service is working!")
        
    except Exception as e:
        print(f"\n❌ Error testing OTP service: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main setup function"""
    print_header("🎯 OTP Verification Setup")
    
    print("Choose setup option:")
    print("1. Development Mode (Console OTP - Recommended for testing)")
    print("2. MSG91 (India - ₹0.20/SMS)")
    print("3. Twilio (Global - ₹1.00/SMS)")
    print("4. Fast2SMS (India - ₹0.15/SMS)")
    print("5. Test OTP Service")
    print("6. Exit")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == '1':
        setup_development_mode()
    elif choice == '2':
        setup_msg91()
    elif choice == '3':
        setup_twilio()
    elif choice == '4':
        setup_fast2sms()
    elif choice == '5':
        test_otp_service()
    elif choice == '6':
        print("\n👋 Goodbye!")
        return
    else:
        print("\n❌ Invalid choice!")
        return
    
    print("\n" + "="*60)
    print("✅ Setup complete!")
    print("="*60)
    print("\n📝 Next steps:")
    print("1. Restart your Flask app")
    print("2. Visit http://localhost:5000/login")
    print("3. Test OTP login")
    print()

if __name__ == '__main__':
    main()

