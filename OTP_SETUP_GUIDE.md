# 📱 OTP Login Setup Guide

Complete guide to set up OTP (One-Time Password) authentication for your Kirana Shop Manager app.

---

## ✅ What's Implemented

Your app now has:
- ✅ **OTP Login System** - Phone number based authentication
- ✅ **Automatic User Creation** - New users are created on first login
- ✅ **Session Management** - Secure login sessions
- ✅ **Multiple SMS Providers** - Twilio, MSG91, Fast2SMS support
- ✅ **Development Mode** - Console OTP for testing
- ✅ **Beautiful UI** - Modern, responsive login page
- ✅ **Auto Shop Creation** - Each user gets their own shop

---

## 🚀 Quick Start (Development Mode)

**For testing, OTP is printed to console - no SMS setup needed!**

1. **Start the app:**
   ```bash
   python app.py
   ```

2. **Open login page:**
   ```
   http://127.0.0.1:5000/login
   ```

3. **Enter phone number:** Any 10-digit number (e.g., 9876543210)

4. **Check console:** OTP will be printed like this:
   ```
   ============================================================
   📱 OTP for 9876543210: 123456
   ⏰ Valid for 10 minutes
   ============================================================
   ```

5. **Enter OTP:** Copy the OTP from console and paste in the app

6. **Enter name:** (for new users only)

7. **Login!** You'll be redirected to the app

---

## 📲 Production Setup (Real SMS)

### **Option 1: MSG91 (Recommended for India) 🇮🇳**

**Why MSG91?**
- ✅ Best for Indian phone numbers
- ✅ Affordable (₹0.15 per SMS)
- ✅ Fast delivery
- ✅ Easy setup

**Setup Steps:**

1. **Sign up:** https://msg91.com/signup
2. **Get API Key:** Dashboard → API → Auth Key
3. **Create Template:**
   - Go to SMS → Templates
   - Create OTP template
   - Get Template ID

4. **Add to .env file:**
   ```env
   SMS_PROVIDER=msg91
   MSG91_AUTH_KEY=your_auth_key_here
   MSG91_SENDER_ID=KIRANA
   MSG91_TEMPLATE_ID=your_template_id_here
   ```

5. **Restart app** and test!

---

### **Option 2: Twilio (International)**

**Why Twilio?**
- ✅ Works worldwide
- ✅ Reliable
- ✅ Good documentation

**Setup Steps:**

1. **Sign up:** https://www.twilio.com/try-twilio
2. **Get credentials:**
   - Account SID
   - Auth Token
   - Phone Number (buy one from Twilio)

3. **Install Twilio:**
   ```bash
   pip install twilio
   ```

4. **Add to .env file:**
   ```env
   SMS_PROVIDER=twilio
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

5. **Restart app** and test!

---

### **Option 3: Fast2SMS (India)**

**Why Fast2SMS?**
- ✅ Indian service
- ✅ Simple API
- ✅ Affordable

**Setup Steps:**

1. **Sign up:** https://www.fast2sms.com/
2. **Get API Key:** Dashboard → API Keys

3. **Add to .env file:**
   ```env
   SMS_PROVIDER=fast2sms
   FAST2SMS_API_KEY=your_api_key_here
   ```

4. **Restart app** and test!

---

## 🔧 Configuration

### **Environment Variables**

Add these to your `.env` file:

```env
# Session secret (required)
SECRET_KEY=your-secret-key-here-change-this

# SMS Provider (console, twilio, msg91, fast2sms)
SMS_PROVIDER=console

# MSG91 (if using)
MSG91_AUTH_KEY=
MSG91_SENDER_ID=KIRANA
MSG91_TEMPLATE_ID=

# Twilio (if using)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# Fast2SMS (if using)
FAST2SMS_API_KEY=
```

---

## 🎯 How It Works

### **Login Flow:**

```
1. User enters phone number
   ↓
2. System generates 6-digit OTP
   ↓
3. OTP sent via SMS (or console in dev mode)
   ↓
4. User enters OTP
   ↓
5. System verifies OTP
   ↓
6. If new user: Ask for name, create shop
   ↓
7. Create session and login
   ↓
8. Redirect to app
```

### **Security Features:**

- ✅ **OTP Expiry:** 10 minutes validity
- ✅ **Max Attempts:** 3 attempts per OTP
- ✅ **One-time Use:** OTP can only be used once
- ✅ **Session Security:** Secure session management
- ✅ **Auto Invalidation:** Old OTPs invalidated when new one is sent

---

## 📱 Testing

### **Test Scenarios:**

1. **New User Login:**
   - Enter phone: 9876543210
   - Get OTP from console
   - Enter OTP
   - Enter name: "Test User"
   - Should create shop and login

2. **Existing User Login:**
   - Enter same phone again
   - Get OTP
   - Enter OTP
   - Should login directly (no name required)

3. **Wrong OTP:**
   - Enter wrong OTP
   - Should show error with remaining attempts

4. **Expired OTP:**
   - Wait 10 minutes
   - Try to use OTP
   - Should show "OTP expired" error

5. **Resend OTP:**
   - Click "Resend OTP"
   - Should get new OTP

---

## 🎨 Customization

### **Change OTP Length:**
Edit `otp_service.py`:
```python
self.otp_length = 6  # Change to 4 or 8
```

### **Change OTP Validity:**
Edit `otp_service.py`:
```python
self.otp_validity_minutes = 10  # Change to 5 or 15
```

### **Change Max Attempts:**
Edit `otp_service.py`:
```python
self.max_attempts = 3  # Change to 5
```

### **Customize SMS Message:**
Edit `otp_service.py` → `send_otp()` method

---

## 🚀 Deployment

### **For Railway/Heroku:**

1. Add environment variables in dashboard
2. Set `SMS_PROVIDER` to your chosen provider
3. Add provider credentials
4. Deploy!

### **For Production:**

1. **Use HTTPS** (required for sessions)
2. **Set strong SECRET_KEY**
3. **Use real SMS provider** (not console)
4. **Enable rate limiting** (prevent spam)

---

## 📞 SMS Provider Comparison

| Provider | Best For | Cost | Setup | Speed |
|----------|----------|------|-------|-------|
| **MSG91** | India | ₹0.15/SMS | Easy | Fast |
| **Twilio** | Global | $0.0075/SMS | Medium | Fast |
| **Fast2SMS** | India | ₹0.10/SMS | Easy | Medium |
| **Console** | Testing | Free | None | Instant |

---

## ✅ Success!

Your OTP login system is ready! 🎉

**Next Steps:**
1. Test in development mode (console)
2. Choose SMS provider for production
3. Add credentials to .env
4. Deploy and test with real SMS

---

**Need help?** Check the code in:
- `otp_service.py` - OTP logic
- `app.py` - Login routes
- `templates/login.html` - Login UI
- `static/login.js` - Login JavaScript

