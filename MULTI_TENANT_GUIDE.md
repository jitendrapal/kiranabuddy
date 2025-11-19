# 🏪 Multi-Tenant Shopkeeper System

## Overview

The Kirana Shop Manager app is **fully multi-tenant**, allowing multiple shopkeepers to use the same application with their own phone numbers and see only their own shop's data.

---

## 🔐 How It Works

### 1. **Phone Number-Based Authentication**
- Each shopkeeper logs in with their unique phone number
- OTP verification (currently hardcoded to `12345` for testing)
- No hardcoded phone numbers - any shopkeeper can register

### 2. **Automatic Shop Creation**
- When a new shopkeeper logs in for the first time:
  - System creates a new shop: `{Name}'s Shop`
  - Creates a user account linked to that shop
  - Assigns the user as shop OWNER

### 3. **Data Isolation**
- Every database query filters by `shop_id`
- Each shopkeeper sees only their own:
  - Products
  - Transactions
  - Sales reports
  - Stock levels
  - Profit calculations
  - Seasonal analysis

---

## 📱 How Shopkeepers Use the App

### **Login Process:**

1. **Open:** http://127.0.0.1:5000/login
2. **Enter:** Your 10-digit phone number
3. **Click:** "Send OTP"
4. **Enter:** OTP code (currently `12345` for testing)
5. **First time only:** Enter your name
6. **Done!** You're logged in to your shop's chatbot

### **Using the Chatbot:**

Once logged in, each shopkeeper can:
- Add stock: "10 Maggi aaye"
- Record sales: "Sold 5 oil bottles"
- Check stock: "How much atta?"
- View reports: "Today's profit"
- Get seasonal suggestions: "Diwali products"
- And much more!

---

## 🏗️ Technical Architecture

### **Session Management:**
```python
session['user_phone'] = user.phone
session['user_id'] = user.user_id
session['shop_id'] = user.shop_id
session['user_name'] = user.name
session['user_role'] = user.role.value
```

### **Data Flow:**
```
Phone Number → User → Shop ID → Filtered Data
```

### **Database Collections:**
- `shops` - One per shopkeeper
- `users` - One per phone number
- `products` - Filtered by shop_id
- `transactions` - Filtered by shop_id
- `otps` - For authentication

---

## 🧪 Testing Multi-Tenant

### **Test with Multiple Shopkeepers:**

1. **Shopkeeper 1:**
   - Phone: `9876543210`
   - OTP: `12345`
   - Name: `Rajesh`
   - Shop: `Rajesh's Shop`

2. **Shopkeeper 2:**
   - Phone: `9876543211`
   - OTP: `12345`
   - Name: `Priya`
   - Shop: `Priya's Shop`

3. **Verify Data Isolation:**
   - Login as Rajesh, add "10 Maggi"
   - Logout, login as Priya
   - Check stock - Priya should NOT see Rajesh's Maggi
   - Add "5 Biscuits" as Priya
   - Logout, login as Rajesh
   - Rajesh should NOT see Priya's Biscuits

---

## ✅ Features

- ✅ **Unlimited Shopkeepers** - Any phone number can register
- ✅ **Automatic Shop Creation** - No manual setup needed
- ✅ **Complete Data Isolation** - Each shop's data is separate
- ✅ **Session-Based Security** - Login required for access
- ✅ **Shop Name Display** - Shows shopkeeper's shop name in header
- ✅ **User Info Display** - Shows name and phone in header
- ✅ **Easy Logout** - Logout button in menu
- ✅ **WhatsApp Integration** - Each shopkeeper can use their own WhatsApp number

---

## 🚀 Production Deployment

### **For Production Use:**

1. **Configure Real OTP Provider:**
   - Set `SMS_PROVIDER` environment variable
   - Options: `twilio`, `msg91`, `fast2sms`
   - Add API credentials in environment variables

2. **Remove Hardcoded OTP:**
   - Update `otp_service.py` to generate random OTPs
   - Remove the hardcoded `12345` check

3. **Add Security:**
   - Enable HTTPS
   - Set secure session cookies
   - Add rate limiting for OTP requests
   - Add phone number verification

4. **Database Indexes:**
   - Create Firestore indexes for common queries
   - Optimize for shop_id filtering

---

## 📞 Support

Each shopkeeper manages their own shop independently. The system automatically handles:
- User registration
- Shop creation
- Data isolation
- Session management
- Access control

**No manual intervention needed!** 🎉

