# 📱 Phone OTP Verification Implementation Guide

## 🎯 What You Need for Phone OTP Verification

### 1. **SMS Gateway Service Provider**

You need a third-party SMS service to send OTP messages. Popular options:

#### **Option A: Twilio (Most Popular)**

- **Website:** https://www.twilio.com/
- **Pricing:** Pay-as-you-go (₹0.50-₹1.50 per SMS in India)
- **Free Trial:** $15 credit
- **Features:**
  - Global coverage
  - High delivery rate
  - Detailed analytics
  - Phone number verification API
  - WhatsApp integration

#### **Option B: MSG91 (India-focused)**

- **Website:** https://msg91.com/
- **Pricing:** ₹0.15-₹0.25 per SMS
- **Free Trial:** 100 free SMS
- **Features:**
  - India-specific routes
  - Better delivery in India
  - OTP templates
  - Cheaper than Twilio for India

#### **Option C: Firebase Phone Authentication (Google)**

- **Website:** https://firebase.google.com/
- **Pricing:** Free for most use cases
- **Features:**
  - Built-in OTP verification
  - No SMS gateway needed
  - Automatic OTP reading on Android
  - reCAPTCHA for web

#### **Option D: AWS SNS (Amazon)**

- **Website:** https://aws.amazon.com/sns/
- **Pricing:** $0.00645 per SMS
- **Features:**
  - Scalable
  - Reliable
  - Global coverage

#### **Option E: Fast2SMS (India)**

- **Website:** https://www.fast2sms.com/
- **Pricing:** ₹0.10-₹0.20 per SMS
- **Free Trial:** 50 free SMS
- **Features:**
  - Very cheap for India
  - Good for startups

### 2. **Backend Requirements**

#### **A. Database Schema**

You need to store OTP data temporarily:

```sql
CREATE TABLE otp_verification (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone_number VARCHAR(15) NOT NULL,
    otp_code VARCHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INT DEFAULT 0,
    ip_address VARCHAR(45),
    INDEX idx_phone (phone_number),
    INDEX idx_expires (expires_at)
);
```

**For Firebase (Firestore):**

```javascript
{
  "otp_verifications": {
    "phone_number": "+919876543210",
    "otp_code": "123456",
    "created_at": "2024-01-15T10:30:00Z",
    "expires_at": "2024-01-15T10:35:00Z",
    "is_verified": false,
    "attempts": 0,
    "ip_address": "192.168.1.1"
  }
}
```

#### **B. Backend API Endpoints**

You need these endpoints:

**1. Send OTP**

```
POST /api/auth/send-otp
Request: { "phone_number": "+919876543210" }
Response: { "success": true, "message": "OTP sent successfully" }
```

**2. Verify OTP**

```
POST /api/auth/verify-otp
Request: { "phone_number": "+919876543210", "otp": "123456" }
Response: { "success": true, "token": "jwt_token_here" }
```

**3. Resend OTP**

```
POST /api/auth/resend-otp
Request: { "phone_number": "+919876543210" }
Response: { "success": true, "message": "OTP resent successfully" }
```

### 3. **Security Requirements**

#### **A. Rate Limiting**

Prevent spam and abuse:

- Max 3 OTP requests per phone number per hour
- Max 5 verification attempts per OTP
- Block IP after 10 failed attempts

#### **B. OTP Generation Rules**

- **Length:** 6 digits (recommended)
- **Validity:** 5 minutes (300 seconds)
- **Type:** Numeric only (easier to type)
- **Randomness:** Use cryptographically secure random generator

#### **C. Security Best Practices**

✅ Hash OTP before storing in database  
✅ Use HTTPS for all API calls  
✅ Implement CAPTCHA for web (prevent bots)  
✅ Log all OTP attempts with IP address  
✅ Expire OTP after successful verification  
✅ Don't send OTP in API response (security risk)  
✅ Validate phone number format before sending

### 4. **Frontend Requirements**

#### **A. UI Components Needed**

**1. Phone Number Input Screen**

```
┌─────────────────────────────────┐
│  Enter Your Phone Number       │
│                                 │
│  ┌───┬─────────────────────┐   │
│  │+91│ 9876543210          │   │
│  └───┴─────────────────────┘   │
│                                 │
│  [  Send OTP  ]                │
└─────────────────────────────────┘
```

**2. OTP Input Screen**

```
┌─────────────────────────────────┐
│  Enter OTP                      │
│  Sent to +91 9876543210         │
│                                 │
│  ┌───┬───┬───┬───┬───┬───┐    │
│  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │    │
│  └───┴───┴───┴───┴───┴───┘    │
│                                 │
│  Resend OTP in 00:45           │
│                                 │
│  [  Verify OTP  ]              │
└─────────────────────────────────┘
```

#### **B. Features to Implement**

✅ Country code selector (+91, +1, etc.)  
✅ Phone number validation  
✅ Auto-focus on OTP input boxes  
✅ Auto-submit when all digits entered  
✅ Countdown timer (5 minutes)  
✅ Resend OTP button (enabled after 30 seconds)  
✅ Loading states  
✅ Error messages  
✅ Success feedback

### 5. **Cost Estimation**

#### **For 1000 Users/Month:**

| Provider | Cost per SMS | Total Cost |
| -------- | ------------ | ---------- |
| Twilio   | ₹1.00        | ₹1,000     |
| MSG91    | ₹0.20        | ₹200       |
| Fast2SMS | ₹0.15        | ₹150       |
| Firebase | Free         | ₹0         |

**Note:** Assuming 1 OTP per user. If users request resend, multiply by 1.5-2x.

### 6. **Legal Requirements (India)**

#### **A. DLT Registration (Mandatory in India)**

**What is DLT?**

- Distributed Ledger Technology
- Required by TRAI (Telecom Regulatory Authority of India)
- All commercial SMS must be registered

**Steps:**

1. Register on DLT platform (Airtel, Jio, Vodafone, etc.)
2. Register your company/entity
3. Create SMS template (e.g., "Your OTP is {#var#}. Valid for 5 minutes.")
4. Get template approved
5. Get Principal Entity ID and Template ID
6. Provide these to SMS gateway

**Cost:** ₹500-₹1000 one-time registration

#### **B. Privacy Policy**

You must inform users:

- Why you're collecting phone numbers
- How you'll use them
- How long you'll store them
- Third-party services used (SMS gateway)

### 7. **Technical Implementation Steps**

#### **Step 1: Choose SMS Provider**

- Sign up for Twilio/MSG91/Firebase
- Get API credentials (Account SID, Auth Token)
- Add credits to account

#### **Step 2: Set Up Backend**

- Create database table for OTP storage
- Install SMS provider SDK
- Create API endpoints (send-otp, verify-otp)
- Implement rate limiting
- Add logging

#### **Step 3: Implement OTP Generation**

```python
import random
import hashlib
from datetime import datetime, timedelta

def generate_otp():
    return str(random.randint(100000, 999999))

def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()

def create_otp_record(phone_number):
    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    expires_at = datetime.now() + timedelta(minutes=5)

    # Save to database
    save_to_db(phone_number, hashed_otp, expires_at)

    return otp  # Send this via SMS
```

#### **Step 4: Send OTP via SMS**

```python
# Using Twilio
from twilio.rest import Client

def send_otp_sms(phone_number, otp):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is {otp}. Valid for 5 minutes. Do not share with anyone.",
        from_='+1234567890',  # Your Twilio number
        to=phone_number
    )

    return message.sid
```

#### **Step 5: Verify OTP**

```python
def verify_otp(phone_number, entered_otp):
    # Get OTP record from database
    record = get_from_db(phone_number)

    # Check if expired
    if datetime.now() > record.expires_at:
        return {"success": False, "message": "OTP expired"}

    # Check attempts
    if record.attempts >= 5:
        return {"success": False, "message": "Too many attempts"}

    # Verify OTP
    if hash_otp(entered_otp) == record.otp_code:
        mark_as_verified(phone_number)
        return {"success": True, "message": "Verified"}
    else:
        increment_attempts(phone_number)
        return {"success": False, "message": "Invalid OTP"}
```

#### **Step 6: Frontend Implementation**

```javascript
// Send OTP
async function sendOTP(phoneNumber) {
  const response = await fetch("/api/auth/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone_number: phoneNumber }),
  });

  const data = await response.json();
  return data;
}

// Verify OTP
async function verifyOTP(phoneNumber, otp) {
  const response = await fetch("/api/auth/verify-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      phone_number: phoneNumber,
      otp: otp,
    }),
  });

  const data = await response.json();
  return data;
}
```

### 8. **Complete Example: Flask Backend**

```python
from flask import Flask, request, jsonify
from twilio.rest import Client
import random
import hashlib
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'

# Initialize Firestore
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_otp():
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))

def hash_otp(otp):
    """Hash OTP for secure storage"""
    return hashlib.sha256(otp.encode()).hexdigest()

@app.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')

        # Validate phone number
        if not phone_number or len(phone_number) < 10:
            return jsonify({
                'success': False,
                'message': 'Invalid phone number'
            }), 400

        # Check rate limiting
        otp_ref = db.collection('otp_verifications').document(phone_number)
        otp_doc = otp_ref.get()

        if otp_doc.exists:
            data = otp_doc.to_dict()
            created_at = data.get('created_at')

            # Allow resend only after 30 seconds
            if (datetime.now() - created_at).seconds < 30:
                return jsonify({
                    'success': False,
                    'message': 'Please wait before requesting new OTP'
                }), 429

        # Generate OTP
        otp = generate_otp()
        hashed_otp = hash_otp(otp)

        # Send SMS via Twilio
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP is {otp}. Valid for 5 minutes. Do not share with anyone.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        # Save to Firestore
        otp_ref.set({
            'phone_number': phone_number,
            'otp_code': hashed_otp,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(minutes=5),
            'is_verified': False,
            'attempts': 0,
            'ip_address': request.remote_addr
        })

        return jsonify({
            'success': True,
            'message': 'OTP sent successfully',
            'message_sid': message.sid
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        entered_otp = data.get('otp')

        # Get OTP record
        otp_ref = db.collection('otp_verifications').document(phone_number)
        otp_doc = otp_ref.get()

        if not otp_doc.exists:
            return jsonify({
                'success': False,
                'message': 'No OTP found. Please request a new one.'
            }), 404

        otp_data = otp_doc.to_dict()

        # Check if expired
        if datetime.now() > otp_data['expires_at']:
            return jsonify({
                'success': False,
                'message': 'OTP expired. Please request a new one.'
            }), 400

        # Check attempts
        if otp_data['attempts'] >= 5:
            return jsonify({
                'success': False,
                'message': 'Too many failed attempts. Please request a new OTP.'
            }), 400

        # Verify OTP
        if hash_otp(entered_otp) == otp_data['otp_code']:
            # Mark as verified
            otp_ref.update({
                'is_verified': True,
                'verified_at': datetime.now()
            })

            # Generate JWT token or session
            # token = generate_jwt_token(phone_number)

            return jsonify({
                'success': True,
                'message': 'OTP verified successfully',
                # 'token': token
            }), 200
        else:
            # Increment attempts
            otp_ref.update({
                'attempts': otp_data['attempts'] + 1
            })

            return jsonify({
                'success': False,
                'message': 'Invalid OTP. Please try again.'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 9. **Complete Example: React Frontend**

```javascript
import React, { useState, useEffect } from "react";

function PhoneOTPVerification() {
  const [step, setStep] = useState(1); // 1: Phone, 2: OTP
  const [phoneNumber, setPhoneNumber] = useState("");
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [timer, setTimer] = useState(300); // 5 minutes
  const [canResend, setCanResend] = useState(false);

  // Countdown timer
  useEffect(() => {
    if (step === 2 && timer > 0) {
      const interval = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(interval);
    }
    if (timer === 0) {
      setError("OTP expired. Please request a new one.");
    }
  }, [step, timer]);

  // Enable resend after 30 seconds
  useEffect(() => {
    if (step === 2) {
      setTimeout(() => setCanResend(true), 30000);
    }
  }, [step]);

  const handleSendOTP = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch("/api/auth/send-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number: `+91${phoneNumber}` }),
      });

      const data = await response.json();

      if (data.success) {
        setStep(2);
        setTimer(300);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError("Failed to send OTP. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    setLoading(true);
    setError("");

    const otpCode = otp.join("");

    try {
      const response = await fetch("/api/auth/verify-otp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone_number: `+91${phoneNumber}`,
          otp: otpCode,
        }),
      });

      const data = await response.json();

      if (data.success) {
        alert("Phone verified successfully!");
        // Redirect or save token
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError("Failed to verify OTP. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleOTPChange = (index, value) => {
    if (value.length <= 1 && /^\d*$/.test(value)) {
      const newOtp = [...otp];
      newOtp[index] = value;
      setOtp(newOtp);

      // Auto-focus next input
      if (value && index < 5) {
        document.getElementById(`otp-${index + 1}`).focus();
      }

      // Auto-submit when all filled
      if (index === 5 && value) {
        handleVerifyOTP();
      }
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className="otp-container">
      {step === 1 ? (
        <div className="phone-input">
          <h2>Enter Your Phone Number</h2>
          <div className="input-group">
            <span>+91</span>
            <input
              type="tel"
              maxLength="10"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              placeholder="9876543210"
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button
            onClick={handleSendOTP}
            disabled={loading || phoneNumber.length !== 10}
          >
            {loading ? "Sending..." : "Send OTP"}
          </button>
        </div>
      ) : (
        <div className="otp-input">
          <h2>Enter OTP</h2>
          <p>Sent to +91 {phoneNumber}</p>
          <div className="otp-boxes">
            {otp.map((digit, index) => (
              <input
                key={index}
                id={`otp-${index}`}
                type="text"
                maxLength="1"
                value={digit}
                onChange={(e) => handleOTPChange(index, e.target.value)}
              />
            ))}
          </div>
          <p className="timer">Time remaining: {formatTime(timer)}</p>
          {error && <p className="error">{error}</p>}
          <button
            onClick={handleVerifyOTP}
            disabled={loading || otp.join("").length !== 6}
          >
            {loading ? "Verifying..." : "Verify OTP"}
          </button>
          <button
            onClick={handleSendOTP}
            disabled={!canResend || loading}
            className="resend"
          >
            Resend OTP
          </button>
        </div>
      )}
    </div>
  );
}

export default PhoneOTPVerification;
```

### 10. **Testing Checklist**

Before going live, test these scenarios:

✅ **Happy Path**

- [ ] Send OTP to valid phone number
- [ ] Receive SMS within 10 seconds
- [ ] Enter correct OTP
- [ ] Successfully verify

✅ **Error Cases**

- [ ] Invalid phone number format
- [ ] Expired OTP (wait 5 minutes)
- [ ] Wrong OTP (5 attempts)
- [ ] Rate limiting (3 requests/hour)
- [ ] Network failure handling

✅ **Security**

- [ ] OTP not visible in API response
- [ ] OTP hashed in database
- [ ] HTTPS enabled
- [ ] Rate limiting working
- [ ] IP logging enabled

✅ **UX**

- [ ] Loading states shown
- [ ] Error messages clear
- [ ] Timer countdown working
- [ ] Resend button enabled after 30s
- [ ] Auto-focus on OTP inputs
- [ ] Auto-submit when complete

---

## 📋 **Quick Summary: What You Need**

### **Mandatory:**

1. ✅ SMS Gateway account (Twilio/MSG91/Firebase)
2. ✅ Backend API (Flask/Node.js/Java)
3. ✅ Database (Firestore/MySQL/PostgreSQL)
4. ✅ Frontend UI (React/HTML/Android)
5. ✅ HTTPS certificate (for production)

### **For India:**

6. ✅ DLT registration (₹500-₹1000)
7. ✅ SMS template approval
8. ✅ Privacy policy

### **Optional but Recommended:**

9. ✅ Rate limiting
10. ✅ CAPTCHA (prevent bots)
11. ✅ Analytics/logging
12. ✅ Backup SMS provider

---

## 💰 **Total Cost Estimate (India)**

| Item                     | Cost                 |
| ------------------------ | -------------------- |
| DLT Registration         | ₹500 (one-time)      |
| SMS Gateway (MSG91)      | ₹0.20 per SMS        |
| Server Hosting           | ₹500-₹2000/month     |
| SSL Certificate          | Free (Let's Encrypt) |
| **Total for 1000 users** | **₹700-₹2700**       |

---

**Need help implementing this in your Kirana app? Let me know!** 📱✨
