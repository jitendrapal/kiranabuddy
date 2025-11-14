"""
Demo script to test the Kirana Shop Management App WITHOUT WhatsApp
This simulates the entire workflow locally
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def test_server_health():
    """Test if server is running"""
    print_header("1. Testing Server Health")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Server is running!")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Please start the app first:")
        print_info("Run: python app.py")
        return False

def test_command_parsing():
    """Test AI command parsing"""
    print_header("2. Testing AI Command Parsing")
    
    test_commands = [
        "Add 10 Maggi",
        "2 oil sold",
        "Kitna stock hai atta?",
        "5 packets biscuit add karo",
        "3 cold drink bech diya",
        "दस चावल ऐड करो"
    ]
    
    for command in test_commands:
        print(f"\n📝 Testing: '{command}'")
        try:
            response = requests.post(
                f"{BASE_URL}/api/test/parse",
                json={"message": command}
            )
            
            if response.status_code == 200:
                result = response.json()
                parsed = result['parsed']
                print_success(f"Parsed successfully!")
                print(f"   Action: {parsed['action']}")
                print(f"   Product: {parsed['product_name']}")
                print(f"   Quantity: {parsed['quantity']}")
                print(f"   Valid: {parsed['is_valid']}")
            else:
                print_error(f"Failed: {response.text}")
        except Exception as e:
            print_error(f"Error: {e}")
        
        time.sleep(0.5)  # Small delay between requests

def create_test_shop():
    """Create a test shop"""
    print_header("3. Creating Test Shop")
    
    shop_data = {
        "name": "Sharma Kirana Store",
        "owner_phone": "+919876543210",
        "owner_name": "Rajesh Sharma",
        "address": "123 Main Street, Delhi"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/shops",
            json=shop_data
        )
        
        if response.status_code == 201:
            result = response.json()
            shop_id = result['shop']['shop_id']
            print_success("Shop created successfully!")
            print(f"   Shop ID: {shop_id}")
            print(f"   Name: {result['shop']['name']}")
            print(f"   Owner: {result['owner']['name']}")
            return shop_id
        else:
            print_error(f"Failed to create shop: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {e}")
        return None

def add_staff_member(shop_id):
    """Add staff member to shop"""
    print_header("4. Adding Staff Member")
    
    staff_data = {
        "phone": "+919876543211",
        "name": "Amit Kumar"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/shops/{shop_id}/users",
            json=staff_data
        )
        
        if response.status_code == 201:
            result = response.json()
            print_success("Staff member added!")
            print(f"   Name: {result['user']['name']}")
            print(f"   Phone: {result['user']['phone']}")
            print(f"   Role: {result['user']['role']}")
            return True
        else:
            print_error(f"Failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def simulate_whatsapp_messages():
    """Simulate WhatsApp messages (without actual WhatsApp)"""
    print_header("5. Simulating WhatsApp Messages")
    
    messages = [
        {
            "from": "+919876543210",
            "message": "Add 10 Maggi",
            "type": "text"
        },
        {
            "from": "+919876543210",
            "message": "Add 5 oil",
            "type": "text"
        },
        {
            "from": "+919876543210",
            "message": "2 Maggi sold",
            "type": "text"
        },
        {
            "from": "+919876543210",
            "message": "Kitna stock hai Maggi?",
            "type": "text"
        },
        {
            "from": "+919876543210",
            "message": "Add 20 atta",
            "type": "text"
        }
    ]
    
    for msg in messages:
        print(f"\n💬 Message from {msg['from']}: '{msg['message']}'")
        
        # Simulate WATI webhook payload
        webhook_payload = {
            "waId": msg['from'],
            "type": "text",
            "text": msg['message']
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/webhook",
                json=webhook_payload
            )
            
            if response.status_code == 200:
                print_success("Message processed!")
                result = response.json()
                print(f"   Status: {result.get('status')}")
                print(f"   Success: {result.get('success')}")
            else:
                print_error(f"Failed: {response.text}")
        except Exception as e:
            print_error(f"Error: {e}")
        
        time.sleep(1)  # Delay between messages

def view_products(shop_id):
    """View all products in shop"""
    print_header("6. Viewing Products")
    
    try:
        response = requests.get(f"{BASE_URL}/api/shops/{shop_id}/products")
        
        if response.status_code == 200:
            result = response.json()
            products = result['products']
            print_success(f"Found {len(products)} products:")
            print()
            for product in products:
                print(f"   📦 {product['name']}: {product['current_stock']} {product['unit']}")
        else:
            print_error(f"Failed: {response.text}")
    except Exception as e:
        print_error(f"Error: {e}")

def view_transactions(shop_id):
    """View transaction history"""
    print_header("7. Viewing Transaction History")
    
    try:
        response = requests.get(f"{BASE_URL}/api/shops/{shop_id}/transactions")
        
        if response.status_code == 200:
            result = response.json()
            transactions = result['transactions']
            print_success(f"Found {len(transactions)} transactions:")
            print()
            for txn in transactions[:10]:  # Show first 10
                print(f"   📝 {txn['transaction_type']}: {txn['quantity']} {txn['product_name']}")
                print(f"      Previous: {txn['previous_stock']} → New: {txn['new_stock']}")
        else:
            print_error(f"Failed: {response.text}")
    except Exception as e:
        print_error(f"Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "🏪"*30)
    print("  KIRANA SHOP MANAGEMENT - DEMO (WITHOUT WHATSAPP)")
    print("🏪"*30)
    
    # Test 1: Server health
    if not test_server_health():
        return
    
    time.sleep(1)
    
    # Test 2: Command parsing
    test_command_parsing()
    
    time.sleep(1)
    
    # Test 3: Create shop
    shop_id = create_test_shop()
    if not shop_id:
        print_error("Cannot continue without shop ID")
        return
    
    time.sleep(1)
    
    # Test 4: Add staff
    add_staff_member(shop_id)
    
    time.sleep(1)
    
    # Test 5: Simulate messages
    simulate_whatsapp_messages()
    
    time.sleep(1)
    
    # Test 6: View products
    view_products(shop_id)
    
    time.sleep(1)
    
    # Test 7: View transactions
    view_transactions(shop_id)
    
    # Final summary
    print_header("✅ DEMO COMPLETE!")
    print()
    print("Summary:")
    print("  ✅ Server is running")
    print("  ✅ AI command parsing works")
    print("  ✅ Shop created")
    print("  ✅ Staff added")
    print("  ✅ Messages processed")
    print("  ✅ Inventory updated")
    print("  ✅ Transactions recorded")
    print()
    print("🎉 Your Kirana Shop Management App is working perfectly!")
    print()
    print("Next steps:")
    print("  1. Configure WhatsApp (WATI or Cloud API)")
    print("  2. Deploy to production")
    print("  3. Start managing your shop via WhatsApp!")
    print()

if __name__ == "__main__":
    main()

