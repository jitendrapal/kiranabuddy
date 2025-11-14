"""
Command processing logic for Kirana Shop Management
"""
from typing import Dict, Any, Optional
from models import CommandAction, ParsedCommand
from database import FirestoreDB
from ai_service import AIService
from whatsapp_service import WhatsAppService


class CommandProcessor:
    """Process commands from WhatsApp messages"""
    
    def __init__(self, db: FirestoreDB, ai_service: AIService, whatsapp_service: WhatsAppService):
        """Initialize command processor"""
        self.db = db
        self.ai_service = ai_service
        self.whatsapp_service = whatsapp_service
    
    def process_message(self, from_phone: str, message_type: str, 
                       text: Optional[str] = None, 
                       media_url: Optional[str] = None,
                       media_format: Optional[str] = None) -> Dict[str, Any]:
        """
        Process incoming WhatsApp message
        
        Args:
            from_phone: Sender's phone number
            message_type: "text" or "voice"
            text: Message text (for text messages)
            media_url: Media URL or ID (for voice messages)
            media_format: Media format (ogg, mp3, etc.)
        
        Returns:
            Result dictionary with success status and response message
        """
        try:
            # Step 1: Get or validate user and shop
            user = self.db.get_user_by_phone(from_phone)
            
            if not user:
                # Try to find shop by owner phone
                shop = self.db.get_shop_by_phone(from_phone)
                if not shop:
                    return {
                        'success': False,
                        'message': "❌ You are not registered. Please contact admin to register your shop.",
                        'send_reply': True
                    }
                # User is shop owner but not in users table, get shop_id
                shop_id = shop.shop_id
            else:
                shop_id = user.shop_id
            
            # Step 2: Get message text (transcribe if voice)
            if message_type == "voice":
                if not media_url:
                    return {
                        'success': False,
                        'message': "❌ Voice message received but no audio file found.",
                        'send_reply': True
                    }
                
                # Download media if needed (for WhatsApp Cloud API)
                if not media_url.startswith('http'):
                    media_url = self.whatsapp_service.download_media(media_url)
                    if not media_url:
                        return {
                            'success': False,
                            'message': "❌ Could not download voice message.",
                            'send_reply': True
                        }
                
                # Transcribe audio
                text = self.ai_service.transcribe_audio(media_url, media_format or 'ogg')
                
                if not text:
                    return {
                        'success': False,
                        'message': "❌ Could not understand voice message. Please try again.",
                        'send_reply': True
                    }
                
                print(f"Transcribed voice message: {text}")
            
            if not text:
                return {
                    'success': False,
                    'message': "❌ No message text found.",
                    'send_reply': True
                }
            
            # Step 3: Parse command using AI
            parsed_command = self.ai_service.parse_command(text)
            # Detect language for response (Hindi vs English)
            response_language = self.ai_service.detect_language(text)

            print(f"Parsed command: action={parsed_command.action.value}, "
                  f"product={parsed_command.product_name}, quantity={parsed_command.quantity}, "
                  f"language={response_language}")

            # Step 4: Validate command
            if not parsed_command.is_valid():
                return {
                    'success': False,
                    'message': f"❌ Sorry, I couldn't understand: '{text}'\n\n"
                              f"💡 You can say things like:\n"
                              f"• 'I bought 10 Maggi today'\n"
                              f"• 'Sold 2 oil bottles'\n"
                              f"• 'How much atta stock do we have?'\n"
                              f"• '5 biscuit packets aaye hain'\n"
                              f"• 'Customer ne 3 cold drink liya'\n\n"
                              f"Just tell me naturally what happened! 😊",
                    'send_reply': True
                }
            
            # Step 5: Execute command
            result = self._execute_command(shop_id, from_phone, parsed_command)

            # Step 6: Generate response
            if result['success']:
                response_message = self.ai_service.generate_response(
                    parsed_command.action.value,
                    result,
                    language=response_language,
                )
            else:
                response_message = result.get('message', '❌ Command failed.')

            return {
                'success': result['success'],
                'message': response_message,
                'send_reply': True,
                'result': result
            }
            
        except Exception as e:
            print(f"❌ ERROR in process_message: {e}")
            import traceback
            traceback.print_exc()

            # Return detailed error for debugging
            error_details = str(e)
            return {
                'success': False,
                'message': f"❌ Error: {error_details}",
                'send_reply': True,
                'error': error_details
            }
    
    def _execute_command(self, shop_id: str, user_phone: str, 
                        command: ParsedCommand) -> Dict[str, Any]:
        """
        Execute parsed command
        
        Args:
            shop_id: Shop ID
            user_phone: User's phone number
            command: Parsed command
        
        Returns:
            Result dictionary
        """
        try:
            if command.action == CommandAction.ADD_STOCK:
                return self.db.add_stock(
                    shop_id=shop_id,
                    product_name=command.product_name,
                    quantity=command.quantity,
                    user_phone=user_phone
                )
            
            elif command.action == CommandAction.REDUCE_STOCK:
                return self.db.reduce_stock(
                    shop_id=shop_id,
                    product_name=command.product_name,
                    quantity=command.quantity,
                    user_phone=user_phone
                )
            
            elif command.action == CommandAction.CHECK_STOCK:
                return self.db.check_stock(
                    shop_id=shop_id,
                    product_name=command.product_name
                )

            elif command.action == CommandAction.TOTAL_SALES:
                return self.db.get_total_sales_today(shop_id=shop_id)

            elif command.action == CommandAction.TOP_PRODUCT_TODAY:
                base = self.db.get_total_sales_today(shop_id=shop_id)
                if not base.get('success'):
                    return base
                products_sold = base.get('products_sold', {}) or {}
                if products_sold:
                    top_product, top_qty = max(products_sold.items(), key=lambda item: item[1])
                    base['top_product_name'] = top_product
                    base['top_product_quantity'] = top_qty
                else:
                    base['top_product_name'] = None
                    base['top_product_quantity'] = 0
                return base

            elif command.action == CommandAction.LIST_PRODUCTS:
                return self.db.get_products_summary(shop_id=shop_id)

            elif command.action == CommandAction.LOW_STOCK:
                return self.db.get_low_stock_products(shop_id=shop_id)

            elif command.action == CommandAction.ADJUST_STOCK:
                return self.db.adjust_last_transaction(
                    shop_id=shop_id,
                    product_name=command.product_name,
                    correct_quantity=command.quantity,
                    user_phone=user_phone,
                )

            else:
                return {
                    'success': False,
                    'message': 'Unknown command'
                }

        except Exception as e:
            print(f"Error executing command: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }

