# Live Customer Display Screen - User Guide

## Overview

The **Live Customer Display Screen** allows customers to see scanned items in real-time on a second screen while the cashier scans products. This creates transparency and improves the customer experience.

## How It Works

### Architecture
- **Cashier Screen**: The main test interface where products are scanned
- **Customer Screen**: A separate window/screen that shows items as they're scanned
- **Backend Session**: In-memory storage that syncs the cart between both screens

### Data Flow
1. Cashier clicks "📺 Customer Screen" button
2. Backend creates a new display session with unique ID
3. Customer display opens in new window/tab
4. As cashier scans items, the cart updates live on customer screen
5. When cashier clicks "Send", customer screen shows "Thank You" message

## How to Use

### Step 1: Open Customer Display
1. Open the test interface at `http://127.0.0.1:5000/`
2. Login if required
3. Click the **"📺 Customer Screen"** button (purple button in quick-reports bar)
4. A new window will open showing the customer display
5. Position this window on your second monitor/screen

### Step 2: Scan Products
1. On the cashier screen, click the camera button (📷) to start scanning
2. Scan product barcodes using your camera
3. **Watch the customer screen** - items appear live as you scan!
4. The customer screen shows:
   - Product name
   - Quantity
   - Unit price
   - Line total
   - Grand total (large, prominent)

### Step 3: Adjust Quantities (Optional)
- Use the +/- buttons on cashier screen to adjust quantities
- Customer screen updates automatically

### Step 4: Complete Transaction
1. Click **"Send"** on the cashier screen
2. Customer screen switches to "Thank You" screen
3. Shows final total paid

### Step 5: Start New Transaction
1. Click **"📺 Customer Screen"** again to create a new session
2. Repeat the process

## Customer Display States

### 1. Idle State (Welcome)
- Shown when no items are scanned yet
- Displays: "Welcome! / स्वागत है!"
- Message: "Your items will appear here as they are scanned"

### 2. Active State (Scanning)
- Shown when items are being scanned
- Displays table with:
  - Item name
  - Quantity + unit
  - Rate (price per unit)
  - Amount (line total)
- Large total at bottom
- Last scanned item is highlighted briefly (green flash)
- Status bar: "🟢 Scanning in progress…"

### 3. Checked Out State (Thank You)
- Shown after cashier clicks "Send"
- Displays:
  - 🙏 emoji
  - "Thank You!"
  - "धन्यवाद! पधारो फिर।" (Hindi)
  - Final total paid
- Status bar: "✅ Payment complete – Thank you!"

## Technical Details

### Backend Routes
- `GET /customer-display?session=<id>` - Customer display page
- `POST /api/display-session` - Create new session
- `GET /api/display-session/<id>` - Get session data
- `PATCH /api/display-session/<id>` - Update session data

### Session Data Structure
```json
{
  "session_id": "uuid",
  "shop_name": "Kirana Shop",
  "items": [
    {
      "code": "barcode",
      "name": "Product Name",
      "qty": 2,
      "unit": "pkt",
      "unit_price": 10.00,
      "line_total": 20.00
    }
  ],
  "grand_total": 20.00,
  "status": "active",  // or "checked_out"
  "updated_at": "2026-03-12T21:00:00"
}
```

### Polling Interval
- Customer screen polls backend every **1.5 seconds**
- Lightweight GET request
- Updates UI only when data changes

## Tips for Best Experience

1. **Use a Second Monitor**: Position customer display on a second screen facing the customer
2. **Full Screen**: Press F11 on customer display for full-screen mode
3. **Keep Session Active**: Don't close customer display window between transactions
4. **Refresh if Needed**: If customer display gets out of sync, just refresh the page

## Troubleshooting

### Customer display doesn't open
- **Check popup blocker**: Allow popups for this site
- **Try manually**: Copy the URL from console and open in new tab

### Items don't appear on customer screen
- **Check session ID**: Make sure both screens use same session
- **Refresh customer display**: Press F5 to reload
- **Check network**: Ensure both screens can reach the server

### Display shows old data
- **Create new session**: Click "📺 Customer Screen" again
- **Clear browser cache**: Ctrl+Shift+Delete

## Future Enhancements (Not Yet Implemented)

- Persistent sessions in Firestore (currently in-memory only)
- WebSocket for instant updates (currently polling)
- Multiple concurrent sessions per shop
- Customer display customization (logo, colors, language)
- QR code for easy customer display setup
- Mobile-friendly customer display

## Notes

- Sessions are stored **in-memory** only (lost on server restart)
- Only one active session per browser recommended
- Customer display works on any device with a browser
- No authentication required for customer display (read-only)

