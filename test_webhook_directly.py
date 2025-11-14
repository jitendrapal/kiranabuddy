"""
Test webhook directly to see what's happening
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_webhook_message(phone, message):
    """Test sending a message through webhook"""
    
    print("="*60)
    print(f"Testing: '{message}'")
    print(f"From: {phone}")
    print("="*60)
    
    # Simulate WATI webhook payload
    payload = {
        "waId": phone,
        "type": "text",
        "text": message
    }
    
    print("\n📤 Sending to webhook...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=payload,
            timeout=30
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Message processed successfully!")
        else:
            print(f"\n❌ Error: {response.status_code}")
            
        return response
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server!")
        print("Make sure the app is running: python app.py")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_parse_only(message):
    """Test just the parsing without executing"""
    
    print("\n" + "="*60)
    print(f"Testing Parse Only: '{message}'")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/test/parse",
            json={"message": message},
            timeout=10
        )
        
        print(f"\n📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            parsed = result['parsed']
            print(f"\n✅ Parsed successfully!")
            print(f"   Action: {parsed['action']}")
            print(f"   Product: {parsed['product_name']}")
            print(f"   Quantity: {parsed['quantity']}")
            print(f"   Valid: {parsed['is_valid']}")
        
        return response
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def check_products(shop_id):
    """Check current products"""
    
    print("\n" + "="*60)
    print(f"Checking Products for Shop: {shop_id}")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/shops/{shop_id}/products",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            products = result['products']
            
            print(f"\n📦 Found {len(products)} products:")
            for product in products:
                print(f"   - {product['name']}: {product['current_stock']} {product['unit']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🧪 WEBHOOK TESTING TOOL\n")
    
    # Test 1: Parse only
    print("\n" + "🔍 TEST 1: Parse Command Only")
    test_parse_only("Add 10 Maggi")
    
    input("\nPress Enter to continue...")
    
    # Test 2: Full webhook test
    print("\n" + "💬 TEST 2: Full Webhook Message")
    test_webhook_message("+919876543210", "Add 10 Maggi")
    
    input("\nPress Enter to continue...")
    
    # Test 3: Check products
    print("\n" + "📦 TEST 3: Check Products")
    shop_id = "8e70a29d-acda-423e-a27b-9b9c870616a7"  # From setup
    check_products(shop_id)
    
    input("\nPress Enter to continue...")
    
    # Test 4: Another message
    print("\n" + "💬 TEST 4: Another Message")
    test_webhook_message("+919876543210", "2 oil sold")
    
    input("\nPress Enter to continue...")
    
    # Test 5: Check products again
    print("\n" + "📦 TEST 5: Check Products Again")
    check_products(shop_id)
    
    print("\n✅ Testing complete!")
    print("\nIf all tests passed, the webhook is working correctly.")
    print("If not, check the server logs for errors.")

