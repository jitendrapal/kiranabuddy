# KiranaBuddy POS - Quick Start Guide

## 🚀 Get Your POS Running in 10 Minutes!

This is the **fastest way** to get KiranaBuddy running on your POS device.

---

## Choose Your Device

Click the option that matches your POS device:

### 🖥️ [Windows PC/Tablet](#windows-quick-start) ← Most Common
### 📱 [Android Tablet](#android-quick-start)
### 🍓 [Raspberry Pi](#raspberry-pi-quick-start)
### 🍎 [iPad](#ipad-quick-start)

---

## Windows Quick Start

### What You Need:
- Windows 10/11 PC or tablet
- Internet connection
- 10 minutes

### Steps:

**1. Install Python** (2 minutes)
- Go to: https://www.python.org/downloads/
- Download Python 3.11
- ✅ **IMPORTANT:** Check "Add Python to PATH"
- Click "Install Now"

**2. Download KiranaBuddy** (1 minute)
- Download this folder to `C:\KiranaBuddy`
- Or use Git: `git clone <repo-url> C:\KiranaBuddy`

**3. Install Dependencies** (3 minutes)
- Open Command Prompt
- Run:
  ```cmd
  cd C:\KiranaBuddy
  pip install -r requirements.txt
  ```

**4. Configure** (2 minutes)
- Make sure `.env` file exists
- Make sure `firbasekey.json` exists
- Edit `.env` if needed

**5. Start POS** (1 minute)
- Double-click `start_pos.bat`
- Browser opens automatically!
- Login and start scanning!

**6. Make it Auto-Start** (1 minute)
- Press `Win + R`
- Type: `shell:startup`
- Copy `start_pos.bat` shortcut here
- Done! Starts on boot now.

### 🎉 You're Done!
- App runs at: `http://localhost:5000`
- Bookmark it or add to home screen

---

## Android Quick Start

### What You Need:
- Android tablet (8.0+)
- Internet connection
- 5 minutes

### Option A: Cloud Access (Easiest)

**1. Deploy to Cloud** (one-time setup)
- Use Render, Railway, or Heroku
- See: `CLOUD_DEPLOYMENT_GUIDE.md`
- Get your app URL (e.g., `https://yourapp.onrender.com`)

**2. Add to Home Screen**
- Open Chrome on tablet
- Go to your app URL
- Tap menu (⋮) → "Add to Home Screen"
- Name it "KiranaBuddy POS"
- Tap "Add"

**3. Open from Home Screen**
- Tap the icon
- Runs like a native app!

### Option B: Local Server Access

**1. Install on Windows PC** (see above)

**2. Find PC's IP Address**
- On PC, open Command Prompt
- Type: `ipconfig`
- Note the IPv4 address (e.g., `192.168.1.100`)

**3. Access from Tablet**
- Open Chrome
- Go to: `http://192.168.1.100:5000`
- Add to home screen (steps above)

### 🎉 You're Done!
- Tap icon to open POS
- Works like a native app

---

## Raspberry Pi Quick Start

### What You Need:
- Raspberry Pi 4 or 5
- Raspberry Pi OS installed
- Internet connection
- 15 minutes

### Steps:

**1. Update System** (2 minutes)
```bash
sudo apt update
sudo apt upgrade -y
```

**2. Install Python** (1 minute)
```bash
sudo apt install -y python3 python3-pip python3-venv git
```

**3. Download KiranaBuddy** (2 minutes)
```bash
cd ~
git clone <repo-url> KiranaBuddy
cd KiranaBuddy
```

**4. Create Virtual Environment** (3 minutes)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Configure** (2 minutes)
```bash
# Make sure .env and firbasekey.json exist
nano .env  # Edit if needed
```

**6. Test Run** (1 minute)
```bash
python app.py
```
- Open browser: `http://localhost:5000`

**7. Set Auto-Start** (4 minutes)
```bash
# Make script executable
chmod +x start_pos.sh

# Add to crontab
crontab -e
# Add this line:
@reboot cd /home/pi/KiranaBuddy && ./start_pos.sh
```

**8. Reboot and Test**
```bash
sudo reboot
```

### 🎉 You're Done!
- App starts automatically on boot
- Access at: `http://localhost:5000`

---

## iPad Quick Start

### What You Need:
- iPad (iOS 14+)
- Internet connection
- Cloud-deployed app
- 5 minutes

### Steps:

**1. Deploy to Cloud** (one-time)
- See: `CLOUD_DEPLOYMENT_GUIDE.md`
- Get your app URL

**2. Add to Home Screen**
- Open Safari
- Go to your app URL
- Tap Share button (□↑)
- Tap "Add to Home Screen"
- Name it "KiranaBuddy POS"
- Tap "Add"

**3. Enable Kiosk Mode** (optional)
- Settings → Accessibility → Guided Access
- Turn ON
- Set passcode
- Open KiranaBuddy app
- Triple-click home button
- Tap "Start"

### 🎉 You're Done!
- Tap icon to open POS
- Looks like a native app

---

## Common Issues

### "Python not found"
- **Windows:** Reinstall Python, check "Add to PATH"
- **Linux:** Run `sudo apt install python3`

### "Module not found"
- Run: `pip install -r requirements.txt`
- Or: `pip install <module-name>`

### "Port 5000 already in use"
- Change port in `.env`: `PORT=5001`
- Or kill process: `netstat -ano | findstr :5000`

### "Can't connect to database"
- Check `firbasekey.json` exists
- Check `.env` has correct `FIREBASE_PROJECT_ID`
- Check internet connection

### Browser doesn't open automatically
- Open manually: `http://localhost:5000`
- Increase timeout in `start_pos.bat` (line with `timeout`)

---

## Next Steps

### ✅ Basic Setup Complete!

Now set up:

1. **Auto-Start on Boot**
   - See: `AUTO_START_GUIDE.md`

2. **Kiosk Mode** (full-screen, locked)
   - See: `KIOSK_MODE_GUIDE.md`

3. **Customer Display** (second screen)
   - See: `CUSTOMER_DISPLAY_GUIDE.md`

4. **Cloud Deployment** (access from anywhere)
   - See: `CLOUD_DEPLOYMENT_GUIDE.md`

5. **Backup & Updates**
   - See: `MAINTENANCE_GUIDE.md`

---

## Support

### Documentation
- `POS_INSTALLATION_GUIDE.md` - Detailed installation
- `AUTO_START_GUIDE.md` - Auto-start setup
- `KIOSK_MODE_GUIDE.md` - Kiosk mode setup
- `PAYMENT_FLOW_GUIDE.md` - Payment system usage
- `CUSTOMER_DISPLAY_GUIDE.md` - Customer display setup

### Need Help?
- Check documentation files
- Review error messages
- Check logs: `app.log` (if exists)

---

## Tips for Best Experience

1. **Use Touchscreen** - Much easier for POS
2. **Set Static IP** - Easier for customer display
3. **Disable Sleep** - Keep POS always on
4. **Auto-Login** - No password on boot
5. **Backup Config** - Save `.env` and `firbasekey.json`
6. **Test Thoroughly** - Before going live
7. **Train Staff** - Show them how to use it

---

## You're All Set! 🎉

Your POS system is ready to use. Start scanning products and processing payments!

**Happy Selling! 🛒💰**

