"""
Command processing logic for Kirana Shop Management
"""
from typing import Dict, Any, Optional, List
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
                if not media_url.startswith("http"):
                    media_url = self.whatsapp_service.download_media(media_url)
                    if not media_url:
                        return {
                            'success': False,
                            'message': "❌ Could not download voice message.",
                            'send_reply': True,
                        }

                # Transcribe audio
                text = self.ai_service.transcribe_audio(media_url, media_format or "ogg")

                if not text:
                    print("⚠️ Voice transcription returned no text.")
                    return {
                        'success': False,
                        'message': "❌ Could not understand voice message. Please try again.",
                        'send_reply': True,
                    }

                print(f"Transcribed voice message: {text}")

            if not text:
                return {
                    'success': False,
                    'message': "❌ No message text found.",
                    'send_reply': True
                }

            # Detect language for response (Hindi vs English)
            # For *voice* messages, always reply in English as requested.
            if message_type == "voice":
                response_language = "english"
            else:
                response_language = self.ai_service.detect_language(text)

            # Special handling: batch of multiple barcode + quantity lines
            batch_result = self._try_process_barcode_batch(
                shop_id=shop_id,
                user_phone=from_phone,
                text=text,
                response_language=response_language,
            )
            if batch_result is not None:
                return batch_result

            # Step 3: Parse single command using AI
            parsed_command = self.ai_service.parse_command(text)

            print(
                f"Parsed command: action={parsed_command.action.value}, "
                f"product={parsed_command.product_name}, "
                f"quantity={parsed_command.quantity}, "
                f"language={response_language}"
            )

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
                    'send_reply': True,
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
                'result': result,
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


    def _try_process_barcode_batch(
        self,
        shop_id: str,
        user_phone: str,
        text: str,
        response_language: str,
    ) -> Optional[Dict[str, Any]]:
        """Detect and process a batch of barcode + quantity lines in one go.

        This is used for scanner-style input where the user sends multiple lines like:
        "8901000000001 -1"\n"8902000000002 +5".

        If the message is not a pure batch of such lines, returns None so the
        normal single-command flow can handle it.
        """

        # Normalize newlines and split into non-empty lines
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
        raw_lines = normalized_text.split("\n")
        lines = [line.strip() for line in raw_lines if line.strip()]

        # Need at least 2 lines to treat as a batch
        if len(lines) <= 1:
            return None

        parsed_commands: List[ParsedCommand] = []

        # Try to parse each line as its own simple command (typically barcode + delta)
        for line in lines:
            cmd = self.ai_service.parse_command(line)

            # If any line is not a clear stock-add/reduce command, bail out and
            # let the normal flow handle the whole message.
            if (not cmd.is_valid() or
                    cmd.action not in (CommandAction.ADD_STOCK, CommandAction.REDUCE_STOCK) or
                    not cmd.product_name or
                    cmd.quantity is None):
                return None

            parsed_commands.append(cmd)

        # At this point, treat as a batch of valid stock updates
        results: List[Dict[str, Any]] = []
        messages: List[str] = []
        all_success = True

        # Use CRLF so WhatsApp-style clients render line breaks correctly
        nl = "\r\n"

        for cmd in parsed_commands:
            res = self._execute_command(shop_id, user_phone, cmd)
            results.append(res)

            if not res.get("success"):
                all_success = False
                messages.append(res.get("message", "❌ Command failed."))
            else:
                # Reuse existing response generator for each line
                line_msg = self.ai_service.generate_response(
                    cmd.action.value,
                    res,
                    language=response_language,
                )
                messages.append(line_msg)

        if not messages:
            return {
                "success": False,
                "message": "❌ No valid product updates found.",
                "send_reply": True,
                "result": {"batch": True, "items": results},
            }

        if response_language == "english":
            header = "✅ Products updated:" + nl
        else:
            # Simple Hinglish/Hindi-friendly header
            header = "✅ Products update ho gaye:" + nl

        full_message = header + nl.join(messages)

        return {
            "success": all_success,
            "message": full_message,
            "send_reply": True,
            "result": {
                "batch": True,
                "items": results,
            },
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
                # For voice/text commands, only update existing products from the
                # shop's catalog. Do NOT auto-create new products if the name
                # doesn't match.
                product = self.db.find_existing_product_by_name(shop_id, command.product_name)
                if not product:
                    return {
                        'success': False,
                        'message': f"❌ '{command.product_name}' product list mein nahi mila. Pehle product ko list mein add karo ya sahi naam bolo.",
                    }
                return self.db.add_stock(
                    shop_id=shop_id,
                    product_name=product.name,
                    quantity=command.quantity,
                    user_phone=user_phone,
                )

            elif command.action == CommandAction.REDUCE_STOCK:
                product = self.db.find_existing_product_by_name(shop_id, command.product_name)
                if not product:
                    return {
                        'success': False,
                        'message': f"❌ '{command.product_name}' product list mein nahi mila. Pehle product ko list mein add karo ya sahi naam bolo.",
                    }
                return self.db.reduce_stock(
                    shop_id=shop_id,
                    product_name=product.name,
                    quantity=command.quantity,
                    user_phone=user_phone,
                )

            elif command.action == CommandAction.CHECK_STOCK:
                product = self.db.find_existing_product_by_name(shop_id, command.product_name)
                if not product:
                    return {
                        'success': False,
                        'message': f"❌ '{command.product_name}' product list mein nahi mila. Pehle product ko list mein add karo ya sahi naam bolo.",
                    }
                # Build the same shape as db.check_stock would return, but without
                # creating any new product.
                return {
                    'success': True,
                    'product_name': product.name,
                    'current_stock': product.current_stock,
                    'unit': product.unit,
                }

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

            elif command.action == CommandAction.TODAY_PROFIT:
                # For now, profit is estimated as the same as total revenue
                # because purchase cost is not yet tracked separately.
                return self.db.get_total_sales_today(shop_id=shop_id)

            elif command.action == CommandAction.MONTHLY_PROFIT:
                return self.db.get_total_sales_current_month(shop_id=shop_id)


            elif command.action == CommandAction.ZERO_SALE_TODAY:
                return self.db.get_zero_sale_products_today(shop_id=shop_id)

            elif command.action == CommandAction.EXPIRY_PRODUCTS:
                return self.db.get_expiry_products(shop_id=shop_id)

            elif command.action == CommandAction.LIST_PRODUCTS:
                # If product_name is provided (e.g. "dal"), treat it as a
                # keyword filter to show only matching products/brands.
                return self.db.get_products_summary(
                    shop_id=shop_id,
                    keyword=command.product_name,
                )

            elif command.action == CommandAction.LOW_STOCK:
                return self.db.get_low_stock_products(shop_id=shop_id)

            elif command.action == CommandAction.ADJUST_STOCK:
                product = self.db.find_existing_product_by_name(shop_id, command.product_name)
                if not product:
                    return {
                        'success': False,
                        'message': f"❌ '{command.product_name}' product list mein nahi mila. Pehle product ko list mein add karo ya sahi naam bolo.",
                    }
                # Use the canonical product.name so DB lookup is stable, but do
                # not allow creating a new product implicitly.
                return self.db.adjust_last_transaction(
                    shop_id=shop_id,
                    product_name=product.name,
                    correct_quantity=command.quantity,
                    user_phone=user_phone,
                )

            elif command.action == CommandAction.UNDO_LAST:
                return self.db.undo_last_transaction_for_shop(
                    shop_id=shop_id,
                    user_phone=user_phone,
                )

            elif command.action == CommandAction.ADD_UDHAR:
                # Udhar: product_name is reused as customer_name, quantity as amount in rupees
                return self.db.create_udhar_entry(
                    shop_id=shop_id,
                    customer_name=command.product_name,
                    amount=command.quantity,
                    user_phone=user_phone,
                    note=command.raw_message,
                )

            elif command.action == CommandAction.PAY_UDHAR:
                # Payment reduces outstanding udhar (store as negative amount)
                return self.db.create_udhar_entry(
                    shop_id=shop_id,
                    customer_name=command.product_name,
                    amount=-abs(command.quantity),
                    user_phone=user_phone,
                    note="Payment received",
                )

            elif command.action == CommandAction.LIST_UDHAR:
                return self.db.get_udhar_summary(shop_id=shop_id)

            elif command.action == CommandAction.HELP:
                # No DB change; generate_response will format the help message.
                return {
                    'success': True,
                    'help': True,
                }

            else:
                return {
                    'success': False,
                    'message': 'Unknown command',
                }

        except Exception as e:
            print(f"Error executing command: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }

