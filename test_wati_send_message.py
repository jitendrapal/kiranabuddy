"""
Test sending WhatsApp message via WATI
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_test_message():
    """Send a test WhatsApp message"""
    
    print("="*60)
    print("  TESTING WATI - SEND MESSAGE")
    print("="*60)
    print()
    
    api_key = os.getenv('WATI_API_KEY')
    base_url = os.getenv('WATI_BASE_URL')
    
    print("📋 Configuration:")
    print(f"   Base URL: {base_url}")
    print(f"   WATI Number: +31683078160")
    print()
    
    # Get recipient number
    print("📱 Enter recipient WhatsApp number:")
    print("   (Include country code, e.g., +919876543210)")
    recipient = input("   Number: ").strip()
    
    if not recipient:
        print("❌ No number entered!")
        return
    
    # Remove spaces and ensure + prefix
    recipient = recipient.replace(" ", "").replace("-", "")
    if not recipient.startswith("+"):
        recipient = "+" + recipient
    
    print()
    print(f"📤 Sending test message to: {recipient}")
    print()
    
    # Prepare message
    url = f"{base_url}/api/v1/sendSessionMessage/{recipient}"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "messageText": "🏪 Hello from Kirana Shop Management!\n\nThis is a test message. Your WhatsApp integration is working! ✅\n\nYou can now send commands like:\n• Add 10 Maggi\n• 2 oil sold\n• Kitna stock hai atta?"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! Message sent!")
            print()
            print("📱 Check your WhatsApp to see the message!")
            print()
            print("Next steps:")
            print("1. Reply to the message with: Add 10 Maggi")
            print("2. Setup webhook to receive replies")
            print("3. Your app will process the command automatically!")
            
        elif response.status_code == 401:
            print("❌ Authentication failed!")
            print("   Check your API key")
            
        elif response.status_code == 400:
            print("❌ Bad request!")
            print("   Check the phone number format")
            print("   Should be: +919876543210")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    send_test_message()

