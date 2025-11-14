"""
Check what users and shops exist in Firebase
"""
from database import FirestoreDB
from config import Config
from dotenv import load_dotenv

load_dotenv()

def check_data():
    """Check existing users and shops"""
    
    print("="*60)
    print("  CHECKING FIREBASE DATA")
    print("="*60)
    print()
    
    db = FirestoreDB(
        credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
        project_id=Config.FIREBASE_PROJECT_ID
    )
    
    # Check shops
    print("🏪 SHOPS:")
    shops_ref = db.db.collection('shops').stream()
    shops = list(shops_ref)
    
    if shops:
        for shop_doc in shops:
            shop = shop_doc.to_dict()
            print(f"\n   Shop ID: {shop.get('shop_id')}")
            print(f"   Name: {shop.get('name')}")
            print(f"   Owner Phone: {shop.get('owner_phone')}")
    else:
        print("   ❌ No shops found!")
    
    print()
    
    # Check users
    print("👥 USERS:")
    users_ref = db.db.collection('users').stream()
    users = list(users_ref)
    
    if users:
        for user_doc in users:
            user = user_doc.to_dict()
            print(f"\n   User ID: {user.get('user_id')}")
            print(f"   Name: {user.get('name')}")
            print(f"   Phone: {user.get('phone')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Shop ID: {user.get('shop_id')}")
    else:
        print("   ❌ No users found!")
    
    print()
    print("="*60)
    
    # Test specific phone
    test_phone = "+919876543210"
    print(f"\n🔍 Testing phone: {test_phone}")
    
    user = db.get_user_by_phone(test_phone)
    if user:
        print(f"   ✅ User found: {user.name} ({user.role.value})")
        print(f"   Shop ID: {user.shop_id}")
    else:
        print(f"   ⚠️  No user found with this phone")
        
        shop = db.get_shop_by_phone(test_phone)
        if shop:
            print(f"   ✅ Shop found: {shop.name}")
            print(f"   Shop ID: {shop.shop_id}")
        else:
            print(f"   ❌ No shop found with this phone either!")
            print()
            print("   💡 This is why messages are failing!")
            print("   💡 You need to use a registered phone number")
            
            if shops:
                print()
                print("   📱 Available phone numbers:")
                for shop_doc in shops:
                    shop = shop_doc.to_dict()
                    print(f"      - {shop.get('owner_phone')} (Shop: {shop.get('name')})")
    
    print()

if __name__ == "__main__":
    check_data()

