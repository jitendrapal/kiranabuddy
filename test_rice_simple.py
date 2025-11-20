"""
Simple test for rice stock check
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

def test_rice():
    """Test rice product matching"""
    
    print("=" * 80)
    print("Testing Rice Product Matching")
    print("=" * 80)
    
    db = FirestoreDB()
    
    # Get user's shop_id (using phone number from earlier tests)
    # You mentioned you're using phone: 1234567890
    user = db.get_user_by_phone("1234567890")
    
    if not user:
        print("❌ User not found! Please provide your phone number.")
        print("\nTrying to find any shop with rice products...")
        
        # Try to find shops
        shops_ref = db.db.collection('shops')
        shops = list(shops_ref.limit(5).stream())
        
        if shops:
            print(f"\nFound {len(shops)} shops. Testing with first shop...")
            shop_id = shops[0].id
        else:
            print("❌ No shops found!")
            return
    else:
        shop_id = user.shop_id
        print(f"✅ Found user! Shop ID: {shop_id}")
    
    print(f"\n📍 Using shop_id: {shop_id}\n")
    
    # Test 1: Find rice products
    print("Test 1: Finding rice products...")
    rice_products = db.find_all_matching_products(shop_id, "rice", min_matches=1)
    
    if rice_products:
        print(f"✅ Found {len(rice_products)} rice products:")
        for i, p in enumerate(rice_products, 1):
            print(f"   {i}. {p.name}")
            print(f"      Stock: {p.current_stock} {p.unit or 'pieces'}")
            print(f"      Normalized: {p.normalized_name}")
    else:
        print("❌ No rice products found!")
    
    print("\n" + "=" * 80)
    
    # Test 2: Parse command
    print("\nTest 2: Parsing 'rice ka stock dikhao'...")
    ai_service = AIService(Config.OPENAI_API_KEY)
    parsed = ai_service.parse_command("rice ka stock dikhao")
    
    print(f"   Action: {parsed.action.value}")
    print(f"   Product: '{parsed.product_name}'")
    print(f"   Confidence: {parsed.confidence:.2f}")
    
    print("\n" + "=" * 80)
    
    # Test 3: Search again with parsed product name
    print(f"\nTest 3: Searching for '{parsed.product_name}'...")
    products = db.find_all_matching_products(shop_id, parsed.product_name, min_matches=1)
    
    if products:
        print(f"✅ Found {len(products)} products:")
        for p in products:
            print(f"   - {p.name} (Stock: {p.current_stock})")
    else:
        print("❌ No products found!")
    
    print("\n" + "=" * 80)
    print("✅ Test Complete!")
    print("=" * 80)


if __name__ == "__main__":
    test_rice()

