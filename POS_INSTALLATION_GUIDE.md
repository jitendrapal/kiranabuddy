# POS System Installation Guide

## Overview

This guide helps you install KiranaBuddy on a **dedicated POS device** (tablet, touchscreen PC, or POS terminal) so it runs constantly and starts automatically on boot.

## Supported POS Devices

### ✅ Recommended Devices

1. **Windows Tablet/PC** (Most Common)
   - Windows 10/11 tablet
   - Touchscreen all-in-one PC
   - Regular PC with touchscreen monitor
   - Examples: Dell Venue, Surface Pro, HP EliteOne

2. **Android Tablet** (Budget-Friendly)
   - 10" or larger Android tablet
   - Examples: Samsung Tab, Lenovo Tab, Amazon Fire HD

3. **Linux Mini PC** (Advanced)
   - Raspberry Pi 4/5
   - Intel NUC
   - Any Linux mini PC

4. **iPad** (Premium)
   - iPad Air or iPad Pro
   - 10.2" or larger recommended

## Installation Options

### Option A: Cloud Deployment (Recommended)
**Best for:** Multiple devices, remote access, professional setup

- Deploy app to cloud (Render, Railway, Heroku)
- Access from any device via URL
- Always online, no local installation needed
- **See: CLOUD_DEPLOYMENT_GUIDE.md**

### Option B: Local Installation (This Guide)
**Best for:** Single device, offline capability, full control

- Install app directly on POS device
- Runs locally on the device
- Works offline (after initial setup)
- **Continue reading below**

---

## Option B: Local Installation Steps

### Step 1: Choose Your Device Type

Click the section that matches your POS device:
- [Windows POS Device](#windows-pos-installation)
- [Android Tablet](#android-tablet-installation)
- [Linux/Raspberry Pi](#linux-pos-installation)
- [iPad](#ipad-installation)

---

## Windows POS Installation

### Requirements
- Windows 10 or 11
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Internet connection (for initial setup)
- Admin access

### Step 1: Install Python

1. Download Python 3.11 from: https://www.python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Click "Install Now"
4. Verify: Open Command Prompt, type `python --version`

### Step 2: Install Git (Optional but Recommended)

1. Download from: https://git-scm.com/download/win
2. Install with default settings
3. Verify: `git --version`

### Step 3: Download KiranaBuddy

**Option A: Using Git**
```cmd
cd C:\
git clone <your-repo-url> KiranaBuddy
cd KiranaBuddy
```

**Option B: Manual Download**
1. Download ZIP from your repository
2. Extract to `C:\KiranaBuddy`
3. Open folder in Command Prompt

### Step 4: Install Dependencies

```cmd
cd C:\KiranaBuddy
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Environment

1. Copy `.env.example` to `.env` (if exists)
2. Edit `.env` file with your settings
3. Make sure `firbasekey.json` is in the folder

### Step 6: Test the App

```cmd
python app.py
```

Open browser: `http://localhost:5000`

If it works, press `Ctrl+C` to stop.

### Step 7: Create Auto-Start Script

See: [Windows Auto-Start Setup](#windows-auto-start)

---

## Android Tablet Installation

### Requirements
- Android 8.0 or higher
- 2GB RAM minimum
- Chrome browser installed
- Internet connection

### Option 1: Access Cloud Deployment (Easiest)

1. Deploy app to cloud (see CLOUD_DEPLOYMENT_GUIDE.md)
2. Open Chrome on tablet
3. Go to your app URL (e.g., `https://yourapp.onrender.com`)
4. Tap menu (⋮) → "Add to Home Screen"
5. Name it "KiranaBuddy POS"
6. Tap "Add"
7. Icon appears on home screen
8. Open from home screen → runs like an app!

### Option 2: Local Server + Tablet Access

1. Install app on a Windows PC (see above)
2. Find PC's IP address: `ipconfig` → look for IPv4
3. On tablet, open Chrome
4. Go to `http://[PC-IP]:5000` (e.g., `http://192.168.1.100:5000`)
5. Add to home screen (steps above)

### Kiosk Mode Setup (Android)

1. Install "Kiosk Browser" from Play Store
2. Set KiranaBuddy URL as homepage
3. Enable full-screen mode
4. Disable navigation bars
5. Set as default launcher (optional)

---

## Linux POS Installation

### For Raspberry Pi / Ubuntu / Debian

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Python & Dependencies

```bash
sudo apt install -y python3 python3-pip python3-venv git
```

### Step 3: Download KiranaBuddy

```bash
cd /home/pi  # or your home directory
git clone <your-repo-url> KiranaBuddy
cd KiranaBuddy
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Environment

```bash
cp .env.example .env  # if exists
nano .env  # edit configuration
```

### Step 6: Test the App

```bash
python app.py
```

Open browser: `http://localhost:5000`

### Step 7: Create Auto-Start Service

See: [Linux Auto-Start Setup](#linux-auto-start)

---

## iPad Installation

### Requirements
- iPad with iOS 14 or higher
- Safari or Chrome browser
- Internet connection

### Setup (Cloud Deployment Required)

1. Deploy app to cloud (see CLOUD_DEPLOYMENT_GUIDE.md)
2. Open Safari on iPad
3. Go to your app URL
4. Tap Share button (□↑)
5. Tap "Add to Home Screen"
6. Name it "KiranaBuddy POS"
7. Tap "Add"
8. Open from home screen

### Guided Access (Kiosk Mode)

1. Settings → Accessibility → Guided Access
2. Turn on Guided Access
3. Set passcode
4. Open KiranaBuddy app
5. Triple-click home button
6. Tap "Start"
7. Device locked to app only!

---

## Next Steps

After installation, set up:
1. [Auto-Start on Boot](#auto-start-setup)
2. [Kiosk Mode](#kiosk-mode-setup)
3. [Customer Display](#customer-display-setup)
4. [Backup & Updates](#backup-and-updates)

Continue to next section for detailed setup...

