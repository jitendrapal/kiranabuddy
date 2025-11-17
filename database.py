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

from models import Shop, User, Product, Transaction, UserRole, TransactionType

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

            # Require at least half the product tokens to match to avoid
            # obviously wrong matches.
            if coverage < 0.5:
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

        return {
            "success": True,
            "product_name": product.name,
            "quantity": quantity,
            "previous_stock": previous_stock,
            "new_stock": new_stock,
            "unit": product.unit,
            "unit_price": unit_price,
            "total_amount": total_amount,
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
            "month": now.strftime("%Y-%m"),
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



