"""
Fix duplicate shops issue - Delete empty shops and keep the one with products
"""
from database import FirestoreDB

# Initialize database
db = FirestoreDB(
    credentials_path='firbasekey.json',
    project_id='kiranabuddy-55330'
)

phone = "9876543210"

print("="*60)
print(f"🔧 Fixing duplicate shops for phone: {phone}")
print("="*60)

# Get all shops for this owner
all_shops = list(db.db.collection('shops').where('owner_phone', '==', phone).stream())

print(f"\n📊 Found {len(all_shops)} shop(s)")

shops_with_products = []
empty_shops = []

for shop_doc in all_shops:
    shop_data = shop_doc.to_dict()
    shop_id = shop_data.get('shop_id')
    shop_name = shop_data.get('name')
    
    # Count products
    products = db.get_products_by_shop(shop_id)
    product_count = len(products)
    
    print(f"\n🏪 Shop: {shop_name}")
    print(f"   ID: {shop_id}")
    print(f"   Products: {product_count}")
    print(f"   Created: {shop_data.get('created_at')}")
    
    if product_count > 0:
        shops_with_products.append((shop_id, shop_name, product_count))
    else:
        empty_shops.append((shop_id, shop_name))

print("\n" + "="*60)
print("📋 Summary:")
print("="*60)
print(f"✅ Shops with products: {len(shops_with_products)}")
print(f"❌ Empty shops: {len(empty_shops)}")

if len(shops_with_products) == 1 and len(empty_shops) > 0:
    print("\n💡 SOLUTION: Delete empty shops and keep the one with products")
    
    correct_shop_id, correct_shop_name, product_count = shops_with_products[0]
    print(f"\n✅ Keeping: {correct_shop_name} ({product_count} products)")
    print(f"   Shop ID: {correct_shop_id}")
    
    print(f"\n❌ Deleting {len(empty_shops)} empty shop(s):")
    for shop_id, shop_name in empty_shops:
        print(f"   • {shop_name} (ID: {shop_id})")
        
        # Delete the empty shop
        db.db.collection('shops').document(shop_id).delete()
        print(f"     ✅ Deleted shop: {shop_id}")
        
        # Delete any users linked to this shop
        users_to_delete = db.db.collection('users').where('shop_id', '==', shop_id).stream()
        for user_doc in users_to_delete:
            user_data = user_doc.to_dict()
            print(f"     ✅ Deleted user: {user_data.get('name')} ({user_data.get('user_id')})")
            db.db.collection('users').document(user_data.get('user_id')).delete()
    
    print("\n✅ Cleanup complete!")
    print(f"\n📱 Now login again with phone: {phone}")
    print(f"   You should see: {correct_shop_name}")
    print(f"   With {product_count} products!")
    
elif len(shops_with_products) > 1:
    print("\n⚠️ WARNING: Multiple shops with products!")
    print("   Manual intervention required.")
    for shop_id, shop_name, product_count in shops_with_products:
        print(f"   • {shop_name}: {product_count} products")
        
elif len(shops_with_products) == 0:
    print("\n⚠️ WARNING: No shops with products found!")
    print("   All shops are empty.")
    
else:
    print("\n✅ Everything looks good! Only one shop with products.")

print("\n" + "="*60)

