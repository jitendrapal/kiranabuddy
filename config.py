"""
Configuration module for Kirana Shop Management App
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Firebase
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    # WhatsApp / WATI
    WATI_API_KEY = os.getenv('WATI_API_KEY')
    WATI_BASE_URL = os.getenv('WATI_BASE_URL', 'https://live-server.wati.io')
    WATI_WEBHOOK_SECRET = os.getenv('WATI_WEBHOOK_SECRET')
    
    # WhatsApp Cloud API (alternative to WATI)
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
    WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', 'kirana-verify-token')
    
    # App Settings
    MAX_VOICE_FILE_SIZE = int(os.getenv('MAX_VOICE_FILE_SIZE', 25 * 1024 * 1024))  # 25MB
    SUPPORTED_AUDIO_FORMATS = ['ogg', 'mp3', 'wav', 'm4a', 'opus']
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        required = [
            'OPENAI_API_KEY',
            'FIREBASE_PROJECT_ID'
        ]
        
        missing = [key for key in required if not os.getenv(key)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        # Check if at least one WhatsApp provider is configured
        has_wati = os.getenv('WATI_API_KEY')
        has_whatsapp_cloud = os.getenv('WHATSAPP_ACCESS_TOKEN')
        
        if not (has_wati or has_whatsapp_cloud):
            raise ValueError("Either WATI_API_KEY or WHATSAPP_ACCESS_TOKEN must be configured")

