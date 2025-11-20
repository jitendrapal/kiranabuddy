# 🔢 "Do" (दो) Conversion - How It Works

## 🎯 The Problem

When you speak in Hindi and say **"do" (दो)** meaning **"2"**, Whisper transcribes it as the English word **"do"**.

This creates confusion because "do" has **two meanings**:
1. **Number 2** (दो) - "Maggi **do** add karo" = Add **2** Maggi
2. **Command suffix** (करो/do) - "Maggi add kar **do**" = Please add Maggi

## ✅ The Solution

The code uses **smart context-aware conversion** that only converts "do" → "2" when it makes sense.

### **Conversion Rules (ai_service.py lines 99-110)**

```python
# Convert "do" → "2" ONLY when followed by action words
cleaned = re.sub(
    r'\bdo\b(?=\s+(add|aad|dal|daal|bik|sold|sell|bech|stock|check|kitna|hai))', 
    '2', 
    cleaned, 
    flags=re.IGNORECASE
)
```

**This uses a "lookahead" pattern** `(?=\s+(...))` which means:
- ✅ Convert "do" to "2" **IF** it's followed by action words like `add`, `bik`, `sold`, etc.
- ❌ Don't convert "do" if it's followed by anything else

---

## 📝 Examples

### **✅ CONVERTS "do" → "2"**

| Input | Cleaned | Why? |
|-------|---------|------|
| "Maggi **do** add kar do" | "Maggi **2** add kar do" | "do" followed by "add" ✅ |
| "Maggi **do** bik gaya" | "Maggi **2** bik gaya" | "do" followed by "bik" ✅ |
| "Parle G **do** sold" | "Parle G **2** sold" | "do" followed by "sold" ✅ |
| "**do** add karo" | "**2** add karo" | "do" followed by "add" ✅ |
| "**do** bik gaya" | "**2** bik gaya" | "do" followed by "bik" ✅ |

### **❌ DOESN'T CONVERT "do"**

| Input | Cleaned | Why? |
|-------|---------|------|
| "add kar **do**" | "add kar **do**" | "do" at end (command suffix) ❌ |
| "karo **do**" | "karo **do**" | "do" at end (command suffix) ❌ |
| "**do** Maggi add" | "**do** Maggi add" | "do" followed by product name ❌ |
| "Maggi **do** karo" | "Maggi **do** karo" | "do" followed by "karo" (not an action) ❌ |

---

## 🔍 How Whisper Transcribes Your Voice

When you speak **"Maggi do add kar do"** in Hindi:

```
🎤 You say (Hindi): "Maggi do add kar do"
                           ↓
🔊 Whisper transcribes: "Maggi do add kar do"
                           ↓
✨ Voice cleaning: "Maggi 2 add kar do"
                           ↓
🤖 AI parses: ADD_STOCK, "maggi", 2.0
                           ↓
✅ Result: "2 Maggi add ho gaya!"
```

**Key points:**
1. Whisper uses **`translations.create`** which translates Hindi audio to English text
2. When you say "do" (दो = 2), Whisper writes it as "do" (English word)
3. Our cleaning function converts "do" → "2" based on context
4. The AI then parses "Maggi 2 add" correctly

---

## 🧪 Testing

All 10 test cases pass:

```
✅ "Maggi do add kar do" → "Maggi 2 add kar do"
✅ "Maggi do add" → "Maggi 2 add"
✅ "add kar do" → "add kar do" (no conversion)
✅ "Maggi do bik gaya" → "Maggi 2 bik gaya"
✅ "do Maggi add" → "do Maggi add" (no conversion)
✅ "Maggi 2 add kar do" → "Maggi 2 add kar do" (already has number)
✅ "do add" → "2 add"
✅ "do bik" → "2 bik"
✅ "kar do" → "kar do" (no conversion)
✅ "karo do" → "karo do" (no conversion)
```

---

## 🎯 What You Can Say

**All these work perfectly:**

### **Hindi Numbers:**
- "Maggi **do** add kar do" → Add 2 Maggi
- "Maggi **teen** add karo" → Add 3 Maggi
- "Maggi **panch** bik gaya" → Sell 5 Maggi
- "Maggi **das** add" → Add 10 Maggi

### **With Command Suffixes:**
- "Maggi do add **kar do**" → Add 2 Maggi (first "do" converts, second doesn't)
- "Maggi teen bik **gaya**" → Sell 3 Maggi
- "Maggi panch add **karo**" → Add 5 Maggi

### **Natural Speech:**
- "um Maggi do add kar do" → Add 2 Maggi (filler removed)
- "uh Maggi teen bik gaya" → Sell 3 Maggi (filler removed)

---

## 🔧 Technical Details

### **Regex Pattern Breakdown**

```python
r'\bdo\b(?=\s+(add|aad|dal|daal|bik|sold|sell|bech|stock|check|kitna|hai))'
```

- `\b` = Word boundary (ensures we match whole word "do", not "doh" or "doing")
- `do` = The word "do"
- `\b` = Word boundary (end of word)
- `(?=...)` = Positive lookahead (check what comes after, but don't consume it)
- `\s+` = One or more whitespace characters
- `(add|aad|dal|...)` = Match any of these action words
- `flags=re.IGNORECASE` = Case-insensitive matching

### **Why Lookahead?**

Lookahead `(?=...)` checks what comes **after** "do" without consuming it. This means:
- We can check if "do" is followed by an action word
- But we don't remove the action word from the text
- So "Maggi do add" → "Maggi 2 add" (not "Maggi 2")

---

## 📊 Summary

✅ **"do" → "2" conversion is working perfectly**
✅ **Smart context-aware conversion** (only converts when followed by action words)
✅ **All 10 test cases pass**
✅ **Handles command suffixes correctly** ("kar do" stays as "kar do")
✅ **Works with all Hindi numbers** (do, teen, panch, das, etc.)
✅ **Removes filler words** (um, uh, hmm)

**The system correctly handles the ambiguity of "do" in Hindi/Hinglish commands!** 🎉

