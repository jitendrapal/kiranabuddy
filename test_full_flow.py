"""
Test the full flow step by step to find the error
"""
from database import FirestoreDB
from ai_service import AIService
from whatsapp_service import WhatsAppService
from command_processor import CommandProcessor
from config import Config
from dotenv import load_dotenv

load_dotenv()

def test_full_flow():
    """Test each step of the flow"""
    
    print("="*60)
    print("  TESTING FULL FLOW")
    print("="*60)
    
    try:
        # Step 1: Initialize services
        print("\n1️⃣ Initializing services...")
        
        db = FirestoreDB(
            credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
            project_id=Config.FIREBASE_PROJECT_ID
        )
        print("   ✅ Database initialized")
        
        ai_service = AIService(
            api_key=Config.OPENAI_API_KEY,
            model=Config.OPENAI_MODEL
        )
        print("   ✅ AI Service initialized")
        
        # Determine WhatsApp provider
        whatsapp_provider = "wati" if Config.WATI_API_KEY else "whatsapp_cloud"
        
        if whatsapp_provider == "wati":
            whatsapp_service = WhatsAppService(
                provider="wati",
                api_key=Config.WATI_API_KEY,
                base_url=Config.WATI_BASE_URL
            )
        else:
            whatsapp_service = WhatsAppService(
                provider="whatsapp_cloud",
                access_token=Config.WHATSAPP_ACCESS_TOKEN,
                phone_number_id=Config.WHATSAPP_PHONE_NUMBER_ID
            )
        print(f"   ✅ WhatsApp Service initialized ({whatsapp_provider})")
        
        command_processor = CommandProcessor(
            db=db,
            ai_service=ai_service,
            whatsapp_service=whatsapp_service
        )
        print("   ✅ Command Processor initialized")
        
        # Step 2: Test user lookup
        print("\n2️⃣ Testing user lookup...")
        from_phone = "+919876543210"
        user = db.get_user_by_phone(from_phone)
        
        if user:
            print(f"   ✅ User found: {user.name}")
            print(f"   Shop ID: {user.shop_id}")
        else:
            print(f"   ❌ User not found!")
            return
        
        # Step 3: Test AI parsing
        print("\n3️⃣ Testing AI command parsing...")
        test_message = "Add 10 Maggi"
        parsed = ai_service.parse_command(test_message)
        
        print(f"   Message: '{test_message}'")
        print(f"   Action: {parsed.action.value}")
        print(f"   Product: {parsed.product_name}")
        print(f"   Quantity: {parsed.quantity}")
        print(f"   Valid: {parsed.is_valid()}")
        
        if not parsed.is_valid():
            print("   ❌ Command not valid!")
            return
        
        print("   ✅ Command parsed successfully")
        
        # Step 4: Test command processing
        print("\n4️⃣ Testing command processing...")
        result = command_processor.process_message(
            from_phone=from_phone,
            message_type="text",
            text=test_message
        )
        
        print(f"   Success: {result.get('success')}")
        print(f"   Message: {result.get('message')}")
        
        if result.get('result'):
            res = result['result']
            print(f"   Product: {res.get('product_name')}")
            print(f"   Quantity: {res.get('quantity')}")
            print(f"   New Stock: {res.get('new_stock')}")
        
        if result.get('success'):
            print("\n   ✅ Command processed successfully!")
        else:
            print("\n   ❌ Command processing failed!")
            
        # Step 5: Verify in database
        print("\n5️⃣ Verifying in database...")
        products = db.get_products_by_shop(user.shop_id)
        
        print(f"   Total products: {len(products)}")
        for product in products:
            if product.name.lower() == "maggi":
                print(f"   📦 Maggi stock: {product.current_stock} {product.unit}")
        
        print("\n" + "="*60)
        print("  TEST COMPLETE!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_flow()

