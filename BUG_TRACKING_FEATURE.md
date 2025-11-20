# 🐛 Bug Tracking Feature

## ✅ Feature Complete!

This feature automatically tracks voice/text commands that the AI bot doesn't understand, allowing shopkeepers to review them in a GUI.

---

## 🎯 What This Feature Does

When a shopkeeper sends a voice or text message that the bot **cannot understand**, the system now:

1. **Automatically saves** the failed command to the database
2. **Stores detailed information** including:
   - Original text (raw message)
   - Whisper transcription (for voice messages)
   - Cleaned text (after Hindi number conversion)
   - What action the AI tried to parse
   - AI confidence score
   - Timestamp and user phone
3. **Provides a GUI** to view, manage, and resolve these bugs

---

## 📊 When Bugs Are Saved

Commands are automatically saved as bugs when:

1. **Command validation fails** (`is_valid() == False`)
2. **AI returns UNKNOWN action**
3. **AI confidence is below 50%** (`confidence < 0.5`)

---

## 🚀 How to Use

### **Step 1: Start the Flask App**
```bash
cd c:\Users\Archana\Downloads\kiranaBook
python app.py
```

### **Step 2: Open the Bug Tracking Page**
Open your browser and go to:
```
http://127.0.0.1:5000/bug
```

### **Step 3: Enter Shop Phone & Load**
- Enter shop phone number (e.g., `9876543210`)
- Click **Load** button
- View all bugs (unrecognized commands)!

### **Step 4: Test It!**
1. Go to the test chat: `http://127.0.0.1:5000/test`
2. Send an invalid command like: **"xyz abc random gibberish"**
3. Go back to bug tracking page: `http://127.0.0.1:5000/bug`
4. Click **🔄 Refresh** - you'll see your bug!

---

## 🗂️ Routes Changed

### **Old Routes → New Routes**

| Old Route | New Route |
|-----------|-----------|
| `/unrecognized_commands` | `/bug` |
| `/api/unrecognized_commands` | `/api/bug` |
| `/api/unrecognized_commands/resolve` | `/api/bug/resolve` |
| `/api/unrecognized_commands/delete` | `/api/bug/delete` |

### **Template File**
- **Old:** `templates/unrecognized_commands.html`
- **New:** `templates/bug.html`

---

## 📱 GUI Features

### **Header**
- 🐛 **Bug Report** (changed from "Unrecognized Commands")
- ← Back to Chat button
- 🔄 Refresh button

### **Statistics Cards**
- **Total Bugs** (changed from "Total Unrecognized")
- Voice Messages count
- Text Messages count

### **Bug List**
Each bug shows:
- 🎤 Voice or 💬 Text badge
- 📅 Timestamp
- 📞 User phone
- 🎯 Parsed action
- AI Confidence bar
- Raw text
- Whisper transcription (for voice)
- Cleaned text (after Hindi number conversion)
- ✓ Mark as Resolved button
- 🗑️ Delete button

### **Empty State**
- 🎉 **No Bugs Found!** (changed from "No Unrecognized Commands!")
- "All commands are being understood correctly."

---

## 💡 Example: What You'll See

When a shopkeeper says **"Maggi do add kar do"** but the AI has low confidence:

```
🎤 Voice Message
📅 2025-11-20 10:17:10
📞 9876543210
🎯 Action: ADD_STOCK
AI Confidence: 45% ⚠️

Raw Text:
"Maggi do add kar do"

Whisper Transcription:
"Maggi do add kar do"

Cleaned Text (After Hindi Number Conversion):
"Maggi 2 add kar do"

[✓ Mark as Resolved]  [🗑️ Delete]
```

---

## 🔧 Backend (No Changes Needed)

The backend database methods remain the same:
- `save_unrecognized_command()`
- `get_unrecognized_commands()`
- `mark_command_resolved()`
- `delete_unrecognized_command()`

Only the **routes** and **UI text** were changed to use "bug" terminology.

---

## ✅ Changes Summary

### **Files Modified:**

1. **app.py**
   - Changed route: `/unrecognized_commands` → `/bug`
   - Changed route: `/api/unrecognized_commands` → `/api/bug`
   - Changed route: `/api/unrecognized_commands/resolve` → `/api/bug/resolve`
   - Changed route: `/api/unrecognized_commands/delete` → `/api/bug/delete`
   - Updated function names: `unrecognized_commands_page()` → `bug_page()`

2. **templates/bug.html** (renamed from unrecognized_commands.html)
   - Title: "Unrecognized Commands" → "Bug Report"
   - Header: "🤔 Unrecognized Commands" → "🐛 Bug Report"
   - Stats: "Total Unrecognized" → "Total Bugs"
   - Empty state: "No Unrecognized Commands!" → "No Bugs Found!"
   - API endpoints updated to `/api/bug/*`
   - Delete confirmation: "delete this command?" → "delete this bug?"

---

## 🎨 UI Theme

The beautiful purple gradient design remains the same:
- Modern, responsive layout
- Real-time refresh
- Detailed view of all processing stages
- Visual confidence indicator
- Easy-to-use filters

---

**Feature is ready to use with the new "Bug" terminology! 🎉**

