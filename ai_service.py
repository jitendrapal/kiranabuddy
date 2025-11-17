"""
OpenAI integration for voice transcription and command parsing
"""
import os
import json
import tempfile
import re
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
        """Transcribe audio using OpenAI Whisper (or compatible model).

        Returns plain text or None if something goes wrong.
        """
        temp_file_path = None
        try:
            print(f"🔊 Downloading audio from {audio_url} ...")
            response = requests.get(audio_url, timeout=30)
            response.raise_for_status()
            print(f"   Downloaded {len(response.content)} bytes (format={audio_format})")

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format}") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            # Transcribe using Whisper, but always return English text
            # (use Whisper translation so Hindi audio becomes English text)
            with open(temp_file_path, "rb") as audio_file:
                transcript = self.client.audio.translations.create(
                    model="whisper-1",  # or gpt-4o-transcribe if enabled
                    file=audio_file,
                )

            text = getattr(transcript, "text", None)
            print(f"   Transcript: {repr(text)}")

            if text is None:
                return None

            text = text.strip()
            if not text:
                print("⚠️ Transcription returned empty text.")
                return None

            return text

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception:
                    pass
    def detect_language(self, message: str) -> str:
        """Very simple language detector: returns 'hindi' or 'english'.

        We look for Devanagari characters and some common Hindi/English
        keywords. This is not perfect but works well for short shop
        messages.
        """
        if not message:
            return "hinglish"

        normalized = message.lower()

        # Check for Devanagari script (Unicode range for Hindi)
        has_devanagari = any("\u0900" <= ch <= "\u097f" for ch in message)

        hindi_keywords = [
            "hai",
            "kitna",
            "kitne",
            "batao",
            "aaj",
            "kal",
            "maal",
            "becha",
            "bika",
            "kam",
            "khatam",
            "liya",
            "diya",
            "aaya",
            "aaye",
        ]
        english_keywords = [
            "how much",
            "stock",
            "today",
            "total",
            "sale",
            "sold",
            "add",
            "bought",
            "purchase",
            "remaining",
            "inventory",
            "report",
        ]

        hindi_score = sum(1 for w in hindi_keywords if w in normalized)
        english_score = sum(1 for w in english_keywords if w in normalized)

        if has_devanagari or hindi_score > english_score:
            return "hindi"
        else:
            return "english"

    def _normalize_hindi_to_hinglish(self, text: str) -> str:
        """Convert common Hindi (Devanagari) phrases into simple Hinglish.

        This is a lightweight, rule-based transliteration for very common
        shop phrases so that voice transcripts like "१० मैगी ऐड कर दो"
        become "10 maggi add kar do" before parsing and sending to the LLM.
        """
        if not text:
            return text

        # Only do work if there is Devanagari script present
        if not any("\u0900" <= ch <= "\u097f" for ch in text):
            return text

        # Map Devanagari digits to ASCII digits
        devanagari_digits = "०१२३४५६७८९"
        latin_digits = "0123456789"
        digit_map = {ord(d): latin_digits[i] for i, d in enumerate(devanagari_digits)}
        text = text.translate(digit_map)

        # Very small dictionary of high-value words
        word_map = {
            # Products / nouns
            "मैगी": "maggi",
            "मैग्गी": "maggi",
            "मेगी": "maggi",
            "प्रोडक्ट": "product",
            "प्रोडक्ट्स": "products",
            "प्रॉडक्ट": "product",
            "आइटम": "item",
            "आइटम्स": "items",
            "स्टॉक": "stock",
            "स्टाक": "stock",
            "बिक्री": "bikri",
            "सेल": "sale",
            "सामान": "samaan",

            # Verbs / helpers
            "ऐड": "add",
            "एड": "add",
            "बेच": "bech",
            "बिक": "bik",
            "कर": "kar",
            "करो": "karo",
            "करो।": "karo.",
            "करना": "karna",
            "दो": "do",
            "लो": "lo",

            # Particles / small words
            "आज": "aaj",
            "कल": "kal",
            "की": "ki",
            "का": "ka",
            "के": "ke",
            "है": "hai",
            "हैं": "hain",
            "कितनी": "kitni",
            "कितना": "kitna",
            "कितने": "kitne",
            "कौन": "kaun",
            "से": "se",
            "कम": "kam",
        }

        punctuation = ",.!?:\"'“”‘’"

        def map_word(token: str) -> str:
            # Preserve simple leading/trailing punctuation
            leading = ""
            trailing = ""
            core = token
            while core and core[0] in punctuation:
                leading += core[0]
                core = core[1:]
            while core and core[-1] in punctuation:
                trailing = core[-1] + trailing
                core = core[:-1]

            mapped_core = word_map.get(core, core)
            return f"{leading}{mapped_core}{trailing}"

        tokens = text.split()
        mapped_tokens = [map_word(tok) for tok in tokens]
        return " ".join(mapped_tokens)




    def parse_command(self, message: str) -> ParsedCommand:
        """
        Parse user message to extract action, product, and quantity

        Args:
            message: User message (text or transcribed voice)

        Returns:
            ParsedCommand object with extracted information
        """
        # Normalize common Hindi script to Hinglish for more robust parsing
        hinglish_message = self._normalize_hindi_to_hinglish(message)

        # Simple heuristic before calling OpenAI: detect some common intents
        normalized = hinglish_message.lower().strip()
        hindi_msg = message.strip()

        # 1) Help / guidance commands
        help_keywords_latin = [
            "what can i say",
            "how to use",
            "help me",
            "how do i use",
            "kya bol sakta",
            "kya bol sakti",
        ]
        help_keywords_hindi = [
            "मैं क्या कह सकता हूँ",
            "मैं क्या कह सकती हूँ",
            "मैं क्या बोल सकता हूँ",
            "मैं क्या बोल सकती हूँ",
        ]
        if any(kw in normalized for kw in help_keywords_latin) or any(
            kw in hindi_msg for kw in help_keywords_hindi
        ):
            return ParsedCommand(
                action=CommandAction.HELP,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # 2) Undo last entry (shop-level)
        undo_keywords_latin = [
            "undo last entry",
            "undo last action",
            "last entry undo",
            "pichli entry wapas",
            "pichli entry hata do",
        ]
        undo_keywords_hindi = [
            "अंतिम एंट्री वापस लो",
            "आखिरी एंट्री वापस लो",
            "पिछली एंट्री वापस लो",
        ]
        if any(kw in normalized for kw in undo_keywords_latin) or any(
            kw in hindi_msg for kw in undo_keywords_hindi
        ):
            return ParsedCommand(
                action=CommandAction.UNDO_LAST,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )


        # 2b) Udhar (credit) tracking heuristics
        # We support simple one-line commands like:
        #   - "udhar Ramesh 200"  (add udhar)
        #   - "udhar pay Ramesh 200" (record payment)
        #   - "udhar list" / "kitna udhar hai" (summary)
        #   - "kitna udhar baki hai" (summary)
        udhar_words = ["udhar", "udhaar", "khata", "baki", "baaki"]
        has_udhar_word = any(w in normalized for w in udhar_words)

        # (a) Summary / list style queries
        if has_udhar_word:
            if any(kw in normalized for kw in ["udhar list", "udhar ka hisab", "udhar ka hisaab", "udhar summary"]):
                return ParsedCommand(
                    action=CommandAction.LIST_UDHAR,
                    product_name=None,
                    quantity=None,
                    confidence=0.98,
                    raw_message=message,
                )

            if (
                ("kitna" in normalized or "kitni" in normalized or "total" in normalized)
                and any(w in normalized for w in ["udhar", "udhaar", "baki", "baaki"])
                and not any(ch.isdigit() for ch in normalized)
            ):
                # "kitna udhar hai", "kitna baki hai" etc.
                return ParsedCommand(
                    action=CommandAction.LIST_UDHAR,
                    product_name=None,
                    quantity=None,
                    confidence=0.95,
                    raw_message=message,
                )

            # (b) One-line add / pay udhar commands starting with "udhar ..."
            if normalized.startswith("udhar ") or normalized.startswith("udhaar "):
                # Remove the leading keyword and parse the rest.
                parts = normalized.split(maxsplit=1)
                rest = parts[1] if len(parts) > 1 else ""

                # Detect first number in the remaining text as amount
                m = re.search(r"(\d+(?:\.\d+)?)", rest)
                amount = float(m.group(1)) if m else None

                if amount and amount > 0:
                    before_amount = rest[: m.start()].strip() if m else rest.strip()
                    # Remove generic verbs like "pay" / "payment" etc. from name
                    for junk in ["pay", "payment", "ne", "se"]:
                        before_amount = before_amount.replace(junk, " ")
                    customer_name = before_amount.strip() or None

                    # Decide if this is a payment or new udhar based on keywords
                    pay_markers = ["pay", "payment", "de diya", "de dia", "de diya hai", "wapis", "wapas", "wapsi"]
                    is_payment = any(pm in normalized for pm in pay_markers)

                    if customer_name:
                        return ParsedCommand(
                            action=CommandAction.PAY_UDHAR if is_payment else CommandAction.ADD_UDHAR,
                            product_name=customer_name,
                            quantity=amount,
                            confidence=0.96,
                            raw_message=message,
                        )

            # If message clearly talks about udhar but we couldn't parse amount,
            # fall back to showing overall summary so shopkeeper still gets value.
            if has_udhar_word and not any(ch.isdigit() for ch in normalized):
                return ParsedCommand(
                    action=CommandAction.LIST_UDHAR,
                    product_name=None,
                    quantity=None,
                    confidence=0.8,
                    raw_message=message,
                )

        # 3) Total-sales queries (today's sales)
        # Common patterns like: "kinta aaj sell huyi hai", "aaj kitna bika", "aaj ka total sale",
        # and also Hinglish phrases like "aaj ki bikri kitni hai" / "aaj ki bikri".

        # If shopkeeper simply writes "sale" or "sales", treat it as
        # "show me today's sale".
        simple_sale_words = ["sale", "sales"]
        if normalized.strip() in simple_sale_words:
            return ParsedCommand(
                action=CommandAction.TOTAL_SALES,
                product_name=None,
                quantity=None,
                confidence=0.99,
                raw_message=message,
            )

        # Extra phrases user asked for, mapped directly to today's sale.
        extra_total_sale_phrases = [
            "kitne aaj bika",
            "kitna bikri huya",
            "kitna bikri hua",
            "total sale",
            "kitna aaj sale huya",
            "kitna aaj sale hua",
        ]
        if any(phrase in normalized for phrase in extra_total_sale_phrases):
            return ParsedCommand(
                action=CommandAction.TOTAL_SALES,
                product_name=None,
                quantity=None,
                confidence=0.99,
                raw_message=message,
            )

        # Generic: if message contains the word "sale" / "sales" anywhere,
        # and it's not clearly about zero-sale / not selling, show today's sale.
        if any(w in normalized for w in ["sale", "sales"]):
            zero_sale_markers = [
                "zero sale",
                "nahi sale",
                "nahi sell",
                "not selling",
                "slow moving",
            ]
            if not any(z in normalized for z in zero_sale_markers):
                return ParsedCommand(
                    action=CommandAction.TOTAL_SALES,
                    product_name=None,
                    quantity=None,
                    confidence=0.98,
                    raw_message=message,
                )

        total_sales_keywords_latin = [
            "total sale",
            "sell hui",
            "sell huyi",
            "sale hui",
            "kitna bika",
            "kitni bikri",
            "kitna bikri",
            "kitni bikri hui",
            "kitna bikri hui",
            "kitna maal becha",
            "kitna becha",
            "kinta aaj sell",
            "kitna aaj sell",
            "aaj ka sale",
            "aaj ka total sale",
            # Extra common patterns requested by user
            "aaj ki bikri",
            "bikri kitni",
            "bikri kitni hai",
        ]
        # Also handle English phrasing like "total sale - show me the sale of today".
        if ("aaj" in normalized or "aj " in normalized or "today" in normalized) and any(
            kw in normalized for kw in total_sales_keywords_latin
        ):
            return ParsedCommand(
                action=CommandAction.TOTAL_SALES,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # Additional Hindi (Devanagari) patterns for total sales, e.g. "आज की बिक्री कितनी है"
        if "आज" in hindi_msg and any(
            kw in hindi_msg
            for kw in [
                "बिक्री",
                "सेल",
                "बिका",
                "बिकी",
                "बिके",
            ]
        ):
            return ParsedCommand(
                action=CommandAction.TOTAL_SALES,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # 3b) Profit queries (estimated profit)
        # Examples:
        # - "Today's estimated profit"
        # - "Aaj ka profit"
        # - "Monthly estimated profit" / "mahine ka profit"
        if ("profit" in normalized) or ("munafa" in normalized):
            monthly_markers = ["month", "mahina", "mahine", "mahine ka", "monthly"]
            today_markers = ["aaj", "aj ", "today"]

            if any(m in normalized for m in monthly_markers):
                return ParsedCommand(
                    action=CommandAction.MONTHLY_PROFIT,
                    product_name=None,
                    quantity=None,
                    confidence=0.99,
                    raw_message=message,
                )

            if any(t in normalized for t in today_markers):
                return ParsedCommand(
                    action=CommandAction.TODAY_PROFIT,
                    product_name=None,
                    quantity=None,
                    confidence=0.99,
                    raw_message=message,
                )

            # If period is not specified, default to today's profit
            return ParsedCommand(
                action=CommandAction.TODAY_PROFIT,
                product_name=None,
                quantity=None,
                confidence=0.95,
                raw_message=message,
            )


        # 4) Zero-sale products today (which products did NOT sell today)
        zero_sale_keywords_latin = [
            "zero sale",
            "nahi sale",
            "nahi sell",
            "nahi bika",
            "nahi bik",
            "not selling",
            "slow moving",
        ]
        if ("aaj" in normalized or "aj " in normalized or "today" in normalized) and (
            any(kw in normalized for kw in zero_sale_keywords_latin)
        ):
            return ParsedCommand(
                action=CommandAction.ZERO_SALE_TODAY,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # Additional Hindi (Devanagari) patterns for zero sale, e.g. "आज जो नहीं बिका"
        if "आज" in hindi_msg and "नहीं" in hindi_msg and any(
            kw in hindi_msg
            for kw in [
                "बिका",
                "बिके",
                "बिक",
                "बिक्री",
                "बिकरी",
            ]
        ):
            return ParsedCommand(
                action=CommandAction.ZERO_SALE_TODAY,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # 5) Expiry / near-expiry products
        # Examples:
        # - "expiry products"
        # - "expiry items"
        # - "kaun sa maal expire hone wala hai"
        # - "expiring stock"
        expiry_keywords = [
            "expiry",
            "expire",
            "expiring",
            "expired",
        ]
        if any(kw in normalized for kw in expiry_keywords):
            return ParsedCommand(
                action=CommandAction.EXPIRY_PRODUCTS,
                product_name=None,
                quantity=None,
                confidence=0.98,
                raw_message=message,
            )




        # 4) Generic keyword-based product search.
        # If user sends a short single word like "dal", "atta", "rice" etc.,
        # treat it as a request to list all matching products/brands with
        # stock and price.
        one_word = normalized.strip()
        if " " not in one_word and one_word:
            # Map common spelling variants (especially from voice) to a base keyword.
            # Example: "daal" (spoken) → "dal" (product names), "aata" → "atta".
            category_aliases = {
                "daal": "dal",
                "dall": "dal",
                "aata": "atta",
                "ata": "atta",
                # "oil" already matches product names; kept for clarity/extensibility.
                "oil": "oil",
            }
            base_word = category_aliases.get(one_word, one_word)

            # Avoid obviously non-product words which are handled by other
            # rules above.
            blocked = {"help", "undo", "sale", "stock", "products", "product", "item", "items", "saman", "samaan", "maal"}
            if base_word not in blocked and not any(ch.isdigit() for ch in base_word):
                return ParsedCommand(
                    action=CommandAction.LIST_PRODUCTS,
                    product_name=base_word,
                    quantity=None,
                    confidence=0.95,
                    raw_message=message,
                )

        # 5) Product list / inventory summary / how many products
        list_keywords = [
            "product list",
            "products list",
            "all product",
            "all products",
            "saare product",
            "saare products",
            "saari product list",
            "pura stock list",
            "full stock list",
            "all items",
            "show all products",
            "show products",
            # How many products/items style
            "kitne product",
            "kitne products",
            "kitna product",
            "kitna products",
            "kitne item",
            "kitni item",
            "kitne items",
            "kitni items",
            "how many products",
            "how many items",
            # Hindi (Devanagari) variants
            "कितने प्रोडक्ट",
            "कितने प्रॉडक्ट",
            "कितने प्रोडक्ट हैं",
            "कितने आइटम",
            "कितने आइटम हैं",
            "सभी प्रोडक्ट",
            "सब प्रोडक्ट",
        ]
        if any(kw in normalized for kw in list_keywords) or any(
            kw in hindi_msg
            for kw in [
                "कितने प्रोडक्ट",
                "कितने प्रॉडक्ट",
                "कितने आइटम",
                "सभी प्रोडक्ट",
                "सभी प्रॉडक्ट",
            ]
        ):
            return ParsedCommand(
                action=CommandAction.LIST_PRODUCTS,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # 6) Low stock queries (which products are low)
        low_stock_keywords = [
            "low stock",
            "kam stock",
            "stock kam",
            "low-stock",
            "low quantity",
            "near out of stock",
            "khatam hone wala",
            "khatam hone wale",
        ]
        if any(kw in normalized for kw in low_stock_keywords) or (
            "low" in normalized
            and any(w in normalized for w in ["product", "products", "item", "items"])
        ) or (
            "कम" in hindi_msg
            and any(w in hindi_msg for w in ["प्रोडक्ट", "प्रॉडक्ट", "आइटम"])
        ):
            return ParsedCommand(
                action=CommandAction.LOW_STOCK,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # Simple heuristic for top-selling product today
        if (
            "aaj" in normalized
            and "bika" in normalized
            and any(kw in normalized for kw in ["zyada", "jada", "jayda", "sabse zyada", "sabse jyada", "most"])
        ):
            return ParsedCommand(
                action=CommandAction.TOP_PRODUCT_TODAY,
                product_name=None,
                quantity=None,
                confidence=1.0,
                raw_message=message,
            )

        # Simple heuristic: barcode + quantity pattern, e.g. "8901000000001 +5" or "8901000000001 -3"
        #
        # Supports decimal quantities as well, so loose items can be sold by
        # weight/volume when using the scanner, e.g. "8901000000001 -0.5" for
        # 0.5 kg/litre.
        parts = normalized.split()
        if len(parts) == 2 and parts[0].isdigit() and 8 <= len(parts[0]) <= 16:
            sign_part = parts[1]
            if sign_part.startswith("+") or sign_part.startswith("-"):
                try:
                    delta = float(sign_part.replace(" ", ""))
                    qty = abs(delta)
                    if qty > 0:
                        action = CommandAction.ADD_STOCK if delta > 0 else CommandAction.REDUCE_STOCK
                        return ParsedCommand(
                            action=action,
                            product_name=parts[0],
                            quantity=qty,
                            confidence=0.98,
                            raw_message=message,
                        )
                except ValueError:
                    pass
        # Simple heuristic for Hindi/Hinglish numeric commands like
        # "10 मैगी ऐड कर दो" or "10 maggi add karo" or "5 oil bech diya".
        #
        # Now supports loose items by understanding decimal quantities and
        # simple weight/volume units like kg/gm/ltr/ml. For example:
        #   "0.5 kg dal add karo"  -> quantity = 0.5
        #   "250 gm sugar bech diya" -> quantity = 0.25 (kg)
        if any(ch.isdigit() for ch in normalized):
            # Capture first number, with optional decimal, plus an optional unit word.
            # Example matches:
            #   "0.5 kg dal"  -> qty_str="0.5", unit_word="kg"
            #   "250 gm sugar" -> qty_str="250", unit_word="gm"
            #   "10 maggi"     -> qty_str="10", unit_word=None
            m = re.search(r"(\d+(?:\.\d+)?)[ ]*(kg|kilogram|kilo|g|gm|gram|grams|ml|ltr|liter|litre|l|piece|pieces|pc|pcs)?\b", normalized)
            if m:
                qty_val = None
                unit_word = m.group(2).lower() if m.group(2) else None

                try:
                    qty_val = float(m.group(1))
                except ValueError:
                    qty_val = None

                # For loose items, convert grams/ml to kg/litre equivalents so
                # that stock can be tracked as a float in base units.
                if qty_val is not None and unit_word:
                    if unit_word in {"g", "gm", "gram", "grams"}:
                        qty_val = qty_val / 1000.0  # grams -> kilograms
                    elif unit_word in {"ml"}:
                        qty_val = qty_val / 1000.0  # millilitres -> litres
                    # For kg/ltr/pieces we keep the quantity as-is.

                if qty_val and qty_val > 0:
                    add_keywords = ["add", "a dd", "aad", "ऐड", "एड", "dal do", "daal do", "डाल", "डाल दो"]
                    reduce_keywords = ["sold", "sell", "bech", "बेच", "bik", "बिक", "nikal", "निकाल", "निकाला"]

                    action = None
                    if any(kw in normalized for kw in add_keywords):
                        action = CommandAction.ADD_STOCK
                    elif any(kw in normalized for kw in reduce_keywords):
                        action = CommandAction.REDUCE_STOCK

                    if action is not None:
                        # Try to infer product name as the words between the number
                        # and the first verb-like keyword.
                        orig_words = message.split()
                        norm_words = normalized.split()
                        if len(orig_words) == len(norm_words):
                            num_idx = next(
                                (i for i, w in enumerate(norm_words) if any(ch.isdigit() for ch in w)),
                                None,
                            )
                            verb_indices = [
                                i
                                for i, w in enumerate(norm_words)
                                if any(kw in w for kw in add_keywords + reduce_keywords)
                            ]
                            verb_idx = verb_indices[0] if verb_indices else None

                            product_tokens = []
                            if num_idx is not None and verb_idx is not None and verb_idx > num_idx:
                                product_tokens = orig_words[num_idx + 1 : verb_idx]
                            elif verb_idx is not None and verb_idx > 0:
                                product_tokens = [orig_words[verb_idx - 1]]

                            product_name = " ".join(t.strip() for t in product_tokens).strip() or message.strip()
                        else:
                            product_name = message.strip()

                        return ParsedCommand(
                            action=action,
                            product_name=product_name,
                            quantity=qty_val,
                            confidence=0.95,
                            raw_message=message,
                        )



        # Simple heuristic: numeric-only message with 8-16 digits (likely barcode)
        # Treat as a CHECK_STOCK query where the barcode itself is the product name.
        stripped = normalized.replace(" ", "")
        if stripped.isdigit() and 8 <= len(stripped) <= 16:
            return ParsedCommand(
                action=CommandAction.CHECK_STOCK,
                product_name=stripped,
                quantity=None,
                confidence=0.95,
                raw_message=message,
            )

        # Simple heuristic: if user just types a product name (1-3 words,
        # without any numbers), treat it as a CHECK_STOCK query.
        if not any(ch.isdigit() for ch in normalized):
            words = [w for w in normalized.split() if w]
            if 1 <= len(words) <= 3:
                # Avoid misclassifying clear non-product phrases
                ignore_keywords = [
                    "total",
                    "sale",
                    "stock",
                    "kitna",
                    "how much",
                    "aaj",
                    "today",
                    "list",
                    "low",
                    "kam",
                    "khatam", "product", "products", "item", "items", "saman", "samaan", "maal",
                ]
                if not any(kw in normalized for kw in ignore_keywords):
                    product_name = message.strip()
                    return ParsedCommand(
                        action=CommandAction.CHECK_STOCK,
                        product_name=product_name,
                        quantity=None,
                        confidence=0.9,
                        raw_message=message,
                    )


        # 7) Generic inventory summary:
        # - If message mentions generic words like "product", "products", "item",
        #   "items", "saman/samaan" or "maal" anywhere, show full product list
        #   (simple rule for shopkeeper).
        # - Additionally, if message is a general "stock" sentence
        #   (no numbers, not clearly a "kitna stock" question),
        #   also show full product list.
        if any(kw in normalized for kw in ["product", "products", "item", "items", "saman", "samaan", "maal"]):
            return ParsedCommand(
                action=CommandAction.LIST_PRODUCTS,
                product_name=None,
                quantity=None,
                confidence=0.95,
                raw_message=message,
            )

        stock_query_markers = ["kitna", "kitni", "how much", "bacha", "remaining", "baki", "check"]
        if (
            "stock" in normalized
            and not any(ch.isdigit() for ch in normalized)
            and not any(marker in normalized for marker in stock_query_markers)
        ):
            return ParsedCommand(
                action=CommandAction.LIST_PRODUCTS,
                product_name=None,
                quantity=None,
                confidence=0.9,
                raw_message=message,
            )

        system_prompt = """You are an AI assistant for a Kirana (grocery) shop inventory management system.
Your job is to understand natural language messages in Hindi (Devanagari script), English, or Hinglish and extract:
1. action: one of "add_stock", "reduce_stock", "check_stock", "total_sales", "today_profit", "monthly_profit", "list_products", "low_stock", "adjust_stock", "top_product_today", "zero_sale_today", "expiry_products", "undo_last", "help", "add_udhar", "pay_udhar", "list_udhar", or "unknown"
2. product_name: the name of the product mentioned (for udhar actions this is the customer name; not needed for total_sales, today_profit, monthly_profit, list_products, low_stock, top_product_today, zero_sale_today, expiry_products, undo_last, help, or list_udhar)
3. quantity: the quantity mentioned (if applicable). For "adjust_stock", quantity should be the CORRECT quantity for the last entry (e.g., if user says "Maggi 3 nahi 1 the" then quantity is 1). For udhar actions, quantity is the rupee amount (always positive).

IMPORTANT: Be VERY flexible and understand natural conversational language. Users can say things in ANY way they want, including full Hindi script.

Examples of ADD STOCK (adding inventory):
- "Add 10 Maggi" / "10 Maggi add karo" / "Maggi 10 pieces laye hain"
- "I bought 5 oil bottles" / "5 oil purchase kiya"
- "Stock mein 20 atta daal do" / "20 kg atta aaya hai"
- "New stock: 15 biscuit packets" / "15 biscuit ka stock aaya"
- "Received 30 cold drinks today" / "Aaj 30 cold drink mila"
- "Got 100 pieces of soap" / "100 sabun aaye hain"
- "१० मैगी ऐड कर दो" / "10 मैगी ऐड कर दो" (Hindi script) -> treat as add_stock for product_name "मैगी" with quantity 10.

Examples of REDUCE STOCK (sales/consumption):
- "2 oil sold" / "2 oil bik gaya" / "2 oil bech diya"
- "Sold 5 Maggi" / "5 Maggi customer ko diya"
- "3 biscuit nikala" / "3 biscuit gaya"
- "Customer ne 10 atta liya" / "10 atta sale hua"
- "Bech diya 7 cold drink" / "7 cold drink customer ko diya"
- "१० मैगी बिक गए" / "10 मैगी बिक गए" (Hindi script) -> treat as reduce_stock for product_name "मैगी" with quantity 10.

Examples of CHECK STOCK (query inventory):
- "Kitna stock hai atta?" / "How much atta do we have?"
- "Maggi ka stock batao" / "Check Maggi stock"
- "Oil kitna bacha hai?" / "Remaining oil?"
- "Biscuit ka inventory check karo" / "What's the biscuit count?"
- "Tell me cold drink stock" / "Cold drink kitna hai?"
- "Maggi" / "Biscuit" / "Oil" (just product name -> check stock for that product)

Examples of TOTAL SALES (daily sales summary):
- "Aaj ka total sale kitna hai?" / "What's today's total sales?"
- "Aaj kitna bika?" / "How much sold today?"
- "Today's sales batao" / "Tell me today's sales"
- "Aaj ka business kaisa raha?" / "How was today's business?"
- "Total sale today" / "Aaj ka total"
- "Kitna maal becha aaj?" / "Sales report for today"
- "आज की बिक्री कितनी है?" (Hindi script) -> treat as total_sales for today.

Examples of LIST PRODUCTS (all products / how many products):
- "Show all products"
- "How many products do we have?"
- "Kitne product hai?" / "Kitne items hai?"
- "सभी प्रोडक्ट दिखाओ" / "कितने प्रोडक्ट हैं?"

Examples of LOW STOCK (which products are low on stock):
- "Which products are low?"
- "Low stock items?"
- "Kaun se product kam hain?"
- "कौन से प्रोडक्ट कम हैं?"

Examples of ADJUST STOCK (fixing wrong entries):
- "Galat entry ho gayi, Maggi 3 nahi 1 the" -> user earlier recorded 3 Maggi but correct is 1 piece; treat as adjust_stock with product_name "Maggi" and quantity 1.
- "Oil 5 nahi 2 tha" -> adjust_stock for Oil with quantity 2.

Examples of UNDO LAST (undo last entry for the shop):
- "Undo last entry" / "Undo last action" -> treat as "undo_last" with no product_name and no quantity.
- "अंतिम एंट्री वापस लो" -> treat as "undo_last" with no product_name and no quantity.

Examples of HELP (show guidance / examples):
- "What can I say?" -> action "help" (no product, no quantity).
- "मैं क्या कह सकता हूँ?" / "मैं क्या कह सकती हूँ?" -> action "help".

	Examples of UDHAR (credit tracking):
	- "udhar Ramesh 200" -> action "add_udhar" with product_name "Ramesh" and quantity 200
	- "Ramesh udhar 300 doodh" -> action "add_udhar" with product_name "Ramesh" and quantity 300 (note like "doodh" is optional context)
	- "udhar list" / "kitna udhar hai" -> action "list_udhar" (no product_name, no quantity)
	- "udhar pay Ramesh 200" / "Ramesh ne 200 de diya" -> action "pay_udhar" with product_name "Ramesh" and quantity 200


Key words to identify actions:
- ADD: add, laya, aaya, purchase, bought, received, new stock, stock mein daal, mila, got
- REDUCE: sold, bik gaya, bech diya, nikala, sale, customer ko diya, gaya
- CHECK: kitna, how much, stock, batao, check, remaining, bacha, inventory, count (for specific product)
- TOTAL_SALES: total sale, aaj ka sale, today's sales, kitna bika, business, sales report, aaj ka total
- PROFIT: profit, munafa, estimated profit

Messages may contain Devanagari Hindi words like "मैगी", "ऐड कर दो", "बिक गए". Parse them the same way as the Hinglish examples above.

Be intelligent and understand the INTENT, not just exact phrases.

Return ONLY a JSON object with this exact structure:
{
    "action": "add_stock" | "reduce_stock" | "check_stock" | "total_sales" | "today_profit" | "monthly_profit" | "list_products" | "low_stock" | "adjust_stock" | "top_product_today" | "zero_sale_today" | "expiry_products" | "undo_last" | "help" | "add_udhar" | "pay_udhar" | "list_udhar" | "unknown",
    "product_name": "product name" or null (for udhar actions this is the customer name; not needed for total_sales, today_profit, monthly_profit, list_products, low_stock, adjust_stock, zero_sale_today, expiry_products, undo_last, help, list_udhar, or top_product_today),
    "quantity": number or null (for udhar actions this is the amount in rupees, always positive),
    "confidence": 0.0 to 1.0
}

Do not include any explanation, just the JSON."""

        # Use the Hinglish-normalized version for the LLM, so that
        # Devanagari voice transcripts become easy Hinglish like
        # "10 maggi add kar do".
        user_prompt = f"Parse this message: {hinglish_message}"

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
                "total_sales": CommandAction.TOTAL_SALES,
                "today_profit": CommandAction.TODAY_PROFIT,
                "monthly_profit": CommandAction.MONTHLY_PROFIT,
                "list_products": CommandAction.LIST_PRODUCTS,
                "low_stock": CommandAction.LOW_STOCK,
                "adjust_stock": CommandAction.ADJUST_STOCK,
                "top_product_today": CommandAction.TOP_PRODUCT_TODAY,
                "zero_sale_today": CommandAction.ZERO_SALE_TODAY,
                "expiry_products": CommandAction.EXPIRY_PRODUCTS,
                "undo_last": CommandAction.UNDO_LAST,
                "help": CommandAction.HELP,
                "add_udhar": CommandAction.ADD_UDHAR,
                "pay_udhar": CommandAction.PAY_UDHAR,
                "list_udhar": CommandAction.LIST_UDHAR,
                "unknown": CommandAction.UNKNOWN,
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
        """Generate a natural language response for the user.

        Args:
            action: The action performed (add_stock, reduce_stock, check_stock)
            result: The result dictionary from database operation
            language: Response language hint ("hindi" or "english" or "hinglish")
        """
        lang = (language or "hinglish").lower()
        is_english = lang.startswith("en")

        if not result.get('success'):
            if is_english:
                return "Sorry, something went wrong. Please try again."
            return "Sorry, kuch problem hui. Please try again."

        product_name = result.get('product_name', 'product')

        if action == 'add_stock':
            quantity = result.get('quantity', 0)
            new_stock = result.get('new_stock', 0)
            unit = result.get('unit', 'pieces')
            if is_english:
                return f"✅ {quantity} {product_name} added! Total stock: {new_stock} {unit}"
            return f"✅ {quantity} {product_name} add ho gaya! Total stock: {new_stock} {unit}"

        elif action == 'reduce_stock':
            quantity = result.get('quantity', 0)
            new_stock = result.get('new_stock', 0)
            unit = result.get('unit', 'pieces')
            if is_english:
                return f"✅ {quantity} {product_name} sold! Remaining stock: {new_stock} {unit}"
            return f"✅ {quantity} {product_name} sold! Remaining stock: {new_stock} {unit}"

        elif action == 'adjust_stock':
            old_qty = result.get('old_quantity')
            new_qty = result.get('new_quantity')
            new_stock = result.get('new_stock', 0)
            unit = result.get('unit', 'pieces')
            if is_english:
                if old_qty is None or new_qty is None:
                    return (
                        f"✅ Incorrect entry corrected for {product_name}. "
                        f"Current stock: {new_stock} {unit}"
                    )
                return (
                    f"✅ Incorrect entry corrected. {product_name}: {old_qty} → {new_qty}. "
                    f"Now total stock: {new_stock} {unit}"
                )
            # Hindi / Hinglish
            if old_qty is None or new_qty is None:
                return f"✅ {product_name} ki galat entry correct ho gayi. Ab total stock: {new_stock} {unit}"
            return (
                f"✅ Galat entry correct ho gayi. {product_name}: {old_qty} se {new_qty} kar diya. "
                f"Ab total stock: {new_stock} {unit}"
            )

        elif action == 'top_product_today':
            top_name = result.get('top_product_name')
            top_qty = result.get('top_product_quantity', 0)
            total_items = result.get('total_items_sold', 0)
            if not top_name:
                if is_english:
                    return "❌ No sales yet today."
                return "❌ Aaj abhi tak koi sale nahi hui."
            if is_english:
                return (
                    f"📊 Top-selling product today: {top_name} ({top_qty} sold). "
                    f"(Total items sold: {total_items})"
                )
            return (
                f"📊 Aaj sabse zyada {top_qty} {top_name} bika. "
                f"(Total items sold: {total_items})"
            )

        elif action == 'list_products':
            products = result.get('products', [])
            total = result.get('total_products', len(products))
            keyword = result.get('keyword')

            if not products:
                if is_english:
                    return "📦 No products registered yet."
                return "📦 Abhi tak koi product register nahi hua."

            # Build a clean multi-line list: each product on its own line.
            # Use CRLF (\r\n) which some WhatsApp providers respect more
            # reliably than just \n.
            lines = []
            for p in products:
                name = p.get('name', 'Product')
                brand = p.get('brand') or ""
                stock = p.get('stock', 0)
                unit = p.get('unit', 'pieces')
                price = p.get('price')

                price_part = ""
                if price is not None:
                    try:
                        price_val = float(price)
                        price_part = f" (₹{price_val:,.2f})"
                    except Exception:
                        price_part = ""

                if brand:
                    display_name = f"{name} ({brand})"
                else:
                    display_name = name

                lines.append(f"• {display_name}: {stock} {unit}{price_part}")

            lines_str = "\r\n".join(lines)

            if keyword:
                if is_english:
                    response = f"📦 Products matching '{keyword}':\r\n" + lines_str
                else:
                    response = f"📦 '{keyword}' wale products:\r\n" + lines_str
            else:
                if is_english:
                    response = "📦 Your shop products:\r\n" + lines_str
                else:
                    response = "📦 Aapke shop ke products:\r\n" + lines_str

            response += f"\r\nTotal products: {total}"
            return response

        elif action == 'low_stock':
            low_products = result.get('low_products', [])
            threshold = result.get('threshold', 5)
            if not low_products:
                if is_english:
                    return "✅ No items are low on stock right now. Everything looks good."
                return "✅ Abhi koi item low stock mein nahi hai. Sab theek hai."

            # Use CRLF for clean multi-line formatting
            nl = "\r\n"
            if is_english:
                response = f"⚠️ Low stock items (≤ {threshold}):{nl}{nl}"
            else:
                response = f"⚠️ Low stock items (≤ {threshold}):{nl}{nl}"

            for p in low_products:
                name = p.get('name', 'Product')
                stock = p.get('stock', 0)
                unit = p.get('unit', 'pieces')
                response += f"• {name}: {stock} {unit}{nl}"

            total_low = result.get('total_low_products', len(low_products))
            response += f"{nl}Total low-stock products: {total_low}"
            return response

        elif action == 'check_stock':
            current_stock = result.get('current_stock', 0)
            unit = result.get('unit', 'pieces')
            if is_english:
                return f"📦 Stock for {product_name}: {current_stock} {unit}"
            return f"📦 {product_name} ka stock: {current_stock} {unit}"

        elif action == 'total_sales':
            total_items = result.get('total_items_sold', 0)
            total_revenue = result.get('total_revenue')
            products_sold = result.get('products_sold', {}) or {}
            revenue_by_product = result.get('revenue_by_product', {}) or {}

            # Use CRLF (\r\n) so WhatsApp-style clients show clean line breaks
            nl = "\r\n"

            if is_english:
                response = f"📊 Today's total sales:{nl}"
            else:
                response = f"📊 Aaj ka total sale:{nl}"

            response += f"✅ Total items sold: {total_items}{nl}"

            # Show total revenue if available
            if total_revenue is not None:
                try:
                    total_revenue_val = float(total_revenue)
                    if is_english:
                        response += f"💰 Total revenue: ₹{total_revenue_val:,.2f}{nl}"
                    else:
                        response += f"💰 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}{nl}"
                except Exception:
                    # If formatting fails, just add a blank line
                    response += nl

            if products_sold:
                if is_english:
                    response += f"📦 Product-wise breakdown:{nl}"
                else:
                    response += f"📦 Product-wise breakdown:{nl}"

                for product, qty in products_sold.items():
                    revenue = revenue_by_product.get(product)
                    if revenue is not None:
                        try:
                            rev_val = float(revenue)
                            response += f"• {product}: {qty} (₹{rev_val:,.2f}){nl}"
                        except Exception:
                            response += f"• {product}: {qty}{nl}"
                    else:
                        response += f"• {product}: {qty}{nl}"
            else:
                if is_english:
                    response += "❌ No sales yet today!"
                else:
                    response += "❌ Koi sale nahi hui aaj!"

            return response

        elif action == 'today_profit':
            total_items = result.get('total_items_sold', 0)
            total_revenue = result.get('total_revenue')
            total_cost = result.get('total_cost')
            total_profit = result.get('total_profit')

            nl = "\r\n"

            if total_revenue is None:
                if is_english:
                    return (
                        "💰 Today's profit: ₹0.00" + nl +
                        "ℹ️ No sales recorded today, so profit is zero."
                    )
                return (
                    "💰 Aaj ka munafa: ₹0.00" + nl +
                    "ℹ️ Aaj koi sale record nahi hui, isliye munafa zero hai."
                )

            try:
                total_revenue_val = float(total_revenue)
            except Exception:
                total_revenue_val = 0.0

            total_cost_val = None
            if total_cost is not None:
                try:
                    total_cost_val = float(total_cost)
                except Exception:
                    total_cost_val = None

            total_profit_val = None
            if total_profit is not None:
                try:
                    total_profit_val = float(total_profit)
                except Exception:
                    total_profit_val = None

            # Fallback: if profit not provided but we have revenue and cost, compute it
            if total_profit_val is None and total_cost_val is not None:
                total_profit_val = total_revenue_val - total_cost_val

            # If still None, treat profit as revenue (best-effort)
            if total_profit_val is None:
                total_profit_val = total_revenue_val

            if is_english:
                lines = [
                    "💰 Today's profit:",
                    f"✅ Total items sold: {total_items}",
                    f"📦 Total sales (revenue): ₹{total_revenue_val:,.2f}",
                ]
                if total_cost_val is not None:
                    lines.append(f"🧾 Purchase cost (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Profit: ₹{total_profit_val:,.2f}")
            else:
                lines = [
                    "💰 Aaj ka munafa:",
                    f"✅ Total items sold: {total_items}",
                    f"📦 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}",
                ]
                if total_cost_val is not None:
                    lines.append(f"🧾 Khareed ka kharcha (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Munafa: ₹{total_profit_val:,.2f}")

            return nl.join(lines)

        elif action == 'monthly_profit':
            total_items = result.get('total_items_sold', 0)
            total_revenue = result.get('total_revenue')
            total_cost = result.get('total_cost')
            total_profit = result.get('total_profit')
            month_label = result.get('month')

            nl = "\r\n"

            if total_revenue is None:
                if is_english:
                    header = "💰 This month's profit: ₹0.00"
                    note = "ℹ️ No sales recorded this month, so profit is zero."
                else:
                    header = "💰 Is mahine ka munafa: ₹0.00"
                    note = "ℹ️ Is mahine koi sale record nahi hui, isliye munafa zero hai."
                if month_label:
                    header = f"{header} (month: {month_label})"
                return header + nl + note

            try:
                total_revenue_val = float(total_revenue)
            except Exception:
                total_revenue_val = 0.0

            total_cost_val = None
            if total_cost is not None:
                try:
                    total_cost_val = float(total_cost)
                except Exception:
                    total_cost_val = None

            total_profit_val = None
            if total_profit is not None:
                try:
                    total_profit_val = float(total_profit)
                except Exception:
                    total_profit_val = None

            # Fallback: if profit not provided but we have revenue and cost, compute it
            if total_profit_val is None and total_cost_val is not None:
                total_profit_val = total_revenue_val - total_cost_val

            # If still None, treat profit as revenue (best-effort)
            if total_profit_val is None:
                total_profit_val = total_revenue_val

            if is_english:
                header = "💰 This month's profit:"
                if month_label:
                    header += f" (month: {month_label})"
                lines = [
                    header,
                    f"✅ Total items sold: {total_items}",
                    f"📦 Total sales (revenue): ₹{total_revenue_val:,.2f}",
                ]
                if total_cost_val is not None:
                    lines.append(f"🧾 Purchase cost (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Profit: ₹{total_profit_val:,.2f}")
            else:
                header = "💰 Is mahine ka munafa:"
                if month_label:
                    header += f" (month: {month_label})"
                lines = [
                    header,
                    f"✅ Total items sold: {total_items}",
                    f"📦 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}",
                ]
                if total_cost_val is not None:
                    lines.append(f"🧾 Khareed ka kharcha (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Munafa: ₹{total_profit_val:,.2f}")

            return nl.join(lines)


        elif action == 'zero_sale_today':
            zero_products = result.get('zero_sale_products', [])
            total_zero = result.get('total_zero_sale_products', len(zero_products))

            if not zero_products:
                if is_english:
                    return "✅ No zero-sale products today. All products with stock had at least one sale."
                return "✅ Aaj koi 'zero sale' product nahi hai. Jinke paas stock tha, sab ki sale hui."

            # Use CRLF for clean multi-line formatting
            nl = "\r\n"
            shown = len(zero_products)
            if is_english:
                response = f"😴 Top {shown} products with zero sales today (still in stock):{nl}{nl}"
            else:
                response = f"😴 Aaj ke top {shown} product jinki sale zero hai (stock mein hain):{nl}{nl}"

            for p in zero_products:
                name = p.get('name', 'Product')
                stock = p.get('stock', 0)
                unit = p.get('unit', 'pieces')
                response += f"• {name}: {stock} {unit}{nl}"

            # Mention total zero-sale products if there are more than shown
            if total_zero > shown:
                if is_english:
                    response += f"{nl}Total zero-sale products today: {total_zero} (showing top {shown})."
                else:
                    response += f"{nl}Aaj zero-sale products kul: {total_zero} (sirf top {shown} dikhaye gaye)."
            else:
                if is_english:
                    response += f"{nl}Total zero-sale products today: {total_zero}"
                else:
                    response += f"{nl}Aaj zero-sale products: {total_zero}"

            return response

        elif action == 'expiry_products':
            expired = result.get('expired_products', []) or []
            expiring = result.get('expiring_products', []) or []
            days = result.get('days_ahead', 30)

            if not expired and not expiring:
                if is_english:
                    return f"✅ No products are expired or expiring in the next {days} days."
                return f"✅ Agle {days} din mein koi product expiry ke kareeb nahi hai."

            nl = "\r\n"
            lines = []

            if expiring:
                if is_english:
                    lines.append(f"⏰ Products expiring in next {days} days:")
                else:
                    lines.append(f"⏰ Agle {days} din mein expiry ke kareeb products:")
                for p in expiring:
                    name = p.get('name', 'Product')
                    brand = p.get('brand') or ""
                    stock = p.get('stock', 0)
                    unit = p.get('unit', 'pieces')
                    expiry_date = p.get('expiry_date', '')
                    if brand:
                        display_name = f"{name} ({brand})"
                    else:
                        display_name = name
                    lines.append(f"• {display_name}: {stock} {unit} — expiry {expiry_date}")

            if expired:
                if lines:
                    lines.append("")  # blank line between sections
                if is_english:
                    lines.append("❌ Already expired products:")
                else:
                    lines.append("❌ Jo products ab tak expire ho chuke hain:")
                for p in expired:
                    name = p.get('name', 'Product')
                    brand = p.get('brand') or ""
                    stock = p.get('stock', 0)
                    unit = p.get('unit', 'pieces')
                    expiry_date = p.get('expiry_date', '')
                    if brand:
                        display_name = f"{name} ({brand})"
                    else:
                        display_name = name
                    lines.append(f"• {display_name}: {stock} {unit} — expiry {expiry_date}")

            return nl.join(lines)




        elif action == 'undo_last':
            old_stock = result.get('old_stock')
            new_stock = result.get('new_stock')
            unit = result.get('unit', 'pieces')

            if is_english:
                return (
                    f"✅ Last entry for {product_name} has been undone. "
                    f"Stock: {old_stock} → {new_stock} {unit}"
                )
            return (
                f"✅ {product_name} ki last entry undo ho gayi. "
                f"Stock {old_stock} se {new_stock} {unit} ho gaya."
            )

        elif action == 'add_udhar':
            customer_name = result.get('customer_name') or product_name or "Customer"
            amount = result.get('amount', 0) or 0
            balance = result.get('balance', 0) or 0
            if is_english:
                return (
                    f"✅ Udhar added for {customer_name}: ₹{amount:.2f}\r\n"
                    f"Total balance: ₹{balance:.2f}"
                )
            return (
                f"✅ {customer_name} ka udhar add ho gaya: ₹{amount:.2f}\r\n"
                f"Total baaki: ₹{balance:.2f}"
            )

        elif action == 'pay_udhar':
            customer_name = result.get('customer_name') or product_name or "Customer"
            amount = abs(result.get('amount', 0) or 0)
            balance = result.get('balance', 0) or 0
            if is_english:
                return (
                    f"✅ Payment received from {customer_name}: ₹{amount:.2f}\r\n"
                    f"Remaining balance: ₹{balance:.2f}"
                )
            return (
                f"✅ {customer_name} ne ₹{amount:.2f} de diya\r\n"
                f"Baaki balance: ₹{balance:.2f}"
            )

        elif action == 'list_udhar':
            customers = result.get('customers') or []
            total_udhar = result.get('total_udhar', 0) or 0
            total_customers = result.get('total_customers', len(customers))
            nl = "\r\n"

            if not customers:
                if is_english:
                    return "📒 No outstanding udhar."
                return "📒 Koi udhar baaki nahi hai."

            lines = []
            if is_english:
                lines.append(f"📒 Udhar summary ({total_customers} customers):")
            else:
                lines.append(f"📒 Udhar ki list ({total_customers} customers):")

            for c in customers:
                name = c.get('name', 'Customer')
                balance = c.get('balance', 0) or 0
                lines.append(f"• {name}: ₹{balance:.2f}")

            lines.append("")
            lines.append(f"Total udhar: ₹{total_udhar:.2f}")
            return nl.join(lines)


        elif action == 'help':
            # Return a small help message with example commands.
            nl = "\r\n"
            if is_english:
                return (
                    f"Here are some things you can say:{nl}{nl}"
                    f"• 'Add 10 Maggi' (add stock){nl}"
                    f"• 'Sold 2 oil bottles' (reduce stock){nl}"
                    f"• 'Maggi ka stock batao' (check stock){nl}"
                    f"• 'Aaj ki bikri kitni hai?' (today's total sales){nl}"
                    f"• 'Show all products' or 'Kitne product hai?' (list products){nl}"
                    f"• 'Which products are low?' (low stock alert){nl}"
                    f"• 'Undo last entry' (undo last action){nl}"
                )
            return (
                f"Aap yeh sab bol sakte hain:{nl}{nl}"
                f"• '10 Maggi add karo' (stock badhao){nl}"
                f"• '5 oil bech diya' (stock kam karo){nl}"
                f"• 'Maggi ka stock batao' (stock check){nl}"
                f"• 'Aaj ki bikri kitni hai?' (aaj ka total sale){nl}"
                f"• 'Sabhi product dikhao' ya 'Kitne product hain?' (saare products){nl}"
                f"• 'Kaun se product kam hain?' (low stock alert){nl}"
                f"• 'Antim entry wapas lo' (last entry undo){nl}"
            )

        return "Command processed successfully!"

