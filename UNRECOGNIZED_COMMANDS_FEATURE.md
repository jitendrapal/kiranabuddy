# 🤔 Unrecognized Commands Tracking Feature

## ✅ Feature Complete!

This feature automatically saves voice/text commands that the AI bot doesn't understand, allowing shopkeepers to review them in a GUI and help improve the system.

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
3. **Provides a GUI** to view, manage, and resolve these commands

---

## 📊 When Commands Are Saved

Commands are automatically saved when:

1. **Command validation fails** (`is_valid() == False`)
2. **AI returns UNKNOWN action**
3. **AI confidence is below 50%** (`confidence < 0.5`)

---

## 🗂️ Files Modified/Created

### **1. models.py** - Added UnrecognizedCommand Model
```python
@dataclass
class UnrecognizedCommand:
    command_id: str
    shop_id: str
    user_phone: str
    message_type: str  # 'voice' or 'text'
    raw_text: str
    transcribed_text: Optional[str] = None
    cleaned_text: Optional[str] = None
    parsed_action: Optional[str] = None
    confidence: float = 0.0
    timestamp: datetime = None
    resolved: bool = False
    resolution_notes: Optional[str] = None
```

### **2. database.py** - Added 4 New Methods

**save_unrecognized_command()** - Save a failed command
```python
db.save_unrecognized_command(
    shop_id=shop_id,
    user_phone=from_phone,
    message_type="voice",  # or "text"
    raw_text="Maggi do add kar do",
    transcribed_text="Maggi do add kar do",
    cleaned_text="Maggi 2 add kar do",
    parsed_action="ADD_STOCK",
    confidence=0.45
)
```

**get_unrecognized_commands()** - Retrieve commands for a shop
```python
commands = db.get_unrecognized_commands(
    shop_id=shop_id,
    include_resolved=False,  # Only unresolved
    limit=100
)
```

**mark_command_resolved()** - Mark as resolved
```python
db.mark_command_resolved(
    command_id="abc-123",
    resolution_notes="Fixed by improving parser"
)
```

**delete_unrecognized_command()** - Delete a command
```python
db.delete_unrecognized_command(command_id="abc-123")
```

### **3. command_processor.py** - Auto-Save Failed Commands

Added logic to automatically save unrecognized commands:
```python
if not is_valid or parsed_command.action == CommandAction.UNKNOWN or parsed_command.confidence < 0.5:
    db.save_unrecognized_command(
        shop_id=shop_id,
        user_phone=from_phone,
        message_type=message_type,
        raw_text=text,
        transcribed_text=transcribed_text if message_type == "voice" else None,
        cleaned_text=cleaned_text,
        parsed_action=parsed_command.action.value,
        confidence=parsed_command.confidence,
    )
```

### **4. ai_service.py** - Store Cleaned Text

Added `_last_cleaned_text` attribute to track cleaned voice text:
```python
self._last_cleaned_text = cleaned_text
```

### **5. app.py** - Added 4 New Routes

**Page Route:**
- `/unrecognized_commands` - GUI page to view commands

**API Routes:**
- `/api/unrecognized_commands` (GET) - Get commands for a shop
- `/api/unrecognized_commands/resolve` (POST) - Mark as resolved
- `/api/unrecognized_commands/delete` (POST) - Delete a command

### **6. templates/unrecognized_commands.html** - Beautiful GUI

Created a modern, responsive GUI with:
- 📊 Statistics cards (Total, Voice, Text)
- 🔍 Filter by resolved/unresolved
- 📱 Shows all command details
- ✅ Mark as resolved button
- 🗑️ Delete button
- 🎨 Beautiful gradient design

---

## 🚀 How to Use

### **Step 1: Start the Flask App**
```bash
cd c:\Users\Archana\Downloads\kiranaBook
python app.py
```

### **Step 2: Open the GUI**
Open browser: `http://127.0.0.1:5000/unrecognized_commands`

### **Step 3: Enter Shop Phone**
Enter the shop phone number (e.g., `9876543210`) and click **Load**

### **Step 4: View Unrecognized Commands**
You'll see all commands that the bot couldn't understand, with:
- 🎤 Voice or 💬 Text badge
- Original text
- Whisper transcription (for voice)
- Cleaned text (after Hindi number conversion)
- AI confidence score
- Timestamp

### **Step 5: Manage Commands**
- Click **✓ Mark as Resolved** to mark a command as fixed
- Click **🗑️ Delete** to remove a command
- Check **Show Resolved** to see resolved commands

---

## 🧪 Testing

Run the test script:
```bash
python test_unrecognized_feature.py
```

**Test Results:**
```
✅ Test 1: Save Unrecognized Voice Command - PASSED
✅ Test 2: Save Unrecognized Text Command - PASSED
✅ Test 3: Retrieve Unrecognized Commands - PASSED
✅ Test 4: Mark Command as Resolved - PASSED
✅ Test 5: Retrieve Including Resolved - PASSED
✅ Test 6: Delete Command - PASSED
```

---

## 💡 Example Scenarios

### **Scenario 1: Voice Command with Low Confidence**
```
🎤 Shopkeeper says: "Maggi do add kar do"
🔊 Whisper transcribes: "Maggi do add kar do"
✨ Cleaned: "Maggi 2 add kar do"
🤖 AI parses: ADD_STOCK, confidence=0.45 (LOW!)
💾 Saved to database automatically
```

### **Scenario 2: Completely Unknown Text**
```
💬 Shopkeeper types: "xyz abc random gibberish"
🤖 AI parses: UNKNOWN action
💾 Saved to database automatically
```

### **Scenario 3: Invalid Command**
```
💬 Shopkeeper types: "add stock"  (missing product name)
🤖 AI parses: ADD_STOCK, but is_valid() = False
💾 Saved to database automatically
```

---

## 📈 Benefits

1. **Identify Patterns** - See which commands users struggle with
2. **Improve AI** - Use real failed commands to improve parsing
3. **Better UX** - Understand user language and add new keywords
4. **Debug Issues** - See exactly what Whisper transcribed vs what AI parsed
5. **Track Progress** - Mark commands as resolved when fixes are deployed

---

## 🎨 GUI Features

- **Modern Design** - Beautiful gradient purple theme
- **Responsive** - Works on desktop and mobile
- **Real-time** - Refresh button to reload data
- **Detailed View** - Shows all stages of processing
- **Confidence Bar** - Visual indicator of AI confidence
- **Badges** - Easy identification of voice vs text, resolved vs unresolved

---

## ✅ All Tests Passed!

```
============================================================
✅ All Tests Completed!
============================================================

📊 Test Summary:
✅ Saved voice command: 17875d0c-9c66-4f89-9ccf-b1617c169b46
✅ Saved text command: 9ca3872b-d2f2-4540-9b7c-e834f46ad8d1
✅ Retrieved 2 unrecognized commands
✅ Marked command as resolved
✅ Total commands: 3 (Resolved: 2, Unresolved: 1)
✅ Deleted command successfully
```

---

**Feature is ready to use! 🎉**

