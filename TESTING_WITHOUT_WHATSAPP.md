# 🧪 Testing Kirana Shop Management App WITHOUT WhatsApp

You can fully test and use the app **without WhatsApp integration**! Here are 3 easy ways:

---

## 🎯 Method 1: Web Test Interface (Easiest!)

### Step 1: Start the App
```bash
python app.py
```

### Step 2: Open Your Browser
Go to: **http://localhost:5000/test**

### Step 3: Test Features
- ✅ Parse commands in Hindi/English/Hinglish
- ✅ Simulate WhatsApp messages
- ✅ See real-time results
- ✅ Click example commands to try them

**No coding required! Just click and test!** 🎉

---

## 🤖 Method 2: Automated Demo Script

### Run the Complete Demo
```bash
# Terminal 1: Start the app
python app.py

# Terminal 2: Run the demo
python test_app_demo.py
```

### What It Does:
1. ✅ Tests server health
2. ✅ Tests AI command parsing (6 different commands)
3. ✅ Creates a test shop
4. ✅ Adds staff member
5. ✅ Simulates 5 WhatsApp messages
6. ✅ Shows all products
7. ✅ Shows transaction history

**Fully automated - just watch it work!** 🚀

---

## 🔧 Method 3: Manual API Testing

### Using cURL (Command Line)

#### 1. Test Command Parsing
```bash
curl -X POST http://localhost:5000/api/test/parse \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Add 10 Maggi\"}"
```

**Response:**
```json
{
  "success": true,
  "parsed": {
    "action": "add_stock",
    "product_name": "Maggi",
    "quantity": 10,
    "confidence": 0.95,
    "is_valid": true
  }
}
```

#### 2. Create a Shop
```bash
curl -X POST http://localhost:5000/api/shops \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"My Kirana Store\", \"owner_phone\": \"+919876543210\", \"owner_name\": \"Owner Name\"}"
```

#### 3. Simulate WhatsApp Message
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d "{\"waId\": \"+919876543210\", \"type\": \"text\", \"text\": \"Add 10 Maggi\"}"
```

#### 4. View Products (replace SHOP_ID)
```bash
curl http://localhost:5000/api/shops/SHOP_ID/products
```

#### 5. View Transactions (replace SHOP_ID)
```bash
curl http://localhost:5000/api/shops/SHOP_ID/transactions
```

---

## 📱 Method 4: Using Postman or Insomnia

### Import These Endpoints:

**Base URL:** `http://localhost:5000`

| Method | Endpoint | Body |
|--------|----------|------|
| GET | `/` | - |
| GET | `/test` | - |
| POST | `/api/test/parse` | `{"message": "Add 10 Maggi"}` |
| POST | `/api/shops` | `{"name": "Shop", "owner_phone": "+91...", "owner_name": "Name"}` |
| POST | `/webhook` | `{"waId": "+91...", "type": "text", "text": "Add 10 Maggi"}` |
| GET | `/api/shops/{shop_id}/products` | - |
| GET | `/api/shops/{shop_id}/transactions` | - |

---

## 🎮 Interactive Python Testing

### Start Python Interactive Shell
```bash
python
```

### Test Commands:
```python
import requests

# Test command parsing
response = requests.post(
    'http://localhost:5000/api/test/parse',
    json={'message': 'Add 10 Maggi'}
)
print(response.json())

# Create shop
response = requests.post(
    'http://localhost:5000/api/shops',
    json={
        'name': 'Test Shop',
        'owner_phone': '+919876543210',
        'owner_name': 'Test Owner'
    }
)
shop_id = response.json()['shop']['shop_id']
print(f"Shop ID: {shop_id}")

# Simulate message
response = requests.post(
    'http://localhost:5000/webhook',
    json={
        'waId': '+919876543210',
        'type': 'text',
        'text': 'Add 10 Maggi'
    }
)
print(response.json())

# View products
response = requests.get(f'http://localhost:5000/api/shops/{shop_id}/products')
print(response.json())
```

---

## 📊 What You Can Test

### ✅ AI Features
- [x] Command parsing (Hindi/English/Hinglish)
- [x] Natural language understanding
- [x] Product name extraction
- [x] Quantity detection
- [x] Action classification

### ✅ Inventory Management
- [x] Add stock
- [x] Reduce stock (sales)
- [x] Check stock
- [x] Product auto-creation
- [x] Stock updates

### ✅ Multi-Shop Features
- [x] Create shops
- [x] Add staff members
- [x] Shop-specific inventory
- [x] Role-based access

### ✅ Database Operations
- [x] Firebase Firestore integration
- [x] Transaction history
- [x] Audit trail
- [x] Real-time updates

---

## 🎯 Test Scenarios

### Scenario 1: New Shop Setup
1. Create shop
2. Add staff members
3. Add initial inventory
4. Check stock levels

### Scenario 2: Daily Operations
1. Record sales (reduce stock)
2. Add new stock
3. Check stock levels
4. View transaction history

### Scenario 3: Multi-language Commands
1. Test English: "Add 10 Maggi"
2. Test Hindi: "दस मैगी ऐड करो"
3. Test Hinglish: "5 packets biscuit add karo"

---

## 🔍 Debugging Tips

### Check Server Logs
The Flask app shows all requests and responses in the terminal.

### Check Firebase Console
Go to Firebase Console → Firestore Database to see:
- Shops collection
- Users collection
- Products collection
- Transactions collection

### Test Individual Components
```python
# Test AI service
from ai_service import AIService
import os

ai = AIService(api_key=os.getenv('OPENAI_API_KEY'))
result = ai.parse_command("Add 10 Maggi")
print(result)

# Test database
from database import FirestoreDB
from config import Config

db = FirestoreDB(
    credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
    project_id=Config.FIREBASE_PROJECT_ID
)

# Create test shop
shop = db.create_shop("Test Shop", "+919876543210")
print(shop)
```

---

## ✅ Success Checklist

- [ ] Server starts without errors
- [ ] Web interface loads at `/test`
- [ ] Command parsing works
- [ ] Shop creation works
- [ ] Inventory updates work
- [ ] Products are visible
- [ ] Transactions are recorded
- [ ] Firebase data is saved

---

## 🎉 You're Ready!

Once all tests pass, you can:
1. ✅ Use the app locally without WhatsApp
2. ✅ Add WhatsApp integration later
3. ✅ Deploy to production
4. ✅ Scale to multiple shops

**No WhatsApp needed for testing!** 🚀

