"""
Test "rice ka stock dikhao" command with real database
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from database import FirestoreDB
from ai_service import AIService
from command_processor import CommandProcessor
from config import Config

def test_rice_stock_check():
    """Test 'rice ka stock dikhao' command"""

    print("=" * 80)
    print("Testing 'rice ka stock dikhao' Command")
    print("=" * 80)

    # Initialize services
    db = FirestoreDB()
    ai_service = AIService(Config.OPENAI_API_KEY)
    processor = CommandProcessor(db, ai_service, whatsapp_service=None)
    
    # Use the test shop
    shop_id = "test_shop_001"
    
    print(f"\n📍 Using shop_id: {shop_id}\n")
    
    # Step 1: Check what rice products exist
    print("Step 1: Finding all rice products in database...")
    rice_products = db.find_all_matching_products(shop_id, "rice", min_matches=1)
    
    if rice_products:
        print(f"✅ Found {len(rice_products)} rice products:")
        for i, p in enumerate(rice_products, 1):
            print(f"   {i}. {p.name} - Stock: {p.current_stock} {p.unit or 'pieces'}")
    else:
        print("❌ No rice products found!")
        print("\nLet me search for all products containing 'rice'...")
        all_products = db.get_all_products(shop_id)
        rice_like = [p for p in all_products if 'rice' in p.name.lower()]
        if rice_like:
            print(f"Found {len(rice_like)} products with 'rice' in name:")
            for p in rice_like:
                print(f"   - {p.name}")
        else:
            print("No products with 'rice' in name found.")
    
    print("\n" + "=" * 80)
    
    # Step 2: Parse the command
    print("\nStep 2: Parsing command 'rice ka stock dikhao'...")
    parsed = ai_service.parse_command("rice ka stock dikhao")
    
    print(f"   Action: {parsed.action.value}")
    print(f"   Product: '{parsed.product_name}'")
    print(f"   Confidence: {parsed.confidence:.2f}")
    
    print("\n" + "=" * 80)
    
    # Step 3: Process the command
    print("\nStep 3: Processing command through CommandProcessor...")
    result = processor.process_message("rice ka stock dikhao", shop_id=shop_id)
    
    print(f"\n📋 Result:")
    print(f"   Success: {result.get('success', False)}")
    print(f"\n💬 Message:")
    print(result.get('message', 'No message'))
    
    print("\n" + "=" * 80)
    
    # Step 4: Test variations
    print("\nStep 4: Testing variations...")
    
    variations = [
        "rice kitna hai",
        "rice dikhao",
        "rice ki quantity batao",
    ]
    
    for cmd in variations:
        print(f"\n🧪 Testing: '{cmd}'")
        parsed = ai_service.parse_command(cmd)
        print(f"   → Action: {parsed.action.value}, Product: '{parsed.product_name}'")
    
    print("\n" + "=" * 80)
    print("✅ Test Complete!")
    print("=" * 80)


if __name__ == "__main__":
    test_rice_stock_check()

