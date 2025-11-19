"""
Check shops and products for phone 9876543210
"""
from database import FirestoreDB

# Initialize database
db = FirestoreDB("firbasekey.json", "kiranabuddy-55330")

# Get shop for this phone
phone = "9876543210"
shop = db.get_shop_by_phone(phone)

if shop:
    print(f"\n🏪 Shop: {shop.name}")
    print(f"   ID: {shop.shop_id}")
    print("=" * 80)

    # Get products for this shop
    products = db.get_products_by_shop(shop.shop_id)
    print(f"\n   Total Products: {len(products)}")

    if len(products) > 0:
        print(f"\n   First 10 products:")
        for i, p in enumerate(products[:10], 1):
            print(f"   {i}. {p.name} (Stock: {p.current_stock} {p.unit})")
    else:
        print("\n   ⚠️ No products found in this shop!")
        print("\n   You need to add products first:")
        print("   1. Go to http://127.0.0.1:5000/stock_management")
        print("   2. Click 'Add New Product'")
        print("   3. Add products like Maggi, Parle G, etc.")
else:
    print(f"\n❌ No shop found for phone {phone}")

print("\n" + "=" * 80)

