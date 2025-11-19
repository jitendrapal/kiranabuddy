# 🚀 Quick Login Guide

## ✅ Hardcoded Login Credentials

For easy testing, the login is now hardcoded with fixed values:

---

## 📱 Login Credentials

| Field | Value |
|-------|-------|
| **Phone Number** | `9876543210` |
| **OTP** | `12345` |

---

## 🎯 How to Login

### **Step 1: Open Login Page**
```
http://127.0.0.1:5000/login
```

### **Step 2: Phone Number (Pre-filled)**
- Phone number is already filled: `9876543210`
- Just click **"Send OTP"**

### **Step 3: Enter OTP (Pre-filled)**
- OTP is already filled: `12345`
- Just click **"Verify & Login"**

### **Step 4: Enter Name (First Time Only)**
- If it's your first login, enter your name
- Example: `Test User`
- Click **"Verify & Login"** again

### **Step 5: Done!**
- You'll be redirected to `/test`
- You're now logged in! 🎉

---

## ⚡ Super Quick Login

**For returning users:**
1. Open: http://127.0.0.1:5000/login
2. Click "Send OTP"
3. Click "Verify & Login"
4. Done! (2 clicks only!)

---

## 🔧 What Was Changed

### **1. Hardcoded OTP**
- File: `otp_service.py`
- OTP is always: `12345`
- No random generation

### **2. Pre-filled Phone Number**
- File: `templates/login.html`
- Phone input has default value: `9876543210`

### **3. Pre-filled OTP**
- File: `templates/login.html`
- OTP input has default value: `12345`

### **4. Updated Validation**
- Changed from 6-digit to 5-digit OTP
- Updated in both HTML and JavaScript

---

## 📝 Notes

- ✅ **No SMS needed** - OTP is hardcoded
- ✅ **No console check needed** - OTP is pre-filled
- ✅ **Super fast testing** - Just 2 clicks to login
- ✅ **Works offline** - No external dependencies
- ✅ **Perfect for development** - Easy and quick

---

## 🎨 Login Flow

```
1. Open /login
   ↓
2. Phone: 9876543210 (pre-filled)
   ↓
3. Click "Send OTP"
   ↓
4. OTP: 12345 (pre-filled)
   ↓
5. Click "Verify & Login"
   ↓
6. [First time only] Enter name
   ↓
7. Redirected to /test
   ↓
8. ✅ Logged in!
```

---

## 🚀 Start Testing Now!

1. **Start app:**
   ```bash
   python app.py
   ```

2. **Open browser:**
   ```
   http://127.0.0.1:5000/login
   ```

3. **Login in 2 clicks!**
   - Click "Send OTP"
   - Click "Verify & Login"

---

## 🔒 For Production

**Remember to change these before deploying:**

1. **Remove hardcoded OTP:**
   - Edit `otp_service.py`
   - Uncomment random OTP generation

2. **Remove pre-filled values:**
   - Edit `templates/login.html`
   - Remove `value="9876543210"` from phone input
   - Remove `value="12345"` from OTP input

3. **Enable real SMS:**
   - Set `SMS_PROVIDER` in `.env`
   - Add SMS provider credentials

---

## ✅ Success!

**Your login is now super easy!**

Just remember:
- Phone: `9876543210`
- OTP: `12345`

**Happy testing!** 🎉

