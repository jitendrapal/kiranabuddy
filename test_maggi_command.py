"""
Test script to debug "Maggi do add kar do" command
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

# Test the complete flow
print("=" * 80)
print("🧪 Testing: 'Maggi do add kar do' command")
print("=" * 80)

# Step 1: Voice cleaning
raw_text = "Maggi do add kar do"
print(f"\n1️⃣ Raw text: '{raw_text}'")

cleaned_text = ai_service.clean_voice_text(raw_text)
print(f"2️⃣ Cleaned text: '{cleaned_text}'")

# Step 2: Command parsing
parsed = ai_service.parse_command(cleaned_text)
print(f"\n3️⃣ Parsed command:")
print(f"   Action: {parsed.action}")
print(f"   Product: {parsed.product_name}")
print(f"   Quantity: {parsed.quantity}")
print(f"   Confidence: {parsed.confidence}")

# Step 3: Check if product exists
shop_id = "shop_9876543210_0"  # Your shop ID
print(f"\n4️⃣ Looking for product in shop: {shop_id}")

if parsed.product_name:
    product = db.find_existing_product_by_name(shop_id, parsed.product_name)
    
    if product:
        print(f"   ✅ Product found: {product.name}")
        print(f"   Current stock: {product.current_stock} {product.unit}")
    else:
        print(f"   ❌ Product NOT found: '{parsed.product_name}'")
        print(f"\n   Let me check what products you have...")
        
        # List first 10 products
        products = db.get_products_by_shop(shop_id)
        print(f"\n   Total products in shop: {len(products)}")
        print(f"\n   First 10 products:")
        for i, p in enumerate(products[:10], 1):
            print(f"   {i}. {p.name} (normalized: {p.normalized_name})")
else:
    print(f"   ⚠️ No product name parsed!")

print("\n" + "=" * 80)

