"""
Debug login issue
"""
from database import FirestoreDB

# Initialize database
db = FirestoreDB(
    credentials_path='firbasekey.json',
    project_id='kiranabuddy-55330'
)

# Test different phone formats
phone_formats = [
    "9876543210",
    "+919876543210",
    "+91 9876543210",
    "91987654321 0",
]

print("="*60)
print("🔍 Testing phone number formats")
print("="*60)

for phone in phone_formats:
    print(f"\n📱 Testing: '{phone}'")
    
    # Clean phone number (same as in app.py)
    cleaned = phone.replace('+91', '').replace('+', '').replace('-', '').replace(' ', '')
    print(f"   Cleaned: '{cleaned}'")
    
    # Try to get user
    user = db.get_user_by_phone(cleaned)
    
    if user:
        print(f"   ✅ User found: {user.name}")
        print(f"   Shop ID: {user.shop_id}")
    else:
        print(f"   ❌ No user found")

print("\n" + "="*60)
print("🔍 Checking database directly")
print("="*60)

# Check what's actually in the database
all_users = db.db.collection('users').stream()

print("\nAll users in database:")
for doc in all_users:
    user_data = doc.to_dict()
    print(f"\n   Phone in DB: '{user_data.get('phone')}'")
    print(f"   Name: {user_data.get('name')}")
    print(f"   Active: {user_data.get('active')}")
    print(f"   Shop ID: {user_data.get('shop_id')}")

print("\n" + "="*60)

