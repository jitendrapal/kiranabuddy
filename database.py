"""
Firebase Firestore database layer
"""
import os
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from google.cloud import firestore
from google.oauth2 import service_account
import uuid

from models import Shop, User, Product, Transaction, UserRole, TransactionType, UdharEntry

# Dummy Indian products catalog for barcode-based demo.
# In a real deployment you would load this from your own product master data.
DEMO_BARCODE_PRODUCTS: Dict[str, Dict[str, Any]] = {
    # Dal variants
    "8901000000001": {
        "name": "Tata Sampann Toor Dal 1kg",
        "brand": "Tata Sampann",
        "unit": "kg",
        "selling_price": 150.0,
    },
    "8901000000002": {
        "name": "Tata Sampann Moong Dal 1kg",
        "brand": "Tata Sampann",
        "unit": "kg",
        "selling_price": 140.0,
    },
    "8901000000003": {
        "name": "Tata Sampann Masoor Dal 1kg",
        "brand": "Tata Sampann",
        "unit": "kg",
        "selling_price": 130.0,
    },
    # Oil
    "8902000000001": {
        "name": "Fortune Sunlite Refined Sunflower Oil 1L",
        "brand": "Fortune",
        "unit": "litre",
        "selling_price": 190.0,
    },
    "8902000000002": {
        "name": "Fortune Kachi Ghani Mustard Oil 1L",
        "brand": "Fortune",
        "unit": "litre",
        "selling_price": 210.0,
    },
    # Atta
    "8903000000001": {
        "name": "Aashirvaad Atta 10kg",
        "brand": "Aashirvaad",
        "unit": "kg",
        "selling_price": 420.0,
    },
    # Biscuits
    "8904000000001": {
        "name": "Parle-G Biscuits 800g",
        "brand": "Parle",
        "unit": "gram",
        "selling_price": 60.0,
    },
    "8904000000002": {
        "name": "Britannia Good Day 600g",
        "brand": "Britannia",
        "unit": "gram",
        "selling_price": 70.0,
    },
}

# Map some common Hindi product names (Devanagari) to a canonical key
# so that "मैगी" and "Maggi" are treated as the same product.
HINDI_PRODUCT_CANONICAL = {
    "मैगी": "maggi",
    "मैग्गी": "maggi",
    "मेगी": "maggi",
}


def canonical_product_key(name: str) -> str:
    """Return a canonical normalized key for product lookup.

    This ensures different scripts/spellings (e.g. "मैगी", "Maggi")
    map to the same normalized_name such as "maggi".
    """
    base = (name or "").strip().lower()
    return HINDI_PRODUCT_CANONICAL.get(base, base)




class FirestoreDB:
    """Firestore database manager"""

    def __init__(self, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        """Initialize Firestore client"""
        print(f"🔥 FirestoreDB.__init__ called with:")
        print(f"   credentials_path: {credentials_path}")
        print(f"   project_id: {project_id}")

        # Option 1: Use credentials file if path exists
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            print(f"   Credentials loaded, project in file: {credentials.project_id}")
            self.db = firestore.Client(credentials=credentials, project=project_id)
            print(f"   Firestore client created for project: {self.db.project}")
        else:
            # Option 2: Try credentials from environment JSON (for Railway, etc.)
            creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
            if creds_json:
                try:
                    info = json.loads(creds_json)
                    credentials = service_account.Credentials.from_service_account_info(info)
                    effective_project = project_id or info.get("project_id")
                    print(f"   Loaded credentials from FIREBASE_CREDENTIALS_JSON, project: {effective_project}")
                    self.db = firestore.Client(credentials=credentials, project=effective_project)
                    print(f"   Firestore client created for project: {self.db.project}")
                    return
                except Exception as e:
                    print(f"   Error loading FIREBASE_CREDENTIALS_JSON: {e}")
                    # Fall through to default credentials
            # Option 3: Use default credentials (e.g., GOOGLE_APPLICATION_CREDENTIALS handled by SDK)
            print(f"   Using default credentials")
            self.db = firestore.Client(project=project_id)
            print(f"   Firestore client created for project: {self.db.project}")

    # ==================== SHOP OPERATIONS ====================

    def create_shop(self, name: str, owner_phone: str, address: Optional[str] = None) -> Shop:
        """Create a new shop"""
        shop_id = str(uuid.uuid4())
        shop = Shop(
            shop_id=shop_id,
            name=name,
            owner_phone=owner_phone,
            address=address,
            created_at=datetime.utcnow(),
            active=True
        )

        self.db.collection('shops').document(shop_id).set(shop.to_dict())
        return shop

    def get_shop(self, shop_id: str) -> Optional[Shop]:
        """Get shop by ID"""
        doc = self.db.collection('shops').document(shop_id).get()
        if doc.exists:
            return Shop.from_dict(doc.to_dict())
        return None

    def get_shop_by_phone(self, phone: str) -> Optional[Shop]:
        """Get shop by owner phone number"""
        docs = self.db.collection('shops').where('owner_phone', '==', phone).where('active', '==', True).limit(1).stream()
        for doc in docs:
            return Shop.from_dict(doc.to_dict())
        return None

    # ==================== USER OPERATIONS ====================

    def create_user(self, phone: str, name: str, shop_id: str, role: UserRole) -> User:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        user = User(
            user_id=user_id,
            phone=phone,
            name=name,
            shop_id=shop_id,
            role=role,
            created_at=datetime.utcnow(),
            active=True
        )

        self.db.collection('users').document(user_id).set(user.to_dict())
        return user

    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone number"""
        docs = self.db.collection('users').where('phone', '==', phone).where('active', '==', True).limit(1).stream()
        for doc in docs:
            return User.from_dict(doc.to_dict())
        return None

    def get_users_by_shop(self, shop_id: str) -> List[User]:
        """Get all users for a shop"""
        docs = self.db.collection('users').where('shop_id', '==', shop_id).where('active', '==', True).stream()
        return [User.from_dict(doc.to_dict()) for doc in docs]

    # ==================== PRODUCT OPERATIONS ====================

    def get_or_create_product(self, shop_id: str, product_name: str, unit: str = "pieces") -> Product:
        """Get existing product or create new one.

        If product_name looks like a known demo barcode, map it to a
        branded Indian product from DEMO_BARCODE_PRODUCTS so that
        scanner-based flows show proper names.

        Also normalize common Hindi-script names (e.g. "मैगी") so they
        resolve to the same product as their Latin-script equivalents
        ("Maggi").
        """
        # First build a canonical normalized key for lookups
        normalized_name = canonical_product_key(product_name)

        # 1) Try exact name match first (using canonical normalized_name)
        docs = (
            self.db.collection("products")
            .where("shop_id", "==", shop_id)
            .where("normalized_name", "==", normalized_name)
            .limit(1)
            .stream()
        )
        for doc in docs:
            return Product.from_dict(doc.to_dict())

        # 2) If input looks like a barcode AND we have it in our demo catalog,
        #    use the demo product definition (brand + proper name).
        barcode_candidate = normalized_name.replace(" ", "")
        if barcode_candidate.isdigit() and barcode_candidate in DEMO_BARCODE_PRODUCTS:
            info = DEMO_BARCODE_PRODUCTS[barcode_candidate]

            # See if we already created this barcode product for this shop
            for existing in self.get_products_by_shop(shop_id):
                if existing.barcode == barcode_candidate:
                    return existing

            canonical_name = info.get("name", product_name).strip()
            canonical_norm = canonical_product_key(canonical_name)
            unit_from_catalog = info.get("unit", unit)
            selling_price = info.get("selling_price")

            product_id = str(uuid.uuid4())
            product = Product(
                product_id=product_id,
                shop_id=shop_id,
                name=canonical_name,
                normalized_name=canonical_norm,
                current_stock=0.0,
                unit=unit_from_catalog,
                brand=info.get("brand"),
                barcode=barcode_candidate,
                selling_price=selling_price,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            self.db.collection("products").document(product_id).set(product.to_dict())
            return product

        # 3) Fallback: create a new product with the given name
        product_id = str(uuid.uuid4())
        product = Product(
            product_id=product_id,
            shop_id=shop_id,
            name=product_name,
            normalized_name=normalized_name,
            current_stock=0.0,
            unit=unit,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.db.collection("products").document(product_id).set(product.to_dict())
        return product

    def find_existing_product_by_name(self, shop_id: str, product_name: str) -> Optional[Product]:
        """Find an existing product for natural-language/Barcode commands.

        IMPORTANT: This function **never** creates a new product. It is used in
        the shopkeeper flows (text / voice / barcode) where we only want to
        update existing catalog items.

        It supports:
        - Exact normalized_name match for text names ("Maggi", "Tata Salt 1kg")
        - Barcode match when the input looks like a barcode (all digits)
        - Fuzzy token-overlap match for partial names, e.g.
          "Tata Sampann Toor Dal" -> "Tata Sampann Toor Dal 1kg"
        """
        if not product_name:
            return None

        normalized_name = canonical_product_key(product_name)

        # 0) If this looks like a barcode (all digits, typical length), try to
        #    match by barcode field first.
        stripped = normalized_name.replace(" ", "")
        if stripped.isdigit() and 8 <= len(stripped) <= 16:
            docs = (
                self.db.collection("products")
                .where("shop_id", "==", shop_id)
                .where("barcode", "==", stripped)
                .limit(1)
                .stream()
            )
            for doc in docs:
                return Product.from_dict(doc.to_dict())

        # 1) Exact normalized_name match for text-based names
        docs = (
            self.db.collection("products")
            .where("shop_id", "==", shop_id)
            .where("normalized_name", "==", normalized_name)
            .limit(1)
            .stream()
        )
        for doc in docs:
            return Product.from_dict(doc.to_dict())

        # 2) Fuzzy token-overlap match: handle cases like
        #    "add 10 Tata Sampann Toor Dal" vs stored "Tata Sampann Toor Dal 1kg".
        #
        # We aggressively clean the search text and product names to focus on
        # brand/product words and ignore quantities or verbs like "add"/
        # "sold" so that phrases like "add 10 parle g biscuits" match the
        # stored product "Parle-G Biscuits 200g".
        def _tokenize_for_match(text: str) -> set:
            if not text:
                return set()

            # Normalize case and break hyphenated names like "Parle-G" into
            # separate tokens "parle" and "g".
            s = text.lower().replace("-", " ")

            # Remove digits and +/- signs (quantities like "10", "+5", "-3").
            cleaned_chars = []
            for ch in s:
                if ch.isdigit() or ch in "+-":
                    cleaned_chars.append(" ")
                else:
                    cleaned_chars.append(ch)
            s = "".join(cleaned_chars)

            # Drop very generic words that are not part of the product name.
            stopwords = {
                "add",
                "added",
                "sold",
                "sale",
                "bought",
                "purchase",
                "customer",
                "new",
                "stock",
                "ne",
                "ko",
                "hai",
                "pieces",
                "piece",
                "packet",
                "packets",
                "kg",
                "g",
                "gm",
                "ml",
                "ltr",
                "l",
            }

            tokens = [t for t in s.split() if t and t not in stopwords]
            return set(tokens)

        target_tokens = _tokenize_for_match(normalized_name)
        if not target_tokens:
            return None

        best_product = None
        best_score = 0

        for p in self.get_products_by_shop(shop_id):
            name_norm = (p.normalized_name or "").strip().lower()
            if not name_norm:
                continue
            product_tokens = _tokenize_for_match(name_norm)
            if not product_tokens:
                continue

            common = target_tokens & product_tokens
            if not common:
                continue

            score = len(common)
            coverage = score / max(1, len(product_tokens))

            # For single-word searches (like "maggi"), be more lenient
            # For multi-word searches, require at least half the product tokens to match
            min_coverage = 0.3 if len(target_tokens) == 1 else 0.5

            if coverage < min_coverage:
                continue

            if score > best_score:
                best_score = score
                best_product = p

        return best_product


    def update_product_stock(self, product_id: str, new_stock: float) -> None:
        """Update product stock"""
        self.db.collection('products').document(product_id).update({
            'current_stock': new_stock,
            'updated_at': datetime.utcnow().isoformat()
        })
    def update_product_fields(self, product_id: str, updates: Dict[str, Any]) -> None:
        """Update arbitrary fields on a product document.

        This is a lightweight helper used by the stock management UI to edit
        things like barcode, simple expiry dates, or batch details.
        """
        if not updates:
            return

        # Always bump updated_at so changes are visible in Firestore history
        updates = dict(updates)
        updates["updated_at"] = datetime.utcnow().isoformat()
        self.db.collection("products").document(product_id).update(updates)

    def set_low_stock_threshold(self, shop_id: str, product_name: str, threshold: float) -> Dict[str, Any]:
        """Set the low stock threshold for a product.

        When stock drops to or below this threshold during sales, an alert will be triggered.
        """
        product = self.find_existing_product_by_name(shop_id, product_name)
        if not product:
            return {
                'success': False,
                'message': f"❌ Product '{product_name}' not found."
            }

        # Update the threshold
        self.update_product_fields(product.product_id, {'low_stock_threshold': threshold})

        return {
            'success': True,
            'product_name': product.name,
            'threshold': threshold,
            'unit': product.unit,
        }



    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        doc = self.db.collection('products').document(product_id).get()
        if doc.exists:
            return Product.from_dict(doc.to_dict())
        return None

    def get_products_by_shop(self, shop_id: str) -> List[Product]:
        """Get all products for a shop"""
        docs = self.db.collection('products').where('shop_id', '==', shop_id).stream()
        return [Product.from_dict(doc.to_dict()) for doc in docs]

    def get_products_summary(self, shop_id: str, keyword: Optional[str] = None) -> Dict[str, Any]:
        """Get summary of products and current stock for a shop.

        If `keyword` is provided (e.g. "dal"), only products whose name,
        brand or normalized_name contains that keyword (case-insensitive)
        are returned.
        """
        products = self.get_products_by_shop(shop_id)

        keyword_norm = (keyword or "").strip().lower() or None

        product_list = []
        for p in products:
            try:
                if keyword_norm:
                    name_norm = (p.name or "").lower()
                    brand_norm = (getattr(p, "brand", "") or "").lower()
                    normalized_name = (getattr(p, "normalized_name", "") or "").lower()
                    haystack = f"{name_norm} {brand_norm} {normalized_name}"
                    if keyword_norm not in haystack:
                        continue

                product_list.append(
                    {
                        "name": p.name,
                        "brand": getattr(p, "brand", None),
                        "stock": p.current_stock,
                        "unit": p.unit,
                        "price": getattr(p, "selling_price", None),
                    }
                )
            except Exception:
                # Be defensive; skip any bad records
                continue

        return {
            "success": True,
            "total_products": len(product_list),
            "products": product_list,
            "keyword": keyword_norm,
        }

    def get_low_stock_products(self, shop_id: str, threshold: Optional[float] = None) -> Dict[str, Any]:
        """Get products whose stock is at or below a threshold"""
        # Allow overriding threshold via env var, default to 5 units
        if threshold is None:
            try:
                threshold_env = os.getenv("LOW_STOCK_THRESHOLD")
                threshold = float(threshold_env) if threshold_env else 5.0
            except Exception:
                threshold = 5.0

        products = self.get_products_by_shop(shop_id)

        low_products = []
        for p in products:
            try:
                if p.current_stock is not None and p.current_stock <= threshold:
                    low_products.append({
                        'name': p.name,
                        'stock': p.current_stock,
                        'unit': p.unit,
                    })
            except Exception:
                # Be defensive; skip any bad records
                continue

        return {
            'success': True,
            'threshold': threshold,
            'low_products': low_products,
            'total_low_products': len(low_products),
        }





    # ==================== TRANSACTION OPERATIONS ====================

    def create_transaction(
        self,
        shop_id: str,
        product_id: str,
        product_name: str,
        transaction_type: TransactionType,
        quantity: float,
        previous_stock: float,
        new_stock: float,
        user_phone: str,
        unit_price: Optional[float] = None,
        total_amount: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> Transaction:
        """Create a new transaction record"""
        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            transaction_id=transaction_id,
            shop_id=shop_id,
            product_id=product_id,
            product_name=product_name,
            transaction_type=transaction_type,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            timestamp=datetime.utcnow(),
            unit_price=unit_price,
            total_amount=total_amount,
            notes=notes,
        )

        self.db.collection("transactions").document(transaction_id).set(transaction.to_dict())
        return transaction

    def get_transactions_by_shop(self, shop_id: str, limit: int = 100) -> List[Transaction]:
        """Get recent transactions for a shop"""
        docs = self.db.collection('transactions').where('shop_id', '==', shop_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        return [Transaction.from_dict(doc.to_dict()) for doc in docs]


    def undo_last_transaction_for_shop(self, shop_id: str, user_phone: str) -> Dict[str, Any]:
        """Undo the most recent inventory transaction for this shop.

        This resets the affected product's stock to the "previous_stock" value
        stored on that transaction and records an ADJUSTMENT entry.
        """
        # Get the last transaction for this shop
        tx_list = self.get_transactions_by_shop(shop_id, limit=1)
        if not tx_list:
            return {
                "success": False,
                "message": "❌ Koi previous entry nahi mili, undo nahi kar sakte.",
            }

        last_tx = tx_list[0]
        product = self.get_product(last_tx.product_id)
        if not product:
            return {
                "success": False,
                "message": "❌ Last entry ka product nahi mila, undo nahi kar sakte.",
            }

        # Revert stock back to the recorded previous_stock
        previous_stock = product.current_stock
        new_stock = last_tx.previous_stock
        self.update_product_stock(product.product_id, new_stock)

        # Record an adjustment transaction capturing the delta
        delta_effect = new_stock - previous_stock
        notes = f"Undo last transaction {last_tx.transaction_id} for {product.name}"
        adjustment = self.create_transaction(
            shop_id=shop_id,
            product_id=product.product_id,
            product_name=product.name,
            transaction_type=TransactionType.ADJUSTMENT,
            quantity=delta_effect,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            notes=notes,
        )

        return {
            "success": True,
            "product_name": product.name,
            "old_stock": previous_stock,
            "new_stock": new_stock,
            "unit": product.unit,
            "undone_transaction_id": last_tx.transaction_id,
            "adjustment_id": adjustment.transaction_id,
        }

    def get_transactions_by_product(self, product_id: str, limit: int = 50) -> List[Transaction]:
        """Get recent transactions for a product"""
        docs = self.db.collection('transactions').where('product_id', '==', product_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        return [Transaction.from_dict(doc.to_dict()) for doc in docs]

    # ==================== INVENTORY OPERATIONS ====================

    def add_stock(self, shop_id: str, product_name: str, quantity: float, user_phone: str) -> Dict[str, Any]:
        """Add stock to a product

        For now, price is not tracked on stock additions (only on sales), so
        we do not set unit_price/total_amount here.
        """
        product = self.get_or_create_product(shop_id, product_name)
        previous_stock = product.current_stock
        new_stock = previous_stock + quantity

        # Update product stock
        self.update_product_stock(product.product_id, new_stock)

        # Create transaction record
        self.create_transaction(
            shop_id=shop_id,
            product_id=product.product_id,
            product_name=product.name,
            transaction_type=TransactionType.ADD_STOCK,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            notes=f"Added {quantity} {product.unit}",
        )

        return {
            "success": True,
            "product_name": product.name,
            "quantity": quantity,
            "previous_stock": previous_stock,
            "new_stock": new_stock,
            "unit": product.unit,
        }

    def reduce_stock(self, shop_id: str, product_name: str, quantity: float, user_phone: str) -> Dict[str, Any]:
        """Reduce stock from a product (sale or consumption).

        We treat every reduce_stock as a sale and compute revenue using the
        product's selling_price if available.
        """
        product = self.get_or_create_product(shop_id, product_name)
        previous_stock = product.current_stock
        new_stock = max(0, previous_stock - quantity)  # Don't go negative

        # Determine price for this sale
        unit_price: Optional[float] = None
        total_amount: Optional[float] = None
        try:
            # 1) Use product.selling_price if already stored
            if getattr(product, "selling_price", None) is not None:
                unit_price = float(product.selling_price)
            else:
                # 2) Fallback for older barcode products: look up demo catalog
                barcode = getattr(product, "barcode", None)
                if barcode and barcode in DEMO_BARCODE_PRODUCTS:
                    demo_info = DEMO_BARCODE_PRODUCTS[barcode]
                    sp = demo_info.get("selling_price")
                    if sp is not None:
                        unit_price = float(sp)
                        # Persist selling_price back to product document for future
                        try:
                            self.db.collection("products").document(product.product_id).update(
                                {
                                    "selling_price": unit_price,
                                    "updated_at": datetime.utcnow().isoformat(),
                                }
                            )
                        except Exception:
                            # If we can't update price, still continue with this sale
                            pass

            if unit_price is not None:
                total_amount = unit_price * float(quantity)
        except Exception:
            # Be defensive; if anything goes wrong, fall back to None
            unit_price = None
            total_amount = None

        # Update product stock
        self.update_product_stock(product.product_id, new_stock)

        # Create transaction record
        self.create_transaction(
            shop_id=shop_id,
            product_id=product.product_id,
            product_name=product.name,
            transaction_type=TransactionType.REDUCE_STOCK,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            unit_price=unit_price,
            total_amount=total_amount,
            notes=f"Reduced {quantity} {product.unit}",
        )

        # Check for low stock alert
        low_stock_alert = None
        threshold = getattr(product, 'low_stock_threshold', None)

        # If no custom threshold, use default of 10
        if threshold is None:
            threshold = 10

        # Trigger alert if new stock drops below threshold
        if new_stock <= threshold and new_stock < previous_stock:
            low_stock_alert = {
                'triggered': True,
                'product_name': product.name,
                'brand': getattr(product, 'brand', None),
                'current_stock': new_stock,
                'threshold': threshold,
                'unit': product.unit,
            }

        return {
            "success": True,
            "product_name": product.name,
            "quantity": quantity,
            "previous_stock": previous_stock,
            "new_stock": new_stock,
            "unit": product.unit,
            "unit_price": unit_price,
            "total_amount": total_amount,
            "low_stock_alert": low_stock_alert,
        }
    def adjust_last_transaction(self, shop_id: str, product_name: str, correct_quantity: float,
                                user_phone: str) -> Dict[str, Any]:
        """Adjust the most recent transaction for a product to a new correct quantity.

        Assumes the last transaction for this product is the one to correct
        (e.g., user immediately fixes a mistake like "Maggi 3 nahi 1 the").
        """
        product = self.get_or_create_product(shop_id, product_name)

        # Find the most recent transaction for this product.
        # To avoid Firestore composite index requirements, we fetch all
        # transactions for this product_id and sort in Python by timestamp.
        trans_query = (
            self.db.collection('transactions')
            .where('product_id', '==', product.product_id)
        )

        last_trans = None
        for d in trans_query.stream():
            t = d.to_dict()
            ts = t.get('timestamp')
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                except Exception:
                    continue
            if not isinstance(ts, datetime):
                continue
            if last_trans is None or ts > last_trans[0]:
                last_trans = (ts, t)

        if not last_trans:
            return {
                'success': False,
                'message': f"❌ {product.name} ke liye koi previous entry nahi mili, adjust nahi kar sakte."
            }

        trans = last_trans[1]
        trans_type = trans.get('transaction_type')

        if trans_type not in ['add_stock', 'reduce_stock', 'sale']:
            return {
                'success': False,
                'message': f"❌ Last entry adjustment ke liye suitable nahi hai ({trans_type})."
            }

        original_qty = float(trans.get('quantity', 0) or 0)
        correct_quantity = float(correct_quantity)

        if original_qty == correct_quantity:
            return {
                'success': True,
                'product_name': product.name,
                'old_quantity': original_qty,
                'new_quantity': correct_quantity,
                'delta': 0.0,
                'unit': product.unit,
                'new_stock': product.current_stock,
                'message': "ℹ️ Entry already matches the correct quantity."
            }

        # Determine how this transaction affected stock
        if trans_type in ['add_stock', 'sale']:
            # Positive effect on stock
            delta_effect = correct_quantity - original_qty
        else:  # reduce_stock
            # Negative effect on stock
            delta_effect = original_qty - correct_quantity

        previous_stock = product.current_stock
        new_stock = max(0, previous_stock + delta_effect)

        # Update product stock
        self.update_product_stock(product.product_id, new_stock)

        # Record an adjustment transaction
        notes = f"Adjustment for {product.name}: {original_qty} -> {correct_quantity}"
        adjustment = self.create_transaction(
            shop_id=shop_id,
            product_id=product.product_id,
            product_name=product.name,
            transaction_type=TransactionType.ADJUSTMENT,
            quantity=delta_effect,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            notes=notes,
        )

        return {
            'success': True,
            'product_name': product.name,
            'old_quantity': original_qty,
            'new_quantity': correct_quantity,
            'delta': delta_effect,
            'unit': product.unit,
            'new_stock': new_stock,
            'adjustment_id': adjustment.transaction_id,
        }



    def check_stock(self, shop_id: str, product_name: str) -> Dict[str, Any]:
        """Check current stock for a product"""
        product = self.get_or_create_product(shop_id, product_name)

        return {
            'success': True,
            'product_name': product.name,
            'current_stock': product.current_stock,
            'unit': product.unit
        }

    def get_total_sales_today(self, shop_id: str) -> Dict[str, Any]:
        """Get total sales for today (items + revenue + cost + profit).

        We look at today's transactions and consider any transaction of type
        "reduce_stock" or "sale" as a sale event. If price information is
        available (unit_price/total_amount), we accumulate revenue. If
        `cost_price` is stored on the corresponding Product, we also
        approximate purchase cost and profit.
        """
        from datetime import datetime, timedelta

        # Get start of today (midnight)
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Build a cost map from products (so we can compute profit per sale)
        products = self.get_products_by_shop(shop_id)
        cost_by_id: Dict[str, float] = {}
        cost_by_name: Dict[str, float] = {}
        for p in products:
            try:
                cp = getattr(p, "cost_price", None)
                if cp is None:
                    continue
                cp_val = float(cp)
            except Exception:
                continue
            if getattr(p, "product_id", None):
                cost_by_id[p.product_id] = cp_val
            if getattr(p, "name", None):
                cost_by_name[p.name] = cp_val

        # Query transactions for today
        transactions_ref = self.db.collection("transactions").where("shop_id", "==", shop_id)

        # Filter by date and type
        all_transactions = transactions_ref.stream()

        total_items_sold = 0.0
        total_revenue = 0.0
        total_cost = 0.0
        products_sold: Dict[str, float] = {}
        revenue_by_product: Dict[str, float] = {}
        cost_by_product: Dict[str, float] = {}

        for trans_doc in all_transactions:
            trans = trans_doc.to_dict()

            # Check if transaction is from today
            trans_time = trans.get("timestamp")
            if trans_time:
                # Convert string timestamps back to datetime for comparison
                if isinstance(trans_time, str):
                    try:
                        trans_time = datetime.fromisoformat(trans_time)
                    except Exception:
                        # Skip records with bad timestamp format
                        continue

                if trans_time >= today_start:
                    # Check if it's a sale (reduce_stock)
                    if trans.get("transaction_type") in ("reduce_stock", "sale"):
                        quantity = float(trans.get("quantity", 0) or 0)
                        product_name = trans.get("product_name", "Unknown") or "Unknown"
                        product_id = trans.get("product_id")

                        total_items_sold += quantity
                        products_sold[product_name] = products_sold.get(product_name, 0.0) + quantity

                        # Revenue (if price is stored)
                        unit_price = trans.get("unit_price")
                        total_amount = trans.get("total_amount")

                        # Prefer stored total_amount; otherwise compute from unit_price
                        sale_amount = 0.0
                        try:
                            if total_amount is not None:
                                sale_amount = float(total_amount)
                            elif unit_price is not None:
                                sale_amount = float(unit_price) * quantity
                        except Exception:
                            sale_amount = 0.0

                        if sale_amount:
                            total_revenue += sale_amount
                            revenue_by_product[product_name] = revenue_by_product.get(product_name, 0.0) + sale_amount

                        # Approximate purchase cost using cost_price from Product
                        cost_unit = None
                        try:
                            if product_id and product_id in cost_by_id:
                                cost_unit = cost_by_id[product_id]
                            elif product_name in cost_by_name:
                                cost_unit = cost_by_name[product_name]
                        except Exception:
                            cost_unit = None

                        if cost_unit is not None:
                            try:
                                cost_amount = float(cost_unit) * quantity
                            except Exception:
                                cost_amount = 0.0
                            if cost_amount:
                                total_cost += cost_amount
                                cost_by_product[product_name] = cost_by_product.get(product_name, 0.0) + cost_amount

        total_profit = total_revenue - total_cost

        return {
            "success": True,
            "total_items_sold": total_items_sold,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "products_sold": products_sold,
            "revenue_by_product": {k: round(v, 2) for k, v in revenue_by_product.items()},
            "cost_by_product": {k: round(v, 2) for k, v in cost_by_product.items()},
            "date": today_start.strftime("%Y-%m-%d"),
        }


    def get_total_sales_current_month(self, shop_id: str) -> Dict[str, Any]:
        """Get total sales for the current calendar month (items + revenue + cost + profit).

        Similar to get_total_sales_today but includes all days from the first
        of the month up to now.
        """
        from datetime import datetime

        now = datetime.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Build a cost map from products (so we can compute profit per sale)
        products = self.get_products_by_shop(shop_id)
        cost_by_id: Dict[str, float] = {}
        cost_by_name: Dict[str, float] = {}
        for p in products:
            try:
                cp = getattr(p, "cost_price", None)
                if cp is None:
                    continue
                cp_val = float(cp)
            except Exception:
                continue
            if getattr(p, "product_id", None):
                cost_by_id[p.product_id] = cp_val
            if getattr(p, "name", None):
                cost_by_name[p.name] = cp_val

        transactions_ref = self.db.collection("transactions").where("shop_id", "==", shop_id)
        all_transactions = transactions_ref.stream()

        total_items_sold = 0.0
        total_revenue = 0.0
        total_cost = 0.0
        products_sold: Dict[str, float] = {}
        revenue_by_product: Dict[str, float] = {}
        cost_by_product: Dict[str, float] = {}

        for trans_doc in all_transactions:
            trans = trans_doc.to_dict()
            trans_time = trans.get("timestamp")
            if not trans_time:
                continue

            # Convert string timestamps back to datetime for comparison
            if isinstance(trans_time, str):
                try:
                    trans_time = datetime.fromisoformat(trans_time)
                except Exception:
                    # Skip records with bad timestamp format
                    continue

            # Only include transactions within the current month window
            if not (month_start <= trans_time <= now):
                continue

            if trans.get("transaction_type") in ("reduce_stock", "sale"):
                quantity = float(trans.get("quantity", 0) or 0)
                product_name = trans.get("product_name", "Unknown") or "Unknown"
                product_id = trans.get("product_id")

                total_items_sold += quantity
                products_sold[product_name] = products_sold.get(product_name, 0.0) + quantity

                unit_price = trans.get("unit_price")
                total_amount = trans.get("total_amount")

                sale_amount = 0.0
                try:
                    if total_amount is not None:
                        sale_amount = float(total_amount)
                    elif unit_price is not None:
                        sale_amount = float(unit_price) * quantity
                except Exception:
                    sale_amount = 0.0

                if sale_amount:
                    total_revenue += sale_amount
                    revenue_by_product[product_name] = revenue_by_product.get(product_name, 0.0) + sale_amount

                # Approximate purchase cost using cost_price from Product
                cost_unit = None
                try:
                    if product_id and product_id in cost_by_id:
                        cost_unit = cost_by_id[product_id]
                    elif product_name in cost_by_name:
                        cost_unit = cost_by_name[product_name]
                except Exception:
                    cost_unit = None

                if cost_unit is not None:
                    try:
                        cost_amount = float(cost_unit) * quantity
                    except Exception:
                        cost_amount = 0.0
                    if cost_amount:
                        total_cost += cost_amount
                        cost_by_product[product_name] = cost_by_product.get(product_name, 0.0) + cost_amount

        total_profit = total_revenue - total_cost

        return {
            "success": True,
            "total_items_sold": total_items_sold,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "products_sold": products_sold,
            "revenue_by_product": {k: round(v, 2) for k, v in revenue_by_product.items()},
            "cost_by_product": {k: round(v, 2) for k, v in cost_by_product.items()},
            "month": now.strftime("%B %Y"),
        }


    def get_total_sales_current_week(self, shop_id: str) -> Dict[str, Any]:
        """Get total sales for the current week (items + revenue + cost + profit).

        Week starts on Monday and includes all days from Monday to now.
        """
        from datetime import datetime, timedelta

        now = datetime.now()
        # Calculate the start of the current week (Monday)
        days_since_monday = now.weekday()  # Monday is 0, Sunday is 6
        week_start = now - timedelta(days=days_since_monday)
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

        # Build a cost map from products (so we can compute profit per sale)
        products = self.get_products_by_shop(shop_id)
        cost_by_id: Dict[str, float] = {}
        cost_by_name: Dict[str, float] = {}
        for p in products:
            try:
                cp = getattr(p, "cost_price", None)
                if cp is None:
                    continue
                cp_val = float(cp)
            except Exception:
                continue
            if getattr(p, "product_id", None):
                cost_by_id[p.product_id] = cp_val
            if getattr(p, "name", None):
                cost_by_name[p.name] = cp_val

        transactions_ref = self.db.collection("transactions").where("shop_id", "==", shop_id)
        all_transactions = transactions_ref.stream()

        total_items_sold = 0.0
        total_revenue = 0.0
        total_cost = 0.0
        products_sold: Dict[str, float] = {}
        revenue_by_product: Dict[str, float] = {}
        cost_by_product: Dict[str, float] = {}

        for trans_doc in all_transactions:
            trans = trans_doc.to_dict()
            trans_time = trans.get("timestamp")
            if not trans_time:
                continue

            # Convert string timestamps back to datetime for comparison
            if isinstance(trans_time, str):
                try:
                    trans_time = datetime.fromisoformat(trans_time)
                except Exception:
                    # Skip records with bad timestamp format
                    continue

            # Only include transactions within the current week window
            if not (week_start <= trans_time <= now):
                continue

            if trans.get("transaction_type") in ("reduce_stock", "sale"):
                quantity = float(trans.get("quantity", 0) or 0)
                product_name = trans.get("product_name", "Unknown") or "Unknown"
                product_id = trans.get("product_id")

                total_items_sold += quantity
                products_sold[product_name] = products_sold.get(product_name, 0.0) + quantity

                unit_price = trans.get("unit_price")
                total_amount = trans.get("total_amount")

                sale_amount = 0.0
                try:
                    if total_amount is not None:
                        sale_amount = float(total_amount)
                    elif unit_price is not None:
                        sale_amount = float(unit_price) * quantity
                except Exception:
                    sale_amount = 0.0

                if sale_amount:
                    total_revenue += sale_amount
                    revenue_by_product[product_name] = revenue_by_product.get(product_name, 0.0) + sale_amount

                # Approximate purchase cost using cost_price from Product
                cost_unit = None
                try:
                    if product_id and product_id in cost_by_id:
                        cost_unit = cost_by_id[product_id]
                    elif product_name in cost_by_name:
                        cost_unit = cost_by_name[product_name]
                except Exception:
                    cost_unit = None

                if cost_unit is not None:
                    try:
                        cost_amount = float(cost_unit) * quantity
                    except Exception:
                        cost_amount = 0.0
                    if cost_amount:
                        total_cost += cost_amount
                        cost_by_product[product_name] = cost_by_product.get(product_name, 0.0) + cost_amount

        total_profit = total_revenue - total_cost

        # Format week label (e.g., "Week of Nov 18, 2025")
        week_label = f"Week of {week_start.strftime('%b %d, %Y')}"

        return {
            "success": True,
            "total_items_sold": total_items_sold,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "products_sold": products_sold,
            "revenue_by_product": {k: round(v, 2) for k, v in revenue_by_product.items()},
            "cost_by_product": {k: round(v, 2) for k, v in cost_by_product.items()},
            "week": week_label,
        }


    def get_total_sales_current_year(self, shop_id: str) -> Dict[str, Any]:
        """Get total sales for the current calendar year (items + revenue + cost + profit).

        Similar to get_total_sales_current_month but includes all days from January 1st
        of the current year up to now.
        """
        from datetime import datetime

        now = datetime.now()
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        # Build a cost map from products (so we can compute profit per sale)
        products = self.get_products_by_shop(shop_id)
        cost_by_id: Dict[str, float] = {}
        cost_by_name: Dict[str, float] = {}
        for p in products:
            try:
                cp = getattr(p, "cost_price", None)
                if cp is None:
                    continue
                cp_val = float(cp)
            except Exception:
                continue
            if getattr(p, "product_id", None):
                cost_by_id[p.product_id] = cp_val
            if getattr(p, "name", None):
                cost_by_name[p.name] = cp_val

        transactions_ref = self.db.collection("transactions").where("shop_id", "==", shop_id)
        all_transactions = transactions_ref.stream()

        total_items_sold = 0.0
        total_revenue = 0.0
        total_cost = 0.0
        products_sold: Dict[str, float] = {}
        revenue_by_product: Dict[str, float] = {}
        cost_by_product: Dict[str, float] = {}

        for trans_doc in all_transactions:
            trans = trans_doc.to_dict()
            trans_time = trans.get("timestamp")
            if not trans_time:
                continue

            # Convert string timestamps back to datetime for comparison
            if isinstance(trans_time, str):
                try:
                    trans_time = datetime.fromisoformat(trans_time)
                except Exception:
                    # Skip records with bad timestamp format
                    continue

            # Only include transactions within the current year window
            if not (year_start <= trans_time <= now):
                continue

            if trans.get("transaction_type") in ("reduce_stock", "sale"):
                quantity = float(trans.get("quantity", 0) or 0)
                product_name = trans.get("product_name", "Unknown") or "Unknown"
                product_id = trans.get("product_id")

                total_items_sold += quantity
                products_sold[product_name] = products_sold.get(product_name, 0.0) + quantity

                unit_price = trans.get("unit_price")
                total_amount = trans.get("total_amount")

                sale_amount = 0.0
                try:
                    if total_amount is not None:
                        sale_amount = float(total_amount)
                    elif unit_price is not None:
                        sale_amount = float(unit_price) * quantity
                except Exception:
                    sale_amount = 0.0

                if sale_amount:
                    total_revenue += sale_amount
                    revenue_by_product[product_name] = revenue_by_product.get(product_name, 0.0) + sale_amount

                # Approximate purchase cost using cost_price from Product
                cost_unit = None
                try:
                    if product_id and product_id in cost_by_id:
                        cost_unit = cost_by_id[product_id]
                    elif product_name in cost_by_name:
                        cost_unit = cost_by_name[product_name]
                except Exception:
                    cost_unit = None

                if cost_unit is not None:
                    try:
                        cost_amount = float(cost_unit) * quantity
                    except Exception:
                        cost_amount = 0.0
                    if cost_amount:
                        total_cost += cost_amount
                        cost_by_product[product_name] = cost_by_product.get(product_name, 0.0) + cost_amount

        total_profit = total_revenue - total_cost

        return {
            "success": True,
            "total_items_sold": total_items_sold,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "products_sold": products_sold,
            "revenue_by_product": {k: round(v, 2) for k, v in revenue_by_product.items()},
            "cost_by_product": {k: round(v, 2) for k, v in cost_by_product.items()},
            "year": now.strftime("%Y"),
        }


    def get_total_sales_for_period(self, shop_id: str, start_datetime, end_datetime) -> Dict[str, Any]:
        """Get total sales for an arbitrary period (items + revenue + cost + profit).

        The period is inclusive of both start_datetime and end_datetime.
        This is used for flexible "hisaab" / report queries like
        "aaj ka hisaab", monthly reports, yearly reports, etc.
        """
        from datetime import datetime

        if not start_datetime or not end_datetime:
            return {
                "success": False,
                "message": "❌ Report period samajh nahi aaya.",
            }

        # Normalise ordering just in case
        if start_datetime > end_datetime:
            start_datetime, end_datetime = end_datetime, start_datetime

        # Build a cost map from products (so we can compute profit per sale)
        products = self.get_products_by_shop(shop_id)
        cost_by_id: Dict[str, float] = {}
        cost_by_name: Dict[str, float] = {}
        for p in products:
            try:
                cp = getattr(p, "cost_price", None)
                if cp is None:
                    continue
                cp_val = float(cp)
            except Exception:
                continue
            if getattr(p, "product_id", None):
                cost_by_id[p.product_id] = cp_val
            if getattr(p, "name", None):
                cost_by_name[p.name] = cp_val

        transactions_ref = self.db.collection("transactions").where("shop_id", "==", shop_id)
        all_transactions = transactions_ref.stream()

        total_items_sold = 0.0
        total_revenue = 0.0
        total_cost = 0.0
        products_sold: Dict[str, float] = {}
        revenue_by_product: Dict[str, float] = {}
        cost_by_product: Dict[str, float] = {}

        for trans_doc in all_transactions:
            trans = trans_doc.to_dict()
            trans_time = trans.get("timestamp")
            if not trans_time:
                continue

            # Convert string timestamps back to datetime for comparison
            if isinstance(trans_time, str):
                try:
                    trans_time = datetime.fromisoformat(trans_time)
                except Exception:
                    # Skip records with bad timestamp format
                    continue

            if not (start_datetime <= trans_time <= end_datetime):
                continue

            if trans.get("transaction_type") in ("reduce_stock", "sale"):
                quantity = float(trans.get("quantity", 0) or 0)
                product_name = trans.get("product_name", "Unknown") or "Unknown"
                product_id = trans.get("product_id")

                total_items_sold += quantity
                products_sold[product_name] = products_sold.get(product_name, 0.0) + quantity

                unit_price = trans.get("unit_price")
                total_amount = trans.get("total_amount")

                sale_amount = 0.0
                try:
                    if total_amount is not None:
                        sale_amount = float(total_amount)
                    elif unit_price is not None:
                        sale_amount = float(unit_price) * quantity
                except Exception:
                    sale_amount = 0.0

                if sale_amount:
                    total_revenue += sale_amount
                    revenue_by_product[product_name] = revenue_by_product.get(product_name, 0.0) + sale_amount

                # Approximate purchase cost using cost_price from Product
                cost_unit = None
                try:
                    if product_id and product_id in cost_by_id:
                        cost_unit = cost_by_id[product_id]
                    elif product_name in cost_by_name:
                        cost_unit = cost_by_name[product_name]
                except Exception:
                    cost_unit = None

                if cost_unit is not None:
                    try:
                        cost_amount = float(cost_unit) * quantity
                    except Exception:
                        cost_amount = 0.0
                    if cost_amount:
                        total_cost += cost_amount
                        cost_by_product[product_name] = cost_by_product.get(product_name, 0.0) + cost_amount

        total_profit = total_revenue - total_cost

        return {
            "success": True,
            "total_items_sold": total_items_sold,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "products_sold": products_sold,
            "revenue_by_product": {k: round(v, 2) for k, v in revenue_by_product.items()},
            "cost_by_product": {k: round(v, 2) for k, v in cost_by_product.items()},
        }



    def get_zero_sale_products_today(self, shop_id: str) -> Dict[str, Any]:
        """Get **top 3** products that had zero sales today (but are in stock).

        We still compute the full zero-sale list, but only return up to
        the "top 3" items (by current stock) to keep the WhatsApp reply
        short and useful.
        """
        # First fetch today's sales summary
        sales_data = self.get_total_sales_today(shop_id)
        if not sales_data.get("success"):
            return sales_data

        products_sold = sales_data.get("products_sold", {}) or {}

        # Then get all products for the shop
        products = self.get_products_by_shop(shop_id)

        zero_sale_products: List[Dict[str, Any]] = []
        for p in products:
            # Only consider products that still have some stock and had no sales today
            if p.current_stock > 0 and p.name not in products_sold:
                zero_sale_products.append(
                    {
                        "name": p.name,
                        "stock": p.current_stock,
                        "unit": p.unit,
                    }
                )

        # Sort by current stock (descending = most stock left unsold first)
        zero_sale_products_sorted = sorted(
            zero_sale_products,
            key=lambda item: float(item.get("stock", 0) or 0),
            reverse=True,
        )

        # Only keep top 3 items for the response, but keep total count
        top_three = zero_sale_products_sorted[:3]

        return {
            "success": True,
            "zero_sale_products": top_three,
            "total_zero_sale_products": len(zero_sale_products_sorted),
            "date": sales_data.get("date"),
        }

    def get_predictive_alerts(self, shop_id: str) -> Dict[str, Any]:
        """Get predictive alerts for products that will run out soon.

        Analyzes current month's sales velocity to predict when products will run out.
        Formula: days_until_stockout = current_stock / daily_sales_rate

        Returns products that will run out in the next 7 days.
        """
        from datetime import datetime, timedelta

        now = datetime.now()
        # Get current month's start date
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate days elapsed in current month
        days_elapsed = (now - month_start).days + 1  # +1 to include today

        # Get all products for this shop
        products = self.get_products_by_shop(shop_id)

        # Get current month's sales data
        current_month_sales = self.get_total_sales_current_month(shop_id=shop_id)
        products_sold_this_month = current_month_sales.get('products_sold', {}) or {}

        alerts = []

        for product in products:
            product_name = product.name
            current_stock = product.current_stock or 0
            unit = product.unit or 'pieces'
            brand = product.brand

            # Get this month's sales for this product
            month_sales_qty = products_sold_this_month.get(product_name, 0)

            # Skip products with no sales this month or no stock
            if month_sales_qty <= 0 or current_stock <= 0:
                continue

            # Calculate daily sales rate (average per day)
            daily_sales_rate = month_sales_qty / days_elapsed

            # Skip if daily sales rate is too low (less than 0.1 per day)
            if daily_sales_rate < 0.1:
                continue

            # Predict days until stockout
            days_until_stockout = current_stock / daily_sales_rate

            # Alert if product will run out in next 7 days
            if days_until_stockout <= 7:
                # Calculate the predicted date
                stockout_date = now + timedelta(days=int(days_until_stockout))

                # Determine urgency level
                if days_until_stockout <= 2:
                    urgency = 'critical'  # 🔴 Red - 2 days or less
                elif days_until_stockout <= 4:
                    urgency = 'high'      # 🟠 Orange - 3-4 days
                else:
                    urgency = 'medium'    # 🟡 Yellow - 5-7 days

                alerts.append({
                    'name': product_name,
                    'brand': brand,
                    'current_stock': current_stock,
                    'unit': unit,
                    'daily_sales_rate': round(daily_sales_rate, 2),
                    'days_until_stockout': round(days_until_stockout, 1),
                    'stockout_date': stockout_date.strftime('%Y-%m-%d'),
                    'month_sales': month_sales_qty,
                    'days_elapsed': days_elapsed,
                    'urgency': urgency
                })

        # Sort by days_until_stockout (most urgent first)
        alerts.sort(key=lambda x: x['days_until_stockout'])

        return {
            'success': True,
            'alerts': alerts,
            'total_alerts': len(alerts),
            'analysis_period': f"{month_start.strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}",
            'days_analyzed': days_elapsed,
        }


    def get_purchase_suggestions(self, shop_id: str) -> Dict[str, Any]:
        """Get purchase suggestions based on sales patterns.

        Analyzes last month's sales and current stock to suggest products
        that need to be reordered.

        Logic:
        - Compare current stock with last month's sales
        - If current stock < 20% of last month's sales, suggest reorder
        - Show products sorted by urgency (lowest stock ratio first)
        """
        from datetime import datetime, timedelta

        now = datetime.now()
        # Get last month's date range
        last_month_end = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Get all products for this shop
        products = self.get_products_by_shop(shop_id)

        # Get last month's sales data
        last_month_sales = self.get_total_sales_for_period(
            shop_id=shop_id,
            start_datetime=last_month_start,
            end_datetime=last_month_end
        )

        products_sold_last_month = last_month_sales.get('products_sold', {}) or {}

        suggestions = []

        for product in products:
            product_name = product.name
            current_stock = product.current_stock or 0
            unit = product.unit or 'pieces'
            brand = product.brand

            # Get last month's sales for this product
            last_month_qty = products_sold_last_month.get(product_name, 0)

            # Skip products with no sales last month
            if last_month_qty <= 0:
                continue

            # Calculate stock ratio (current stock / last month sales)
            stock_ratio = current_stock / last_month_qty if last_month_qty > 0 else 1.0

            # Suggest reorder if current stock is less than 20% of last month's sales
            # This means if you sold 100 last month and have only 20 left, suggest reorder
            if stock_ratio < 0.2:
                # Calculate suggested order quantity (to match last month's sales)
                suggested_qty = max(0, last_month_qty - current_stock)

                suggestions.append({
                    'name': product_name,
                    'brand': brand,
                    'current_stock': current_stock,
                    'unit': unit,
                    'last_month_sales': last_month_qty,
                    'suggested_order_qty': suggested_qty,
                    'stock_ratio': stock_ratio,
                    'urgency': 'high' if stock_ratio < 0.1 else 'medium'
                })

        # Sort by stock ratio (most urgent first)
        suggestions.sort(key=lambda x: x['stock_ratio'])

        return {
            'success': True,
            'suggestions': suggestions,
            'total_suggestions': len(suggestions),
            'last_month_start': last_month_start.strftime('%Y-%m-%d'),
            'last_month_end': last_month_end.strftime('%Y-%m-%d'),
        }

    def get_seasonal_analysis(self, shop_id: str, season_or_festival: Optional[str] = None) -> Dict[str, Any]:
        """Get seasonal sales analysis and product suggestions.

        Analyzes historical sales data to identify:
        1. Top-selling products during specific festivals/seasons
        2. Sales trends for different time periods
        3. Product recommendations for upcoming festivals

        Args:
            shop_id: Shop ID
            season_or_festival: Optional specific festival/season (e.g., 'diwali', 'holi', 'summer')

        Returns:
            Dictionary with seasonal analysis and product suggestions
        """
        try:
            print(f"🎉 get_seasonal_analysis called: shop_id={shop_id}, season_or_festival={season_or_festival}")
            from datetime import datetime, timedelta
            from collections import defaultdict

            now = datetime.now()
            current_year = now.year
            current_month = now.month

            # Define festival/season periods (approximate dates)
            festivals = {
                'diwali': {
                    'months': [10, 11],  # October-November
                    'keywords': ['sweets', 'mithai', 'dry fruits', 'oil', 'ghee', 'crackers', 'diyas', 'decorations']
                },
                'holi': {
                    'months': [3],  # March
                    'keywords': ['colors', 'sweets', 'gujiya', 'thandai', 'snacks', 'namkeen']
                },
                'raksha bandhan': {
                    'months': [8],  # August
                    'keywords': ['sweets', 'mithai', 'dry fruits', 'chocolates', 'gifts']
                },
                'eid': {
                    'months': [4, 5],  # April-May (varies)
                    'keywords': ['dates', 'dry fruits', 'sweets', 'seviyan', 'biryani', 'meat']
                },
                'christmas': {
                    'months': [12],  # December
                    'keywords': ['cake', 'chocolates', 'dry fruits', 'wine', 'decorations']
                },
                'new year': {
                    'months': [1, 12],  # December-January
                    'keywords': ['snacks', 'drinks', 'party', 'decorations']
                },
                'summer': {
                    'months': [4, 5, 6],  # April-June
                    'keywords': ['cold drinks', 'ice cream', 'juice', 'water', 'coolers', 'aam panna']
                },
                'winter': {
                    'months': [11, 12, 1, 2],  # November-February
                    'keywords': ['tea', 'coffee', 'hot chocolate', 'dry fruits', 'gur', 'til']
                },
                'monsoon': {
                    'months': [7, 8, 9],  # July-September
                    'keywords': ['tea', 'pakora', 'snacks', 'umbrella', 'raincoat']
                }
            }

            # Get all transactions for the shop (last 2 years for better analysis)
            two_years_ago = now - timedelta(days=730)

            # Get all products
            products = self.get_products_by_shop(shop_id)
            product_map = {p.product_id: p for p in products}

            # Get transactions from last 2 years
            # Note: We only filter by shop_id to avoid needing a composite index
            # We'll filter by timestamp in Python
            transactions_ref = (self.db.collection('transactions')
                               .where('shop_id', '==', shop_id)
                               .stream())

            # Analyze sales by month and product
            monthly_sales = defaultdict(lambda: defaultdict(float))  # {month: {product_name: quantity}}
            product_sales_history = defaultdict(list)  # {product_name: [(month, quantity)]}

            for txn_doc in transactions_ref:
                txn_data = txn_doc.to_dict()
                txn_type = txn_data.get('type')

                # Only analyze sales transactions
                if txn_type != 'sale':
                    continue

                timestamp = txn_data.get('timestamp')
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

                # Filter by timestamp in Python (to avoid needing Firestore index)
                if timestamp < two_years_ago:
                    continue

                month = timestamp.month
                product_id = txn_data.get('product_id')
                quantity = abs(txn_data.get('quantity', 0))

                if product_id in product_map:
                    product_name = product_map[product_id].name
                    monthly_sales[month][product_name] += quantity
                    product_sales_history[product_name].append((month, quantity))

            # Determine which festival/season to analyze
            target_festival = None
            target_months = []

            if season_or_festival:
                # User specified a festival/season
                season_lower = season_or_festival.lower()
                for fest_name, fest_data in festivals.items():
                    if fest_name in season_lower or season_lower in fest_name:
                        target_festival = fest_name
                        target_months = fest_data['months']
                        break

            if not target_festival:
                # Auto-detect upcoming festival based on current month
                for fest_name, fest_data in festivals.items():
                    if current_month in fest_data['months']:
                        target_festival = fest_name
                        target_months = fest_data['months']
                        break

                # If no current festival, find next upcoming one
                if not target_festival:
                    next_month = (current_month % 12) + 1
                    for fest_name, fest_data in festivals.items():
                        if next_month in fest_data['months']:
                            target_festival = fest_name
                            target_months = fest_data['months']
                            break

            # Calculate top products for target months
            seasonal_products = defaultdict(float)
            for month in target_months:
                for product_name, quantity in monthly_sales[month].items():
                    seasonal_products[product_name] += quantity

            # Sort products by sales volume
            top_seasonal_products = sorted(
                seasonal_products.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10 products

            # Build suggestions
            suggestions = []
            for product_name, total_qty in top_seasonal_products:
                # Find the product in current inventory
                current_product = None
                for p in products:
                    if p.name == product_name:
                        current_product = p
                        break

                current_stock = current_product.current_stock if current_product else 0
                avg_seasonal_sales = total_qty / len(target_months) if target_months else total_qty

                suggestions.append({
                    'product_name': product_name,
                    'historical_sales': total_qty,
                    'avg_monthly_sales': round(avg_seasonal_sales, 2),
                    'current_stock': current_stock,
                    'stock_status': 'sufficient' if current_stock >= avg_seasonal_sales else 'low',
                    'suggested_order': max(0, round(avg_seasonal_sales * 1.5 - current_stock, 2))
                })

            print(f"✅ Seasonal analysis complete: {len(suggestions)} products found")
            return {
                'success': True,
                'festival_or_season': target_festival or 'general',
                'analysis_months': target_months,
                'current_month': current_month,
                'top_products': suggestions,
                'total_products_analyzed': len(suggestions),
                'festival_keywords': festivals.get(target_festival, {}).get('keywords', []) if target_festival else [],
                'message': f"Seasonal analysis for {target_festival or 'current period'}"
            }
        except Exception as e:
            print(f"❌ Error in get_seasonal_analysis: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error analyzing seasonal data: {str(e)}'
            }

    def get_expiry_products(self, shop_id: str, days: int = 30) -> Dict[str, Any]:
        """Get products that are expired or expiring within the next `days` days.

        Supports two schemas on the Product document:
        1) Simple per-product expiry (legacy):
           - `expiry_date`: string or timestamp for the whole product.
        2) Per-batch expiry (recommended):
           - `batches`: {
           -   "batch_001": {"expiry": "2025-02-10", "qty": 12},
           -   "batch_002": {"expiry": "2025-03-15", "qty": 10},
           - }

        We then split into:
        - `expired_products`: expiry date < today
        - `expiring_products`: today <= expiry date <= today + days
        """
        # Allow overriding the window via environment if needed
        window_days = days
        try:
            env_days = os.getenv("EXPIRY_ALERT_DAYS")
            if env_days is not None:
                window_days = int(env_days)
        except Exception:
            window_days = days

        today = datetime.utcnow().date()
        cutoff = today + timedelta(days=window_days)

        products = self.get_products_by_shop(shop_id)
        expired: List[Dict[str, Any]] = []
        expiring: List[Dict[str, Any]] = []

        for p in products:
            # Prefer per-batch expiry if available, but only skip the legacy
            # per-product path if we actually manage to read at least one
            # usable batch expiry.
            any_batch_handled = False
            batches_obj = getattr(p, "batches", None)

            if isinstance(batches_obj, dict) and batches_obj:
                for batch_id, batch_data in batches_obj.items():
                    try:
                        batch = batch_data or {}
                        expiry_raw = batch.get("expiry") or batch.get("expiry_date")
                        if not expiry_raw:
                            continue

                        exp_date = None
                        if isinstance(expiry_raw, datetime):
                            exp_date = expiry_raw.date()
                        elif isinstance(expiry_raw, str):
                            text = expiry_raw.strip()
                            # First try flexible ISO-style parsing (handles
                            # "2025-12-31" and "2025-12-31T00:00:00" etc.).
                            try:
                                exp_date = datetime.fromisoformat(text).date()
                            except Exception:
                                # Fall back to a few common day/month/year styles.
                                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
                                    try:
                                        exp_date = datetime.strptime(text, fmt).date()
                                        break
                                    except Exception:
                                        continue

                        if not exp_date:
                            continue

                        qty_raw = batch.get("qty") or batch.get("quantity")
                        try:
                            stock_val = float(qty_raw) if qty_raw is not None else p.current_stock
                        except Exception:
                            stock_val = p.current_stock

                        info = {
                            "name": p.name,
                            "brand": getattr(p, "brand", None),
                            "stock": stock_val,
                            "unit": p.unit,
                            "expiry_date": exp_date.isoformat(),
                            "batch_id": batch_id,
                        }

                        if exp_date < today:
                            expired.append(info)
                        elif today <= exp_date <= cutoff:
                            expiring.append(info)

                        any_batch_handled = True
                    except Exception:
                        # Be defensive: a bad batch should not break the whole report
                        continue

                # If we successfully handled at least one batch expiry, skip the
                # legacy per-product expiry for this product to avoid double
                # counting. If no batch expiries were usable (e.g. bad formats),
                # fall through to the legacy path below.
                if any_batch_handled:
                    continue

            # Legacy/simple per-product expiry path
            expiry_raw = getattr(p, "expiry_date", None)
            if not expiry_raw:
                continue

            exp_date = None
            # Handle Firestore timestamp or datetime
            if isinstance(expiry_raw, datetime):
                exp_date = expiry_raw.date()
            elif isinstance(expiry_raw, str):
                text = expiry_raw.strip()
                # Try a few common formats
                for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
                    try:
                        exp_date = datetime.strptime(text, fmt).date()
                        break
                    except Exception:
                        continue

            if not exp_date:
                # Skip if we cannot parse the date safely
                continue

            info = {
                "name": p.name,
                "brand": getattr(p, "brand", None),
                "stock": p.current_stock,
                "unit": p.unit,
                "expiry_date": exp_date.isoformat(),
            }

            if exp_date < today:
                expired.append(info)
            elif today <= exp_date <= cutoff:
                expiring.append(info)

        # Sort by date (nearest first), then by name for stability
        expiring_sorted = sorted(expiring, key=lambda item: (item["expiry_date"], item["name"]))
        expired_sorted = sorted(expired, key=lambda item: (item["expiry_date"], item["name"]))

        return {
            "success": True,
            "expired_products": expired_sorted,
            "expiring_products": expiring_sorted,
            "days_ahead": window_days,
            "today": today.isoformat(),
        }

    # ==================== UDHAR (CREDIT) OPERATIONS ====================

    def create_udhar_entry(
        self,
        shop_id: str,
        customer_name: str,
        amount: float,
        user_phone: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new udhar entry for a customer.

        Positive amount -> customer owes shopkeeper (credit given).
        Negative amount -> customer paid back (payment received).
        """
        try:
            if not customer_name:
                return {
                    "success": False,
                    "message": "❌ Customer name missing for udhar entry.",
                }

            try:
                amt = float(amount)
            except Exception:
                return {
                    "success": False,
                    "message": "❌ Udhar amount samajh nahi aaya. Please send again.",
                }

            if amt == 0:
                return {
                    "success": False,
                    "message": "❌ Udhar amount zero nahi ho sakta.",
                }

            customer_key = (customer_name or "").strip().lower()

            entry_id = str(uuid.uuid4())
            entry = UdharEntry(
                entry_id=entry_id,
                shop_id=shop_id,
                customer_key=customer_key,
                customer_name=customer_name,
                amount=amt,
                timestamp=datetime.utcnow(),
                user_phone=user_phone,
                note=note,
            )

            self.db.collection("udhar_entries").document(entry_id).set(entry.to_dict())

            balance = self.get_customer_udhar_balance(shop_id, customer_key)

            return {
                "success": True,
                "entry_id": entry_id,
                "customer_name": customer_name,
                "customer_key": customer_key,
                "amount": amt,
                "balance": balance,
            }
        except Exception as e:
            print(f"Error creating udhar entry: {e}")
            return {
                "success": False,
                "message": "❌ Udhar entry save nahi ho paayi.",
            }

    def get_customer_udhar_balance(self, shop_id: str, customer_key: str) -> float:
        """Get current udhar balance for a single customer."""
        try:
            docs = (
                self.db.collection("udhar_entries")
                .where("shop_id", "==", shop_id)
                .where("customer_key", "==", customer_key)
                .stream()
            )
            total = 0.0
            for doc in docs:
                data = doc.to_dict() or {}
                try:
                    amt = float(data.get("amount", 0) or 0)
                except Exception:
                    amt = 0.0
                total += amt
            return round(total, 2)
        except Exception as e:
            print(f"Error reading udhar balance: {e}")
            return 0.0

    def get_udhar_summary(self, shop_id: str) -> Dict[str, Any]:
        """Get summary of all customers with outstanding udhar."""
        try:
            docs = self.db.collection("udhar_entries").where("shop_id", "==", shop_id).stream()

            by_customer: Dict[str, Dict[str, Any]] = {}

            for doc in docs:
                data = doc.to_dict() or {}
                raw_key = data.get("customer_key") or ""
                key = str(raw_key).strip().lower()
                name = data.get("customer_name") or "Customer"
                try:
                    amt = float(data.get("amount", 0) or 0)
                except Exception:
                    amt = 0.0

                if not key:
                    key = name.strip().lower() or "unknown"

                if key not in by_customer:
                    by_customer[key] = {"name": name, "balance": 0.0}

                by_customer[key]["balance"] += amt

            customers: List[Dict[str, Any]] = []
            total_udhar = 0.0

            for obj in by_customer.values():
                balance = round(obj["balance"], 2)
                # Ignore customers whose balance is effectively zero.
                if abs(balance) < 0.01:
                    continue
                customers.append({"name": obj["name"], "balance": balance})
                total_udhar += balance

            # Sort customers by highest balance first so the most important are on top.
            customers.sort(key=lambda c: c.get("balance", 0.0), reverse=True)

            return {
                "success": True,
                "customers": customers,
                "total_udhar": round(total_udhar, 2),
                "total_customers": len(customers),
            }
        except Exception as e:
            print(f"Error building udhar summary: {e}")
            return {
                "success": False,
                "customers": [],
                "total_udhar": 0.0,
                "total_customers": 0,
                "message": "❌ Udhar summary nikalte waqt error aaya.",
            }

    def get_udhar_history(self, shop_id: str, customer_name: str) -> Dict[str, Any]:
        """Get detailed udhar history for a single customer.

        Returns all entries (credit given + payments) and the current
        outstanding balance.
        """
        try:
            customer_key = (customer_name or "").strip().lower()
            if not customer_key:
                return {
                    "success": False,
                    "customer_name": customer_name,
                    "customer_key": customer_key,
                    "entries": [],
                    "balance": 0.0,
                    "message": "❌ Customer name missing for udhar history.",
                }

            docs = (
                self.db.collection("udhar_entries")
                .where("shop_id", "==", shop_id)
                .where("customer_key", "==", customer_key)
                .stream()
            )

            entries: List[Dict[str, Any]] = []
            balance = 0.0
            resolved_name = customer_name

            for doc in docs:
                data = doc.to_dict() or {}
                if data.get("customer_name"):
                    resolved_name = data.get("customer_name")

                try:
                    amt = float(data.get("amount", 0) or 0)
                except Exception:
                    amt = 0.0

                balance += amt

                raw_ts = data.get("timestamp")
                ts_sort = ""
                ts_display = ""
                if isinstance(raw_ts, datetime):
                    ts_sort = raw_ts.isoformat()
                    ts_display = raw_ts.strftime("%Y-%m-%d %H:%M")
                elif isinstance(raw_ts, str):
                    try:
                        parsed = datetime.fromisoformat(raw_ts)
                        ts_sort = parsed.isoformat()
                        ts_display = parsed.strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        ts_sort = raw_ts
                        ts_display = raw_ts

                entry_type = "credit" if amt > 0 else "payment" if amt < 0 else "neutral"

                entries.append(
                    {
                        "amount": round(amt, 2),
                        "type": entry_type,
                        "timestamp": ts_display,
                        "_sort_key": ts_sort,
                        "note": data.get("note"),
                    }
                )

            # Sort entries by timestamp so history reads in time order.
            entries.sort(key=lambda e: e.get("_sort_key", ""))
            for e in entries:
                e.pop("_sort_key", None)

            return {
                "success": True,
                "customer_name": resolved_name or customer_name,
                "customer_key": customer_key,
                "entries": entries,
                "balance": round(balance, 2),
            }
        except Exception as e:
            print(f"Error building udhar history: {e}")
            return {
                "success": False,
                "customer_name": customer_name,
                "customer_key": (customer_name or "").strip().lower(),
                "entries": [],
                "balance": 0.0,
                "message": "❌ Udhar history nikalte waqt error aaya.",
            }






        # ==================== UDHAR (CREDIT) OPERATIONS ====================

        def create_udhar_entry(
            self,
            shop_id: str,
            customer_name: str,
            amount: float,
            user_phone: str,
            note: Optional[str] = None,
        ) -> Dict[str, Any]:
            """Create a new udhar entry for a customer.

            Positive amount -> customer owes shopkeeper (credit given).
            Negative amount -> customer paid back (payment received).
            """
            try:
                if not customer_name:
                    return {
                        "success": False,
                        "message": "❌ Customer name missing for udhar entry.",
                    }

                try:
                    amt = float(amount)
                except Exception:
                    return {
                        "success": False,
                        "message": "❌ Udhar amount samajh nahi aaya. Please send again.",
                    }

                if amt == 0:
                    return {
                        "success": False,
                        "message": "❌ Udhar amount zero nahi ho sakta.",
                    }

                customer_key = (customer_name or "").strip().lower()

                entry_id = str(uuid.uuid4())
                entry = UdharEntry(
                    entry_id=entry_id,
                    shop_id=shop_id,
                    customer_key=customer_key,
                    customer_name=customer_name,
                    amount=amt,
                    timestamp=datetime.utcnow(),
                    user_phone=user_phone,
                    note=note,
                )

                self.db.collection("udhar_entries").document(entry_id).set(entry.to_dict())

                balance = self.get_customer_udhar_balance(shop_id, customer_key)

                return {
                    "success": True,
                    "entry_id": entry_id,
                    "customer_name": customer_name,
                    "customer_key": customer_key,
                    "amount": amt,
                    "balance": balance,
                }
            except Exception as e:
                print(f"Error creating udhar entry: {e}")
                return {
                    "success": False,
                    "message": "❌ Udhar entry save nahi ho paayi.",
                }

        def get_customer_udhar_balance(self, shop_id: str, customer_key: str) -> float:
            """Get current udhar balance for a single customer."""
            try:
                docs = (
                    self.db.collection("udhar_entries")
                    .where("shop_id", "==", shop_id)
                    .where("customer_key", "==", customer_key)
                    .stream()
                )
                total = 0.0
                for doc in docs:
                    data = doc.to_dict() or {}
                    try:
                        amt = float(data.get("amount", 0) or 0)
                    except Exception:
                        amt = 0.0
                    total += amt
                return round(total, 2)
            except Exception as e:
                print(f"Error reading udhar balance: {e}")
                return 0.0

        def get_udhar_summary(self, shop_id: str) -> Dict[str, Any]:
            """Get summary of all customers with outstanding udhar."""
            try:
                docs = self.db.collection("udhar_entries").where("shop_id", "==", shop_id).stream()

                by_customer: Dict[str, Dict[str, Any]] = {}

                for doc in docs:
                    data = doc.to_dict() or {}
                    raw_key = data.get("customer_key") or ""
                    key = str(raw_key).strip().lower()
                    name = data.get("customer_name") or "Customer"
                    try:
                        amt = float(data.get("amount", 0) or 0)
                    except Exception:
                        amt = 0.0

                    if not key:
                        key = name.strip().lower() or "unknown"

                    if key not in by_customer:
                        by_customer[key] = {"name": name, "balance": 0.0}

                    by_customer[key]["balance"] += amt

                customers: List[Dict[str, Any]] = []
                total_udhar = 0.0

                for obj in by_customer.values():
                    balance = round(obj["balance"], 2)
                    # Ignore customers whose balance is effectively zero.
                    if abs(balance) < 0.01:
                        continue
                    customers.append({"name": obj["name"], "balance": balance})
                    total_udhar += balance

                # Sort customers by highest balance first so the most important are on top.
                customers.sort(key=lambda c: c.get("balance", 0.0), reverse=True)

                return {
                    "success": True,
                    "customers": customers,
                    "total_udhar": round(total_udhar, 2),
                    "total_customers": len(customers),
                }
            except Exception as e:
                print(f"Error building udhar summary: {e}")
                return {
                    "success": False,
                    "customers": [],
                    "total_udhar": 0.0,
                    "total_customers": 0,
                    "message": "❌ Udhar summary nikalte waqt error aaya.",
                }
