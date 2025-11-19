"""
Quick script to check shop data for a phone number
"""
from database import FirestoreDB

# Initialize database
db = FirestoreDB(
    credentials_path='firbasekey.json',
    project_id='kiranabuddy-55330'
)

# Phone number to check
phone = "9876543210"

print("="*60)
print(f"🔍 Checking data for phone: {phone}")
print("="*60)

# Get user
user = db.get_user_by_phone(phone)

if not user:
    print(f"\n❌ No user found for phone: {phone}")
    print("\n💡 Please login first at: http://127.0.0.1:5000/login")
else:
    print(f"\n✅ User found:")
    print(f"   Name: {user.name}")
    print(f"   Phone: {user.phone}")
    print(f"   Shop ID: {user.shop_id}")
    print(f"   Role: {user.role.value}")
    
    # Get shop details
    shop_doc = db.db.collection('shops').document(user.shop_id).get()
    if shop_doc.exists:
        shop_data = shop_doc.to_dict()
        print(f"\n🏪 Shop Details:")
        print(f"   Name: {shop_data.get('name')}")
        print(f"   Owner: {shop_data.get('owner_phone')}")
        print(f"   Created: {shop_data.get('created_at')}")
    
    # Get products
    products = db.get_products_by_shop(user.shop_id)
    print(f"\n📦 Products: {len(products)} total")
    
    if products:
        print("\n   Product List:")
        for p in products:
            print(f"   • {p.name}: {p.current_stock} {p.unit}")
    else:
        print("\n   ⚠️ No products found!")
        print("\n   💡 Add products by saying:")
        print("      'Add 10 Maggi'")
        print("      '5 oil bottles aaye'")
        print("      '20 biscuit packets'")
    
    # Get transactions
    transactions = db.get_transactions_by_shop(user.shop_id, limit=10)
    print(f"\n📊 Recent Transactions: {len(transactions)} total")
    
    if transactions:
        print("\n   Recent Activity:")
        for t in transactions[:5]:
            print(f"   • {t.type}: {t.product_name} ({t.quantity} {t.unit})")
    else:
        print("\n   ⚠️ No transactions found!")

print("\n" + "="*60)

