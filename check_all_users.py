"""
Check all users and shops for a phone number
"""
from database import FirestoreDB

# Initialize database
db = FirestoreDB(
    credentials_path='firbasekey.json',
    project_id='kiranabuddy-55330'
)

phone = "9876543210"

print("="*60)
print(f"🔍 Checking ALL users for phone: {phone}")
print("="*60)

# Get ALL users with this phone (including inactive)
all_users = db.db.collection('users').where('phone', '==', phone).stream()

users_list = []
for doc in all_users:
    user_data = doc.to_dict()
    users_list.append(user_data)
    print(f"\n👤 User ID: {user_data.get('user_id')}")
    print(f"   Name: {user_data.get('name')}")
    print(f"   Phone: {user_data.get('phone')}")
    print(f"   Shop ID: {user_data.get('shop_id')}")
    print(f"   Role: {user_data.get('role')}")
    print(f"   Active: {user_data.get('active')}")
    print(f"   Created: {user_data.get('created_at')}")
    print(f"   Last Login: {user_data.get('last_login')}")

print(f"\n📊 Total users found: {len(users_list)}")

print("\n" + "="*60)
print(f"🏪 Checking ALL shops for owner: {phone}")
print("="*60)

# Get ALL shops with this owner
all_shops = db.db.collection('shops').where('owner_phone', '==', phone).stream()

shops_list = []
for doc in all_shops:
    shop_data = doc.to_dict()
    shops_list.append(shop_data)
    print(f"\n🏪 Shop ID: {shop_data.get('shop_id')}")
    print(f"   Name: {shop_data.get('name')}")
    print(f"   Owner: {shop_data.get('owner_phone')}")
    print(f"   Active: {shop_data.get('active')}")
    print(f"   Created: {shop_data.get('created_at')}")
    
    # Count products in this shop
    products = db.get_products_by_shop(shop_data.get('shop_id'))
    print(f"   Products: {len(products)}")

print(f"\n📊 Total shops found: {len(shops_list)}")

print("\n" + "="*60)
print("💡 SOLUTION:")
print("="*60)

if len(users_list) > 1:
    print("\n⚠️ You have MULTIPLE user accounts!")
    print("   This happens when the user was deleted and recreated.")
    print("\n   Active users:")
    for user in users_list:
        if user.get('active'):
            print(f"   • {user.get('name')} - Shop: {user.get('shop_id')}")
    
if len(shops_list) > 1:
    print("\n⚠️ You have MULTIPLE shops!")
    print("   This happens when you logged in multiple times.")
    print("\n   Shops with products:")
    for shop in shops_list:
        products = db.get_products_by_shop(shop.get('shop_id'))
        if len(products) > 0:
            print(f"   • {shop.get('name')} - {len(products)} products")

print("\n✅ To fix: We need to ensure you login to the shop with products!")
print("="*60)

