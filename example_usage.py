"""
Example usage script for Kirana Shop Management App
This demonstrates how to use the API programmatically
"""
import requests
import json

# Base URL - change this to your deployed URL
BASE_URL = "http://localhost:5000"


def create_shop():
    """Example: Create a new shop"""
    print("📝 Creating a new shop...")
    
    url = f"{BASE_URL}/api/shops"
    data = {
        "name": "Sharma Kirana Store",
        "owner_phone": "+919876543210",
        "owner_name": "Rajesh Sharma",
        "address": "123 Main Street, Delhi"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Shop created successfully!")
        print(f"   Shop ID: {result['shop']['shop_id']}")
        print(f"   Name: {result['shop']['name']}")
        return result['shop']['shop_id']
    else:
        print(f"❌ Failed to create shop: {response.text}")
        return None


def add_staff(shop_id):
    """Example: Add staff member to shop"""
    print(f"\n👥 Adding staff to shop {shop_id}...")
    
    url = f"{BASE_URL}/api/shops/{shop_id}/users"
    data = {
        "phone": "+919876543211",
        "name": "Amit Kumar"
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Staff added successfully!")
        print(f"   Name: {result['user']['name']}")
        print(f"   Phone: {result['user']['phone']}")
    else:
        print(f"❌ Failed to add staff: {response.text}")


def test_parse_command(message):
    """Example: Test command parsing"""
    print(f"\n🤖 Testing command parsing for: '{message}'")
    
    url = f"{BASE_URL}/api/test/parse"
    data = {"message": message}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        parsed = result['parsed']
        print("✅ Command parsed successfully!")
        print(f"   Action: {parsed['action']}")
        print(f"   Product: {parsed['product_name']}")
        print(f"   Quantity: {parsed['quantity']}")
        print(f"   Confidence: {parsed['confidence']}")
        print(f"   Valid: {parsed['is_valid']}")
    else:
        print(f"❌ Failed to parse: {response.text}")


def get_products(shop_id):
    """Example: Get all products for a shop"""
    print(f"\n📦 Getting products for shop {shop_id}...")
    
    url = f"{BASE_URL}/api/shops/{shop_id}/products"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        products = result['products']
        print(f"✅ Found {len(products)} products:")
        for product in products:
            print(f"   - {product['name']}: {product['current_stock']} {product['unit']}")
    else:
        print(f"❌ Failed to get products: {response.text}")


def get_transactions(shop_id):
    """Example: Get transaction history"""
    print(f"\n📊 Getting transactions for shop {shop_id}...")
    
    url = f"{BASE_URL}/api/shops/{shop_id}/transactions"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        transactions = result['transactions']
        print(f"✅ Found {len(transactions)} transactions:")
        for txn in transactions[:5]:  # Show first 5
            print(f"   - {txn['transaction_type']}: {txn['quantity']} {txn['product_name']}")
    else:
        print(f"❌ Failed to get transactions: {response.text}")


def simulate_whatsapp_message(from_phone, message):
    """Example: Simulate a WhatsApp message (for testing)"""
    print(f"\n💬 Simulating WhatsApp message from {from_phone}...")
    print(f"   Message: '{message}'")
    
    # This simulates a WATI webhook payload
    url = f"{BASE_URL}/webhook"
    payload = {
        "waId": from_phone,
        "type": "text",
        "text": message
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Message processed: {result}")
    else:
        print(f"❌ Failed to process message: {response.text}")


def main():
    """Run example usage"""
    print("=" * 60)
    print("  KIRANA SHOP MANAGEMENT - EXAMPLE USAGE")
    print("=" * 60)
    
    # Test if server is running
    try:
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("❌ Server is not running. Please start the app first:")
            print("   python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start the app first:")
        print("   python app.py")
        return
    
    print("✅ Server is running!\n")
    
    # Example 1: Test command parsing
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Test Command Parsing")
    print("=" * 60)
    
    test_parse_command("Add 10 Maggi")
    test_parse_command("2 oil sold")
    test_parse_command("Kitna stock hai atta?")
    test_parse_command("5 packets biscuit add karo")
    
    # Example 2: Create shop and add staff
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Create Shop and Add Staff")
    print("=" * 60)
    
    shop_id = create_shop()
    
    if shop_id:
        add_staff(shop_id)
        
        # Example 3: Simulate WhatsApp messages
        print("\n" + "=" * 60)
        print("EXAMPLE 3: Simulate WhatsApp Messages")
        print("=" * 60)
        
        simulate_whatsapp_message("+919876543210", "Add 10 Maggi")
        simulate_whatsapp_message("+919876543210", "Add 5 oil")
        simulate_whatsapp_message("+919876543210", "2 Maggi sold")
        simulate_whatsapp_message("+919876543210", "Kitna stock hai Maggi?")
        
        # Example 4: Get products and transactions
        print("\n" + "=" * 60)
        print("EXAMPLE 4: View Products and Transactions")
        print("=" * 60)
        
        get_products(shop_id)
        get_transactions(shop_id)
    
    print("\n" + "=" * 60)
    print("  EXAMPLES COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()

