"""
Flask application for Kirana Shop Management
"""
from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from functools import wraps
import os
import uuid
from datetime import datetime
from config import Config
from database import FirestoreDB
from ai_service import AIService
from whatsapp_service import WhatsAppService
from command_processor import CommandProcessor
from models import UserRole
from otp_service import OTPService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production-' + str(uuid.uuid4()))

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

# Initialize OTP service
otp_service = OTPService(db.db)

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


# ==================== AUTHENTICATION DECORATOR ====================

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_phone' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== OTP AUTHENTICATION ROUTES ====================

@app.route('/login')
def login_page():
    """OTP login page"""
    return render_template('login.html')


@app.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    """Send OTP to phone number with rate limiting and security"""
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()

        if not phone:
            return jsonify({
                'success': False,
                'message': 'Phone number is required'
            }), 400

        # Validate phone number (basic validation)
        phone = phone.replace('+91', '').replace('+', '').replace('-', '').replace(' ', '')
        if not phone.isdigit() or len(phone) != 10:
            return jsonify({
                'success': False,
                'message': 'Please enter a valid 10-digit phone number'
            }), 400

        # Create OTP (with rate limiting)
        otp_result = otp_service.create_otp(phone)

        if not otp_result['success']:
            # Rate limit or cooldown error
            return jsonify(otp_result), 429

        otp = otp_result['otp']
        otp_code = otp_result['otp_code']

        # Send OTP
        send_result = otp_service.send_otp(phone, otp_code)

        if send_result['success']:
            response_data = {
                'success': True,
                'message': f'OTP sent to {phone}',
                'otp_id': otp.otp_id,
                'expires_in_minutes': otp_service.otp_validity_minutes,
                'provider': send_result.get('provider', 'unknown')
            }

            # In development mode, include OTP in response
            if otp_service.dev_mode or otp_service.sms_provider == 'console':
                response_data['dev_otp'] = otp_code
                response_data['dev_mode'] = True

            return jsonify(response_data)
        else:
            return jsonify({
                'success': False,
                'message': send_result['message']
            }), 500

    except Exception as e:
        print(f"❌ Error sending OTP: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error sending OTP: {str(e)}'
        }), 500


@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP and login user"""
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        otp_code = data.get('otp', '').strip()
        name = data.get('name', '').strip()

        if not phone or not otp_code:
            return jsonify({
                'success': False,
                'message': 'Phone number and OTP are required'
            }), 400

        # Clean phone number
        phone = phone.replace('+91', '').replace('+', '').replace('-', '').replace(' ', '')

        # Verify OTP
        verify_result = otp_service.verify_otp(phone, otp_code)

        if not verify_result['success']:
            return jsonify(verify_result), 400

        # OTP verified successfully - check if user exists
        user = db.get_user_by_phone(phone)

        if not user:
            # New user - create account
            if not name:
                return jsonify({
                    'success': False,
                    'message': 'Name is required for new users',
                    'requires_name': True
                }), 400

            # Create shop for new user
            shop_id = str(uuid.uuid4())
            shop_name = f"{name}'s Shop"

            db.db.collection('shops').document(shop_id).set({
                'shop_id': shop_id,
                'name': shop_name,
                'owner_phone': phone,
                'created_at': datetime.now().isoformat(),
                'active': True
            })

            # Create user
            user = db.create_user(
                phone=phone,
                name=name,
                shop_id=shop_id,
                role=UserRole.OWNER
            )

        # Update last login
        db.db.collection('users').document(user.user_id).update({
            'last_login': datetime.now().isoformat()
        })

        # Create session
        session['user_phone'] = user.phone
        session['user_id'] = user.user_id
        session['shop_id'] = user.shop_id
        session['user_name'] = user.name
        session['user_role'] = user.role.value

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'phone': user.phone,
                'name': user.name,
                'shop_id': user.shop_id,
                'role': user.role.value
            },
            'redirect_url': '/test'
        })

    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return jsonify({
            'success': False,
            'message': f'Error verifying OTP: {str(e)}'
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })


@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    if 'user_phone' in session:
        return jsonify({
            'authenticated': True,
            'user': {
                'phone': session.get('user_phone'),
                'name': session.get('user_name'),
                'shop_id': session.get('shop_id'),
                'role': session.get('user_role')
            }
        })
    return jsonify({'authenticated': False})


# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Kirana Shop Management API',
        'version': '1.0.0'
    })


@app.route('/test')
@login_required
def test_interface():
    """Test interface - No WhatsApp required!"""
    shop_id = session.get('shop_id')

    # Get shop name from database
    shop_name = "My Shop"
    if shop_id:
        try:
            shop_doc = db.db.collection('shops').document(shop_id).get()
            if shop_doc.exists:
                shop_name = shop_doc.to_dict().get('name', 'My Shop')
        except Exception as e:
            print(f"Error fetching shop name: {e}")

    user_data = {
        'phone': session.get('user_phone'),
        'name': session.get('user_name'),
        'shop_id': shop_id,
        'shop_name': shop_name,
        'role': session.get('user_role')
    }
    return render_template('test_interface.html', user=user_data)



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


@app.route('/api/transcribe-voice', methods=['POST'])
def transcribe_voice():
    """
    Transcribe voice audio directly using Whisper API
    Works on all mobile browsers (Android, iOS, iPad)
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']

        if not audio_file or audio_file.filename == '':
            return jsonify({'success': False, 'error': 'Empty audio file'}), 400

        print(f"🎤 Received voice file: {audio_file.filename}, size: {audio_file.content_length} bytes")

        # Process audio in-memory (no disk storage needed)
        # This works on any server without needing temp directories
        print(f"🔊 Transcribing with Whisper (in-memory)...")

        # Read audio data into memory
        audio_file.seek(0)  # Reset file pointer to beginning
        audio_data = audio_file.read()
        print(f"   Audio size: {len(audio_data)} bytes")

        # Create a file-like object from bytes for Whisper API
        from io import BytesIO
        audio_buffer = BytesIO(audio_data)
        audio_buffer.name = "voice.webm"  # Whisper needs a filename

        try:
            # Two-pass approach:
            # Pass 1: Auto-detect and check what script is used
            # Pass 2: If Urdu script detected, re-transcribe as Hindi (Devanagari)
            print(f"   Pass 1: Auto-detecting language...")

            # First pass - auto-detect
            transcript_detect = ai_service.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_buffer,
                response_format="verbose_json"
            )

            detected_language = transcript_detect.language
            detected_text = transcript_detect.text
            print(f"   🌐 Detected language: {detected_language}")
            print(f"   📝 Detected text: {detected_text[:50]}...")

            # Check if text contains Urdu/Arabic script (U+0600 to U+06FF)
            import re
            has_urdu_script = bool(re.search(r'[\u0600-\u06FF]', detected_text))
            has_devanagari = bool(re.search(r'[\u0900-\u097F]', detected_text))
            has_latin = bool(re.search(r'[a-zA-Z]', detected_text))

            print(f"   Script analysis: Urdu={has_urdu_script}, Devanagari={has_devanagari}, Latin={has_latin}")

            # If Urdu script detected, re-transcribe as Hindi (Devanagari)
            if has_urdu_script:
                print(f"   🔄 Urdu script detected! Re-transcribing as Hindi (Devanagari)...")

                # Create fresh buffer
                audio_buffer_new = BytesIO(audio_data)
                audio_buffer_new.name = "voice.webm"

                transcript = ai_service.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_buffer_new,
                    response_format="text",
                    language="hi"  # Force Devanagari script
                )
                print(f"   ✅ Re-transcribed in Devanagari: {transcript[:50]}...")
            else:
                # English or already Devanagari - use original
                print(f"   ✅ Using original transcription")
                transcript = detected_text

            print(f"   Final transcript: {transcript[:100]}...")

            # Get text from response
            print(f"   Transcript type: {type(transcript)}")
            print(f"   Transcript value: {repr(transcript)}")

            if isinstance(transcript, str):
                text = transcript
            else:
                text = getattr(transcript, 'text', str(transcript))

            text = text.strip()

            print(f"📝 Raw transcript: {repr(text)}")
            print(f"📝 Transcript length: {len(text)} characters")
            print(f"📝 Transcript type: {type(text)}")

            if not text:
                print(f"❌ Empty transcript received from Whisper!")
                print(f"   Audio file size was: {os.path.getsize(temp_path)} bytes")
                return jsonify({
                    'success': False,
                    'error': 'Whisper returned empty transcript. Audio may be too short or unclear.'
                }), 400

            # STEP 1: Remove Whisper artifacts (always appears at end)
            # Whisper sometimes adds these phrases consistently
            import re
            whisper_artifacts = [
                r'\s+coming\s+you\s*$',
                r'\s+also\s+coming\s+you\s*$',
                r'\s+also\s+coming\s*$',
                r'\s+you\s*$',
            ]

            for artifact in whisper_artifacts:
                text = re.sub(artifact, '', text, flags=re.IGNORECASE)

            text = text.strip()

            print(f"🧹 After artifact removal: {repr(text)}")

            # STEP 2: Clean the transcribed text (filler words, etc.)
            cleaned_text = ai_service.clean_voice_text(text)

            print(f"✨ Final cleaned transcript: {repr(cleaned_text)}")

            return jsonify({
                'success': True,
                'text': cleaned_text,
                'raw_text': text
            })

        except Exception as inner_e:
            print(f"❌ Error during transcription: {inner_e}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Transcription error: {str(inner_e)}'
            }), 500

    except Exception as e:
        print(f"❌ Error transcribing voice: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Transcription error: {str(e)}'
        }), 500



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


@app.route('/api/stock/create-product', methods=['POST'])
def create_new_product():
    """Create a new product with barcode, name, quantity, and expiry date.

    Expects JSON:
    {
        "phone": "+91...",
        "barcode": "8901234567890",
        "name": "Maggi Noodles 70g",
        "brand": "Nestle",
        "quantity": 50,
        "unit": "pieces",
        "expiry_date": "2025-12-31",
        "selling_price": 12.0,
        "cost_price": 10.0
    }
    """
    try:
        data = request.get_json() or {}
        phone = (data.get('phone') or '').strip()
        barcode = (data.get('barcode') or '').strip()
        name = (data.get('name') or '').strip()
        brand = (data.get('brand') or '').strip() or None
        quantity = data.get('quantity')
        unit = (data.get('unit') or 'pieces').strip()
        expiry_date = (data.get('expiry_date') or '').strip() or None
        selling_price = data.get('selling_price')
        cost_price = data.get('cost_price')

        # Validation
        if not phone:
            return jsonify({'success': False, 'message': 'phone is required'}), 400
        if not barcode:
            return jsonify({'success': False, 'message': 'barcode is required'}), 400
        if not name:
            return jsonify({'success': False, 'message': 'name is required'}), 400
        if quantity is None or quantity < 0:
            return jsonify({'success': False, 'message': 'valid quantity is required'}), 400

        # Resolve shop from phone
        user = db.get_user_by_phone(phone)
        if user:
            shop_id = user.shop_id
        else:
            shop = db.get_shop_by_phone(phone)
            if not shop:
                return jsonify({'success': False, 'message': 'Shop or user not found for phone'}), 404
            shop_id = shop.shop_id

        # Check if product with this barcode already exists
        existing_product = db.find_product_by_barcode(shop_id, barcode)
        if existing_product:
            return jsonify({
                'success': False,
                'message': f'Product with barcode {barcode} already exists: {existing_product.name}'
            }), 400

        # Create new product
        import uuid
        from datetime import datetime
        from models import Product

        product_id = str(uuid.uuid4())

        # Create batches structure if expiry date is provided
        batches = None
        if expiry_date:
            batch_id = "batch_001"
            batches = {
                batch_id: {
                    "expiry_date": expiry_date,
                    "qty": float(quantity),
                    "cost_price": float(cost_price) if cost_price is not None else None,
                    "added_on": datetime.utcnow().isoformat()
                }
            }

        product = Product(
            product_id=product_id,
            shop_id=shop_id,
            name=name,
            normalized_name=name.lower().strip(),
            current_stock=float(quantity),
            unit=unit,
            brand=brand,
            barcode=barcode,
            selling_price=float(selling_price) if selling_price is not None else None,
            cost_price=float(cost_price) if cost_price is not None else None,
            expiry_date=expiry_date,  # Keep legacy field for backward compatibility
            batches=batches,  # Add batch structure
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Save to database
        db.db.collection("products").document(product_id).set(product.to_dict())

        # Create transaction record for initial stock
        from models import TransactionType
        db.create_transaction(
            shop_id=shop_id,
            product_id=product_id,
            product_name=name,
            transaction_type=TransactionType.ADD_STOCK,
            quantity=float(quantity),
            previous_stock=0.0,
            new_stock=float(quantity),
            user_phone=phone,
            notes=f"Initial stock for new product",
        )

        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
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


# ==================== BUG TRACKING ROUTES ====================

@app.route('/bug')
@login_required
def bug_page():
    """Page to view unrecognized commands (bugs)"""
    return render_template('bug.html')


@app.route('/api/bug', methods=['GET'])
def get_bug_api():
    """API endpoint to get unrecognized commands for a shop"""
    try:
        phone = request.args.get('phone')
        include_resolved = request.args.get('include_resolved', 'false').lower() == 'true'

        if not phone:
            return jsonify({
                'success': False,
                'message': 'Phone number is required'
            }), 400

        # Get shop by phone
        shop = db.get_shop_by_phone(phone)
        if not shop:
            return jsonify({
                'success': False,
                'message': f'No shop found for phone: {phone}'
            }), 404

        # Get unrecognized commands
        commands = db.get_unrecognized_commands(
            shop_id=shop.shop_id,
            include_resolved=include_resolved
        )

        # Convert to dict for JSON response
        commands_data = []
        for cmd in commands:
            commands_data.append({
                'command_id': cmd.command_id,
                'shop_id': cmd.shop_id,
                'user_phone': cmd.user_phone,
                'message_type': cmd.message_type,
                'raw_text': cmd.raw_text,
                'transcribed_text': cmd.transcribed_text,
                'cleaned_text': cmd.cleaned_text,
                'parsed_action': cmd.parsed_action,
                'confidence': cmd.confidence,
                'timestamp': cmd.timestamp.isoformat(),
                'resolved': cmd.resolved,
                'resolution_notes': cmd.resolution_notes,
            })

        return jsonify({
            'success': True,
            'shop_id': shop.shop_id,
            'shop_name': shop.name,
            'commands': commands_data
        }), 200

    except Exception as e:
        print(f"Error getting unrecognized commands: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/bug/resolve', methods=['POST'])
def resolve_bug():
    """API endpoint to mark a command as resolved"""
    try:
        data = request.get_json()
        command_id = data.get('command_id')
        notes = data.get('notes', '')

        if not command_id:
            return jsonify({
                'success': False,
                'message': 'command_id is required'
            }), 400

        success = db.mark_command_resolved(command_id, notes)

        return jsonify({
            'success': success,
            'message': 'Command marked as resolved' if success else 'Failed to mark as resolved'
        }), 200

    except Exception as e:
        print(f"Error resolving command: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/bug/delete', methods=['POST'])
def delete_bug():
    """API endpoint to delete a command"""
    try:
        data = request.get_json()
        command_id = data.get('command_id')

        if not command_id:
            return jsonify({
                'success': False,
                'message': 'command_id is required'
            }), 400

        success = db.delete_unrecognized_command(command_id)

        return jsonify({
            'success': success,
            'message': 'Command deleted' if success else 'Failed to delete command'
        }), 200

    except Exception as e:
        print(f"Error deleting command: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)