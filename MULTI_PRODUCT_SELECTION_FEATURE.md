# 🎯 Multi-Product Selection Feature

## ✅ Feature Complete!

This feature solves the problem where multiple products match a search term (e.g., "rice" matches multiple brands). Instead of showing an error, the bot now displays a numbered list and asks the user to select which product they want to update.

---

## 🎯 **Problem Solved**

**Before:**
- User says: "Rice 10 packet add kar do"
- Bot finds multiple rice products (India Gate, Daawat, Kohinoor, etc.)
- Bot picks one randomly or shows error
- ❌ Wrong product gets updated!

**After:**
- User says: "Rice 10 packet add kar do"
- Bot finds multiple rice products
- Bot shows numbered list:
  ```
  🤔 Multiple products found for 'rice':
  
  1. Basmati Rice India Gate 1kg
  2. Basmati Rice Daawat 1kg
  3. Basmati Rice Kohinoor 1kg
  4. Sona Masoori Rice 1kg
  
  Please reply with the number (1-4) to select which product you want to update.
  ```
- User replies: "2"
- ✅ Correct product (Daawat) gets updated!

---

## 🚀 **How It Works**

### **Step 1: User Sends Command**
```
User: "Rice 10 add kar do"
```

### **Step 2: Bot Finds Multiple Matches**
The bot searches for products matching "rice" and finds 4 products.

### **Step 3: Bot Saves Pending Selection**
The bot saves:
- User phone number
- Action to perform (ADD_STOCK)
- Quantity (10)
- List of matching product IDs
- List of matching product names
- Expiry time (5 minutes)

### **Step 4: Bot Shows Numbered List**
```
🤔 Multiple products found for 'rice':

1. Basmati Rice India Gate 1kg
2. Basmati Rice Daawat 1kg
3. Basmati Rice Kohinoor 1kg
4. Sona Masoori Rice 1kg

Please reply with the number (1-4) to select which product you want to update.
```

### **Step 5: User Selects Product**
```
User: "2"
```

### **Step 6: Bot Executes Action**
The bot:
- Retrieves the pending selection
- Gets product #2 (Basmati Rice Daawat 1kg)
- Executes ADD_STOCK with quantity 10
- Deletes the pending selection
- Sends confirmation:
  ```
  ✅ 10 Basmati Rice Daawat 1kg add ho gaya!
  ```

---

## 📁 **Files Modified/Created**

### **1. models.py** - Added PendingSelection Model
```python
@dataclass
class PendingSelection:
    """Model for storing pending product selections"""
    selection_id: str
    shop_id: str
    user_phone: str
    action: str  # ADD_STOCK, REDUCE_STOCK, CHECK_STOCK
    quantity: float
    product_ids: List[str]
    product_names: List[str]
    timestamp: datetime
    expires_at: datetime  # Expires after 5 minutes
    
    def is_expired(self) -> bool:
        """Check if the selection has expired"""
        return datetime.utcnow() > self.expires_at
```

### **2. database.py** - Added Methods

**find_all_matching_products()** - Find ALL matching products
```python
def find_all_matching_products(self, shop_id: str, product_name: str, min_matches: int = 2) -> List[Product]:
    """Find ALL products that match the search term.
    
    Returns a list of matching products. If only 1 product matches, returns empty list.
    This is used when we want to show the user multiple options to choose from.
    """
```

**save_pending_selection()** - Save pending selection
```python
def save_pending_selection(
    self, shop_id, user_phone, action, quantity, product_ids, product_names
) -> PendingSelection:
    """Save a pending product selection when multiple matches are found."""
```

**get_pending_selection()** - Retrieve pending selection
```python
def get_pending_selection(self, user_phone: str) -> Optional[PendingSelection]:
    """Get the pending selection for a user."""
```

**delete_pending_selection()** - Delete pending selection
```python
def delete_pending_selection(self, user_phone: str) -> bool:
    """Delete pending selection for a user."""
```

### **3. command_processor.py** - Updated Logic

**Check for pending selection** (lines 100-155)
- Before parsing command, check if user has a pending selection
- If user sends a number (1, 2, 3, etc.), execute the pending action
- Delete the pending selection after execution

**Handle multiple matches** (lines 364-498)
- For ADD_STOCK, REDUCE_STOCK, CHECK_STOCK commands
- Check if multiple products match the search term
- If yes, save pending selection and show numbered list
- If no, use existing single-match logic

---

## 🧪 **Test Results**

All tests passed successfully! ✅

```
Test 1: Creating multiple rice products ✅
  - Created 4 rice products with different brands

Test 2: Searching for 'rice' ✅
  - Found 5 matching products

Test 3: Searching for 'basmati' ✅
  - Found 4 matching products

Test 4: Pending selection save/retrieve ✅
  - Saved pending selection
  - Retrieved pending selection
  - Verified expiry check
  - Deleted pending selection

Test 5: Single match returns empty ✅
  - Specific search returns 0 (use find_existing_product_by_name)
```

---

## 💡 **Example Scenarios**

### **Scenario 1: Add Stock with Multiple Matches**
```
👤 User: "Rice 10 add kar do"

🤖 Bot: 🤔 Multiple products found for 'rice':

1. Basmati Rice India Gate 1kg
2. Basmati Rice Daawat 1kg
3. Basmati Rice Kohinoor 1kg
4. Sona Masoori Rice 1kg

Please reply with the number (1-4) to select which product you want to update.

👤 User: "2"

🤖 Bot: ✅ 10 Basmati Rice Daawat 1kg add ho gaya!
```

### **Scenario 2: Reduce Stock with Multiple Matches**
```
👤 User: "Basmati 5 bik gaya"

🤖 Bot: 🤔 Multiple products found for 'basmati':

1. Basmati Rice India Gate 1kg
2. Basmati Rice Daawat 1kg
3. Basmati Rice Kohinoor 1kg

Please reply with the number (1-3) to select which product you want to update.

👤 User: "1"

🤖 Bot: ✅ 5 Basmati Rice India Gate 1kg bik gaya!
```

### **Scenario 3: Check Stock with Multiple Matches**
```
👤 User: "Rice kitna hai?"

🤖 Bot: 🤔 Multiple products found for 'rice':

1. Basmati Rice India Gate 1kg
2. Basmati Rice Daawat 1kg
3. Sona Masoori Rice 1kg

Please reply with the number (1-3) to check stock.

👤 User: "3"

🤖 Bot: 📦 Sona Masoori Rice 1kg: 25 kg available
```

---

## ⏰ **Expiry Handling**

Pending selections expire after **5 minutes**. If the user doesn't respond within 5 minutes:
- The pending selection is automatically deleted
- User needs to send the original command again

---

## ✅ **Benefits**

1. **No More Errors** - Users can select the exact product they want
2. **Better UX** - Clear numbered list instead of confusing error messages
3. **Prevents Mistakes** - No wrong product gets updated
4. **Works with Voice** - Works perfectly with voice commands
5. **Auto-Cleanup** - Pending selections expire after 5 minutes

---

**Feature is ready to use! 🎉**

