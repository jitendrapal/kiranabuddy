"""
Test total sales feature
"""
from database import FirestoreDB
from ai_service import AIService
from command_processor import CommandProcessor
from whatsapp_service import WhatsAppService
from config import Config
from dotenv import load_dotenv

load_dotenv()

def test_total_sales():
    """Test the total sales feature"""
    
    print("="*60)
    print("  TESTING TOTAL SALES FEATURE")
    print("="*60)
    print()
    
    # Initialize services
    db = FirestoreDB(
        credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
        project_id=Config.FIREBASE_PROJECT_ID
    )
    
    ai_service = AIService(api_key=Config.OPENAI_API_KEY)
    
    whatsapp_service = WhatsAppService(
        provider="wati",
        api_key=Config.WATI_API_KEY,
        base_url=Config.WATI_BASE_URL
    )
    
    command_processor = CommandProcessor(
        db=db,
        ai_service=ai_service,
        whatsapp_service=whatsapp_service
    )
    
    # Test queries
    test_queries = [
        "Aaj ka total sale kitna hai?",
        "What's today's total sales?",
        "Aaj kitna bika?",
        "Today's sales batao",
        "Aaj ka business kaisa raha?",
        "Total sale today",
        "Kitna maal becha aaj?"
    ]
    
    print("Testing various total sales queries:\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. Query: '{query}'")
        
        # Parse the command
        parsed = ai_service.parse_command(query)
        
        print(f"   Parsed action: {parsed.action.value}")
        print(f"   Confidence: {parsed.confidence:.2f}")
        
        if parsed.action.value == 'total_sales':
            print(f"   ✅ Correctly identified as total_sales!")
        else:
            print(f"   ❌ Incorrectly identified as {parsed.action.value}")
        
        print()
    
    # Now test actual execution
    print("="*60)
    print("  TESTING ACTUAL EXECUTION")
    print("="*60)
    print()
    
    shop_id = "8e70a29d-acda-423e-a27b-9b9c870616a7"  # From setup
    from_phone = "+919876543210"
    
    # First, make some sales
    print("1. Making some test sales...")
    
    sales = [
        "Sold 5 Maggi",
        "Customer ne 2 oil liya",
        "Bech diya 3 biscuit"
    ]
    
    for sale in sales:
        print(f"   Processing: {sale}")
        result = command_processor.process_message(
            from_phone=from_phone,
            message_type="text",
            text=sale
        )
        if result.get('success'):
            print(f"   ✅ {result.get('message')}")
        else:
            print(f"   ❌ Failed: {result.get('message')}")
    
    print()
    
    # Now check total sales
    print("2. Checking total sales...")
    result = command_processor.process_message(
        from_phone=from_phone,
        message_type="text",
        text="Aaj ka total sale kitna hai?"
    )
    
    if result.get('success'):
        print(f"\n✅ SUCCESS!\n")
        print(result.get('message'))
    else:
        print(f"\n❌ FAILED!")
        print(result.get('message'))
    
    print()
    print("="*60)
    print("  TEST COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    test_total_sales()

