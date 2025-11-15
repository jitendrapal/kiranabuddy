"""
Firebase Firestore database layer
"""
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from google.cloud import firestore
from google.oauth2 import service_account
import uuid

from models import Shop, User, Product, Transaction, UserRole, TransactionType

# Dummy Indian products catalog for barcode-based demo.
# In a real deployment you would load this from your own product master data.
DEMO_BARCODE_PRODUCTS: Dict[str, Dict[str, Any]] = {
    # Dal variants
    "8901000000001": {"name": "Tata Sampann Toor Dal 1kg", "brand": "Tata Sampann", "unit": "kg"},
    "8901000000002": {"name": "Tata Sampann Moong Dal 1kg", "brand": "Tata Sampann", "unit": "kg"},
    "8901000000003": {"name": "Tata Sampann Masoor Dal 1kg", "brand": "Tata Sampann", "unit": "kg"},
    # Oil
    "8902000000001": {"name": "Fortune Sunlite Refined Sunflower Oil 1L", "brand": "Fortune", "unit": "litre"},
    "8902000000002": {"name": "Fortune Kachi Ghani Mustard Oil 1L", "brand": "Fortune", "unit": "litre"},
    # Atta
    "8903000000001": {"name": "Aashirvaad Atta 10kg", "brand": "Aashirvaad", "unit": "kg"},
    # Biscuits
    "8904000000001": {"name": "Parle-G Biscuits 800g", "brand": "Parle", "unit": "gram"},
    "8904000000002": {"name": "Britannia Good Day 600g", "brand": "Britannia", "unit": "gram"},
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
    def get_products_summary(self, shop_id: str) -> Dict[str, Any]:
        """Get summary of all products and current stock for a shop"""
        products = self.get_products_by_shop(shop_id)

        product_list = []
        for p in products:
            product_list.append({
                'name': p.name,
                'stock': p.current_stock,
                'unit': p.unit,
            })

        return {
            'success': True,
            'total_products': len(product_list),
            'products': product_list,
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

    def create_transaction(self, shop_id: str, product_id: str, product_name: str,
                          transaction_type: TransactionType, quantity: float,
                          previous_stock: float, new_stock: float,
                          user_phone: str, notes: Optional[str] = None) -> Transaction:
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
            notes=notes
        )

        self.db.collection('transactions').document(transaction_id).set(transaction.to_dict())
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
        """Add stock to a product"""
        product = self.get_or_create_product(shop_id, product_name)
        previous_stock = product.current_stock
        new_stock = previous_stock + quantity

        # Update product stock
        self.update_product_stock(product.product_id, new_stock)

        # Create transaction record
        transaction = self.create_transaction(
            shop_id=shop_id,
            product_id=product.product_id,
            product_name=product.name,
            transaction_type=TransactionType.ADD_STOCK,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            notes=f"Added {quantity} {product.unit}"
        )

        return {
            'success': True,
            'product_name': product.name,
            'quantity': quantity,
            'previous_stock': previous_stock,
            'new_stock': new_stock,
            'unit': product.unit
        }

    def reduce_stock(self, shop_id: str, product_name: str, quantity: float, user_phone: str) -> Dict[str, Any]:
        """Reduce stock from a product (sale or consumption)"""
        product = self.get_or_create_product(shop_id, product_name)
        previous_stock = product.current_stock
        new_stock = max(0, previous_stock - quantity)  # Don't go negative

        # Update product stock
        self.update_product_stock(product.product_id, new_stock)

        # Create transaction record
        transaction = self.create_transaction(
            shop_id=shop_id,
            product_id=product.product_id,
            product_name=product.name,
            transaction_type=TransactionType.REDUCE_STOCK,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            user_phone=user_phone,
            notes=f"Reduced {quantity} {product.unit}"
        )

        return {
            'success': True,
            'product_name': product.name,
            'quantity': quantity,
            'previous_stock': previous_stock,
            'new_stock': new_stock,
            'unit': product.unit
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
        """Get total sales for today"""
        from datetime import datetime, timedelta

        # Get start of today (midnight)
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Query transactions for today
        transactions_ref = self.db.collection('transactions').where('shop_id', '==', shop_id)

        # Filter by date and type
        all_transactions = transactions_ref.stream()

        total_items_sold = 0
        products_sold = {}

        for trans_doc in all_transactions:
            trans = trans_doc.to_dict()

            # Check if transaction is from today
            trans_time = trans.get('timestamp')
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
                    if trans.get('transaction_type') == 'reduce_stock' or trans.get('transaction_type') == 'sale':
                        quantity = trans.get('quantity', 0)
                        product_name = trans.get('product_name', 'Unknown')

                        total_items_sold += quantity

                        if product_name in products_sold:
                            products_sold[product_name] += quantity
                        else:
                            products_sold[product_name] = quantity

        return {
            'success': True,
            'total_items_sold': total_items_sold,
            'products_sold': products_sold,
            'date': today_start.strftime('%Y-%m-%d')
        }

    def get_zero_sale_products_today(self, shop_id: str) -> Dict[str, Any]:
        """Get products that had zero sales today (but are currently in stock).

        Uses today's transactions (reduce_stock / sale) and the current
        product list to find items that did not sell at all today.
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
            # Only show products that still have some stock and had no sales today
            if p.current_stock > 0 and p.name not in products_sold:
                zero_sale_products.append(
                    {
                        "name": p.name,
                        "stock": p.current_stock,
                        "unit": p.unit,
                    }
                )

        return {
            "success": True,
            "zero_sale_products": zero_sale_products,
            "total_zero_sale_products": len(zero_sale_products),
            "date": sales_data.get("date"),
        }


