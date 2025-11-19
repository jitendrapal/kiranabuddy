"""
OTP Service for Kirana Shop Manager
Handles OTP generation, sending, and verification
"""
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
import requests
from models import OTP
import uuid


class OTPService:
    """Service for handling OTP authentication"""
    
    def __init__(self, db):
        """Initialize OTP service with database connection"""
        self.db = db
        self.otp_length = 5  # Changed to 5 for hardcoded OTP
        self.otp_validity_minutes = 10
        self.max_attempts = 3
        
        # SMS provider configuration (supports multiple providers)
        self.sms_provider = os.getenv('SMS_PROVIDER', 'console')  # console, twilio, msg91, fast2sms
        
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
        # Hardcoded OTP for easy testing
        return '12345'
    
    def create_otp(self, phone: str) -> OTP:
        """Create and store a new OTP for a phone number"""
        print(f"📝 Creating OTP for phone: {phone}")

        # Invalidate any existing OTPs for this phone
        self._invalidate_existing_otps(phone)

        # Generate new OTP
        otp_code = self.generate_otp()
        otp_id = str(uuid.uuid4())
        now = datetime.now()
        expires_at = now + timedelta(minutes=self.otp_validity_minutes)

        otp = OTP(
            otp_id=otp_id,
            phone=phone,
            otp_code=otp_code,
            created_at=now,
            expires_at=expires_at,
            verified=False,
            attempts=0
        )

        # Store in database
        otp_dict = otp.to_dict()
        print(f"💾 Storing OTP: {otp_id}, phone: {phone}, code: {otp_code}, verified: False")
        self.db.collection('otps').document(otp_id).set(otp_dict)

        return otp
    
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
        """Verify an OTP code for a phone number - SIMPLE HARDCODED FOR TESTING"""
        print(f"🔍 Verifying OTP for phone: {phone}, code: {otp_code}")

        # SIMPLE HARDCODED CHECK - Just compare with 12345
        if otp_code == '12345':
            print(f"✅ OTP verified successfully!")
            return {
                'success': True,
                'message': 'OTP verified successfully',
                'otp_id': 'test-otp-id'
            }
        else:
            print(f"❌ Invalid OTP. Expected: 12345, Got: {otp_code}")
            return {
                'success': False,
                'message': 'Invalid OTP. Please use 12345.',
                'error_code': 'INVALID_OTP'
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
            url = "https://api.msg91.com/api/v5/otp"

            # Remove +91 if present
            phone = phone.replace('+91', '').replace('+', '')

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

            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'OTP sent successfully',
                    'provider': 'msg91'
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to send OTP: {response.text}',
                    'provider': 'msg91'
                }
        except Exception as e:
            print(f"MSG91 error: {e}")
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

