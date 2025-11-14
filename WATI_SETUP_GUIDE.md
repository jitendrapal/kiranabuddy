# 📱 WATI WhatsApp Integration Guide

## 🎯 **Complete Guide to Integrate WATI with Your Kirana App**

---

## 📋 **What is WATI?**

WATI (WhatsApp Team Inbox) is an official WhatsApp Business API provider that allows you to:
- Send and receive WhatsApp messages programmatically
- Automate customer interactions
- Integrate WhatsApp with your applications

---

## 🚀 **Step-by-Step Setup**

### **Step 1: Create WATI Account**

#### **Option A: Free Trial (Recommended for Testing)**

1. **Visit:** https://www.wati.io/
2. **Click:** "Start Free Trial" or "Get Started"
3. **Sign Up:**
   - Enter your email
   - Create password
   - Verify email
4. **Get 7-day free trial** with demo number

#### **Option B: Request Demo**

1. **Visit:** https://www.wati.io/request-demo/
2. **Fill form:**
   - Name
   - Email
   - Phone
   - Company
3. **Submit** and wait for demo credentials

---

### **Step 2: Login to WATI Dashboard**

1. **Go to:** https://app.wati.io/login
2. **Enter credentials**
3. **You'll see the dashboard**

---

### **Step 3: Get Your API Key**

#### **Method 1: From Settings**

1. Click **profile icon** (top right corner)
2. Go to **"Settings"**
3. Click **"API Access"** or **"Integrations"**
4. Find **"API Key"** section
5. Click **"Generate API Key"** or **"Copy"**

#### **Method 2: From API Docs**

1. Click **"API Docs"** in sidebar
2. Look for **"Authentication"** section
3. Your API key will be shown there

#### **Your API Key looks like:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5ZjU4YzQ4Yi0xMjM0LTU2NzgtOTBhYi1jZGVmMTIzNDU2NzgiLCJ1bmlxdWVfbmFtZSI6InlvdXJlbWFpbEBleGFtcGxlLmNvbSIsIm5hbWVpZCI6InlvdXJlbWFpbEBleGFtcGxlLmNvbSIsImVtYWlsIjoieW91cmVtYWlsQGV4YW1wbGUuY29tIiwiYXV0aF90aW1lIjoiMDEvMDEvMjAyNCAwMDowMDowMCIsImRiX25hbWUiOiJ3YXRpLXByb2QiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6Imh0dHBzOi8vd2F0aS5pbyIsImF1ZCI6Imh0dHBzOi8vd2F0aS5pbyJ9.abcdefghijklmnopqrstuvwxyz1234567890
```

---

### **Step 4: Get Your Base URL**

Your base URL depends on your server location:

| Region | Base URL |
|--------|----------|
| 🇮🇳 **India** | `https://live-server.wati.io` |
| 🇺🇸 **USA** | `https://live-us-server.wati.io` |
| 🇪🇺 **Europe** | `https://live-eu-server.wati.io` |
| 🌏 **Asia Pacific** | `https://live-ap-server.wati.io` |

**How to find your region:**
1. Check your WATI dashboard URL
2. If it says `app.wati.io` → Use India server
3. If it says `app-us.wati.io` → Use US server
4. Or check in Settings → Account Info

---

### **Step 5: Update .env File**

Open your `.env` file and update:

```env
# WATI Configuration
WATI_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Paste your actual API key
WATI_BASE_URL=https://live-server.wati.io              # Use your region's URL
WATI_WEBHOOK_SECRET=your-webhook-secret                # Optional for now
```

**Example with real values:**
```env
WATI_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI5ZjU4YzQ4Yi0xMjM0LTU2NzgtOTBhYi1jZGVmMTIzNDU2NzgiLCJ1bmlxdWVfbmFtZSI6InlvdXJlbWFpbEBleGFtcGxlLmNvbSIsIm5hbWVpZCI6InlvdXJlbWFpbEBleGFtcGxlLmNvbSIsImVtYWlsIjoieW91cmVtYWlsQGV4YW1wbGUuY29tIiwiYXV0aF90aW1lIjoiMDEvMDEvMjAyNCAwMDowMDowMCIsImRiX25hbWUiOiJ3YXRpLXByb2QiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBRE1JTklTVFJBVE9SIiwiZXhwIjoyNTM0MDIzMDA4MDAsImlzcyI6Imh0dHBzOi8vd2F0aS5pbyIsImF1ZCI6Imh0dHBzOi8vd2F0aS5pbyJ9.abcdefghijklmnopqrstuvwxyz1234567890
WATI_BASE_URL=https://live-server.wati.io
WATI_WEBHOOK_SECRET=my-secret-key-123
```

---

### **Step 6: Test the Connection**

Create a test script to verify WATI is working:

```bash
python test_wati_connection.py
```

(I'll create this script for you)

---

## 🔗 **Step 7: Setup Webhook (To Receive Messages)**

### **What is a Webhook?**

A webhook is a URL that WATI will call when someone sends you a WhatsApp message.

### **Setup Steps:**

#### **1. Get Your Server URL**

You need a **public URL** for your server. Options:

**Option A: Use ngrok (for testing)**
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5000
```

You'll get a URL like:
```
https://abc123.ngrok.io
```

**Option B: Deploy to cloud (for production)**
- Heroku
- AWS
- Google Cloud
- DigitalOcean

#### **2. Configure Webhook in WATI**

1. **Login to WATI dashboard**
2. **Go to:** Settings → Webhooks
3. **Click:** "Add Webhook" or "Configure"
4. **Enter details:**
   - **Webhook URL:** `https://your-server.com/webhook`
   - **Events:** Select "Message Received"
   - **Secret:** Create a secret key (optional)
5. **Save**

#### **3. Your Webhook URL Format:**

```
https://your-domain.com/webhook
```

Example with ngrok:
```
https://abc123.ngrok.io/webhook
```

---

## 📞 **Step 8: Get Your WhatsApp Number**

### **WATI provides you with a WhatsApp Business number**

1. **Go to:** WATI Dashboard
2. **Look for:** "Phone Number" or "WhatsApp Number"
3. **You'll see:** Your assigned WhatsApp number

Example:
```
+91 98765 43210
```

This is the number customers will message!

---

## ✅ **Step 9: Verify Setup**

Run the verification script:

```bash
python test_wati_setup.py
```

This will check:
- ✅ API key is valid
- ✅ Can connect to WATI
- ✅ Can send test message
- ✅ Webhook is configured

---

## 🧪 **Step 10: Test End-to-End**

### **1. Start Your App**

```bash
python run_no_cache.py
```

### **2. Send WhatsApp Message**

From your phone, send a message to your WATI WhatsApp number:

```
Add 10 Maggi
```

### **3. Check Response**

You should receive a reply:

```
✅ 10 Maggi add ho gaya! Total stock: 10 pieces
```

---

## 🎯 **Quick Start Checklist**

- [ ] Created WATI account
- [ ] Got API key from dashboard
- [ ] Identified correct base URL (region)
- [ ] Updated `.env` file with credentials
- [ ] Tested connection with test script
- [ ] Setup webhook (if receiving messages)
- [ ] Got WhatsApp number from WATI
- [ ] Sent test message
- [ ] Received automated reply

---

## 💡 **Tips**

### **For Testing (Free Trial):**
- ✅ Use WATI's demo number
- ✅ Use ngrok for webhook
- ✅ Test with your own phone

### **For Production:**
- ✅ Get paid WATI plan
- ✅ Use your own WhatsApp Business number
- ✅ Deploy to cloud server
- ✅ Use proper domain for webhook

---

## 🆘 **Troubleshooting**

### **Problem: Can't find API key**

**Solution:**
1. Login to https://app.wati.io
2. Click profile icon → Settings
3. Look for "API Access" or "Integrations"
4. Generate new API key if needed

### **Problem: API key not working**

**Solution:**
1. Check if key is copied completely (very long string)
2. No extra spaces before/after
3. Check if trial expired
4. Regenerate API key

### **Problem: Wrong base URL**

**Solution:**
1. Check your WATI dashboard URL
2. Match region with base URL
3. Try different regional URLs

### **Problem: Webhook not receiving messages**

**Solution:**
1. Make sure server is running
2. Check ngrok is active
3. Verify webhook URL in WATI
4. Check webhook secret matches

---

## 📚 **Resources**

- **WATI Website:** https://www.wati.io/
- **WATI Dashboard:** https://app.wati.io/
- **WATI API Docs:** https://docs.wati.io/
- **Support:** support@wati.io

---

**Next: I'll create test scripts to help you verify the setup!** 🚀

