"""
View all data stored in Firebase Firestore
"""
from database import FirestoreDB
from config import Config
from dotenv import load_dotenv

load_dotenv()

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def view_all_data():
    """View all data from Firebase"""
    
    # Initialize database
    db = FirestoreDB(
        credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
        project_id=Config.FIREBASE_PROJECT_ID
    )
    
    print("\n🔥 FIREBASE FIRESTORE DATA")
    print(f"📍 Project: {Config.FIREBASE_PROJECT_ID}")
    
    # View all shops
    print_header("🏪 SHOPS")
    try:
        shops_ref = db.db.collection('shops').stream()
        shops = list(shops_ref)
        
        if shops:
            for shop_doc in shops:
                shop = shop_doc.to_dict()
                print(f"\n📦 Shop ID: {shop.get('shop_id')}")
                print(f"   Name: {shop.get('name')}")
                print(f"   Owner: {shop.get('owner_phone')}")
                print(f"   Address: {shop.get('address', 'N/A')}")
                print(f"   Created: {shop.get('created_at')}")
        else:
            print("   No shops found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # View all users
    print_header("👥 USERS")
    try:
        users_ref = db.db.collection('users').stream()
        users = list(users_ref)
        
        if users:
            for user_doc in users:
                user = user_doc.to_dict()
                print(f"\n👤 User ID: {user.get('user_id')}")
                print(f"   Name: {user.get('name')}")
                print(f"   Phone: {user.get('phone')}")
                print(f"   Role: {user.get('role')}")
                print(f"   Shop ID: {user.get('shop_id')}")
        else:
            print("   No users found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # View all products
    print_header("📦 PRODUCTS")
    try:
        products_ref = db.db.collection('products').stream()
        products = list(products_ref)
        
        if products:
            for product_doc in products:
                product = product_doc.to_dict()
                print(f"\n📦 {product.get('name')}")
                print(f"   Product ID: {product.get('product_id')}")
                print(f"   Current Stock: {product.get('current_stock')} {product.get('unit')}")
                print(f"   Shop ID: {product.get('shop_id')}")
                print(f"   Updated: {product.get('updated_at')}")
        else:
            print("   No products found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # View all transactions
    print_header("📝 TRANSACTIONS (Last 20)")
    try:
        transactions_ref = db.db.collection('transactions').order_by('timestamp', direction='DESCENDING').limit(20).stream()
        transactions = list(transactions_ref)
        
        if transactions:
            for txn_doc in transactions:
                txn = txn_doc.to_dict()
                print(f"\n📝 {txn.get('transaction_type').upper()}")
                print(f"   Product: {txn.get('product_name')}")
                print(f"   Quantity: {txn.get('quantity')}")
                print(f"   Stock: {txn.get('previous_stock')} → {txn.get('new_stock')}")
                print(f"   User: {txn.get('user_phone')}")
                print(f"   Time: {txn.get('timestamp')}")
        else:
            print("   No transactions found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Summary
    print_header("📊 SUMMARY")
    try:
        shops_count = len(list(db.db.collection('shops').stream()))
        users_count = len(list(db.db.collection('users').stream()))
        products_count = len(list(db.db.collection('products').stream()))
        transactions_count = len(list(db.db.collection('transactions').stream()))
        
        print(f"\n   🏪 Shops: {shops_count}")
        print(f"   👥 Users: {users_count}")
        print(f"   📦 Products: {products_count}")
        print(f"   📝 Transactions: {transactions_count}")
        print()
    except Exception as e:
        print(f"   Error: {e}")

def view_shop_data(shop_id):
    """View data for a specific shop"""
    
    db = FirestoreDB(
        credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
        project_id=Config.FIREBASE_PROJECT_ID
    )
    
    print_header(f"🏪 SHOP DATA: {shop_id}")
    
    # Get shop details
    shop = db.get_shop(shop_id)
    if shop:
        print(f"\n📦 Shop Name: {shop.name}")
        print(f"   Owner: {shop.owner_phone}")
        print(f"   Address: {shop.address}")
    
    # Get products
    products = db.get_products_by_shop(shop_id)
    print(f"\n📦 Products ({len(products)}):")
    for product in products:
        print(f"   - {product.name}: {product.current_stock} {product.unit}")
    
    # Get transactions
    transactions = db.get_transactions_by_shop(shop_id, limit=10)
    print(f"\n📝 Recent Transactions ({len(transactions)}):")
    for txn in transactions[:5]:
        print(f"   - {txn.transaction_type.value}: {txn.quantity} {txn.product_name}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # View specific shop
        shop_id = sys.argv[1]
        view_shop_data(shop_id)
    else:
        # View all data
        view_all_data()
    
    print("\n✅ Done!\n")

