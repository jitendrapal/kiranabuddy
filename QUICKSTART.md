# 🚀 Quick Start Guide

Get your Kirana Shop Management App running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Setup Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Required
OPENAI_API_KEY=sk-your-key-here
FIREBASE_PROJECT_ID=your-project-id

# Choose ONE WhatsApp provider
WATI_API_KEY=your-wati-key
# OR
WHATSAPP_ACCESS_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
```

## Step 3: Setup Firebase

1. Download your Firebase service account JSON file
2. Save it somewhere safe (e.g., `firebase-credentials.json`)
3. Update `.env`:

```env
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/firebase-credentials.json
```

## Step 4: Test Your Setup

```bash
python test_setup.py
```

This will verify:
- ✅ All environment variables are set
- ✅ All packages are installed
- ✅ OpenAI API is working
- ✅ Firebase connection is working

## Step 5: Run the App

```bash
python app.py
```

You should see:

```
 * Running on http://0.0.0.0:5000
```

## Step 6: Test the API

Open a new terminal and run:

```bash
python example_usage.py
```

This will:
- Create a test shop
- Add a staff member
- Test command parsing
- Simulate WhatsApp messages
- Show products and transactions

## Step 7: Expose Webhook (for WhatsApp)

For local development, use ngrok:

```bash
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and configure it in your WhatsApp provider:

**For WATI:**
- Go to WATI Dashboard → Settings → Webhooks
- Set webhook URL to: `https://abc123.ngrok.io/webhook`

**For WhatsApp Cloud API:**
- Go to Meta for Developers → Your App → WhatsApp → Configuration
- Set webhook URL to: `https://abc123.ngrok.io/webhook`
- Set verify token to match your `.env` file

## Step 8: Send a Test Message

Send a WhatsApp message to your configured number:

```
Add 10 Maggi
```

You should receive a reply:

```
✅ 10 Maggi add ho gaya! Total stock: 10 pieces
```

## 🎉 You're All Set!

Try these commands:
- "Add 5 oil"
- "2 Maggi sold"
- "Kitna stock hai oil?"
- Send a voice note: "दस बिस्कुट ऐड करो"

## 📝 Next Steps

1. **Create your shop**: Use the API to create your actual shop
2. **Add staff**: Add your team members
3. **Customize responses**: Edit `ai_service.py` to change response language/style
4. **Deploy**: Deploy to Heroku, Google Cloud, or your preferred platform

## 🆘 Troubleshooting

**Server won't start?**
- Check if port 5000 is available
- Verify all environment variables are set

**WhatsApp not receiving messages?**
- Ensure ngrok is running
- Verify webhook URL is configured correctly
- Check webhook verify token matches

**OpenAI errors?**
- Verify API key is valid
- Check you have credits available
- Ensure you have access to gpt-4o-mini and whisper-1

**Firebase errors?**
- Check service account JSON path is correct
- Verify Firestore is enabled in Firebase Console
- Ensure service account has proper permissions

## 📚 More Help

- See [README.md](README.md) for full documentation
- Run `python test_setup.py` to diagnose issues
- Check logs in the terminal where app.py is running

