"""
Command processing logic for Kirana Shop Management
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import re

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
                # creating any new product. Include price and expiry information.
                return {
                    'success': True,
                    'product_name': product.name,
                    'current_stock': product.current_stock,
                    'unit': product.unit,
                    'selling_price': product.selling_price,
                    'cost_price': product.cost_price,
                    'expiry_date': product.expiry_date,
                    'brand': product.brand,
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

            elif command.action == CommandAction.WEEKLY_PROFIT:
                return self.db.get_total_sales_current_week(shop_id=shop_id)

            elif command.action == CommandAction.MONTHLY_PROFIT:
                return self.db.get_total_sales_current_month(shop_id=shop_id)

            elif command.action == CommandAction.YEARLY_PROFIT:
                return self.db.get_total_sales_current_year(shop_id=shop_id)

            elif command.action == CommandAction.REPORT_SUMMARY:
                # Flexible "hisaab" / report queries for arbitrary day/month/year ranges.
                period = self._resolve_report_period(command.raw_message)
                if not period.get("success"):
                    return period

                start_dt = period["start"]
                end_dt = period["end"]
                db_result = self.db.get_total_sales_for_period(
                    shop_id=shop_id,
                    start_datetime=start_dt,
                    end_datetime=end_dt,
                )
                if db_result.get("success"):
                    db_result["period_type"] = period.get("period_type")
                    db_result["period_label"] = period.get("period_label")
                    db_result["start_date"] = period.get("start_date")
                    db_result["end_date"] = period.get("end_date")
                return db_result

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

            elif command.action == CommandAction.UPDATE_PRICE:
                # Simple flow to update the selling price (MRP) for an existing product.
                product = self.db.find_existing_product_by_name(shop_id, command.product_name)
                if not product:
                    return {
                        "success": False,
                        "message": f" '{command.product_name}' product list mein nahi mila. Pehle product ko list mein add karo ya sahi naam bolo.",
                    }
                try:
                    new_price = float(command.quantity) if command.quantity is not None else None
                except Exception:
                    new_price = None
                if new_price is None or new_price <= 0:
                    return {
                        "success": False,
                        "message": " Price samajh nahi aaya. Kirpya naya price (rupaye mein) sahi se likho, jaise 'Maggi price 12'.",
                    }

                # Persist new selling price
                self.db.update_product_fields(product.product_id, {"selling_price": new_price})

                return {
                    "success": True,
                    "product_name": product.name,
                    "selling_price": new_price,
                    "unit": product.unit,
                }


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

            elif command.action == CommandAction.CUSTOMER_UDHAR:
                # Detailed udhar history for a single customer
                return self.db.get_udhar_history(
                    shop_id=shop_id,
                    customer_name=command.product_name,
                )

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

    def _resolve_report_period(self, message: str) -> Dict[str, Any]:
        """Parse a natural-language report request into a concrete date range.

        Supports phrases like:
        - "aaj ka hisaab", "aaj ka report" -> today
        - "kal ka hisaab" -> yesterday
        - "is mahine ka hisaab", "this month report" -> current month
        - "pichle mahine ka hisaab", "last month report" -> previous month
        - "is saal ka hisaab", "this year report" -> current year
        - "pichle saal ka hisaab", "last year report" -> previous year
        - Month names like "march 2024 ka hisaab" -> that full month
        - Year numbers like "2023 ka hisaab" -> that full year
        """
        text = (message or "").strip()
        normalized = text.lower()

        now = datetime.now()

        def day_range(offset_days: int = 0):
            d = now.date() + timedelta(days=offset_days)
            start = datetime(d.year, d.month, d.day, 0, 0, 0)
            end = datetime(d.year, d.month, d.day, 23, 59, 59, 999999)
            return start, end

        # 1) Explicit year (e.g. "2023") and/or month name
        year_match = re.search(r"(20\d{2})", normalized)
        year = int(year_match.group(1)) if year_match else None

        month_keywords = {
            "january": 1,
            "jan ": 1,
            " february": 2,
            "feb ": 2,
            "march": 3,
            "mar ": 3,
            "april": 4,
            "apr ": 4,
            "may": 5,
            "june": 6,
            "jun ": 6,
            "july": 7,
            "jul ": 7,
            "august": 8,
            "aug ": 8,
            "september": 9,
            "sept": 9,
            "sep ": 9,
            "october": 10,
            "oct ": 10,
            "november": 11,
            "nov ": 11,
            "december": 12,
            "dec ": 12,
        }

        found_month = None
        for key, mon in month_keywords.items():
            if key.strip() and key.strip() in normalized:
                found_month = mon
                break

        start = end = None
        period_type = None
        period_label = None

        if found_month is not None:
            # Full month, default year to current if not specified
            y = year or now.year
            start = datetime(y, found_month, 1, 0, 0, 0)
            if found_month == 12:
                next_month = datetime(y + 1, 1, 1, 0, 0, 0)
            else:
                next_month = datetime(y, found_month + 1, 1, 0, 0, 0)
            end = next_month - timedelta(microseconds=1)
            period_type = "month"
            period_label = start.strftime("%B %Y")

        elif year is not None and ("saal" in normalized or "year" in normalized or "yearly" in normalized):
            # Explicit full year
            start = datetime(year, 1, 1, 0, 0, 0)
            end = datetime(year, 12, 31, 23, 59, 59, 999999)
            period_type = "year"
            period_label = str(year)

        # 2) Relative phrases (today / yesterday / this month / last month / this year / last year)
        if start is None and end is None:
            if any(w in normalized for w in ["aaj", "aj ", "today"]):
                start, end = day_range(0)
                period_type = "day"
                period_label = start.strftime("%Y-%m-%d")
            elif any(w in normalized for w in ["kal", "yesterday"]):
                start, end = day_range(-1)
                period_type = "day"
                period_label = start.strftime("%Y-%m-%d")
            elif any(w in normalized for w in ["is mahine", "is mahina", "this month", "current month", "mahine ka", "mahina ka"]):
                # Current month
                y = now.year
                m = now.month
                start = datetime(y, m, 1, 0, 0, 0)
                if m == 12:
                    next_month = datetime(y + 1, 1, 1, 0, 0, 0)
                else:
                    next_month = datetime(y, m + 1, 1, 0, 0, 0)
                end = next_month - timedelta(microseconds=1)
                period_type = "month"
                period_label = start.strftime("%B %Y")
            elif any(w in normalized for w in ["pichle mahine", "pichla mahina", "last month", "previous month"]):
                # Previous month
                y = now.year
                m = now.month - 1
                if m == 0:
                    y -= 1
                    m = 12
                start = datetime(y, m, 1, 0, 0, 0)
                if m == 12:
                    next_month = datetime(y + 1, 1, 1, 0, 0, 0)
                else:
                    next_month = datetime(y, m + 1, 1, 0, 0, 0)
                end = next_month - timedelta(microseconds=1)
                period_type = "month"
                period_label = start.strftime("%B %Y")
            elif any(w in normalized for w in ["is saal", "is saal ka", "this year", "current year", "yearly report", "year report"]):
                y = now.year
                start = datetime(y, 1, 1, 0, 0, 0)
                end = datetime(y, 12, 31, 23, 59, 59, 999999)
                period_type = "year"
                period_label = str(y)
            elif any(w in normalized for w in ["pichle saal", "pichla saal", "last year", "previous year"]):
                y = now.year - 1
                start = datetime(y, 1, 1, 0, 0, 0)
                end = datetime(y, 12, 31, 23, 59, 59, 999999)
                period_type = "year"
                period_label = str(y)

        # 3) Fallbacks
        if start is None or end is None:
            # If message mentions month/mahina but we couldn't parse, treat as current month
            if any(w in normalized for w in ["mahine", "mahina", "month"]):
                y = now.year
                m = now.month
                start = datetime(y, m, 1, 0, 0, 0)
                if m == 12:
                    next_month = datetime(y + 1, 1, 1, 0, 0, 0)
                else:
                    next_month = datetime(y, m + 1, 1, 0, 0, 0)
                end = next_month - timedelta(microseconds=1)
                period_type = period_type or "month"
                period_label = period_label or start.strftime("%B %Y")
            # If message mentions saal/year but we couldn't parse, treat as current year
            elif any(w in normalized for w in ["saal", "year"]):
                y = now.year
                start = datetime(y, 1, 1, 0, 0, 0)
                end = datetime(y, 12, 31, 23, 59, 59, 999999)
                period_type = period_type or "year"
                period_label = period_label or str(y)
            else:
                # Default: today's report
                start, end = day_range(0)
                period_type = period_type or "day"
                period_label = period_label or start.strftime("%Y-%m-%d")

        return {
            "success": True,
            "start": start,
            "end": end,
            "period_type": period_type,
            "period_label": period_label,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
        }


