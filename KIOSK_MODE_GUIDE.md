# Kiosk Mode Setup Guide

## Overview

Kiosk mode locks your POS device to only run KiranaBuddy, preventing users from accessing other apps or settings. Perfect for dedicated POS terminals.

---

## What is Kiosk Mode?

### Features:
- ✅ Full-screen app (no browser bars)
- ✅ No access to other apps
- ✅ Can't close or minimize
- ✅ Hides mouse cursor (optional)
- ✅ Disables keyboard shortcuts
- ✅ Auto-restarts if crashed
- ✅ Professional POS experience

### Use Cases:
- Dedicated POS terminal
- Customer-facing display
- Unmanned kiosk
- Public-facing device

---

## Windows Kiosk Mode

### Method 1: Chrome Kiosk Mode (Easiest)

1. **Use the Kiosk Script**
   - Double-click `start_kiosk.bat`
   - Browser opens in full-screen
   - No address bar, no tabs

2. **Exit Kiosk Mode**
   - Press `Alt + F4`
   - Or `Ctrl + W`

3. **Auto-Start on Boot**
   - Copy `start_kiosk.bat` to Startup folder
   - Press `Win + R` → `shell:startup`

### Method 2: Windows Kiosk Mode (Professional)

**Windows 10/11 Pro/Enterprise only**

1. **Create Kiosk User**
   - Settings → Accounts → Family & other users
   - Add someone else to this PC
   - Create "POS User" (no Microsoft account)

2. **Set Up Assigned Access**
   - Settings → Accounts → Family & other users
   - Click "Set up assigned access"
   - Choose "POS User"
   - Choose app: Microsoft Edge or Chrome

3. **Configure Kiosk App**
   - Set homepage: `http://localhost:5000`
   - Enable full-screen
   - Disable navigation

4. **Auto-Login as Kiosk User**
   - Press `Win + R` → `netplwiz`
   - Select "POS User"
   - Uncheck "Users must enter password"
   - Click OK, enter password

5. **Test**
   - Restart computer
   - Logs in as POS User automatically
   - Only KiranaBuddy accessible!

### Method 3: Third-Party Kiosk Software

**Recommended: SiteKiosk, KioWare, or Porteus Kiosk**

1. Download and install kiosk software
2. Set URL: `http://localhost:5000`
3. Configure restrictions
4. Set auto-start

---

## Linux Kiosk Mode (Raspberry Pi)

### Method 1: Chromium Kiosk (Recommended)

1. **Install Required Packages**
   ```bash
   sudo apt update
   sudo apt install -y chromium-browser unclutter xdotool
   ```

2. **Make Kiosk Script Executable**
   ```bash
   chmod +x start_kiosk.sh
   ```

3. **Test Kiosk Mode**
   ```bash
   ./start_kiosk.sh
   ```

4. **Auto-Start on Boot**
   ```bash
   mkdir -p ~/.config/autostart
   nano ~/.config/autostart/kiranabuddy-kiosk.desktop
   ```

   Add:
   ```ini
   [Desktop Entry]
   Type=Application
   Name=KiranaBuddy Kiosk
   Exec=/home/pi/KiranaBuddy/start_kiosk.sh
   X-GNOME-Autostart-enabled=true
   ```

5. **Disable Screen Blanking**
   ```bash
   sudo nano /etc/lightdm/lightdm.conf
   ```

   Add under `[Seat:*]`:
   ```
   xserver-command=X -s 0 -dpms
   ```

6. **Auto-Login**
   ```bash
   sudo raspi-config
   ```
   - System Options → Boot / Auto Login
   - Desktop Autologin

### Method 2: Minimal Kiosk (No Desktop)

1. **Install Minimal X Server**
   ```bash
   sudo apt install -y --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox chromium-browser
   ```

2. **Create Kiosk User**
   ```bash
   sudo adduser kiosk
   ```

3. **Configure Openbox**
   ```bash
   sudo -u kiosk mkdir -p /home/kiosk/.config/openbox
   sudo -u kiosk nano /home/kiosk/.config/openbox/autostart
   ```

   Add:
   ```bash
   # Disable screen saver
   xset s off
   xset -dpms
   xset s noblank

   # Hide cursor
   unclutter -idle 0.1 -root &

   # Start Flask app
   cd /home/pi/KiranaBuddy
   source venv/bin/activate
   python3 app.py &

   # Wait for server
   sleep 8

   # Start browser in kiosk mode
   chromium-browser --kiosk --app=http://localhost:5000 \
     --disable-pinch \
     --overscroll-history-navigation=0 \
     --noerrdialogs \
     --disable-infobars
   ```

4. **Auto-Start X on Boot**
   ```bash
   sudo nano /etc/systemd/system/kiosk.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Kiosk Mode
   After=network.target

   [Service]
   Type=simple
   User=kiosk
   Environment=DISPLAY=:0
   ExecStart=/usr/bin/startx /usr/bin/openbox-session
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Enable Service**
   ```bash
   sudo systemctl enable kiosk.service
   sudo systemctl start kiosk.service
   ```

---

## Android Kiosk Mode

### Method 1: Kiosk Browser App

1. **Install Kiosk Browser**
   - Open Play Store
   - Search "Kiosk Browser Lockdown"
   - Install

2. **Configure**
   - Open Kiosk Browser
   - Set URL: `http://[your-server-ip]:5000`
   - Enable full-screen mode
   - Disable navigation
   - Set password to exit

3. **Set as Default Launcher**
   - Settings → Apps → Default apps
   - Home app → Kiosk Browser

4. **Lock Settings**
   - Enable "Prevent uninstall"
   - Set admin password

### Method 2: Android Enterprise (Professional)

1. **Enroll in Android Enterprise**
2. **Create Kiosk Policy**
3. **Deploy to device**
4. **Lock to single app**

---

## iPad Kiosk Mode

### Guided Access (Built-in)

1. **Enable Guided Access**
   - Settings → Accessibility → Guided Access
   - Turn ON
   - Set passcode

2. **Open KiranaBuddy**
   - Open Safari
   - Go to your app URL
   - Add to Home Screen

3. **Start Guided Access**
   - Open KiranaBuddy from home screen
   - Triple-click home button (or side button on newer iPads)
   - Tap "Options"
   - Disable: Touch, Motion, Keyboards
   - Tap "Start"

4. **Exit Guided Access**
   - Triple-click home button
   - Enter passcode

---

## Advanced Kiosk Features

### Hide Mouse Cursor

**Windows:**
```batch
REM Install AutoHotkey
REM Create script: hide_cursor.ahk
#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%
Loop {
    MouseMove, 10000, 10000
    Sleep, 100
}
```

**Linux:**
```bash
sudo apt install unclutter
unclutter -idle 0.1 -root &
```

### Disable Keyboard Shortcuts

**Windows:**
- Use AutoHotkey to intercept keys
- Or use kiosk software

**Linux:**
```bash
# Add to Openbox config
nano ~/.config/openbox/rc.xml
# Remove all keyboard shortcuts
```

### Auto-Restart on Crash

**Windows Task Scheduler:**
- Create task to monitor process
- Restart if not running

**Linux Systemd:**
```ini
[Service]
Restart=always
RestartSec=5
```

### Watchdog Timer

Create `watchdog.sh`:
```bash
#!/bin/bash
while true; do
    if ! curl -s http://localhost:5000 > /dev/null; then
        echo "App crashed, restarting..."
        pkill python
        sleep 2
        cd /home/pi/KiranaBuddy
        python3 app.py &
    fi
    sleep 30
done
```

---

## Security Best Practices

1. **Disable USB Ports** (BIOS setting)
2. **Lock BIOS with password**
3. **Disable Task Manager** (Windows)
4. **Remove admin rights** from kiosk user
5. **Enable auto-updates** for security patches
6. **Use VPN** if accessing remotely
7. **Backup regularly**

---

## Troubleshooting

### Can't exit kiosk mode
- Windows: `Ctrl + Alt + Del` → Task Manager → End task
- Linux: `Ctrl + Alt + F1` → Login → `pkill chromium`

### Screen goes blank
- Disable power saving in BIOS
- Disable screen saver
- Use `xset` commands (Linux)

### App crashes and doesn't restart
- Check systemd service logs
- Ensure `Restart=always` is set
- Add watchdog script

---

## Next Steps

1. Test kiosk mode thoroughly
2. Set up customer display on second screen
3. Configure automatic backups
4. Train staff on exit procedures
5. Document admin password securely

