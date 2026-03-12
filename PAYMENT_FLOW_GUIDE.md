# Payment Flow - User Guide

## Overview

The scanner now works like a real store! When you finish scanning items, you click **"💰 Pay"** which opens a payment modal where you enter the payment amount. Only after confirming payment does the stock get deducted.

## How It Works (Like a Real Store)

### Traditional Store Flow
1. **Scan items** → Items added to cart
2. **Show total** → Customer sees total amount
3. **Collect payment** → Cashier receives money/card/UPI
4. **Give change** (if cash) → Return excess amount
5. **Deduct stock** → Inventory updated
6. **Print receipt** → Transaction complete

### Our Implementation
1. **Scan items** → Click camera button (📷), scan barcodes
2. **Click "💰 Pay"** → Payment modal opens showing total
3. **Select payment method** → Cash / Card / UPI
4. **Enter amount received** → Type the amount customer gave
5. **See change** (if cash) → Automatically calculated
6. **Confirm payment** → Stock deducts, customer display shows "Thank You"

## Step-by-Step Usage

### Step 1: Scan Products
1. Click the **📷 camera button** to start scanning
2. Scan product barcodes
3. Items appear in the cart with quantities and prices
4. You can adjust quantities using +/- buttons
5. Total amount is shown at the bottom

### Step 2: Click "💰 Pay" Button
- The green **"💰 Pay"** button is at the bottom of the cart
- Click it when customer is ready to pay
- Payment modal opens

### Step 3: Payment Modal

#### What You See:
- **Total Amount** - Large display showing the bill total
- **Payment Method** - Three buttons: 💵 Cash | 💳 Card | 📱 UPI
- **Amount Received** - Input field to enter payment
- **Change to Return** - Shows automatically if overpaid (cash only)
- **Cancel** - Close modal without processing
- **Confirm Payment** - Process the payment and deduct stock

#### Payment Methods:

**💵 Cash (Default)**
- Customer gives cash
- Enter the amount received (e.g., if bill is ₹47 and customer gives ₹50)
- Change is calculated automatically (₹3 in this example)
- You can enter exact amount or more

**💳 Card**
- Customer pays by card
- Amount is auto-filled with exact total
- No change calculation needed
- Just confirm payment

**📱 UPI**
- Customer pays via UPI (PhonePe, GPay, Paytm, etc.)
- Amount is auto-filled with exact total
- No change calculation needed
- Just confirm payment

### Step 4: Enter Amount Received

**For Cash:**
```
Bill Total: ₹47.50
Customer gives: ₹100
You enter: 100
Change shown: ₹52.50
```

**For Card/UPI:**
```
Bill Total: ₹47.50
Auto-filled: 47.50
Just click Confirm
```

### Step 5: Confirm Payment
- Click **"Confirm Payment"** button
- Modal closes
- Stock is deducted from inventory
- Customer display shows "Thank You" screen
- Cart is cleared
- Ready for next customer

## Features

### Smart Change Calculation
- **Real-time calculation** - Updates as you type
- **Only for cash** - Card/UPI don't show change
- **Large display** - Easy to see the change amount
- **Yellow color** - Stands out clearly

### Payment Validation
- **Minimum check** - Can't confirm if amount < total
- **Disabled button** - Confirm button grays out if insufficient
- **Alert message** - Shows error if you try to confirm with less amount

### Auto-Fill for Digital Payments
- **Card/UPI** - Exact amount auto-filled
- **No manual entry** - Just select method and confirm
- **Faster checkout** - One click payment

### Keyboard Support
- **Auto-focus** - Input field focused when modal opens
- **Number input** - Optimized for quick entry
- **Decimal support** - Can enter paise (e.g., 47.50)

## Example Scenarios

### Scenario 1: Cash Payment with Change
```
1. Scan: Maggi (₹12), Bread (₹35)
2. Total: ₹47
3. Click "💰 Pay"
4. Payment method: 💵 Cash (already selected)
5. Customer gives: ₹100
6. Enter: 100
7. Change shown: ₹53
8. Click "Confirm Payment"
9. Give ₹53 change to customer
10. Stock deducted, receipt shown
```

### Scenario 2: Exact Cash Payment
```
1. Scan: Rice 1kg (₹50)
2. Total: ₹50
3. Click "💰 Pay"
4. Customer gives: ₹50
5. Enter: 50
6. No change shown (exact amount)
7. Click "Confirm Payment"
8. Stock deducted
```

### Scenario 3: Card Payment
```
1. Scan: Oil (₹180), Sugar (₹45)
2. Total: ₹225
3. Click "💰 Pay"
4. Click "💳 Card" button
5. Amount auto-filled: 225.00
6. Customer swipes card
7. Click "Confirm Payment"
8. Stock deducted
```

### Scenario 4: UPI Payment
```
1. Scan: Multiple items
2. Total: ₹347.50
3. Click "💰 Pay"
4. Click "📱 UPI" button
5. Amount auto-filled: 347.50
6. Customer scans QR / enters UPI ID
7. Wait for payment confirmation
8. Click "Confirm Payment"
9. Stock deducted
```

### Scenario 5: Cancel Payment
```
1. Scan items
2. Click "💰 Pay"
3. Customer says "Wait, I forgot something"
4. Click "Cancel"
5. Modal closes
6. Cart still has items
7. Can continue scanning or adjust quantities
8. Click "💰 Pay" again when ready
```

## Visual Design

### Colors
- **Green gradient** - Pay button (₹ symbol)
- **Dark modal** - Professional look
- **Green total** - Stands out clearly
- **Yellow change** - Easy to spot
- **Active method** - Green glow effect

### Animations
- **Slide in** - Modal appears smoothly
- **Hover effects** - Buttons lift on hover
- **Active state** - Selected method glows
- **Focus ring** - Input field highlights

## Integration with Customer Display

When payment is confirmed:
1. **Customer display** switches to "Thank You" screen
2. Shows **final total** paid
3. Displays **"धन्यवाद! पधारो फिर।"** (Thank you, come again)
4. **Status bar** shows "✅ Payment complete"

## Tips for Cashiers

1. **Always check the total** before asking for payment
2. **Count cash carefully** before entering amount
3. **Verify card/UPI** payment received before confirming
4. **Give change** immediately after confirming
5. **Clear cart** is automatic after payment
6. **Start fresh** for next customer

## Keyboard Shortcuts (Future)

- `Enter` - Confirm payment (when amount is valid)
- `Esc` - Cancel payment
- `1` - Select Cash
- `2` - Select Card
- `3` - Select UPI

## Common Questions

**Q: What if I enter wrong amount?**
A: Just correct it in the input field. Change updates automatically.

**Q: Can I cancel after clicking Pay?**
A: Yes! Click "Cancel" button. Cart remains unchanged.

**Q: What if customer doesn't have enough money?**
A: Click Cancel, remove some items, then click Pay again.

**Q: Does it work offline?**
A: Payment modal works offline, but stock deduction needs server connection.

**Q: Can I see payment history?**
A: Not yet - coming in future update.

## Technical Details

### Payment Flow
```
Click Pay → Show Modal → Enter Amount → Validate → Confirm → Deduct Stock → Clear Cart
```

### Data Stored
- Payment method (cash/card/upi)
- Amount received
- Change given (if cash)
- Timestamp
- Items sold

### Stock Deduction
- Happens ONLY after payment confirmation
- Uses existing `/webhook` endpoint
- Same logic as before, just triggered after payment

## Future Enhancements

- Payment history log
- Daily cash collection report
- Card/UPI transaction IDs
- Receipt printing
- SMS receipt to customer
- Multiple payment methods (split payment)
- Discount/coupon support

