# 🚂 Railway Deployment Guide

## 🎯 **Deploy Your Kirana App to Railway**

Complete step-by-step guide to deploy your app to Railway.app

---

## 📋 **Prerequisites**

- ✅ GitHub account
- ✅ Railway account (free tier available)
- ✅ Your code pushed to GitHub
- ✅ Firebase credentials (firbasekey.json)
- ✅ WATI API credentials

---

## 🚀 **Step 1: Prepare for Deployment**

### **1.1 Verify Files**

Make sure these files exist:

- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Railway start command
- ✅ `railway.json` - Railway configuration
- ✅ `firbasekey.json` - Firebase credentials
- ✅ `.env` - Environment variables (for reference)

### **1.2 Test Locally**

```bash
python app.py
```

Make sure everything works locally first!

---

## 🌐 **Step 2: Create Railway Account**

### **2.1 Sign Up**

1. Go to: https://railway.app/
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with **GitHub** (recommended)
4. Authorize Railway to access your GitHub

### **2.2 Free Tier**

Railway offers:

- ✅ $5 free credit per month
- ✅ Enough for testing and small apps
- ✅ No credit card required initially

---

## 📦 **Step 3: Deploy from GitHub**

### **3.1 Create New Project**

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: **`kiranabuddy`**
4. Railway will automatically detect it's a Python app

### **3.2 Wait for Initial Build**

Railway will:

- ✅ Clone your repository
- ✅ Install dependencies from `requirements.txt`
- ✅ Build the app
- ⏳ This takes 2-3 minutes

---

## ⚙️ **Step 4: Configure Environment Variables**

### **4.1 Open Settings**

1. Click on your deployed service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**

### **4.2 Add All Variables**

Add these one by one:

#### **Flask Configuration:**

```
SECRET_KEY=kirana-secret-key-production-2024
FLASK_ENV=production
PORT=5000
```

#### **Firebase Configuration:**

```
GOOGLE_APPLICATION_CREDENTIALS=firbasekey.json
FIREBASE_PROJECT_ID=kiranabuddy-55330
```

#### **OpenAI Configuration:**

```
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

#### **WATI Configuration:**

```
WATI_API_KEY=your-wati-api-key
WATI_BASE_URL=https://eu-app-api.wati.io
WATI_WEBHOOK_SECRET=your-wati-webhook-secret
```

#### **App Settings:**

```
MAX_VOICE_FILE_SIZE=26214400
```

### **4.3 Save Variables**

Click **"Add"** for each variable.

---

## 🔑 **Step 5: Add Firebase Credentials**

### **Method 1: Using Railway CLI (Recommended)**

#### **5.1 Install Railway CLI**

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Or download from: https://docs.railway.app/develop/cli
```

#### **5.2 Login**

```bash
railway login
```

#### **5.3 Link Project**

```bash
cd C:\Users\Archana\Downloads\kiranaBook
railway link
```

Select your project from the list.

#### **5.4 Upload Firebase Key**

```bash
railway run --service=web -- echo "Uploading firbasekey.json"
```

Then manually copy the file through Railway dashboard.

### **Method 2: Using Environment Variable (Easier)**

#### **5.1 Convert JSON to Base64**

```bash
# Windows PowerShell
$content = Get-Content firbasekey.json -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)
$base64 | Set-Clipboard
```

#### **5.2 Add to Railway**

1. Go to Railway Variables
2. Add new variable:
   ```
   FIREBASE_CREDENTIALS_BASE64=<paste-base64-here>
   ```

#### **5.3 Update config.py**

We'll need to decode this in the app (I'll create a script for this).

---

## 🌍 **Step 6: Get Your Deployment URL**

### **6.1 Generate Domain**

1. Go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**

You'll get a URL like:

```
https://kiranabuddy-production.up.railway.app
```

### **6.2 Test Your Deployment**

Open the URL in browser:

```
https://your-app.up.railway.app/
```

You should see:

```json
{
  "status": "ok",
  "service": "Kirana Shop Management API"
}
```

---

## 🔗 **Step 7: Configure WATI Webhook**

### **7.1 Get Your Railway URL**

Copy your Railway URL:

```
https://kiranabuddy-production.up.railway.app
```

### **7.2 Update WATI Webhook**

1. Login to: https://eu-app.wati.io
2. Go to: **Settings** → **Webhooks**
3. Update webhook URL:
   ```
   https://kiranabuddy-production.up.railway.app/webhook
   ```
4. Save

---

## ✅ **Step 8: Test End-to-End**

### **8.1 Test Health Check**

```bash
curl https://your-app.up.railway.app/
```

### **8.2 Test via WhatsApp**

Send message to your WATI number (`+31 683078160`):

```
Add 10 Maggi
```

You should get automated reply:

```
✅ 10 Maggi add ho gaya! Total stock: 10 pieces
```

### **8.3 Check Logs**

In Railway dashboard:

1. Click on your service
2. Go to **"Deployments"** tab
3. Click **"View Logs"**
4. See real-time logs

---

## 📊 **Step 9: Monitor Your App**

### **9.1 View Metrics**

Railway shows:

- ✅ CPU usage
- ✅ Memory usage
- ✅ Network traffic
- ✅ Request count

### **9.2 View Logs**

Real-time logs show:

- ✅ Incoming requests
- ✅ Processed commands
- ✅ Errors (if any)

---

## 🔄 **Step 10: Auto-Deploy Updates**

### **10.1 Enable Auto-Deploy**

Railway automatically deploys when you push to GitHub!

### **10.2 Update Your App**

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
```

Railway will:

- ✅ Detect the push
- ✅ Build new version
- ✅ Deploy automatically
- ✅ Zero downtime!

---

## 🆘 **Troubleshooting**

### **Problem: Build Failed**

**Check:**

- ✅ `requirements.txt` is correct
- ✅ All dependencies are listed
- ✅ Python version compatible

**Solution:**

```bash
# Test locally first
pip install -r requirements.txt
python app.py
```

### **Problem: App Crashes**

**Check Logs:**

1. Railway Dashboard → Deployments → View Logs
2. Look for error messages

**Common Issues:**

- ❌ Missing environment variables
- ❌ Firebase credentials not found
- ❌ Port binding issue

### **Problem: Webhook Not Working**

**Check:**

- ✅ Webhook URL is correct in WATI
- ✅ App is running (check Railway status)
- ✅ Logs show incoming requests

---

## 💰 **Pricing**

### **Free Tier:**

- ✅ $5 credit per month
- ✅ ~500 hours of runtime
- ✅ Perfect for testing

### **Paid Plans:**

- 💳 Pay as you go
- 💳 $0.000231 per GB-hour
- 💳 Usually $5-20/month for small apps

---

## ✅ **Deployment Checklist**

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Project deployed from GitHub
- [ ] All environment variables added
- [ ] Firebase credentials configured
- [ ] Domain generated
- [ ] Health check passes
- [ ] WATI webhook updated
- [ ] WhatsApp test successful
- [ ] Logs monitored

---

**Your app is now live on Railway!** 🎉🚂

**Next: I'll create helper scripts for Firebase credentials handling.**
