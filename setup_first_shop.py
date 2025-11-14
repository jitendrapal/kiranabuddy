"""
Setup first shop and add test data to Firebase
This will create collections and sample data
"""
from database import FirestoreDB
from config import Config
from models import UserRole
from dotenv import load_dotenv
import sys

load_dotenv()

def setup_first_shop():
    """Create first shop with sample data"""
    
    print("="*60)
    print("  SETTING UP YOUR FIRST SHOP")
    print("="*60)
    print()
    
    try:
        # Initialize database
        print("📡 Connecting to Firebase...")
        db = FirestoreDB(
            credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
            project_id=Config.FIREBASE_PROJECT_ID
        )
        print("✅ Connected to Firebase!")
        print(f"📍 Project: {Config.FIREBASE_PROJECT_ID}")
        print()
        
        # Create shop
        print("🏪 Creating shop...")
        shop = db.create_shop(
            name="Sharma Kirana Store",
            owner_phone="+919876543210",
            address="123 Main Street, Delhi"
        )
        print(f"✅ Shop created!")
        print(f"   Shop ID: {shop.shop_id}")
        print(f"   Name: {shop.name}")
        print()
        
        # Create owner user
        print("👤 Creating owner user...")
        owner = db.create_user(
            phone="+919876543210",
            name="Rajesh Sharma",
            shop_id=shop.shop_id,
            role=UserRole.OWNER
        )
        print(f"✅ Owner created!")
        print(f"   Name: {owner.name}")
        print(f"   Role: {owner.role.value}")
        print()
        
        # Create staff user
        print("👥 Creating staff member...")
        staff = db.create_user(
            phone="+919876543211",
            name="Amit Kumar",
            shop_id=shop.shop_id,
            role=UserRole.STAFF
        )
        print(f"✅ Staff member created!")
        print(f"   Name: {staff.name}")
        print(f"   Role: {staff.role.value}")
        print()
        
        # Add some products
        print("📦 Adding sample products...")
        
        # Add Maggi
        result1 = db.add_stock(
            shop_id=shop.shop_id,
            product_name="Maggi",
            quantity=50,
            user_phone=owner.phone
        )
        print(f"✅ Added {result1['quantity']} {result1['product_name']}")
        
        # Add Oil
        result2 = db.add_stock(
            shop_id=shop.shop_id,
            product_name="Oil",
            quantity=20,
            user_phone=owner.phone
        )
        print(f"✅ Added {result2['quantity']} {result2['product_name']}")
        
        # Add Atta
        result3 = db.add_stock(
            shop_id=shop.shop_id,
            product_name="Atta",
            quantity=100,
            user_phone=owner.phone
        )
        print(f"✅ Added {result3['quantity']} {result3['product_name']}")
        
        # Add Biscuit
        result4 = db.add_stock(
            shop_id=shop.shop_id,
            product_name="Biscuit",
            quantity=30,
            user_phone=owner.phone
        )
        print(f"✅ Added {result4['quantity']} {result4['product_name']}")
        
        print()
        
        # Record some sales
        print("💰 Recording sample sales...")
        
        sale1 = db.reduce_stock(
            shop_id=shop.shop_id,
            product_name="Maggi",
            quantity=5,
            user_phone=staff.phone
        )
        print(f"✅ Sold {sale1['quantity']} {sale1['product_name']}")
        
        sale2 = db.reduce_stock(
            shop_id=shop.shop_id,
            product_name="Oil",
            quantity=2,
            user_phone=staff.phone
        )
        print(f"✅ Sold {sale2['quantity']} {sale2['product_name']}")
        
        print()
        print("="*60)
        print("  ✅ SETUP COMPLETE!")
        print("="*60)
        print()
        print("📊 Summary:")
        print(f"   🏪 Shop: {shop.name}")
        print(f"   👥 Users: 2 (1 owner, 1 staff)")
        print(f"   📦 Products: 4 (Maggi, Oil, Atta, Biscuit)")
        print(f"   📝 Transactions: 6 (4 add, 2 sales)")
        print()
        print("🔥 Firebase Collections Created:")
        print("   ✅ shops")
        print("   ✅ users")
        print("   ✅ products")
        print("   ✅ transactions")
        print()
        print("📍 View in Firebase Console:")
        print(f"   https://console.firebase.google.com/project/{Config.FIREBASE_PROJECT_ID}/firestore")
        print()
        print("💡 Current Stock:")
        print(f"   - Maggi: 45 pieces")
        print(f"   - Oil: 18 pieces")
        print(f"   - Atta: 100 pieces")
        print(f"   - Biscuit: 30 pieces")
        print()
        print("🎯 Shop ID (save this for testing):")
        print(f"   {shop.shop_id}")
        print()
        
        return shop.shop_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    shop_id = setup_first_shop()
    
    if shop_id:
        print("✅ Success! Now check your Firebase Console.")
        print()
        print("Next steps:")
        print("1. Go to Firebase Console and refresh the page")
        print("2. You should see 4 collections: shops, users, products, transactions")
        print("3. Test the app: python app.py")
        print("4. Open: http://localhost:5000/test")
        print()
        sys.exit(0)
    else:
        print("❌ Setup failed. Please check the error above.")
        sys.exit(1)

