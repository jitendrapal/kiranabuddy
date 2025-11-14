"""
Test webhook and show detailed error
"""
import requests
import json

def test_with_details():
    """Test and show full error details"""
    
    print("="*60)
    print("  TESTING WEBHOOK WITH ERROR DETAILS")
    print("="*60)
    
    url = "http://localhost:5000/webhook"
    
    payload = {
        "waId": "+919876543210",
        "type": "text",
        "text": "Add 10 Maggi"
    }
    
    print(f"\n📤 Sending message...")
    print(f"   From: {payload['waId']}")
    print(f"   Message: {payload['text']}")
    print()
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"📥 Response Status: {response.status_code}")
        print()
        
        data = response.json()
        print("📋 Full Response:")
        print(json.dumps(data, indent=2))
        print()
        
        if data.get('success'):
            print("✅ SUCCESS!")
            print(f"\nMessage: {data.get('message')}")
            
            if data.get('data'):
                print(f"\nData:")
                for key, value in data['data'].items():
                    print(f"   {key}: {value}")
        else:
            print("❌ FAILED!")
            print(f"\nError Message: {data.get('message')}")
            
            if 'error' in data:
                print(f"\nError Details: {data['error']}")
            
            if 'error_type' in data:
                print(f"\nError Type: {data['error_type']}")
        
        print()
        print("="*60)
        print("\n💡 Now check the terminal where app.py is running")
        print("   You should see detailed error logs there!")
        print()
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("\n💡 Make sure app is running:")
        print("   python app.py")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_details()

