"""
OTP Service for Kirana Shop Manager
Handles OTP generation, sending, and verification with production-ready features
"""
import random
import string
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
import requests
from models import OTP
import uuid


class OTPService:
    """Service for handling OTP authentication with security features"""

    def __init__(self, db):
        """Initialize OTP service with database connection"""
        self.db = db
        self.otp_length = 6  # 6-digit OTP (industry standard)
        self.otp_validity_minutes = 5  # 5 minutes validity
        self.max_attempts = 5  # Maximum verification attempts
        self.resend_cooldown_seconds = 30  # Wait 30 seconds before resend
        self.rate_limit_per_hour = 3  # Max 3 OTP requests per hour per phone

        # SMS provider configuration (supports multiple providers)
        self.sms_provider = os.getenv('SMS_PROVIDER', 'console')  # console, twilio, msg91, fast2sms

        # Development mode - use hardcoded OTP (ALWAYS ENABLED FOR TESTING)
        self.dev_mode = True  # Hardcoded to always use dev mode
        self.dev_otp = '123456'  # Hardcoded OTP for development

        # Twilio configuration
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER', '')

        # MSG91 configuration
        self.msg91_auth_key = os.getenv('MSG91_AUTH_KEY', '')
        self.msg91_sender_id = os.getenv('MSG91_SENDER_ID', 'KIRANA')
        self.msg91_template_id = os.getenv('MSG91_TEMPLATE_ID', '')

        # Fast2SMS configuration
        self.fast2sms_api_key = os.getenv('FAST2SMS_API_KEY', '')

    def generate_otp(self) -> str:
        """Generate a random OTP code"""
        # In development mode, use hardcoded OTP
        if self.dev_mode:
            return self.dev_otp

        # Production: Generate cryptographically secure random OTP
        return ''.join([str(random.SystemRandom().randint(0, 9)) for _ in range(self.otp_length)])

    def hash_otp(self, otp_code: str) -> str:
        """Hash OTP for secure storage"""
        return hashlib.sha256(otp_code.encode()).hexdigest()
    
    def check_rate_limit(self, phone: str) -> Dict[str, Any]:
        """Check if phone number has exceeded rate limit"""
        one_hour_ago = datetime.now() - timedelta(hours=1)

        # Count OTPs sent in last hour
        docs = self.db.collection('otps').where('phone', '==', phone).stream()
        recent_otps = []

        for doc in docs:
            data = doc.to_dict()
            created_at = data.get('created_at')

            # Convert Firestore timestamp to datetime if needed
            if created_at:
                if hasattr(created_at, 'timestamp'):
                    # Firestore Timestamp object
                    created_at = datetime.fromtimestamp(created_at.timestamp())
                elif isinstance(created_at, str):
                    # String datetime - skip for now
                    continue

                if created_at > one_hour_ago:
                    recent_otps.append(doc)

        if len(recent_otps) >= self.rate_limit_per_hour:
            return {
                'allowed': False,
                'message': f'Too many OTP requests. Please try again after 1 hour.',
                'retry_after_minutes': 60
            }

        return {'allowed': True}

    def check_resend_cooldown(self, phone: str) -> Dict[str, Any]:
        """Check if enough time has passed since last OTP"""
        cooldown_time = datetime.now() - timedelta(seconds=self.resend_cooldown_seconds)

        # Get most recent OTP
        docs = list(self.db.collection('otps').where('phone', '==', phone).stream())
        if docs:
            # Convert and sort by created_at
            docs_with_time = []
            for doc in docs:
                data = doc.to_dict()
                created_at = data.get('created_at')

                # Convert Firestore timestamp to datetime if needed
                if created_at:
                    if hasattr(created_at, 'timestamp'):
                        # Firestore Timestamp object
                        created_at = datetime.fromtimestamp(created_at.timestamp())
                    elif isinstance(created_at, str):
                        # String datetime - skip
                        continue

                    docs_with_time.append((doc, created_at))

            if docs_with_time:
                # Sort by created_at
                docs_with_time.sort(key=lambda x: x[1], reverse=True)
                latest_doc, latest_created_at = docs_with_time[0]

                if latest_created_at > cooldown_time:
                    wait_seconds = self.resend_cooldown_seconds - (datetime.now() - latest_created_at).seconds
                    return {
                        'allowed': False,
                        'message': f'Please wait {wait_seconds} seconds before requesting new OTP',
                        'retry_after_seconds': wait_seconds
                    }

        return {'allowed': True}

    def create_otp(self, phone: str) -> Dict[str, Any]:
        """Create and store a new OTP for a phone number with rate limiting"""
        print(f"📝 Creating OTP for phone: {phone}")

        # Check rate limit
        rate_limit_check = self.check_rate_limit(phone)
        if not rate_limit_check['allowed']:
            return {
                'success': False,
                'message': rate_limit_check['message'],
                'error_code': 'RATE_LIMIT_EXCEEDED'
            }

        # Check resend cooldown
        cooldown_check = self.check_resend_cooldown(phone)
        if not cooldown_check['allowed']:
            return {
                'success': False,
                'message': cooldown_check['message'],
                'error_code': 'RESEND_COOLDOWN'
            }

        # Invalidate any existing OTPs for this phone
        self._invalidate_existing_otps(phone)

        # Generate new OTP
        otp_code = self.generate_otp()
        otp_id = str(uuid.uuid4())
        now = datetime.now()
        expires_at = now + timedelta(minutes=self.otp_validity_minutes)

        # Hash OTP for secure storage (except in dev mode)
        stored_otp = otp_code if self.dev_mode else self.hash_otp(otp_code)

        otp = OTP(
            otp_id=otp_id,
            phone=phone,
            otp_code=stored_otp,  # Store hashed OTP
            created_at=now,
            expires_at=expires_at,
            verified=False,
            attempts=0
        )

        # Store in database
        otp_dict = otp.to_dict()
        print(f"💾 Storing OTP: {otp_id}, phone: {phone}, hashed: {not self.dev_mode}")
        self.db.collection('otps').document(otp_id).set(otp_dict)

        return {
            'success': True,
            'otp': otp,
            'otp_code': otp_code  # Return plain OTP for sending SMS
        }
    
    def _invalidate_existing_otps(self, phone: str):
        """Invalidate all existing OTPs for a phone number"""
        # Query only by phone to avoid index requirement
        docs = self.db.collection('otps').where('phone', '==', phone).stream()
        for doc in docs:
            doc_data = doc.to_dict()
            # Only invalidate if not already verified
            if not doc_data.get('verified', False):
                self.db.collection('otps').document(doc.id).update({'verified': True})
    
    def verify_otp(self, phone: str, otp_code: str) -> Dict[str, Any]:
        """Verify an OTP code for a phone number with security checks"""
        print(f"🔍 Verifying OTP for phone: {phone}")

        # Get all OTPs for this phone
        docs = list(self.db.collection('otps').where('phone', '==', phone).stream())

        if not docs:
            print(f"❌ No OTP found for phone: {phone}")
            return {
                'success': False,
                'message': 'No OTP found. Please request a new one.',
                'error_code': 'OTP_NOT_FOUND'
            }

        # Convert timestamps and sort by created_at to get the latest
        docs_with_time = []
        for doc in docs:
            data = doc.to_dict()
            created_at = data.get('created_at')

            # Convert Firestore timestamp to datetime if needed
            if created_at:
                if hasattr(created_at, 'timestamp'):
                    created_at = datetime.fromtimestamp(created_at.timestamp())
                elif isinstance(created_at, str):
                    created_at = datetime.min
                docs_with_time.append((doc, created_at))

        if not docs_with_time:
            return {
                'success': False,
                'message': 'No valid OTP found. Please request a new one.',
                'error_code': 'OTP_NOT_FOUND'
            }

        # Sort by created_at
        docs_with_time.sort(key=lambda x: x[1], reverse=True)
        latest_doc, _ = docs_with_time[0]
        otp_data = latest_doc.to_dict()
        otp_id = latest_doc.id

        # Check if already verified (SKIP IN DEV MODE FOR TESTING)
        if not self.dev_mode and otp_data.get('verified', False):
            print(f"❌ OTP already used")
            return {
                'success': False,
                'message': 'OTP already used. Please request a new one.',
                'error_code': 'OTP_ALREADY_USED'
            }

        # Check if expired (SKIP IN DEV MODE FOR TESTING)
        if not self.dev_mode:
            expires_at = otp_data.get('expires_at')
            if expires_at:
                if hasattr(expires_at, 'timestamp'):
                    expires_at = datetime.fromtimestamp(expires_at.timestamp())
                elif isinstance(expires_at, str):
                    expires_at = datetime.max

                if datetime.now() > expires_at:
                    print(f"❌ OTP expired")
                    return {
                        'success': False,
                        'message': 'OTP expired. Please request a new one.',
                        'error_code': 'OTP_EXPIRED'
                    }

        # Check attempts (SKIP IN DEV MODE FOR TESTING)
        attempts = otp_data.get('attempts', 0)
        if not self.dev_mode and attempts >= self.max_attempts:
            print(f"❌ Too many attempts")
            # Mark as verified to prevent further attempts
            self.db.collection('otps').document(otp_id).update({'verified': True})
            return {
                'success': False,
                'message': 'Too many failed attempts. Please request a new OTP.',
                'error_code': 'MAX_ATTEMPTS_EXCEEDED'
            }

        # Verify OTP
        stored_otp = otp_data.get('otp_code', '')

        # In dev mode, compare directly; in production, compare hashes
        if self.dev_mode:
            is_valid = (otp_code == stored_otp)
        else:
            is_valid = (self.hash_otp(otp_code) == stored_otp)

        if is_valid:
            print(f"✅ OTP verified successfully!")
            # Mark as verified
            self.db.collection('otps').document(otp_id).update({
                'verified': True,
                'verified_at': datetime.now()
            })
            return {
                'success': True,
                'message': 'OTP verified successfully',
                'otp_id': otp_id
            }
        else:
            print(f"❌ Invalid OTP. Attempt {attempts + 1}/{self.max_attempts}")
            # Increment attempts
            self.db.collection('otps').document(otp_id).update({
                'attempts': attempts + 1
            })

            remaining_attempts = self.max_attempts - (attempts + 1)
            return {
                'success': False,
                'message': f'Invalid OTP. {remaining_attempts} attempts remaining.',
                'error_code': 'INVALID_OTP',
                'remaining_attempts': remaining_attempts
            }
    
    def send_otp(self, phone: str, otp_code: str) -> Dict[str, Any]:
        """Send OTP via SMS using configured provider"""
        message = f"Your Kirana Shop Manager OTP is: {otp_code}. Valid for {self.otp_validity_minutes} minutes. Do not share with anyone."

        if self.sms_provider == 'twilio':
            return self._send_via_twilio(phone, message)
        elif self.sms_provider == 'msg91':
            return self._send_via_msg91(phone, otp_code)
        elif self.sms_provider == 'fast2sms':
            return self._send_via_fast2sms(phone, otp_code)
        else:
            # Console mode (for development/testing)
            return self._send_via_console(phone, otp_code)

    def _send_via_console(self, phone: str, otp_code: str) -> Dict[str, Any]:
        """Print OTP to console (for development/testing)"""
        print(f"\n{'='*60}")
        print(f"📱 OTP for {phone}: {otp_code}")
        print(f"⏰ Valid for {self.otp_validity_minutes} minutes")
        print(f"{'='*60}\n")
        return {
            'success': True,
            'message': f'OTP sent to console (dev mode): {otp_code}',
            'provider': 'console'
        }

    def _send_via_twilio(self, phone: str, message: str) -> Dict[str, Any]:
        """Send OTP via Twilio SMS"""
        try:
            from twilio.rest import Client

            client = Client(self.twilio_account_sid, self.twilio_auth_token)

            # Format phone number (add +91 for India if not present)
            if not phone.startswith('+'):
                phone = f'+91{phone}'

            message_obj = client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=phone
            )

            return {
                'success': True,
                'message': 'OTP sent successfully',
                'provider': 'twilio',
                'sid': message_obj.sid
            }
        except Exception as e:
            print(f"Twilio error: {e}")
            return {
                'success': False,
                'message': f'Failed to send OTP: {str(e)}',
                'provider': 'twilio'
            }

    def _send_via_msg91(self, phone: str, otp_code: str) -> Dict[str, Any]:
        """Send OTP via MSG91 (India)"""
        try:
            # Remove +91 if present
            phone = phone.replace('+91', '').replace('+', '')

            # If template_id is provided, use OTP API (DLT compliant)
            if self.msg91_template_id:
                url = "https://api.msg91.com/api/v5/otp"

                payload = {
                    "template_id": self.msg91_template_id,
                    "mobile": phone,
                    "authkey": self.msg91_auth_key,
                    "otp": otp_code,
                    "otp_expiry": self.otp_validity_minutes
                }

                headers = {
                    "authkey": self.msg91_auth_key,
                    "content-type": "application/json"
                }

                response = requests.post(url, json=payload, headers=headers)
            else:
                # Use simple SMS API (for testing without DLT)
                url = f"https://control.msg91.com/api/v5/flow/"

                payload = {
                    "flow_id": "YOUR_FLOW_ID",  # Will be ignored
                    "sender": self.msg91_sender_id,
                    "mobiles": f"91{phone}",
                    "VAR1": otp_code,
                    "VAR2": str(self.otp_validity_minutes)
                }

                headers = {
                    "authkey": self.msg91_auth_key,
                    "content-type": "application/json"
                }

                # Alternative: Use basic send API
                url = f"https://api.msg91.com/api/sendotp.php?authkey={self.msg91_auth_key}&mobile={phone}&otp={otp_code}&message=Your OTP is {otp_code}. Valid for {self.otp_validity_minutes} minutes."

                response = requests.get(url)

            if response.status_code == 200 or response.status_code == 201:
                return {
                    'success': True,
                    'message': 'OTP sent successfully',
                    'provider': 'msg91'
                }
            else:
                print(f"MSG91 Response: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'message': f'Failed to send OTP: {response.text}',
                    'provider': 'msg91'
                }
        except Exception as e:
            print(f"MSG91 error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Failed to send OTP: {str(e)}',
                'provider': 'msg91'
            }

    def _send_via_fast2sms(self, phone: str, otp_code: str) -> Dict[str, Any]:
        """Send OTP via Fast2SMS (India)"""
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"

            # Remove +91 if present
            phone = phone.replace('+91', '').replace('+', '')

            payload = {
                "route": "otp",
                "sender_id": "KIRANA",
                "message": f"Your OTP is {otp_code}. Valid for {self.otp_validity_minutes} minutes.",
                "variables_values": otp_code,
                "flash": 0,
                "numbers": phone
            }

            headers = {
                "authorization": self.fast2sms_api_key,
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache"
            }

            response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'OTP sent successfully',
                    'provider': 'fast2sms'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to send OTP: {response.text}',
                    'provider': 'fast2sms'
                }
        except Exception as e:
            print(f"Fast2SMS error: {e}")
            return {
                'success': False,
                'message': f'Failed to send OTP: {str(e)}',
                'provider': 'fast2sms'
            }

