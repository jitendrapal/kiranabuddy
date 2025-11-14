"""
Flask application for Kirana Shop Management
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from config import Config
from database import FirestoreDB
from ai_service import AIService
from whatsapp_service import WhatsAppService
from command_processor import CommandProcessor
from models import UserRole

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    exit(1)

# Initialize services
print(f"🔧 Initializing database with:")
print(f"   credentials_path: {Config.GOOGLE_APPLICATION_CREDENTIALS}")
print(f"   project_id: {Config.FIREBASE_PROJECT_ID}")

db = FirestoreDB(
    credentials_path=Config.GOOGLE_APPLICATION_CREDENTIALS,
    project_id=Config.FIREBASE_PROJECT_ID
)

print(f"✅ Database initialized")

ai_service = AIService(
    api_key=Config.OPENAI_API_KEY,
    model=Config.OPENAI_MODEL
)

# Determine WhatsApp provider
whatsapp_provider = "wati" if Config.WATI_API_KEY else "whatsapp_cloud"

if whatsapp_provider == "wati":
    whatsapp_service = WhatsAppService(
        provider="wati",
        api_key=Config.WATI_API_KEY,
        base_url=Config.WATI_BASE_URL
    )
else:
    whatsapp_service = WhatsAppService(
        provider="whatsapp_cloud",
        access_token=Config.WHATSAPP_ACCESS_TOKEN,
        phone_number_id=Config.WHATSAPP_PHONE_NUMBER_ID
    )

command_processor = CommandProcessor(
    db=db,
    ai_service=ai_service,
    whatsapp_service=whatsapp_service
)


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Kirana Shop Management API',
        'version': '1.0.0'
    })


@app.route('/test')
def test_interface():
    """Test interface - No WhatsApp required!"""
    return render_template('test_interface.html')


@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.svg',
        mimetype='image/svg+xml'
    )


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    WhatsApp webhook endpoint
    Handles both WATI and WhatsApp Cloud API webhooks
    """
    if request.method == 'GET':
        # WhatsApp Cloud API verification
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == Config.WHATSAPP_VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Forbidden', 403

    elif request.method == 'POST':
        try:
            payload = request.get_json()

            if not payload:
                return jsonify({'status': 'error', 'message': 'No payload'}), 400

            # Parse webhook based on provider
            if whatsapp_provider == "wati":
                message_data = WhatsAppService.parse_wati_webhook(payload)
            else:
                message_data = WhatsAppService.parse_whatsapp_cloud_webhook(payload)

            if not message_data or not message_data.get('from_phone'):
                return jsonify({'status': 'ok', 'message': 'No message to process'}), 200

            # Process the message
            result = command_processor.process_message(
                from_phone=message_data['from_phone'],
                message_type=message_data['message_type'],
                text=message_data.get('text'),
                media_url=message_data.get('media_url'),
                media_format=message_data.get('media_format')
            )

            # Send reply if needed (only if WhatsApp is configured)
            reply_sent = False
            if result.get('send_reply') and result.get('message'):
                try:
                    reply_sent = whatsapp_service.send_message(
                        to_phone=message_data['from_phone'],
                        message=result['message']
                    )
                except Exception as e:
                    print(f"WhatsApp send failed (this is OK for testing): {e}")
                    reply_sent = False

            return jsonify({
                'status': 'ok',
                'processed': True,
                'success': result.get('success', False),
                'message': result.get('message', ''),
                'reply_sent': reply_sent,
                'data': result.get('result', {})
            }), 200

        except Exception as e:
            print(f"❌ WEBHOOK ERROR: {e}")
            import traceback
            print("Full traceback:")
            traceback.print_exc()
            return jsonify({
                'status': 'error',
                'message': str(e),
                'error_type': type(e).__name__
            }), 500


@app.route('/api/shops', methods=['POST'])
def create_shop():
    """Create a new shop"""
    try:
        data = request.get_json()

        name = data.get('name')
        owner_phone = data.get('owner_phone')
        address = data.get('address')

        if not name or not owner_phone:
            return jsonify({'error': 'name and owner_phone are required'}), 400

        # Create shop
        shop = db.create_shop(name=name, owner_phone=owner_phone, address=address)

        # Create owner user
        owner_name = data.get('owner_name', 'Owner')
        user = db.create_user(
            phone=owner_phone,
            name=owner_name,
            shop_id=shop.shop_id,
            role=UserRole.OWNER
        )

        return jsonify({
            'success': True,
            'shop': shop.to_dict(),
            'owner': user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/shops/<shop_id>/users', methods=['POST'])
def add_staff(shop_id):
    """Add staff member to a shop"""
    try:
        data = request.get_json()

        phone = data.get('phone')
        name = data.get('name')

        if not phone or not name:
            return jsonify({'error': 'phone and name are required'}), 400

        # Verify shop exists
        shop = db.get_shop(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404

        # Create staff user
        user = db.create_user(
            phone=phone,
            name=name,
            shop_id=shop_id,
            role=UserRole.STAFF
        )

        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/shops/<shop_id>/products', methods=['GET'])
def get_products(shop_id):
    """Get all products for a shop"""
    try:
        products = db.get_products_by_shop(shop_id)

        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/shops/<shop_id>/transactions', methods=['GET'])
def get_transactions(shop_id):
    """Get recent transactions for a shop"""
    try:
        limit = int(request.args.get('limit', 100))
        transactions = db.get_transactions_by_shop(shop_id, limit=limit)

        return jsonify({
            'success': True,
            'transactions': [t.to_dict() for t in transactions]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/parse', methods=['POST'])
def test_parse():
    """Test endpoint to parse a command without executing it"""
    try:
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({'error': 'message is required'}), 400

        parsed = ai_service.parse_command(message)

        return jsonify({
            'success': True,
            'parsed': {
                'action': parsed.action.value,
                'product_name': parsed.product_name,
                'quantity': parsed.quantity,
                'confidence': parsed.confidence,
                'is_valid': parsed.is_valid()
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
