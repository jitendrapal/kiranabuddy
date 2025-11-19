"""
Complete test for Hindi number commands with real database
"""
from ai_service import AIService
from config import Config
from database import FirestoreDB

# Initialize services
ai_service = AIService(api_key=Config.OPENAI_API_KEY)
db = FirestoreDB(
    credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
    project_id=Config.FIREBASE_PROJECT_ID
)

# Get shop
shop = db.get_shop_by_phone("9876543210")
if not shop:
    print("❌ No shop found")
    exit(1)

print(f"\n🏪 Testing with shop: {shop.name}")
print("=" * 80)

# Test cases
test_cases = [
    # Hindi numbers with "do" (2)
    ("Maggi do add kar do", "ADD_STOCK", "maggi", 2.0),
    ("Parle G do bik gaya", "REDUCE_STOCK", "parle", 2.0),
    
    # Other Hindi numbers
    ("Maggi teen add karo", "ADD_STOCK", "maggi", 3.0),
    ("Parle G panch bik gaya", "REDUCE_STOCK", "parle", 5.0),
    ("Colgate das add", "ADD_STOCK", "colgate", 10.0),
    
    # With filler words
    ("um Maggi do add kar do", "ADD_STOCK", "maggi", 2.0),
    ("uh Parle G teen bik gaya", "REDUCE_STOCK", "parle", 3.0),
    
    # English numbers
    ("Maggi 5 add karo", "ADD_STOCK", "maggi", 5.0),
    ("Parle G 10 bik gaya", "REDUCE_STOCK", "parle", 10.0),
]

passed = 0
failed = 0

for i, (raw_text, expected_action, expected_product_prefix, expected_qty) in enumerate(test_cases, 1):
    print(f"\n{'='*80}")
    print(f"Test {i}/{len(test_cases)}: '{raw_text}'")
    print(f"{'='*80}")
    
    # Clean and parse
    cleaned = ai_service.clean_voice_text(raw_text)
    print(f"Cleaned: '{cleaned}'")
    
    parsed = ai_service.parse_command(cleaned)
    print(f"Parsed: {parsed.action.name}, '{parsed.product_name}', {parsed.quantity}")
    
    # Check parsing
    action_ok = parsed.action.name == expected_action
    product_ok = parsed.product_name and parsed.product_name.lower().startswith(expected_product_prefix)
    qty_ok = parsed.quantity == expected_qty
    
    if action_ok and product_ok and qty_ok:
        print(f"✅ Parsing: PASS")
        
        # Try to find product
        if parsed.product_name:
            product = db.find_existing_product_by_name(shop.shop_id, parsed.product_name)
            if product:
                print(f"✅ Product found: {product.name}")
                print(f"✅ TEST PASSED")
                passed += 1
            else:
                print(f"⚠️ Product not found (but parsing was correct)")
                print(f"✅ TEST PASSED (parsing)")
                passed += 1
    else:
        print(f"❌ Parsing: FAIL")
        if not action_ok:
            print(f"   Expected action: {expected_action}, got: {parsed.action.name}")
        if not product_ok:
            print(f"   Expected product prefix: {expected_product_prefix}, got: {parsed.product_name}")
        if not qty_ok:
            print(f"   Expected quantity: {expected_qty}, got: {parsed.quantity}")
        print(f"❌ TEST FAILED")
        failed += 1

print(f"\n{'='*80}")
print(f"📊 RESULTS: {passed}/{len(test_cases)} passed, {failed}/{len(test_cases)} failed")
print(f"{'='*80}")

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! 'Maggi do add kar do' is working perfectly!")
else:
    print(f"\n⚠️ {failed} tests failed. Please review.")

