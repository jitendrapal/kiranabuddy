"""
OpenAI integration for voice transcription and command parsing
"""
import os
import json
import tempfile
from typing import Optional, Dict, Any
import requests
from openai import OpenAI

from models import ParsedCommand, CommandAction


class AIService:
    """OpenAI service for Whisper and GPT-4o-mini"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def transcribe_audio(self, audio_url: str, audio_format: str = "ogg") -> Optional[str]:
        """
        Transcribe audio using OpenAI Whisper
        
        Args:
            audio_url: URL to download audio file
            audio_format: Audio file format (ogg, mp3, wav, etc.)
        
        Returns:
            Transcribed text or None if failed
        """
        try:
            # Download audio file
            response = requests.get(audio_url, timeout=30)
            response.raise_for_status()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{audio_format}') as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            
            # Transcribe using Whisper
            with open(temp_file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="hi"  # Hindi, but Whisper auto-detects
                )
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            return transcript.text
            
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            if 'temp_file_path' in locals():
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
            return None
    
    def parse_command(self, message: str) -> ParsedCommand:
        """
        Parse user message to extract action, product, and quantity
        
        Args:
            message: User message (text or transcribed voice)
        
        Returns:
            ParsedCommand object with extracted information
        """
        system_prompt = """You are an AI assistant for a Kirana (grocery) shop inventory management system.
Your job is to understand natural language messages in Hindi, English, or Hinglish and extract:
1. action: one of "add_stock", "reduce_stock", "check_stock", or "unknown"
2. product_name: the name of the product mentioned
3. quantity: the quantity mentioned (if applicable)

IMPORTANT: Be VERY flexible and understand natural conversational language. Users can say things in ANY way they want.

Examples of ADD STOCK (adding inventory):
- "Add 10 Maggi" / "10 Maggi add karo" / "Maggi 10 pieces laye hain"
- "I bought 5 oil bottles" / "5 oil purchase kiya"
- "Stock mein 20 atta daal do" / "20 kg atta aaya hai"
- "New stock: 15 biscuit packets" / "15 biscuit ka stock aaya"
- "Received 30 cold drinks today" / "Aaj 30 cold drink mila"
- "Got 100 pieces of soap" / "100 sabun aaye hain"

Examples of REDUCE STOCK (sales/consumption):
- "2 oil sold" / "2 oil bik gaya" / "2 oil bech diya"
- "Sold 5 Maggi" / "5 Maggi customer ko diya"
- "3 biscuit nikala" / "3 biscuit gaya"
- "Customer ne 10 atta liya" / "10 atta sale hua"
- "Bech diya 7 cold drink" / "7 cold drink customer ko diya"

Examples of CHECK STOCK (query inventory):
- "Kitna stock hai atta?" / "How much atta do we have?"
- "Maggi ka stock batao" / "Check Maggi stock"
- "Oil kitna bacha hai?" / "Remaining oil?"
- "Biscuit ka inventory check karo" / "What's the biscuit count?"
- "Tell me cold drink stock" / "Cold drink kitna hai?"

Key words to identify actions:
- ADD: add, laya, aaya, purchase, bought, received, new stock, stock mein daal, mila, got
- REDUCE: sold, bik gaya, bech diya, nikala, sale, customer ko diya, gaya
- CHECK: kitna, how much, stock, batao, check, remaining, bacha, inventory, count

Be intelligent and understand the INTENT, not just exact phrases.

Return ONLY a JSON object with this exact structure:
{
    "action": "add_stock" | "reduce_stock" | "check_stock" | "unknown",
    "product_name": "product name" or null,
    "quantity": number or null,
    "confidence": 0.0 to 1.0
}

Do not include any explanation, just the JSON."""

        user_prompt = f"Parse this message: {message}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Map action string to enum
            action_map = {
                "add_stock": CommandAction.ADD_STOCK,
                "reduce_stock": CommandAction.REDUCE_STOCK,
                "check_stock": CommandAction.CHECK_STOCK,
                "unknown": CommandAction.UNKNOWN
            }
            
            action = action_map.get(result.get('action', 'unknown'), CommandAction.UNKNOWN)
            
            return ParsedCommand(
                action=action,
                product_name=result.get('product_name'),
                quantity=result.get('quantity'),
                confidence=result.get('confidence', 0.0),
                raw_message=message
            )
            
        except Exception as e:
            print(f"Error parsing command: {e}")
            return ParsedCommand(
                action=CommandAction.UNKNOWN,
                product_name=None,
                quantity=None,
                confidence=0.0,
                raw_message=message
            )
    
    def generate_response(self, action: str, result: Dict[str, Any], language: str = "hinglish") -> str:
        """
        Generate a natural language response for the user
        
        Args:
            action: The action performed (add_stock, reduce_stock, check_stock)
            result: The result dictionary from database operation
            language: Response language (hinglish, hindi, english)
        
        Returns:
            Natural language response
        """
        if not result.get('success'):
            return "Sorry, kuch problem hui. Please try again."
        
        product_name = result.get('product_name', 'product')
        
        if action == 'add_stock':
            quantity = result.get('quantity', 0)
            new_stock = result.get('new_stock', 0)
            unit = result.get('unit', 'pieces')
            return f"✅ {quantity} {product_name} add ho gaya! Total stock: {new_stock} {unit}"
        
        elif action == 'reduce_stock':
            quantity = result.get('quantity', 0)
            new_stock = result.get('new_stock', 0)
            unit = result.get('unit', 'pieces')
            return f"✅ {quantity} {product_name} sold! Remaining stock: {new_stock} {unit}"
        
        elif action == 'check_stock':
            current_stock = result.get('current_stock', 0)
            unit = result.get('unit', 'pieces')
            return f"📦 {product_name} ka stock: {current_stock} {unit}"
        
        return "Command processed successfully!"

