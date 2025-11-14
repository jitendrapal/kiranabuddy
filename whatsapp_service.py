"""
WhatsApp integration supporting both WATI and WhatsApp Cloud API
"""
import requests
from typing import Optional, Dict, Any
import json


class WhatsAppService:
    """WhatsApp messaging service supporting WATI and WhatsApp Cloud API"""
    
    def __init__(self, provider: str = "wati", **kwargs):
        """
        Initialize WhatsApp service
        
        Args:
            provider: "wati" or "whatsapp_cloud"
            **kwargs: Provider-specific configuration
                For WATI: api_key, base_url
                For WhatsApp Cloud: access_token, phone_number_id
        """
        self.provider = provider.lower()
        
        if self.provider == "wati":
            self.api_key = kwargs.get('api_key')
            self.base_url = kwargs.get('base_url', 'https://live-server.wati.io')
        elif self.provider == "whatsapp_cloud":
            self.access_token = kwargs.get('access_token')
            self.phone_number_id = kwargs.get('phone_number_id')
            self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def send_message(self, to_phone: str, message: str) -> bool:
        """
        Send text message to WhatsApp user
        
        Args:
            to_phone: Recipient phone number (with country code)
            message: Message text
        
        Returns:
            True if sent successfully, False otherwise
        """
        if self.provider == "wati":
            return self._send_wati_message(to_phone, message)
        elif self.provider == "whatsapp_cloud":
            return self._send_whatsapp_cloud_message(to_phone, message)
        return False
    
    def _send_wati_message(self, to_phone: str, message: str) -> bool:
        """Send message via WATI API"""
        try:
            url = f"{self.base_url}/api/v1/sendSessionMessage/{to_phone}"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "messageText": message
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            print(f"Error sending WATI message: {e}")
            return False
    
    def _send_whatsapp_cloud_message(self, to_phone: str, message: str) -> bool:
        """Send message via WhatsApp Cloud API"""
        try:
            url = f"{self.base_url}/messages"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            return True
            
        except Exception as e:
            print(f"Error sending WhatsApp Cloud message: {e}")
            return False
    
    def download_media(self, media_id: str) -> Optional[str]:
        """
        Download media file and return URL
        
        Args:
            media_id: Media ID from WhatsApp
        
        Returns:
            Media URL or None if failed
        """
        if self.provider == "wati":
            return self._download_wati_media(media_id)
        elif self.provider == "whatsapp_cloud":
            return self._download_whatsapp_cloud_media(media_id)
        return None
    
    def _download_wati_media(self, media_id: str) -> Optional[str]:
        """Download media via WATI API"""
        try:
            # WATI typically provides direct media URLs
            # This may need adjustment based on actual WATI API
            return media_id  # Often media_id is already a URL in WATI
            
        except Exception as e:
            print(f"Error downloading WATI media: {e}")
            return None
    
    def _download_whatsapp_cloud_media(self, media_id: str) -> Optional[str]:
        """Download media via WhatsApp Cloud API"""
        try:
            # Step 1: Get media URL
            url = f"https://graph.facebook.com/v18.0/{media_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            media_url = response.json().get('url')
            
            return media_url
            
        except Exception as e:
            print(f"Error downloading WhatsApp Cloud media: {e}")
            return None
    
    @staticmethod
    def parse_wati_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse WATI webhook payload
        
        Returns:
            Standardized message dict with keys: from_phone, message_type, text, media_url, media_format
        """
        try:
            # WATI webhook structure (may vary)
            from_phone = payload.get('waId') or payload.get('from')
            message_type = "text"
            text = None
            media_url = None
            media_format = None
            
            if 'text' in payload:
                text = payload['text']
            elif 'messageText' in payload:
                text = payload['messageText']
            
            # Check for voice/audio message
            if payload.get('type') == 'audio' or 'audio' in payload:
                message_type = "voice"
                audio_data = payload.get('audio', {})
                media_url = audio_data.get('link') or audio_data.get('url')
                media_format = audio_data.get('mimeType', 'audio/ogg').split('/')[-1]
            
            return {
                'from_phone': from_phone,
                'message_type': message_type,
                'text': text,
                'media_url': media_url,
                'media_format': media_format
            }
            
        except Exception as e:
            print(f"Error parsing WATI webhook: {e}")
            return {}

    @staticmethod
    def parse_whatsapp_cloud_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse WhatsApp Cloud API webhook payload

        Returns:
            Standardized message dict with keys: from_phone, message_type, text, media_url, media_format
        """
        try:
            # WhatsApp Cloud API structure
            entry = payload.get('entry', [{}])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            messages = value.get('messages', [{}])

            if not messages:
                return {}

            message = messages[0]
            from_phone = message.get('from')
            msg_type = message.get('type')

            text = None
            media_url = None
            media_format = None
            message_type = "text"

            if msg_type == 'text':
                text = message.get('text', {}).get('body')
            elif msg_type == 'audio':
                message_type = "voice"
                audio_data = message.get('audio', {})
                media_url = audio_data.get('id')  # This is media_id, needs to be downloaded
                media_format = audio_data.get('mime_type', 'audio/ogg').split('/')[-1]

            return {
                'from_phone': from_phone,
                'message_type': message_type,
                'text': text,
                'media_url': media_url,
                'media_format': media_format
            }

        except Exception as e:
            print(f"Error parsing WhatsApp Cloud webhook: {e}")
            return {}

