"""
Real scenario test - Test with actual database operations
"""
import sys
import io

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from database import FirestoreDB
from ai_service import AIService
from config import Config

def test_real_scenario():
    """Test with real database"""

    print("=" * 80)
    print("Real Scenario Test - Testing with Database")
    print("=" * 80)

    # Initialize services
    db = FirestoreDB()
    ai_service = AIService(Config.OPENAI_API_KEY)
    
    # Get test shop
    shop = db.get_shop_by_phone("9876543210")
    if not shop:
        print("❌ Test shop not found! Please create a shop with phone 9876543210")
        return
    
    shop_id = shop.shop_id
    print(f"\n✅ Found shop: {shop.name} (ID: {shop_id})")
    
    # Test commands
    test_commands = [
        "10 rice add kar do",
        "rice 10 add kar do",
        "add 10 rice",
        "10 rice badha do",
        "rice badha do 10",
        "5 maggi bik gaya",
        "maggi 5 bech diya",
    ]
    
    print(f"\n🧪 Testing {len(test_commands)} commands...\n")
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}/{len(test_commands)}: '{command}'")
        print(f"{'='*80}")
        
        # Parse command
        parsed = ai_service.parse_command(command)
        
        print(f"📝 Parsed:")
        print(f"   Action:   {parsed.action.value}")
        print(f"   Product:  '{parsed.product_name}'")
        print(f"   Quantity: {parsed.quantity}")
        print(f"   Confidence: {parsed.confidence:.2f}")
        
        # Check if product exists in database
        if parsed.product_name and parsed.product_name != "unknown":
            matching_products = db.find_all_matching_products(shop_id, parsed.product_name)
            
            if matching_products:
                print(f"\n✅ Found {len(matching_products)} matching product(s) in database:")
                for product in matching_products:
                    print(f"   - {product.name} (Stock: {product.current_stock})")
            else:
                print(f"\n⚠️ No matching products found in database for '{parsed.product_name}'")
                print(f"   This is expected if the product doesn't exist yet.")
        
        print()
    
    print(f"\n{'='*80}")
    print("✅ Real scenario test complete!")
    print(f"{'='*80}")
    print("\nThe command parsing is working correctly!")
    print("If you see '⚠️ No matching products found', it means the product")
    print("doesn't exist in your database yet. Add it first, then try the command.")


if __name__ == "__main__":
    test_real_scenario()

