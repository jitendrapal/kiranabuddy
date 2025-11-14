"""
Quick test to check if webhook is working
"""
import requests
import json

def test_webhook():
    """Test webhook with a simple message"""
    
    print("🧪 Testing Webhook...")
    print("="*60)
    
    url = "http://localhost:5000/webhook"
    
    payload = {
        "waId": "+919876543210",
        "type": "text",
        "text": "Add 10 Maggi"
    }
    
    print(f"\n📤 Sending: {payload['text']}")
    print(f"   From: {payload['waId']}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Response Data:")
            print(json.dumps(data, indent=2))
            
            if data.get('success'):
                print("\n🎉 SUCCESS! Product should be added!")
                print(f"\nMessage: {data.get('message', 'No message')}")
            else:
                print("\n❌ FAILED! Product was NOT added!")
                print(f"\nReason: {data.get('message', 'Unknown error')}")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("\n💡 Solution:")
        print("   1. Make sure app is running: python app.py")
        print("   2. Check if port 5000 is correct")
        print("   3. Try: http://localhost:5000/ in browser")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_webhook()

