# 🧪 Testing OTP Integration

## Quick Test Guide

### **1. Start the App**

```bash
python app.py
```

You should see:
```
✅ Database initialized
📱 OTP Service initialized
   Provider: console
   Dev Mode: True
   OTP: 123456
```

---

### **2. Test via Web Interface**

**Step 1: Open Login Page**
```
http://localhost:5000/login
```

**Step 2: Enter Phone Number**
- Enter: `9876543210`
- Click "Send OTP"

**Step 3: Check Console**
You should see:
```
============================================================
📱 OTP for 9876543210: 123456
⏰ Valid for 5 minutes
============================================================
```

**Step 4: Enter OTP**
- Enter: `123456`
- Enter Name: `Test User` (for new users)
- Click "Verify"

**Step 5: Success!**
- You should be redirected to `/test`
- Session created with user details

---

### **3. Test via API (cURL)**

**Send OTP:**
```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "9876543210"}'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "OTP sent to 9876543210",
  "otp_id": "uuid-here",
  "expires_in_minutes": 5,
  "provider": "console",
  "dev_otp": "123456",
  "dev_mode": true
}
```

**Verify OTP:**
```bash
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "9876543210",
    "otp": "123456",
    "name": "Test User"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "phone": "9876543210",
    "name": "Test User",
    "shop_id": "uuid-here",
    "role": "owner"
  },
  "redirect_url": "/test"
}
```

---

### **4. Test Security Features**

#### **A. Rate Limiting (3 OTP/hour)**

Send 4 OTPs quickly:
```bash
for i in {1..4}; do
  echo "Request $i:"
  curl -X POST http://localhost:5000/api/auth/send-otp \
    -H "Content-Type: application/json" \
    -d '{"phone": "9999999999"}'
  echo -e "\n"
  sleep 2
done
```

**4th Request Should Fail:**
```json
{
  "success": false,
  "message": "Too many OTP requests. Please try again after 1 hour.",
  "error_code": "RATE_LIMIT_EXCEEDED"
}
```

#### **B. Resend Cooldown (30 seconds)**

Send 2 OTPs immediately:
```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "8888888888"}'

# Immediately send again
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "8888888888"}'
```

**2nd Request Should Fail:**
```json
{
  "success": false,
  "message": "Please wait 28 seconds before requesting new OTP",
  "error_code": "RESEND_COOLDOWN"
}
```

#### **C. Wrong OTP Attempts (Max 5)**

Try wrong OTP 6 times:
```bash
# First send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "7777777777"}'

# Try wrong OTP 6 times
for i in {1..6}; do
  echo "Attempt $i:"
  curl -X POST http://localhost:5000/api/auth/verify-otp \
    -H "Content-Type: application/json" \
    -d '{"phone": "7777777777", "otp": "999999"}'
  echo -e "\n"
done
```

**Responses:**
```json
// Attempt 1-5
{
  "success": false,
  "message": "Invalid OTP. 4 attempts remaining.",
  "error_code": "INVALID_OTP",
  "remaining_attempts": 4
}

// Attempt 6
{
  "success": false,
  "message": "Too many failed attempts. Please request a new OTP.",
  "error_code": "MAX_ATTEMPTS_EXCEEDED"
}
```

#### **D. OTP Expiry (5 minutes)**

This requires waiting 5 minutes:
```bash
# Send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "6666666666"}'

# Wait 5+ minutes...
sleep 301

# Try to verify
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "6666666666", "otp": "123456"}'
```

**Should Fail:**
```json
{
  "success": false,
  "message": "OTP expired. Please request a new one.",
  "error_code": "OTP_EXPIRED"
}
```

#### **E. OTP Reuse Prevention**

```bash
# Send OTP
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "5555555555"}'

# Verify successfully
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "5555555555", "otp": "123456", "name": "Test"}'

# Try to use same OTP again
curl -X POST http://localhost:5000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "5555555555", "otp": "123456"}'
```

**2nd Verify Should Fail:**
```json
{
  "success": false,
  "message": "OTP already used. Please request a new one.",
  "error_code": "OTP_ALREADY_USED"
}
```

---

### **5. Test Production SMS (Optional)**

If you've configured MSG91/Twilio/Fast2SMS:

**Update .env:**
```bash
OTP_DEV_MODE=false
SMS_PROVIDER=msg91  # or twilio or fast2sms
# Add your provider credentials
```

**Restart app and test:**
```bash
curl -X POST http://localhost:5000/api/auth/send-otp \
  -H "Content-Type: application/json" \
  -d '{"phone": "YOUR_REAL_PHONE_NUMBER"}'
```

**Check your phone for SMS!** 📱

---

## ✅ Test Checklist

- [ ] App starts without errors
- [ ] Login page loads at `/login`
- [ ] Can send OTP (console shows OTP)
- [ ] Can verify correct OTP
- [ ] Wrong OTP shows error
- [ ] Rate limiting works (4th request fails)
- [ ] Resend cooldown works (immediate resend fails)
- [ ] Max attempts works (6th attempt fails)
- [ ] OTP expiry works (after 5 minutes)
- [ ] OTP reuse prevented (can't use twice)
- [ ] New user registration works
- [ ] Existing user login works
- [ ] Session created after login
- [ ] Logout works

---

## 🐛 Troubleshooting

### **Issue: OTP not showing in console**

**Check:**
```python
# In otp_service.py
print(f"SMS Provider: {self.sms_provider}")
print(f"Dev Mode: {self.dev_mode}")
```

**Solution:**
```bash
# Make sure .env has:
OTP_DEV_MODE=true
SMS_PROVIDER=console
```

### **Issue: "No OTP found" error**

**Check Firestore:**
- Open Firebase Console
- Go to Firestore Database
- Check `otps` collection
- Verify OTP document exists

**Solution:**
- Make sure database connection is working
- Check Firebase credentials

### **Issue: Rate limit not working**

**Check:**
- Firestore `otps` collection has documents
- `created_at` field is datetime object
- Using different phone numbers for testing

### **Issue: SMS not sending (production)**

**Check:**
```python
# In console, look for:
print(f"SMS Provider: {self.sms_provider}")
print(f"Provider credentials configured: {bool(self.msg91_auth_key)}")
```

**Solution:**
- Verify .env has correct credentials
- Check SMS provider dashboard for errors
- Verify phone number format (+91 for India)

---

## 📊 Expected Console Output

```
🔧 Initializing database with:
   credentials_path: firbasekey.json
   project_id: kiranabuddy-55330
✅ Database initialized

📱 OTP Service initialized
   Provider: console
   Dev Mode: True
   OTP Length: 6
   Validity: 5 minutes
   Max Attempts: 5

 * Running on http://127.0.0.1:5000

📝 Creating OTP for phone: 9876543210
💾 Storing OTP: uuid-here, phone: 9876543210, hashed: False

============================================================
📱 OTP for 9876543210: 123456
⏰ Valid for 5 minutes
============================================================

🔍 Verifying OTP for phone: 9876543210
✅ OTP verified successfully!
```

---

**All tests passing? You're ready for production!** 🚀

