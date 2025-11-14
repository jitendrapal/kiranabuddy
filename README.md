# 🏪 Kirana Shop Management App

A complete WhatsApp-based inventory management system for Kirana (grocery) shops built with Python Flask, Firebase Firestore, OpenAI (Whisper + GPT-4o-mini), and WhatsApp integration.

## ✨ Features

### 📱 WhatsApp Integration

- **Text Commands**: Process natural language commands in Hindi, English, or Hinglish
- **Voice Commands**: Transcribe voice notes using OpenAI Whisper and process them
- **Dual Provider Support**: Works with both WATI and WhatsApp Cloud API
- **Auto-Reply**: Sends confirmation messages back to users

### 🤖 AI-Powered Command Processing

- **Natural Language Understanding**: Uses GPT-4o-mini to parse commands
- **Multi-language Support**: Understands Hindi, English, and Hinglish
- **Smart Parsing**: Extracts action, product name, and quantity from messages
- **Examples**:
  - "Add 10 Maggi" → Adds 10 units of Maggi
  - "2 oil sold" → Reduces 2 units of oil
  - "Kitna stock hai atta?" → Checks stock of atta (flour)

### 📊 Inventory Management

- **Add Stock**: Add new inventory to products
- **Reduce Stock**: Record sales or consumption
- **Check Stock**: Query current stock levels
- **Transaction History**: Complete audit trail of all inventory changes

### 🏢 Multi-Shop Support

- **Multiple Shops**: Support for multiple independent shops
- **Owner + Staff**: Each shop can have an owner and multiple staff members
- **Role-Based Access**: Different permissions for owners and staff

### 🔥 Firebase Firestore Database

- **Real-time Updates**: Instant synchronization across devices
- **Scalable**: Cloud-based NoSQL database
- **Structured Data**: Organized collections for shops, users, products, and transactions

## 🏗️ Architecture

```
┌─────────────┐
│  WhatsApp   │
│   User      │
└──────┬──────┘
       │ Text/Voice Message
       ▼
┌─────────────────────────────┐
│  WhatsApp Provider          │
│  (WATI / WhatsApp Cloud)    │
└──────┬──────────────────────┘
       │ Webhook
       ▼
┌─────────────────────────────┐
│  Flask App (app.py)         │
│  - Webhook Handler          │
│  - API Endpoints            │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  Command Processor          │
│  - Message Routing          │
│  - User Validation          │
└──────┬──────────────────────┘
       │
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ OpenAI   │   │ Firebase │   │WhatsApp  │
│ Service  │   │ Firestore│   │ Service  │
│          │   │          │   │          │
│ Whisper  │   │ Database │   │ Sender   │
│ GPT-4o   │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘
```

## 📁 Project Structure

```
kiranaBook/
├── app.py                  # Main Flask application
├── config.py              # Configuration management
├── models.py              # Data models (Shop, User, Product, Transaction)
├── database.py            # Firebase Firestore operations
├── ai_service.py          # OpenAI integration (Whisper + GPT)
├── whatsapp_service.py    # WhatsApp messaging (WATI + Cloud API)
├── command_processor.py   # Command processing logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Firebase Project** with Firestore enabled
3. **OpenAI API Key** with access to GPT-4o-mini and Whisper
4. **WhatsApp Provider** (choose one):
   - WATI account with API access
   - WhatsApp Cloud API (Meta Business)

### Installation Steps

#### 1. Clone and Setup

```bash
cd kiranaBook
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable Firestore Database
4. Go to Project Settings → Service Accounts
5. Click "Generate New Private Key"
6. Save the JSON file securely
7. Note the path to this file

#### 4. Configure OpenAI

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an API key
3. Ensure you have access to:
   - `whisper-1` model (for voice transcription)
   - `gpt-4o-mini` model (for command parsing)

#### 5. Configure WhatsApp Provider

**Option A: Using WATI**

1. Sign up at [WATI](https://www.wati.io/)
2. Get your API key from dashboard
3. Note your base URL (usually `https://live-server.wati.io`)
4. Configure webhook URL in WATI dashboard to point to your server's `/webhook` endpoint

**Option B: Using WhatsApp Cloud API**

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a Business App
3. Add WhatsApp product
4. Get your:
   - Phone Number ID
   - Access Token
5. Configure webhook URL to point to your server's `/webhook` endpoint
6. Set verify token (you choose this)

#### 6. Create Environment File

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Flask Configuration
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development
PORT=5000

# Firebase Configuration
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/firebase-service-account.json
FIREBASE_PROJECT_ID=your-firebase-project-id

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# WhatsApp Configuration - Choose ONE provider

# Option 1: WATI
WATI_API_KEY=your-wati-api-key
WATI_BASE_URL=https://live-server.wati.io

# Option 2: WhatsApp Cloud API
# WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
# WHATSAPP_ACCESS_TOKEN=your-access-token
# WHATSAPP_VERIFY_TOKEN=your-verify-token
```

#### 7. Run the Application

**Development Mode:**

```bash
python app.py
```

**Production Mode (with Gunicorn):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 8. Expose Webhook (for local development)

Use ngrok or similar tool:

```bash
ngrok http 5000
```

Copy the HTTPS URL and configure it in your WhatsApp provider's webhook settings.

## 📚 API Documentation

### Webhook Endpoint

**POST /webhook**

- Receives WhatsApp messages (text and voice)
- Processes commands automatically
- Sends replies back to users

**GET /webhook**

- WhatsApp Cloud API verification endpoint

### Shop Management

**POST /api/shops**
Create a new shop

```json
{
  "name": "Sharma Kirana Store",
  "owner_phone": "+919876543210",
  "owner_name": "Rajesh Sharma",
  "address": "123 Main Street, Delhi"
}
```

**POST /api/shops/{shop_id}/users**
Add staff member to a shop

```json
{
  "phone": "+919876543211",
  "name": "Amit Kumar"
}
```

**GET /api/shops/{shop_id}/products**
Get all products for a shop

**GET /api/shops/{shop_id}/transactions**
Get transaction history

### Testing

**POST /api/test/parse**
Test command parsing without executing

```json
{
  "message": "Add 10 Maggi"
}
```

## 💬 Usage Examples

### Text Commands

Users can send WhatsApp messages like:

1. **Add Stock**

   - "Add 10 Maggi"
   - "5 packets biscuit add karo"
   - "20 cold drink stock mein daalo"

2. **Reduce Stock (Sales)**

   - "2 oil sold"
   - "3 cold drink bech diya"
   - "Sold 5 packets of chips"

3. **Check Stock**
   - "Kitna stock hai atta?"
   - "How much Maggi do we have?"
   - "Check stock for oil"

### Voice Commands

Users can send voice notes with the same commands:

- Record: "दस मैगी ऐड करो" (Add 10 Maggi)
- Record: "दो तेल बिक गया" (2 oil sold)
- Record: "आटा का स्टॉक कितना है?" (How much atta stock?)

### System Responses

The system will reply with:

- ✅ "10 Maggi add ho gaya! Total stock: 50 pieces"
- ✅ "2 oil sold! Remaining stock: 18 pieces"
- 📦 "atta ka stock: 25 kg"

## 🗄️ Database Schema

### Collections

#### shops

```json
{
  "shop_id": "uuid",
  "name": "Sharma Kirana Store",
  "owner_phone": "+919876543210",
  "address": "123 Main Street",
  "active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### users

```json
{
  "user_id": "uuid",
  "phone": "+919876543210",
  "name": "Rajesh Sharma",
  "shop_id": "shop_uuid",
  "role": "owner",
  "active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### products

```json
{
  "product_id": "uuid",
  "shop_id": "shop_uuid",
  "name": "Maggi",
  "normalized_name": "maggi",
  "current_stock": 50,
  "unit": "pieces",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### transactions

```json
{
  "transaction_id": "uuid",
  "shop_id": "shop_uuid",
  "product_id": "product_uuid",
  "product_name": "Maggi",
  "transaction_type": "add_stock",
  "quantity": 10,
  "previous_stock": 40,
  "new_stock": 50,
  "user_phone": "+919876543210",
  "timestamp": "2024-01-01T00:00:00Z",
  "notes": "Added 10 pieces"
}
```

## 🔧 Configuration Options

### Environment Variables

| Variable                         | Required    | Description                                   |
| -------------------------------- | ----------- | --------------------------------------------- |
| `SECRET_KEY`                     | Yes         | Flask secret key for sessions                 |
| `FLASK_ENV`                      | No          | Environment (development/production)          |
| `PORT`                           | No          | Port to run the app (default: 5000)           |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes         | Path to Firebase service account JSON         |
| `FIREBASE_PROJECT_ID`            | Yes         | Firebase project ID                           |
| `OPENAI_API_KEY`                 | Yes         | OpenAI API key                                |
| `OPENAI_MODEL`                   | No          | Model to use (default: gpt-4o-mini)           |
| `WATI_API_KEY`                   | Conditional | WATI API key (if using WATI)                  |
| `WATI_BASE_URL`                  | No          | WATI base URL                                 |
| `WHATSAPP_PHONE_NUMBER_ID`       | Conditional | WhatsApp phone number ID (if using Cloud API) |
| `WHATSAPP_ACCESS_TOKEN`          | Conditional | WhatsApp access token (if using Cloud API)    |
| `WHATSAPP_VERIFY_TOKEN`          | No          | Webhook verification token                    |

## 🧪 Testing

### Test Command Parsing

```bash
curl -X POST http://localhost:5000/api/test/parse \
  -H "Content-Type: application/json" \
  -d '{"message": "Add 10 Maggi"}'
```

Response:

```json
{
  "success": true,
  "parsed": {
    "action": "add_stock",
    "product_name": "Maggi",
    "quantity": 10,
    "confidence": 0.95,
    "is_valid": true
  }
}
```

### Create a Test Shop

```bash
curl -X POST http://localhost:5000/api/shops \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Kirana Store",
    "owner_phone": "+919876543210",
    "owner_name": "Test Owner",
    "address": "Test Address"
  }'
```

## 🚀 Deployment

### Deploy to Heroku

1. Create a Heroku app:

```bash
heroku create your-app-name
```

2. Add buildpack:

```bash
heroku buildpacks:set heroku/python
```

3. Set environment variables:

```bash
heroku config:set OPENAI_API_KEY=your-key
heroku config:set FIREBASE_PROJECT_ID=your-project-id
# ... set all other variables
```

4. Deploy:

```bash
git push heroku main
```

### Deploy to Google Cloud Run

1. Build container:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/kirana-app
```

2. Deploy:

```bash
gcloud run deploy kirana-app \
  --image gcr.io/PROJECT_ID/kirana-app \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **API Keys**: Rotate API keys regularly
3. **Webhook Verification**: Implement webhook signature verification
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Authentication**: Add authentication for admin endpoints
6. **HTTPS**: Always use HTTPS in production
7. **Input Validation**: Validate all user inputs

## 🐛 Troubleshooting

### Common Issues

**1. Firebase Authentication Error**

- Ensure `GOOGLE_APPLICATION_CREDENTIALS` path is correct
- Check if service account has Firestore permissions

**2. OpenAI API Error**

- Verify API key is valid
- Check if you have credits/quota available
- Ensure you have access to required models

**3. WhatsApp Webhook Not Receiving Messages**

- Verify webhook URL is publicly accessible (use ngrok for local testing)
- Check webhook verification token matches
- Ensure webhook is configured in provider dashboard

**4. Voice Transcription Failing**

- Check audio file format is supported
- Verify file size is within limits (25MB)
- Ensure OpenAI API has Whisper access

## 📈 Future Enhancements

- [ ] Admin dashboard (web interface)
- [ ] Product categories and pricing
- [ ] Sales analytics and reports
- [ ] Low stock alerts
- [ ] Barcode scanning support
- [ ] Multi-language response customization
- [ ] Customer management
- [ ] Invoice generation
- [ ] Payment tracking
- [ ] Supplier management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built with ❤️ for Kirana shop owners

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Happy Managing! 🏪📊**
