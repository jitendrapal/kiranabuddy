# Auto-Start Setup Guide

## Overview

This guide shows you how to make KiranaBuddy start automatically when your POS device boots up, so it's always ready to use.

---

## Windows Auto-Start

### Method 1: Startup Folder (Easiest)

1. **Create Desktop Shortcut**
   - Right-click `start_pos.bat`
   - Select "Create shortcut"
   - Rename to "KiranaBuddy POS"

2. **Add to Startup Folder**
   - Press `Win + R`
   - Type: `shell:startup`
   - Press Enter
   - Copy the shortcut to this folder

3. **Test**
   - Restart your computer
   - App should start automatically!

### Method 2: Task Scheduler (Advanced)

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type: `taskschd.msc`
   - Press Enter

2. **Create New Task**
   - Click "Create Basic Task"
   - Name: "KiranaBuddy POS"
   - Description: "Auto-start POS system"
   - Click "Next"

3. **Trigger**
   - Select "When the computer starts"
   - Click "Next"

4. **Action**
   - Select "Start a program"
   - Click "Next"
   - Browse to `C:\KiranaBuddy\start_pos.bat`
   - Click "Next"

5. **Finish**
   - Check "Open Properties dialog"
   - Click "Finish"

6. **Advanced Settings**
   - Check "Run with highest privileges"
   - Check "Run whether user is logged on or not"
   - Click "OK"

7. **Test**
   - Restart computer
   - App starts automatically!

### Method 3: Windows Service (Professional)

Use NSSM (Non-Sucking Service Manager):

1. **Download NSSM**
   - Go to: https://nssm.cc/download
   - Download and extract

2. **Install Service**
   ```cmd
   cd C:\nssm\win64
   nssm install KiranaBuddy
   ```

3. **Configure**
   - Path: `C:\Python311\python.exe`
   - Startup directory: `C:\KiranaBuddy`
   - Arguments: `app.py`
   - Click "Install service"

4. **Start Service**
   ```cmd
   nssm start KiranaBuddy
   ```

5. **Set Auto-Start**
   - Services → KiranaBuddy → Properties
   - Startup type: Automatic
   - Click "OK"

---

## Linux Auto-Start (Raspberry Pi / Ubuntu)

### Method 1: Systemd Service (Recommended)

1. **Edit Service File**
   ```bash
   nano kiranabuddy.service
   ```

2. **Update Paths**
   - Change `User=pi` to your username
   - Change `/home/pi/KiranaBuddy` to your path

3. **Install Service**
   ```bash
   sudo cp kiranabuddy.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable kiranabuddy.service
   sudo systemctl start kiranabuddy.service
   ```

4. **Check Status**
   ```bash
   sudo systemctl status kiranabuddy.service
   ```

5. **View Logs**
   ```bash
   sudo journalctl -u kiranabuddy.service -f
   ```

### Method 2: Crontab (Simple)

1. **Edit Crontab**
   ```bash
   crontab -e
   ```

2. **Add Line**
   ```
   @reboot cd /home/pi/KiranaBuddy && ./start_pos.sh
   ```

3. **Save and Exit**
   - Press `Ctrl+X`
   - Press `Y`
   - Press `Enter`

4. **Make Script Executable**
   ```bash
   chmod +x start_pos.sh
   ```

5. **Test**
   ```bash
   sudo reboot
   ```

### Method 3: rc.local (Old School)

1. **Edit rc.local**
   ```bash
   sudo nano /etc/rc.local
   ```

2. **Add Before `exit 0`**
   ```bash
   su - pi -c "cd /home/pi/KiranaBuddy && ./start_pos.sh" &
   ```

3. **Save and Reboot**
   ```bash
   sudo reboot
   ```

---

## Auto-Start Browser in Kiosk Mode

### Windows - Chrome Kiosk Mode

1. **Create Batch File: `start_kiosk.bat`**
   ```batch
   @echo off
   start /B python C:\KiranaBuddy\app.py
   timeout /t 5 /nobreak
   start chrome --kiosk --app=http://localhost:5000
   ```

2. **Add to Startup**
   - Follow Windows Method 1 above

### Linux - Chromium Kiosk Mode

1. **Install Chromium**
   ```bash
   sudo apt install -y chromium-browser unclutter
   ```

2. **Create Autostart File**
   ```bash
   mkdir -p ~/.config/autostart
   nano ~/.config/autostart/kiranabuddy.desktop
   ```

3. **Add Content**
   ```ini
   [Desktop Entry]
   Type=Application
   Name=KiranaBuddy POS
   Exec=/home/pi/KiranaBuddy/start_kiosk.sh
   ```

4. **Create Kiosk Script: `start_kiosk.sh`**
   ```bash
   #!/bin/bash
   # Hide mouse cursor
   unclutter -idle 0.1 &
   
   # Start Flask app
   cd /home/pi/KiranaBuddy
   source venv/bin/activate
   python app.py &
   
   # Wait for server
   sleep 5
   
   # Start browser in kiosk mode
   chromium-browser --kiosk --app=http://localhost:5000
   ```

5. **Make Executable**
   ```bash
   chmod +x start_kiosk.sh
   ```

---

## Customer Display Auto-Start

### Setup Second Screen

1. **Connect Second Monitor/TV**
   - HDMI or DisplayPort

2. **Extend Display**
   - Windows: `Win + P` → Extend
   - Linux: Display Settings → Extend

3. **Create Customer Display Shortcut**
   - Create `start_customer_display.bat`:
   ```batch
   @echo off
   timeout /t 10
   start chrome --new-window --kiosk http://localhost:5000/customer-display?session=auto
   ```

4. **Add to Startup**
   - Copy to Startup folder

### Auto-Create Display Session

Modify `start_pos.bat` to create session on boot:
```batch
REM After starting Flask app
timeout /t 8
curl -X POST http://localhost:5000/api/display-session -H "Content-Type: application/json" -d "{\"shop_name\":\"My Shop\"}" > session.txt
```

---

## Troubleshooting

### App doesn't start on boot

**Windows:**
- Check Event Viewer for errors
- Ensure Python is in PATH
- Run `start_pos.bat` manually to see errors

**Linux:**
- Check service status: `sudo systemctl status kiranabuddy`
- View logs: `sudo journalctl -u kiranabuddy -n 50`
- Check file permissions: `ls -la`

### Browser doesn't open

- Increase timeout in script (change 5 to 10 seconds)
- Check if server is running: `netstat -an | findstr 5000`
- Try opening manually: `http://localhost:5000`

### Service stops randomly

**Windows:**
- Use NSSM with restart settings
- Check Windows Event Logs

**Linux:**
- Add `Restart=always` to service file
- Increase `RestartSec=30`

---

## Best Practices

1. **Use Virtual Environment**
   - Isolates dependencies
   - Easier updates

2. **Set Static IP**
   - Easier for customer display
   - Consistent access

3. **Disable Sleep Mode**
   - Windows: Power Options → Never sleep
   - Linux: `sudo systemctl mask sleep.target`

4. **Auto-Login**
   - Windows: `netplwiz` → Uncheck "Users must enter password"
   - Linux: Raspberry Pi Config → Auto-login

5. **Backup Configuration**
   - Copy `.env` file
   - Backup `firbasekey.json`
   - Save to USB/cloud

---

## Next Steps

After auto-start is working:
1. Set up [Kiosk Mode](#kiosk-mode-guide)
2. Configure [Customer Display](#customer-display-auto-start)
3. Test [Offline Mode](#offline-mode-setup)
4. Set up [Automatic Backups](#backup-setup)

