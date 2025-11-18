"""
Flask application for Kirana Shop Management
"""
from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import uuid
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



@app.route('/stock')
def stock_management():
    """Simple stock management page to view & edit products for a shop."""
    return render_template('stock_management.html')


@app.route('/test/audio-upload', methods=['POST'])
def test_audio_upload():
    """Upload voice note from test interface and return a temporary URL.

    The test chat records audio in the browser, sends it here, we save it
    under a temp folder, and return a URL that the WhatsApp-style webhook
    pipeline can download for transcription.
    """
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'}), 400

    # Derive extension (default to .webm which is what most browsers use)
    _, ext = os.path.splitext(file.filename)
    if not ext:
        ext = '.webm'

    audio_dir = os.path.join(app.root_path, 'temp_audio')
    os.makedirs(audio_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(audio_dir, filename)
    file.save(file_path)

    # Public URL that this same Flask app can serve and that the
    # transcription code can access via requests.get()
    base_url = request.host_url.rstrip('/')
    url = f"{base_url}/test/audio/{filename}"

    return jsonify({'success': True, 'url': url, 'format': ext.lstrip('.')})


@app.route('/test/audio/<path:filename>')
def test_audio_file(filename):
    """Serve uploaded test audio file for transcription."""
    audio_dir = os.path.join(app.root_path, 'temp_audio')
    return send_from_directory(audio_dir, filename)



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
                'transcribed_text': result.get('transcribed_text', ''),
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



@app.route('/api/stock/products', methods=['GET'])
def get_stock_products():
    """Get all products for the shop identified by phone (for stock UI)."""
    try:
        phone = (request.args.get('phone') or '').strip()
        if not phone:
            return jsonify({'success': False, 'message': 'phone is required'}), 400

        user = db.get_user_by_phone(phone)
        if user:
            shop_id = user.shop_id
        else:
            shop = db.get_shop_by_phone(phone)
            if not shop:
                return jsonify({'success': False, 'message': 'Shop or user not found for phone'}), 404
            shop_id = shop.shop_id

        products = db.get_products_by_shop(shop_id)
        return jsonify({
            'success': True,
            'products': [p.to_dict() for p in products]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/stock/products/<product_id>', methods=['PATCH'])
def update_stock_product(product_id):
    """Update product fields (barcode, batch expiry/qty) for stock UI.

    We require the caller's phone so we can resolve the shop and ensure the
    product belongs to that shop before applying updates.
    """
    try:
        phone = (request.args.get('phone') or '').strip()
        if not phone:
            return jsonify({'success': False, 'message': 'phone is required'}), 400

        # Resolve shop from phone
        user = db.get_user_by_phone(phone)
        if user:
            shop_id = user.shop_id
        else:
            shop = db.get_shop_by_phone(phone)
            if not shop:
                return jsonify({'success': False, 'message': 'Shop or user not found for phone'}), 404
            shop_id = shop.shop_id

        # Load product and verify ownership
        product = db.get_product(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
        if product.shop_id != shop_id:
            return jsonify({'success': False, 'message': 'Product does not belong to this shop'}), 403

        data = request.get_json() or {}
        updates = {}

        if 'barcode' in data:
            barcode_val = (data.get('barcode') or '').strip()
            updates['barcode'] = barcode_val or None

        # Optional simple expiry_date override (rarely used if batches exist)
        if 'expiry_date' in data:
            expiry_val = (data.get('expiry_date') or '').strip() or None
            updates['expiry_date'] = expiry_val

        # Optional batches payload: recompute current_stock from per-batch qty
        batches_val = data.get('batches')
        if isinstance(batches_val, dict):
            total_qty = 0.0
            for b in batches_val.values():
                if not isinstance(b, dict):
                    continue
                qty_raw = b.get('qty') or b.get('quantity')
                if qty_raw is None:
                    continue
                try:
                    total_qty += float(qty_raw)
                except Exception:
                    continue
            updates['batches'] = batches_val
            updates['current_stock'] = total_qty

        if not updates:
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400

        db.update_product_fields(product_id, updates)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500



@app.route('/api/stock/bill', methods=['POST'])
def add_stock_bill():
    """Fast bill entry: add stock for multiple products in one go.

    Expects JSON:
    {
        "phone": "+91...",
        "items": [
            {"product_id": "...", "name": "Maggi 70g", "quantity": 12, "cost_price": 10.5, "note": "optional"},
            ...
        ]
    }
    """
    try:
        data = request.get_json() or {}
        phone = (data.get('phone') or '').strip()
        items = data.get('items') or []

        if not phone:
            return jsonify({'success': False, 'message': 'phone is required'}), 400
        if not items:
            return jsonify({'success': False, 'message': 'items is required'}), 400

        # Resolve shop from phone (same logic as other stock APIs)
        user = db.get_user_by_phone(phone)
        if user:
            shop_id = user.shop_id
        else:
            shop = db.get_shop_by_phone(phone)
            if not shop:
                return jsonify({'success': False, 'message': 'Shop or user not found for phone'}), 404
            shop_id = shop.shop_id

        results = []
        for raw in items:
            if not isinstance(raw, dict):
                continue

            # Parse quantity
            qty_raw = raw.get('quantity')
            try:
                qty = float(qty_raw)
            except Exception:
                continue
            if qty <= 0:
                continue

            # Find product: prefer product_id, fallback to name
            product_id = (raw.get('product_id') or '').strip()
            name = (raw.get('name') or '').strip()
            product_name_for_add = None

            if product_id:
                product = db.get_product(product_id)
                if not product or product.shop_id != shop_id:
                    continue
                product_name_for_add = product.name
            elif name:
                product_name_for_add = name
            else:
                continue

            # Use existing add_stock helper to update stock + create transaction
            res = db.add_stock(shop_id, product_name_for_add, qty, phone)

            # Optional cost_price update on the Product document
            cost_price_raw = raw.get('cost_price')
            unit_cost = None
            if cost_price_raw is not None:
                try:
                    unit_cost = float(cost_price_raw)
                    if unit_cost < 0:
                        unit_cost = None
                except Exception:
                    unit_cost = None

            if unit_cost is not None:
                try:
                    prod = db.find_existing_product_by_name(shop_id, res.get('product_name'))
                    if prod:
                        db.update_product_fields(prod.product_id, {'cost_price': unit_cost})
                except Exception:
                    # Cost update is best-effort; ignore failures here
                    pass

            results.append({
                'product_name': res.get('product_name'),
                'quantity': res.get('quantity'),
                'previous_stock': res.get('previous_stock'),
                'new_stock': res.get('new_stock'),
                'unit': res.get('unit'),
            })

        if not results:
            return jsonify({'success': False, 'message': 'No valid items to process'}), 400

        return jsonify({'success': True, 'items': results}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500





@app.route('/api/product-by-barcode', methods=['GET'])
def get_product_by_barcode():
    """Lookup a product by barcode for the test interface.

    Uses the phone number to resolve the correct shop, then finds an
    existing product for that shop whose barcode matches.
    """
    try:
        barcode = (request.args.get('barcode') or '').strip()
        phone = (request.args.get('phone') or '').strip()

        if not barcode:
            return jsonify({'success': False, 'message': 'barcode is required'}), 400
        if not phone:
            return jsonify({'success': False, 'message': 'phone is required'}), 400

        user = db.get_user_by_phone(phone)
        if user:
            shop_id = user.shop_id
        else:
            shop = db.get_shop_by_phone(phone)
            if not shop:
                return jsonify({'success': False, 'message': 'Shop or user not found for phone'}), 404
            shop_id = shop.shop_id

        product = db.find_existing_product_by_name(shop_id, barcode)
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404

        return jsonify({
            'success': True,
            'product': {
                'name': product.name,
                'brand': getattr(product, 'brand', None),
                'unit': product.unit,
                'barcode': product.barcode,
                'selling_price': getattr(product, 'selling_price', None),
            },
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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
