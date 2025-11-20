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
            print(f"   📝 Whisper Transcript (RAW): {repr(text)}")

            if text is None:
                return None

            text = text.strip()
            if not text:
                print("⚠️ Transcription returned empty text.")
                return None

            # Clean and normalize the transcribed text
            print(f"   🔍 Before cleaning: {repr(text)}")
            cleaned_text = self.clean_voice_text(text)
            print(f"   ✨ After cleaning: {repr(cleaned_text)}")

            # Store for unrecognized command tracking
            self._last_cleaned_text = cleaned_text

            return cleaned_text

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception:
                    pass

    def clean_voice_text(self, text: str) -> str:
        """Clean and normalize voice-to-text output.

        Uses regex-based cleaning for speed and reliability:
        - Converts Hindi number words to digits (do → 2, teen → 3)
        - Removes filler words (um, uh, hmm, like, you know, etc.)
        - Removes repeated consecutive words
        - Removes extra whitespace
        - Normalizes common voice artifacts

        Args:
            text: Raw transcribed text from Whisper

        Returns:
            Cleaned and normalized text ready for command parsing
        """
        if not text or not text.strip():
            return text

        import re

        cleaned = text.strip()

        # Step 0: Convert Hindi number words to digits FIRST (before cleaning)
        # This prevents confusion with "do" (2) vs "do" (command suffix in "kar do")

        # Special handling for "do" - only convert if followed by action words
        # "Maggi do add" → "Maggi 2 add" (convert)
        # "Maggi do bik gaya" → "Maggi 2 bik gaya" (convert)
        # "add kar do" → "add kar do" (don't convert - it's a command suffix)
        # "karo do" → "karo do" (don't convert - it's a command suffix)

        # Pattern: "do" followed by action words (add, bik, sold, etc.) but NOT command suffixes (kar, karo)
        cleaned = re.sub(r'\bdo\b(?=\s+(add|aad|dal|daal|डाल|bik|sold|sell|bech|बेच|stock|check|kitna|hai))', '2', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bdoh\b(?=\s+(add|aad|dal|daal|डाल|bik|sold|sell|bech|बेच|stock|check|kitna|hai))', '2', cleaned, flags=re.IGNORECASE)

        # Other Hindi numbers (no ambiguity, convert all)
        hindi_numbers = {
            r'\bek\b': '1',
            r'\bteen\b': '3',
            r'\btiin\b': '3',
            r'\bchar\b': '4',
            r'\bchaar\b': '4',
            r'\bpanch\b': '5',
            r'\bpaanch\b': '5',
            r'\bchhe\b': '6',
            r'\bchhah\b': '6',
            r'\bsaat\b': '7',
            r'\baath\b': '8',
            r'\baat\b': '8',
            r'\bnau\b': '9',
            r'\bdas\b': '10',
            r'\bdus\b': '10',
            r'\bgyarah\b': '11',
            r'\bbarah\b': '12',
            r'\bterah\b': '13',
            r'\bchaudah\b': '14',
            r'\bpandrah\b': '15',
            r'\bsolah\b': '16',
            r'\bsatrah\b': '17',
            r'\batharah\b': '18',
            r'\bunnis\b': '19',
            r'\bbees\b': '20',
            r'\bikkis\b': '21',
            r'\bbaees\b': '22',
            r'\btees\b': '30',
            r'\bchalis\b': '40',
            r'\bpachas\b': '50',
            r'\bsaath\b': '60',
            r'\bsattar\b': '70',
            r'\bassi\b': '80',
            r'\bnabbe\b': '90',
            r'\bsau\b': '100',
        }

        # Convert Hindi numbers to digits (case-insensitive)
        for hindi_word, digit in hindi_numbers.items():
            cleaned = re.sub(hindi_word, digit, cleaned, flags=re.IGNORECASE)

        # Step 1: Remove common filler words (case-insensitive)
        filler_words = [
            r'\bum\b', r'\buh\b', r'\bhmm\b', r'\bhm\b', r'\buhm\b',
            r'\blike\b', r'\byou know\b', r'\bI mean\b', r'\bactually\b',
            r'\bbasically\b', r'\bliterally\b', r'\bso\b', r'\bwell\b',
            r'\boh\b', r'\bah\b', r'\ber\b', r'\behm\b',
        ]

        for filler in filler_words:
            cleaned = re.sub(filler, '', cleaned, flags=re.IGNORECASE)

        # Step 2: Remove repeated consecutive words (e.g., "Maggi Maggi" → "Maggi")
        # Match word boundaries to avoid breaking product names
        cleaned = re.sub(r'\b(\w+)\s+\1\b', r'\1', cleaned, flags=re.IGNORECASE)

        # Step 3: Remove extra whitespace (multiple spaces → single space)
        cleaned = re.sub(r'\s+', ' ', cleaned)

        # Step 4: Remove leading/trailing whitespace
        cleaned = cleaned.strip()

        # Step 5: If cleaning resulted in empty string, return original
        if not cleaned:
            return text

        return cleaned

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
            "galti",
            "galati",
            "wrong",
            "mistake",
            "undo kar do",
            "undo karo",
            "wapas kar do",
            "wapas karo",
            "hatao",
            "hata do",
            "delete last",
            "remove last",
            "cancel last",
            "galti ho gayi",
            "galati ho gayi",
            "galti ho gai",
            "galati ho gai",
            "wrong entry",
            "galt entry",
            "previous undo",
            "previous wapas",
            "last wapas",
            "last hatao",
        ]
        undo_keywords_hindi = [
            "अंतिम एंट्री वापस लो",
            "आखिरी एंट्री वापस लो",
            "पिछली एंट्री वापस लो",
            "गलती",
            "गलती हो गई",
            "गलत एंट्री",
            "वापस करो",
            "हटाओ",
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
        #   - "Ramesh udhar" / "udhar Ramesh" (customer-specific history)
        udhar_words = ["udhar", "udhaar", "khata", "baki", "baaki"]
        has_udhar_word = any(w in normalized for w in udhar_words)

        # (a) Summary / list style queries and person-specific udhar queries
        if has_udhar_word:
            # (a0) Person-level udhar question like "Ramesh ka udhar kitna hai?"
            # If there is a name + "udhar" + "kitna/kitni/kitne" but no digits,
            # treat it as a customer-specific udhar history instead of global summary.
            if (
                ("kitna" in normalized or "kitni" in normalized or "kitne" in normalized or "amount" in normalized or "money" in normalized)
                and not any(ch.isdigit() for ch in normalized)
            ):
                customer_name = None
                text = normalized

                # Pattern: "<name> ka/ke/ki udhar ..."
                for pattern in [
                    " ka udhar",
                    " ke udhar",
                    " ki udhar",
                    " ka udhaar",
                    " ke udhaar",
                    " ki udhaar",
                ]:
                    if pattern in text:
                        before = text.split(pattern, 1)[0].strip()
                        if before:
                            customer_name = before
                            break

                # Pattern: "udhar/udhaar <name> ..." (e.g. "udhar kitna hai ramesh ka")
                if not customer_name:
                    for marker in ["udhar", "udhaar"]:
                        marker_token = marker + " "
                        idx = text.find(marker_token)
                        if idx != -1:
                            after = text[idx + len(marker_token) :].strip()

                            # Remove leading fillers like "kitna hai", "kitne hai", etc.
                            leading_fillers = [
                                "kitna hai",
                                "kitni hai",
                                "kitne hai",
                                "kitna h",
                                "kitni h",
                                "kitne h",
                                "kitna",
                                "kitni",
                                "kitne",
                                "total",
                                "pura",
                            ]
                            for lf in leading_fillers:
                                lf_with_space = lf + " "
                                if after.startswith(lf_with_space):
                                    after = after[len(lf_with_space) :].strip()

                            # Trim trailing "ka/ke/ki"
                            for suffix in [" ka", " ke", " ki"]:
                                if after.endswith(suffix):
                                    after = after[: -len(suffix)].strip()

                            if after:
                                customer_name = after
                                break

                if customer_name:
                    # Clean out leftover filler tokens from the name
                    for junk in ["mera", "meri", "mere", "sab", "all", "aaj", "kal"]:
                        customer_name = customer_name.replace(" " + junk + " ", " ")
                    customer_name = customer_name.strip()

                    bad_tokens = {"hai", "h", "kya", "kitna", "kitni", "kitne", "total", "list", "summary"}
                    if customer_name and len(customer_name) >= 3 and customer_name not in bad_tokens:
                        return ParsedCommand(
                            action=CommandAction.CUSTOMER_UDHAR,
                            product_name=customer_name,
                            quantity=None,
                            confidence=0.93,
                            raw_message=message,
                        )

            # (a1) Overall udhar summary / list queries
            if any(
                kw in normalized
                for kw in ["udhar list", "udhar ka hisab", "udhar ka hisaab", "udhar summary"]
            ):
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

                # No amount → treat "udhar Ramesh" style as customer history (if it looks like a name)
                clean_rest = rest.strip()
                if clean_rest and not any(
                    marker in clean_rest for marker in ["kitna", "kitni", "total", "list", "summary"]
                ):
                    for junk in ["pay", "payment", "ne", "se", "ka", "ki", "ke"]:
                        clean_rest = clean_rest.replace(junk, " ")
                    customer_name = clean_rest.strip()
                    if customer_name:
                        return ParsedCommand(
                            action=CommandAction.CUSTOMER_UDHAR,
                            product_name=customer_name,
                            quantity=None,
                            confidence=0.9,
                            raw_message=message,
                        )

            # (c) Customer-specific history with pattern "<name> udhar"
            if not any(ch.isdigit() for ch in normalized):
                # e.g. "ramesh udhar", "ramesh ka udhar"
                before = None
                if normalized.endswith(" udhar") or normalized.endswith(" udhaar"):
                    before = normalized.rsplit(" udhar", 1)[0]
                elif normalized.endswith(" ka udhar") or normalized.endswith(" ka udhaar"):
                    before = normalized.rsplit(" ka udhar", 1)[0]

                if before:
                    # Remove small filler words at the end like "ka"/"ki"/"ke"
                    for junk in ["ka", "ki", "ke"]:
                        if before.endswith(" " + junk):
                            before = before[: -len(junk) - 1]
                    customer_name = before.strip()
                    if customer_name and not any(
                        marker in customer_name for marker in ["kitna", "kitni", "total", "list", "summary"]
                    ):
                        return ParsedCommand(
                            action=CommandAction.CUSTOMER_UDHAR,
                            product_name=customer_name,
                            quantity=None,
                            confidence=0.9,
                            raw_message=message,
                        )

            # (d) If message clearly talks about udhar but we couldn't parse amount or name,
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
        # - "Weekly profit" / "hafte ka profit"
        # - "Monthly estimated profit" / "mahine ka profit"
        # - "Yearly profit" / "saal ka profit"
        if ("profit" in normalized) or ("munafa" in normalized):
            yearly_markers = ["year", "saal", "sal", "yearly", "saal ka", "sal ka"]
            monthly_markers = ["month", "mahina", "mahine", "mahine ka", "monthly"]
            weekly_markers = ["week", "hafte", "hafta", "weekly", "hafte ka", "hafta ka"]
            today_markers = ["aaj", "aj ", "today"]

            if any(y in normalized for y in yearly_markers):
                return ParsedCommand(
                    action=CommandAction.YEARLY_PROFIT,
                    product_name=None,
                    quantity=None,
                    confidence=0.99,
                    raw_message=message,
                )

            if any(m in normalized for m in monthly_markers):
                return ParsedCommand(
                    action=CommandAction.MONTHLY_PROFIT,
                    product_name=None,
                    quantity=None,
                    confidence=0.99,
                    raw_message=message,
                )

            if any(w in normalized for w in weekly_markers):
                return ParsedCommand(
                    action=CommandAction.WEEKLY_PROFIT,
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

        # 5b) Purchase suggestions based on sales patterns
        # Examples:
        # - "purchase suggestion"
        # - "kya order karna chahiye"
        # - "kya mangwana chahiye"
        # - "reorder suggestion"
        # - "what to buy"
        purchase_keywords = [
            "purchase suggestion",
            "order suggestion",
            "reorder",
            "kya order",
            "kya mangwa",
            "what to buy",
            "what to order",
            "kya kharidna",
            "suggestion",
        ]
        if any(kw in normalized for kw in purchase_keywords):
            return ParsedCommand(
                action=CommandAction.PURCHASE_SUGGESTION,
                product_name=None,
                quantity=None,
                confidence=0.98,
                raw_message=message,
            )

        # 5c) Set low stock threshold
        # Examples:
        # - "Maggi low stock alert 10"
        # - "Maggi ka minimum stock 5 rakho"
        # - "Set Maggi threshold 15"
        threshold_keywords = ["threshold", "minimum stock", "low stock alert", "alert level", "minimum level"]
        if any(kw in normalized for kw in threshold_keywords):
            # Try to extract product name and threshold value
            tokens = normalized.split()
            threshold_val = None

            # Find the number (threshold value)
            for tok in tokens:
                m = re.fullmatch(r"(\d+(?:\.\d+)?)", tok)
                if m:
                    try:
                        threshold_val = float(m.group(1))
                        break
                    except Exception:
                        continue

            if threshold_val is not None:
                # Extract product name (words before threshold keywords)
                product_tokens = []
                for tok in tokens:
                    if tok in threshold_keywords or tok.replace('.', '').isdigit():
                        break
                    product_tokens.append(tok)

                if product_tokens:
                    product_name_extracted = " ".join(product_tokens)
                    return ParsedCommand(
                        action=CommandAction.SET_LOW_STOCK_THRESHOLD,
                        product_name=product_name_extracted,
                        quantity=threshold_val,
                        confidence=0.95,
                        raw_message=message,
                    )

        # 5d) Predictive alerts
        # Examples:
        # - "predictive alert"
        # - "kab khatam hoga"
        # - "stock kab khatam hoga"
        # - "when will stock run out"
        # - "kitne din mein khatam hoga"
        predictive_keywords = [
            "predictive",
            "predict",
            "kab khatam",
            "when run out",
            "when will",
            "kitne din",
            "stock forecast",
            "forecast",
        ]
        if any(kw in normalized for kw in predictive_keywords):
            return ParsedCommand(
                action=CommandAction.PREDICTIVE_ALERT,
                product_name=None,
                quantity=None,
                confidence=0.98,
                raw_message=message,
            )

        # 5d) Seasonal suggestions
        # Examples:
        # - "diwali products"
        # - "holi ke liye kya stock karu"
        # - "seasonal analysis"
        # - "christmas suggestions"
        seasonal_keywords = [
            "seasonal", "season", "festival", "tyohar", "tyohaar",
            "diwali", "deepavali", "holi", "eid", "christmas", "new year",
            "raksha bandhan", "rakhi", "navratri", "durga puja",
            "summer", "winter", "monsoon", "barish", "garmi", "sardi"
        ]

        # Extract festival/season name if mentioned
        festival_name = None
        for keyword in seasonal_keywords:
            if keyword in normalized:
                festival_name = keyword
                break

        if any(kw in normalized for kw in seasonal_keywords):
            return ParsedCommand(
                action=CommandAction.SEASONAL_SUGGESTION,
                product_name=festival_name,  # Store festival/season name
                quantity=None,
                confidence=0.98,
                raw_message=message,
            )

        # 6) Simple price update ("Maggi price 12", "Maggi ka rate 12").
        # We look for a price/rate keyword + a number and treat it as "update_price".
        price_words = {"price", "rate", "daam", "dam", "kimat", "keemat"}
        tokens = normalized.split()
        price_idx = None
        for i, tok in enumerate(tokens):
            if tok in price_words:
                price_idx = i
                break
        amount = None
        amount_idx = None
        for i, tok in enumerate(tokens):
            m = re.fullmatch(r"(\d+(?:\.\d+)?)", tok)
            if m:
                try:
                    amount = float(m.group(1))
                    amount_idx = i
                    break
                except Exception:
                    continue
        if price_idx is not None and amount is not None and amount > 0:
            # Prefer tokens between "price/rate" and the number as the product name.
            if amount_idx - price_idx > 1:
                name_tokens = tokens[price_idx + 1 : amount_idx]
            else:
                name_tokens = tokens[:price_idx]
            junk_words = {"ka", "ki", "ke", "of", "is", "hai", "set", "change", "update", "naya", "new", "to", "in", "per", "rs", "rs.", "rupaye", "rupay", "rupees", "rs/-"}
            name_tokens = [t for t in name_tokens if t not in junk_words and not any(ch.isdigit() for ch in t)]
            product_name = " ".join(name_tokens).strip()
            if product_name:
                return ParsedCommand(
                    action=CommandAction.UPDATE_PRICE,
                    product_name=product_name,
                    quantity=amount,
                    confidence=0.97,
                    raw_message=message,
                )






        # 4) Flexible hisaab / report queries (day / month / year).
        # If message clearly talks about "hisaab" / "hisab" / "report", let the
        # command processor + DB figure out the exact date range. We only map the
        # intent to REPORT_SUMMARY and pass the raw message through.
        report_markers = [
            "hisaab",
            "hisab",
            "hisaab ka",
            "hisab ka",
            "report",
            "hisaab batao",
            "hisab batao",
        ]
        if any(m in normalized for m in report_markers):
            return ParsedCommand(
                action=CommandAction.REPORT_SUMMARY,
                product_name=None,
                quantity=None,
                confidence=0.97,
                raw_message=message,
            )

        # 5) Generic keyword-based product search.
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

                # IMPROVED: Better pattern matching for "Product Number add/bik" commands
                # Handles: "Maggi 2 add kar do", "Parle G 5 bik gaya", etc.
                if qty_val and qty_val > 0:
                    # Pattern: <product_name> <number> <action_word>
                    # Examples: "Maggi 2 add", "Parle G 5 bik gaya", "Colgate 10 add karo"
                    add_pattern = r'^(.+?)\s+' + re.escape(str(int(qty_val) if qty_val.is_integer() else qty_val)) + r'\s+(add|aad|dal|daal|डाल)'
                    reduce_pattern = r'^(.+?)\s+' + re.escape(str(int(qty_val) if qty_val.is_integer() else qty_val)) + r'\s+(bik|sold|sell|bech|बेच|nikal|निकाल)'

                    add_match = re.search(add_pattern, normalized, re.IGNORECASE)
                    reduce_match = re.search(reduce_pattern, normalized, re.IGNORECASE)

                    if add_match:
                        product_name = add_match.group(1).strip()
                        return ParsedCommand(
                            action=CommandAction.ADD_STOCK,
                            product_name=product_name,
                            quantity=qty_val,
                            confidence=0.98,
                            raw_message=message,
                        )

                    if reduce_match:
                        product_name = reduce_match.group(1).strip()
                        return ParsedCommand(
                            action=CommandAction.REDUCE_STOCK,
                            product_name=product_name,
                            quantity=qty_val,
                            confidence=0.98,
                            raw_message=message,
                        )

                    # Fallback to old logic if pattern doesn't match
                    add_keywords = ["add", "a dd", "aad", "ऐड", "एड", "dal do", "daal do", "डाल", "डाल दो"]
                    reduce_keywords = ["sold", "sell", "bech", "बेच", "bik", "बिक", "nikal", "निकाल", "निकाला"]

                    action = None
                    if any(kw in normalized for kw in add_keywords):
                        action = CommandAction.ADD_STOCK
                    elif any(kw in normalized for kw in reduce_keywords):
                        action = CommandAction.REDUCE_STOCK

                    if action is not None:
                        # Try to infer product name as the words BEFORE the number
                        orig_words = message.split()
                        norm_words = normalized.split()
                        if len(orig_words) == len(norm_words):
                            num_idx = next(
                                (i for i, w in enumerate(norm_words) if any(ch.isdigit() for ch in w)),
                                None,
                            )

                            product_tokens = []
                            if num_idx is not None and num_idx > 0:
                                # Product name is BEFORE the number
                                product_tokens = orig_words[:num_idx]

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
1. action: one of "add_stock", "reduce_stock", "check_stock", "total_sales", "today_profit", "monthly_profit", "list_products", "low_stock", "adjust_stock", "update_price", "top_product_today", "zero_sale_today", "expiry_products", "purchase_suggestion", "set_low_stock_threshold", "predictive_alert", "seasonal_suggestion", "undo_last", "help", "add_udhar", "pay_udhar", "list_udhar", "customer_udhar", "report_summary", or "unknown"
2. product_name: the name of the product mentioned (for udhar actions this is the customer name; for seasonal_suggestion this is the festival/season name like "diwali", "holi", "summer"; not needed for total_sales, today_profit, monthly_profit, list_products, low_stock, top_product_today, zero_sale_today, expiry_products, purchase_suggestion, predictive_alert, undo_last, help, list_udhar, or report_summary)
3. quantity: the quantity mentioned (if applicable). For "adjust_stock", quantity should be the CORRECT quantity for the last entry (e.g., if user says "Maggi 3 nahi 1 the" then quantity is 1). For "update_price", quantity is the new selling price per unit (in rupees). For udhar actions that include an amount (add_udhar, pay_udhar), quantity is the rupee amount (always positive). For list_udhar, customer_udhar, and seasonal_suggestion, quantity should be null.

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

Examples of SEASONAL_SUGGESTION (festival/season product recommendations):
- "diwali products" -> action "seasonal_suggestion" with product_name "diwali"
- "holi ke liye kya stock karu" -> action "seasonal_suggestion" with product_name "holi"
- "seasonal analysis" -> action "seasonal_suggestion" with product_name null
- "summer products" -> action "seasonal_suggestion" with product_name "summer"
- "christmas suggestions" -> action "seasonal_suggestion" with product_name "christmas"
- "tyohar ke liye kya chahiye" -> action "seasonal_suggestion" with product_name null

	Examples of UDHAR (credit tracking):
	- "udhar Ramesh 200" -> action "add_udhar" with product_name "Ramesh" and quantity 200
	- "Ramesh udhar 300 doodh" -> action "add_udhar" with product_name "Ramesh" and quantity 300 (note like "doodh" is optional context)
	- "Ramesh udhar" -> action "customer_udhar" with product_name "Ramesh" (no quantity)
	- "udhar list" / "kitna udhar hai" -> action "list_udhar" (no product_name, no quantity)
	- "udhar pay Ramesh 200" / "Ramesh ne 200 de diya" -> action "pay_udhar" with product_name "Ramesh" and quantity 200


Key words to identify actions:
- ADD: add, laya, aaya, purchase, bought, received, new stock, stock mein daal, mila, got
- REDUCE: sold, bik gaya, bech diya, nikala, sale, customer ko diya, gaya
- CHECK: kitna, how much, stock, batao, check, remaining, bacha, inventory, count (for specific product)
- TOTAL_SALES: total sale, aaj ka sale, today's sales, kitna bika, business, sales report, aaj ka total
- PROFIT: profit, munafa, estimated profit
- UPDATE_PRICE: price, rate, daam, kimat, keemat, "Maggi price 12", "Maggi ka rate 15 rupaye"
- REPORT_SUMMARY: hisaab, hisab, hisaab ka, hisab ka, "aaj ka hisaab", "is mahine ka hisaab", "is saal ka hisaab", "report", "report de do", "aaj ka hisaab batao"

Messages may contain Devanagari Hindi words like "मैगी", "ऐड कर दो", "बिक गए". Parse them the same way as the Hinglish examples above.

Be intelligent and understand the INTENT, not just exact phrases.

Return ONLY a JSON object with this exact structure:
{
    "action": "add_stock" | "reduce_stock" | "check_stock" | "total_sales" | "today_profit" | "weekly_profit" | "monthly_profit" | "yearly_profit" | "list_products" | "low_stock" | "adjust_stock" | "update_price" | "top_product_today" | "zero_sale_today" | "expiry_products" | "purchase_suggestion" | "set_low_stock_threshold" | "predictive_alert" | "seasonal_suggestion" | "undo_last" | "help" | "add_udhar" | "pay_udhar" | "list_udhar" | "customer_udhar" | "report_summary" | "unknown",
    "product_name": "product name" or null (for udhar actions this is the customer name; for seasonal_suggestion this is the festival/season name like "diwali", "holi", "summer"; not needed for total_sales, today_profit, weekly_profit, monthly_profit, yearly_profit, list_products, low_stock, adjust_stock, zero_sale_today, expiry_products, purchase_suggestion, predictive_alert, undo_last, help, list_udhar, top_product_today, or report_summary; for set_low_stock_threshold this is the product name),
    "quantity": number or null (for "update_price" this is the new selling price per unit in rupees; for udhar actions that involve a rupee amount (add_udhar, pay_udhar) this is the amount in rupees, always positive; for list_udhar, customer_udhar, and seasonal_suggestion it should be null),
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
                "weekly_profit": CommandAction.WEEKLY_PROFIT,
                "monthly_profit": CommandAction.MONTHLY_PROFIT,
                "yearly_profit": CommandAction.YEARLY_PROFIT,
                "list_products": CommandAction.LIST_PRODUCTS,
                "low_stock": CommandAction.LOW_STOCK,
                "adjust_stock": CommandAction.ADJUST_STOCK,
                "update_price": CommandAction.UPDATE_PRICE,
                "top_product_today": CommandAction.TOP_PRODUCT_TODAY,
                "zero_sale_today": CommandAction.ZERO_SALE_TODAY,
                "expiry_products": CommandAction.EXPIRY_PRODUCTS,
                "purchase_suggestion": CommandAction.PURCHASE_SUGGESTION,
                "set_low_stock_threshold": CommandAction.SET_LOW_STOCK_THRESHOLD,
                "predictive_alert": CommandAction.PREDICTIVE_ALERT,
                "seasonal_suggestion": CommandAction.SEASONAL_SUGGESTION,
                "undo_last": CommandAction.UNDO_LAST,
                "help": CommandAction.HELP,
                "add_udhar": CommandAction.ADD_UDHAR,
                "pay_udhar": CommandAction.PAY_UDHAR,
                "list_udhar": CommandAction.LIST_UDHAR,
                "customer_udhar": CommandAction.CUSTOMER_UDHAR,
                "report_summary": CommandAction.REPORT_SUMMARY,
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
            low_stock_alert = result.get('low_stock_alert')

            nl = "\r\n"

            # Base success message
            if is_english:
                response = f"✅ {quantity} {product_name} sold! Remaining stock: {new_stock} {unit}"
            else:
                response = f"✅ {quantity} {product_name} bik gaya! Baaki stock: {new_stock} {unit}"

            # Add low stock alert if triggered
            if low_stock_alert and low_stock_alert.get('triggered'):
                alert_product = low_stock_alert.get('product_name', product_name)
                alert_brand = low_stock_alert.get('brand')
                alert_stock = low_stock_alert.get('current_stock', new_stock)
                alert_threshold = low_stock_alert.get('threshold', 10)
                alert_unit = low_stock_alert.get('unit', unit)

                # Build display name
                if alert_brand:
                    display_name = f"{alert_brand} {alert_product}"
                else:
                    display_name = alert_product

                if is_english:
                    response += f"{nl}{nl}⚠️ LOW STOCK ALERT!{nl}"
                    response += f"🔴 {display_name} is running low!{nl}"
                    response += f"📊 Current stock: {alert_stock} {alert_unit}{nl}"
                    response += f"⚡ Threshold: {alert_threshold} {alert_unit}{nl}"
                    response += f"🛒 Please reorder soon!"
                else:
                    response += f"{nl}{nl}⚠️ LOW STOCK ALERT!{nl}"
                    response += f"🔴 {display_name} kam ho gaya hai!{nl}"
                    response += f"📊 Abhi stock: {alert_stock} {alert_unit}{nl}"
                    response += f"⚡ Minimum level: {alert_threshold} {alert_unit}{nl}"
                    response += f"🛒 Jaldi order kar lijiye!"

            return response

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
            selling_price = result.get('selling_price')
            cost_price = result.get('cost_price')
            expiry_date = result.get('expiry_date')
            brand = result.get('brand')

            nl = "\r\n"

            # Build product display name with brand if available
            display_name = f"{brand} {product_name}" if brand else product_name

            if is_english:
                lines = [f"📦 {display_name}:"]
                lines.append(f"📊 Stock: {current_stock} {unit}")

                if selling_price is not None:
                    try:
                        price_val = float(selling_price)
                        lines.append(f"💰 Price: ₹{price_val:,.2f} per {unit}")
                    except Exception:
                        pass

                if cost_price is not None:
                    try:
                        cost_val = float(cost_price)
                        lines.append(f"🧾 Cost: ₹{cost_val:,.2f} per {unit}")
                    except Exception:
                        pass

                if expiry_date:
                    lines.append(f"📅 Expiry: {expiry_date}")

                return nl.join(lines)
            else:
                lines = [f"📦 {display_name}:"]
                lines.append(f"📊 Stock: {current_stock} {unit}")

                if selling_price is not None:
                    try:
                        price_val = float(selling_price)
                        lines.append(f"💰 Price: ₹{price_val:,.2f} per {unit}")
                    except Exception:
                        pass

                if cost_price is not None:
                    try:
                        cost_val = float(cost_price)
                        lines.append(f"🧾 Khareed ka price: ₹{cost_val:,.2f} per {unit}")
                    except Exception:
                        pass

                if expiry_date:
                    lines.append(f"📅 Expiry date: {expiry_date}")

                return nl.join(lines)

        elif action == 'update_price':
            new_price = result.get('selling_price') or result.get('price') or result.get('unit_price')
            unit = result.get('unit', 'pieces')
            try:
                price_val = float(new_price) if new_price is not None else None
            except Exception:
                price_val = None
            if price_val is None:
                if is_english:
                    return f"✅ Price updated for {product_name}."
                return f"✅ {product_name} ka price update ho gaya."
            if is_english:
                return f"✅ Price updated! {product_name} is now ₹{price_val:,.2f} per {unit}."
            return f"✅ {product_name} ka price update ho gaya. Ab ₹{price_val:,.2f} per {unit}."


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

            # Build header
            if is_english:
                header = f"💰 This month's profit ({month_label}):" if month_label else "💰 This month's profit:"
            else:
                header = f"💰 Is mahine ka munafa ({month_label}):" if month_label else "💰 Is mahine ka munafa:"

            lines = [header]
            lines.append(f"✅ Total items sold: {total_items}")
            if is_english:
                lines.append(f"💰 Total revenue: ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Purchase cost (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Profit (approx): ₹{total_profit_val:,.2f}")
            else:
                lines.append(f"💰 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Khareed ka kharcha (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Munafa (approx): ₹{total_profit_val:,.2f}")

            return nl.join(lines)

        elif action == 'weekly_profit':
            total_items = result.get('total_items_sold', 0)
            total_revenue = result.get('total_revenue')
            total_cost = result.get('total_cost')
            total_profit = result.get('total_profit')
            week_label = result.get('week')

            nl = "\r\n"

            if total_revenue is None:
                if is_english:
                    header = "💰 This week's profit: ₹0.00"
                    note = "ℹ️ No sales recorded this week, so profit is zero."
                else:
                    header = "💰 Is hafte ka munafa: ₹0.00"
                    note = "ℹ️ Is hafte koi sale record nahi hui, isliye munafa zero hai."
                if week_label:
                    header = f"{header} ({week_label})"
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

            # Build header
            if is_english:
                header = f"💰 This week's profit ({week_label}):" if week_label else "💰 This week's profit:"
            else:
                header = f"💰 Is hafte ka munafa ({week_label}):" if week_label else "💰 Is hafte ka munafa:"

            lines = [header]
            lines.append(f"✅ Total items sold: {total_items}")
            if is_english:
                lines.append(f"💰 Total revenue: ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Purchase cost (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Profit (approx): ₹{total_profit_val:,.2f}")
            else:
                lines.append(f"💰 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Khareed ka kharcha (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Munafa (approx): ₹{total_profit_val:,.2f}")

            return nl.join(lines)

        elif action == 'yearly_profit':
            total_items = result.get('total_items_sold', 0)
            total_revenue = result.get('total_revenue')
            total_cost = result.get('total_cost')
            total_profit = result.get('total_profit')
            year_label = result.get('year')

            nl = "\r\n"

            if total_revenue is None:
                if is_english:
                    header = "💰 This year's profit: ₹0.00"
                    note = "ℹ️ No sales recorded this year, so profit is zero."
                else:
                    header = "💰 Is saal ka munafa: ₹0.00"
                    note = "ℹ️ Is saal koi sale record nahi hui, isliye munafa zero hai."
                if year_label:
                    header = f"{header} (year: {year_label})"
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

            # Build header
            if is_english:
                header = f"💰 This year's profit ({year_label}):" if year_label else "💰 This year's profit:"
            else:
                header = f"💰 Is saal ka munafa ({year_label}):" if year_label else "💰 Is saal ka munafa:"

            lines = [header]
            lines.append(f"✅ Total items sold: {total_items}")
            if is_english:
                lines.append(f"💰 Total revenue: ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Purchase cost (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Profit (approx): ₹{total_profit_val:,.2f}")
            else:
                lines.append(f"💰 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Khareed ka kharcha (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Munafa (approx): ₹{total_profit_val:,.2f}")

            return nl.join(lines)

        elif action == 'report_summary':
            # Generic report ("hisaab") for an arbitrary period: day / month / year.
            total_items = result.get('total_items_sold', 0)
            total_revenue = result.get('total_revenue')
            total_cost = result.get('total_cost')
            total_profit = result.get('total_profit')
            products_sold = result.get('products_sold', {}) or {}
            revenue_by_product = result.get('revenue_by_product', {}) or {}

            period_type = result.get('period_type') or 'day'
            period_label = result.get('period_label')
            start_date = result.get('start_date')
            end_date = result.get('end_date')

            nl = "\r\n"

            # Build header
            if period_type == 'day':
                label = period_label or start_date or ''
                if is_english:
                    header = f"📊 Report for {label}:"
                else:
                    header = f"📊 {label} ka hisaab:" if label else "📊 Aaj ka hisaab:"
            elif period_type == 'month':
                label = period_label or ''
                if is_english:
                    header = f"📊 Monthly report: {label}" if label else "📊 Monthly report:"
                else:
                    header = f"📊 Is mahine ka hisaab: {label}" if label else "📊 Is mahine ka hisaab:"
            elif period_type == 'year':
                label = period_label or ''
                if is_english:
                    header = f"📊 Yearly report: {label}" if label else "📊 Yearly report:"
                else:
                    header = f"📊 Is saal ka hisaab: {label}" if label else "📊 Is saal ka hisaab:"
            else:
                # Generic date range
                label = None
                if start_date and end_date and start_date != end_date:
                    if is_english:
                        header = f"📊 Report: {start_date} to {end_date}"
                    else:
                        header = f"📊 Hisaab: {start_date} se {end_date} tak"
                else:
                    if is_english:
                        header = "📊 Report:"
                    else:
                        header = "📊 Hisaab:"

            # Handle no revenue case
            if total_revenue is None:
                if is_english:
                    return header + nl + "ℹ️ No sales found in this period."
                return header + nl + "ℹ️ Is period mein koi sale record nahi hui."

            # Safe floats
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

            if total_profit_val is None and total_cost_val is not None:
                total_profit_val = total_revenue_val - (total_cost_val or 0.0)
            if total_profit_val is None:
                total_profit_val = total_revenue_val

            lines = [header]
            lines.append(f"✅ Total items sold: {total_items}")
            if is_english:
                lines.append(f"💰 Total revenue: ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Purchase cost (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Profit (approx): ₹{total_profit_val:,.2f}")
            else:
                lines.append(f"💰 Kul bikri (rupaye mein): ₹{total_revenue_val:,.2f}")
                if total_cost_val is not None:
                    lines.append(f"🧾 Khareed ka kharcha (approx): ₹{total_cost_val:,.2f}")
                lines.append(f"💵 Munafa (approx): ₹{total_profit_val:,.2f}")

            # Product-wise breakdown
            if products_sold:
                if is_english:
                    lines.append("")
                    lines.append("📦 Product-wise breakdown:")
                else:
                    lines.append("")
                    lines.append("📦 Product-wise breakdown:")

                for product, qty in products_sold.items():
                    revenue = revenue_by_product.get(product)
                    if revenue is not None:
                        try:
                            rev_val = float(revenue)
                            lines.append(f"• {product}: {qty} (₹{rev_val:,.2f})")
                        except Exception:
                            lines.append(f"• {product}: {qty}")
                    else:
                        lines.append(f"• {product}: {qty}")

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

        elif action == 'customer_udhar':
            customer_name = result.get('customer_name') or product_name or "Customer"
            balance = result.get('balance', 0) or 0
            entries = result.get('entries') or []
            nl = "\r\n"

            if not entries:
                if is_english:
                    return f"📒 No udhar entries found for {customer_name}."
                return f"📒 {customer_name} ke naam koi udhar entry nahi mili."

            lines = []
            if is_english:
                lines.append(f"📒 Udhar history for {customer_name}:")
            else:
                lines.append(f"📒 {customer_name} ka udhar history:")

            for e in entries:
                raw_amt = e.get('amount', 0) or 0
                try:
                    amt = float(raw_amt)
                except Exception:
                    amt = 0.0
                entry_type = (e.get('type') or "").lower()
                ts = e.get('timestamp') or ""
                note = e.get('note') or ""

                # Decide label text based on amount sign / type
                if amt > 0:
                    label_en = "credit"
                    label_hi = "udhar"
                elif amt < 0:
                    label_en = "payment"
                    label_hi = "payment"
                else:
                    label_en = ""
                    label_hi = ""

                amt_str = f"₹{abs(amt):.2f}"
                label = label_en if is_english else label_hi

                if ts:
                    prefix = f"{ts} – "
                else:
                    prefix = ""

                if label:
                    if note:
                        line = f"• {prefix}{amt_str} ({label}) – {note}"
                    else:
                        line = f"• {prefix}{amt_str} ({label})"
                else:
                    if note:
                        line = f"• {prefix}{amt_str} – {note}"
                    else:
                        line = f"• {prefix}{amt_str}"

                lines.append(line)

            # Summary line with remaining balance
            lines.append("")
            if is_english:
                lines.append(f"Remaining balance: ₹{balance:.2f}")
            else:
                lines.append(f"Baaki balance: ₹{balance:.2f}")

            return nl.join(lines)

        elif action == 'purchase_suggestion':
            suggestions = result.get('suggestions', []) or []
            total_suggestions = result.get('total_suggestions', 0)
            last_month_start = result.get('last_month_start', '')
            last_month_end = result.get('last_month_end', '')

            nl = "\r\n"

            if not suggestions:
                if is_english:
                    return "✅ No purchase suggestions at this time. All products have sufficient stock based on last month's sales."
                return "✅ Abhi koi purchase suggestion nahi hai. Sabhi products ka stock last month ki bikri ke hisaab se theek hai."

            # Build header
            if is_english:
                header = f"🛒 Purchase Suggestions (based on sales from {last_month_start} to {last_month_end}):"
            else:
                header = f"🛒 Purchase Suggestion (last month {last_month_start} se {last_month_end} ki bikri ke hisaab se):"

            lines = [header, ""]

            for s in suggestions:
                name = s.get('name', 'Product')
                brand = s.get('brand') or ""
                current_stock = s.get('current_stock', 0)
                unit = s.get('unit', 'pieces')
                last_month_sales = s.get('last_month_sales', 0)
                suggested_qty = s.get('suggested_order_qty', 0)
                urgency = s.get('urgency', 'medium')

                # Build display name
                if brand:
                    display_name = f"{brand} {name}"
                else:
                    display_name = name

                # Urgency emoji
                urgency_emoji = "🔴" if urgency == 'high' else "🟡"

                if is_english:
                    lines.append(f"{urgency_emoji} {display_name}:")
                    lines.append(f"   📊 Current stock: {current_stock} {unit}")
                    lines.append(f"   📈 Last month sold: {last_month_sales} {unit}")
                    lines.append(f"   🛒 Suggested order: {suggested_qty} {unit}")
                    lines.append("")
                else:
                    lines.append(f"{urgency_emoji} {display_name}:")
                    lines.append(f"   📊 Abhi stock: {current_stock} {unit}")
                    lines.append(f"   📈 Last month bika: {last_month_sales} {unit}")
                    lines.append(f"   🛒 Order karna chahiye: {suggested_qty} {unit}")
                    lines.append("")

            if is_english:
                lines.append(f"Total products needing reorder: {total_suggestions}")
                lines.append("")
                lines.append("🔴 = High urgency (stock < 10% of last month's sales)")
                lines.append("🟡 = Medium urgency (stock < 20% of last month's sales)")
            else:
                lines.append(f"Kul products jinhe order karna chahiye: {total_suggestions}")
                lines.append("")
                lines.append("🔴 = Bahut urgent (stock last month ki bikri ka 10% se kam)")
                lines.append("🟡 = Thoda urgent (stock last month ki bikri ka 20% se kam)")

            return nl.join(lines)

        elif action == 'set_low_stock_threshold':
            threshold = result.get('threshold', 0)
            unit = result.get('unit', 'pieces')

            if is_english:
                return (
                    f"✅ Low stock alert set for {product_name}!\r\n"
                    f"⚡ Alert will trigger when stock drops to or below {threshold} {unit}"
                )
            return (
                f"✅ {product_name} ke liye low stock alert set ho gaya!\r\n"
                f"⚡ Jab stock {threshold} {unit} ya usse kam hoga, alert milega"
            )

        elif action == 'predictive_alert':
            alerts = result.get('alerts', []) or []
            total_alerts = result.get('total_alerts', 0)
            analysis_period = result.get('analysis_period', '')
            days_analyzed = result.get('days_analyzed', 0)

            nl = "\r\n"

            if not alerts:
                if is_english:
                    return f"✅ No products are predicted to run out in the next 7 days. All stock levels look good!"
                return f"✅ Agle 7 din mein koi product khatam nahi hoga. Sab stock theek hai!"

            # Build header
            if is_english:
                header = f"🔮 Predictive Stock Alerts (based on {days_analyzed} days of sales):"
            else:
                header = f"🔮 Stock Prediction ({days_analyzed} din ki bikri ke hisaab se):"

            lines = [header, ""]

            for alert in alerts:
                name = alert.get('name', 'Product')
                brand = alert.get('brand') or ""
                current_stock = alert.get('current_stock', 0)
                unit = alert.get('unit', 'pieces')
                daily_rate = alert.get('daily_sales_rate', 0)
                days_left = alert.get('days_until_stockout', 0)
                stockout_date = alert.get('stockout_date', '')
                urgency = alert.get('urgency', 'medium')

                # Build display name
                if brand:
                    display_name = f"{brand} {name}"
                else:
                    display_name = name

                # Urgency emoji
                if urgency == 'critical':
                    urgency_emoji = "🔴"
                    urgency_text = "CRITICAL" if is_english else "BAHUT URGENT"
                elif urgency == 'high':
                    urgency_emoji = "🟠"
                    urgency_text = "HIGH" if is_english else "URGENT"
                else:
                    urgency_emoji = "🟡"
                    urgency_text = "MEDIUM" if is_english else "DHYAN DIJIYE"

                if is_english:
                    lines.append(f"{urgency_emoji} {display_name} [{urgency_text}]")
                    lines.append(f"   📊 Current stock: {current_stock} {unit}")
                    lines.append(f"   📈 Daily sales rate: {daily_rate} {unit}/day")
                    lines.append(f"   ⏰ Will run out in: {days_left} days")
                    lines.append(f"   📅 Predicted stockout: {stockout_date}")
                    lines.append(f"   🛒 Action: Reorder immediately!")
                    lines.append("")
                else:
                    lines.append(f"{urgency_emoji} {display_name} [{urgency_text}]")
                    lines.append(f"   📊 Abhi stock: {current_stock} {unit}")
                    lines.append(f"   📈 Roz bikta hai: {daily_rate} {unit}/din")
                    lines.append(f"   ⏰ Khatam hoga: {days_left} din mein")
                    lines.append(f"   📅 Khatam hone ki date: {stockout_date}")
                    lines.append(f"   🛒 Abhi order kar lijiye!")
                    lines.append("")

            if is_english:
                lines.append(f"Total products at risk: {total_alerts}")
                lines.append("")
                lines.append("🔴 = Critical (≤2 days)")
                lines.append("🟠 = High urgency (3-4 days)")
                lines.append("🟡 = Medium urgency (5-7 days)")
            else:
                lines.append(f"Kul products jinhe order karna hai: {total_alerts}")
                lines.append("")
                lines.append("🔴 = Bahut urgent (≤2 din)")
                lines.append("🟠 = Urgent (3-4 din)")
                lines.append("🟡 = Dhyan dijiye (5-7 din)")

            return nl.join(lines)

        elif action == 'seasonal_suggestion':
            festival_or_season = result.get('festival_or_season', 'general')
            top_products = result.get('top_products', []) or []
            total_products = result.get('total_products_analyzed', 0)
            festival_keywords = result.get('festival_keywords', []) or []
            current_month = result.get('current_month', 0)
            analysis_months = result.get('analysis_months', [])

            nl = "\r\n"

            if not top_products:
                if is_english:
                    return f"📊 No historical sales data available for {festival_or_season}. Start selling to build seasonal insights!"
                return f"📊 {festival_or_season} ke liye abhi tak koi sales data nahi hai. Bechna shuru kijiye!"

            # Build header with AI-powered insights
            month_names = {
                1: 'January', 2: 'February', 3: 'March', 4: 'April',
                5: 'May', 6: 'June', 7: 'July', 8: 'August',
                9: 'September', 10: 'October', 11: 'November', 12: 'December'
            }

            if is_english:
                header = f"🎉 Seasonal Analysis: {festival_or_season.upper()}"
                subheader = f"📊 AI-Powered Product Recommendations"
            else:
                header = f"🎉 {festival_or_season.upper()} ke liye Analysis"
                subheader = f"📊 AI se Product Suggestions"

            lines = [header, subheader, ""]

            # Add festival context
            if festival_keywords:
                if is_english:
                    lines.append(f"🔑 Popular categories: {', '.join(festival_keywords[:5])}")
                else:
                    lines.append(f"🔑 Popular categories: {', '.join(festival_keywords[:5])}")
                lines.append("")

            # Add top products with intelligent insights
            if is_english:
                lines.append("🏆 Top Products (Based on Historical Sales):")
            else:
                lines.append("🏆 Top Products (Pichle saal ki bikri ke hisaab se):")
            lines.append("")

            for idx, product in enumerate(top_products[:8], 1):  # Top 8 products
                name = product.get('product_name', 'Product')
                historical_sales = product.get('historical_sales', 0)
                avg_monthly = product.get('avg_monthly_sales', 0)
                current_stock = product.get('current_stock', 0)
                stock_status = product.get('stock_status', 'unknown')
                suggested_order = product.get('suggested_order', 0)

                # Status emoji
                if stock_status == 'sufficient':
                    status_emoji = "✅"
                    status_text_en = "Stock OK"
                    status_text_hi = "Stock theek hai"
                else:
                    status_emoji = "⚠️"
                    status_text_en = "Low Stock"
                    status_text_hi = "Stock kam hai"

                if is_english:
                    lines.append(f"{idx}. {status_emoji} {name}")
                    lines.append(f"   📈 Historical sales: {historical_sales:.0f} units")
                    lines.append(f"   📊 Current stock: {current_stock:.0f} units [{status_text_en}]")
                    if suggested_order > 0:
                        lines.append(f"   🛒 Suggested order: {suggested_order:.0f} units")
                    lines.append("")
                else:
                    lines.append(f"{idx}. {status_emoji} {name}")
                    lines.append(f"   📈 Pehle bika: {historical_sales:.0f} units")
                    lines.append(f"   📊 Abhi stock: {current_stock:.0f} units [{status_text_hi}]")
                    if suggested_order > 0:
                        lines.append(f"   🛒 Order karna chahiye: {suggested_order:.0f} units")
                    lines.append("")

            # Add AI insights
            if is_english:
                lines.append("💡 AI Insights:")
                lines.append(f"• Analyzed {total_products} products from past seasons")
                lines.append(f"• Recommendations based on {len(analysis_months)} month(s) of data")
                lines.append(f"• Stock up 50% more than average to avoid stockouts")
                lines.append("")
                lines.append("🎯 Action Items:")

                # Count products needing reorder
                low_stock_count = sum(1 for p in top_products if p.get('stock_status') == 'low')
                if low_stock_count > 0:
                    lines.append(f"• {low_stock_count} products need immediate reordering")
                else:
                    lines.append(f"• All top products have sufficient stock")

                lines.append(f"• Focus on {', '.join(festival_keywords[:3])} categories")
                lines.append(f"• Prepare inventory 2-3 weeks before {festival_or_season}")
            else:
                lines.append("💡 AI Insights:")
                lines.append(f"• {total_products} products ka analysis kiya gaya")
                lines.append(f"• {len(analysis_months)} mahine ke data se suggestions")
                lines.append(f"• Average se 50% zyada stock rakhiye")
                lines.append("")
                lines.append("🎯 Kya karna chahiye:")

                low_stock_count = sum(1 for p in top_products if p.get('stock_status') == 'low')
                if low_stock_count > 0:
                    lines.append(f"• {low_stock_count} products abhi order kar lijiye")
                else:
                    lines.append(f"• Sabhi top products ka stock theek hai")

                lines.append(f"• {', '.join(festival_keywords[:3])} categories pe dhyan dijiye")
                lines.append(f"• {festival_or_season} se 2-3 hafte pehle stock taiyar rakhiye")

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

