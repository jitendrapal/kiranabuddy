"""
Data models for Kirana Shop Management App
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class UserRole(Enum):
    """User roles in the system"""
    OWNER = "owner"
    STAFF = "staff"


class TransactionType(Enum):
    """Types of inventory transactions"""
    ADD_STOCK = "add_stock"
    REDUCE_STOCK = "reduce_stock"
    SALE = "sale"
    ADJUSTMENT = "adjustment"


class CommandAction(Enum):
    """Supported command actions"""
    ADD_STOCK = "add_stock"
    REDUCE_STOCK = "reduce_stock"
    CHECK_STOCK = "check_stock"
    TOTAL_SALES = "total_sales"
    TODAY_PROFIT = "today_profit"
    WEEKLY_PROFIT = "weekly_profit"
    MONTHLY_PROFIT = "monthly_profit"
    YEARLY_PROFIT = "yearly_profit"
    LIST_PRODUCTS = "list_products"
    LOW_STOCK = "low_stock"
    ADJUST_STOCK = "adjust_stock"
    UPDATE_PRICE = "update_price"
    TOP_PRODUCT_TODAY = "top_product_today"
    ZERO_SALE_TODAY = "zero_sale_today"
    EXPIRY_PRODUCTS = "expiry_products"
    PURCHASE_SUGGESTION = "purchase_suggestion"
    UNDO_LAST = "undo_last"
    HELP = "help"
    # Udhar (credit) tracking
    ADD_UDHAR = "add_udhar"
    PAY_UDHAR = "pay_udhar"
    LIST_UDHAR = "list_udhar"
    CUSTOMER_UDHAR = "customer_udhar"
    # Flexible sales/profit reports ("aaj ka hisaab", monthly/yearly reports)
    REPORT_SUMMARY = "report_summary"
    UNKNOWN = "unknown"


@dataclass
class Shop:
    """Shop model"""
    shop_id: str
    name: str
    owner_phone: str
    created_at: datetime
    active: bool = True
    address: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Shop':
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        return Shop(**data)


@dataclass
class User:
    """User model (shop owner or staff)"""
    user_id: str
    phone: str
    name: str
    shop_id: str
    role: UserRole
    created_at: datetime
    active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['role'] = self.role.value
        data['created_at'] = self.created_at.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        data['role'] = UserRole(data['role'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        return User(**data)


@dataclass
class Product:
    """Product model"""
    product_id: str
    shop_id: str
    name: str
    normalized_name: str  # lowercase, for matching
    current_stock: float
    unit: str = "pieces"
    brand: Optional[str] = None
    barcode: Optional[str] = None
    selling_price: Optional[float] = None  # current selling price per unit (in rupees)
    cost_price: Optional[float] = None  # purchase cost per unit (for profit calculation)
    # Optional single expiry date for the whole product (legacy/simple mode)
    expiry_date: Optional[str] = None  # e.g. '2025-12-31'
    # Optional per-batch expiry/quantity info, e.g.:
    # {
    #     "batch_001": {"expiry": "2025-02-10", "qty": 12},
    #     "batch_002": {"expiry": "2025-03-15", "qty": 10},
    # }
    batches: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.created_at:
            data['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            data['updated_at'] = self.updated_at.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Product':
        """Create Product from Firestore dict.

        Be tolerant of older / messy schemas:
        - map legacy `price` -> `selling_price`
        - strip spaces around field names like ` selling_price`
        - ignore any unexpected extra fields.
        """
        # Work on a shallow copy so we don't mutate the caller's dict
        raw = dict(data or {})

        # 1) Normalize keys by stripping whitespace (handles " selling_price")
        normalized: Dict[str, Any] = {}
        for k, v in raw.items():
            clean_key = k.strip() if isinstance(k, str) else k
            # Don't override an existing normalized key
            if clean_key not in normalized:
                normalized[clean_key] = v

        # 2) Legacy field mapping: `price` -> `selling_price`
        if 'price' in normalized and 'selling_price' not in normalized:
            try:
                normalized['selling_price'] = float(normalized['price']) if normalized['price'] is not None else None
            except Exception:
                normalized['selling_price'] = None
            normalized.pop('price', None)

        # 3) Convert timestamps
        if 'created_at' in normalized and normalized['created_at']:
            try:
                normalized['created_at'] = datetime.fromisoformat(normalized['created_at'])
            except Exception:
                normalized['created_at'] = None
        if 'updated_at' in normalized and normalized['updated_at']:
            try:
                normalized['updated_at'] = datetime.fromisoformat(normalized['updated_at'])
            except Exception:
                normalized['updated_at'] = None

        # 4) Filter to known Product fields only so unexpected keys don't break __init__
        allowed_keys = {
            'product_id',
            'shop_id',
            'name',
            'normalized_name',
            'current_stock',
            'unit',
            'brand',
            'barcode',
            'selling_price',
            'cost_price',
            'expiry_date',
            'batches',
            'created_at',
            'updated_at',
        }
        cleaned: Dict[str, Any] = {k: v for k, v in normalized.items() if k in allowed_keys}

        # 5) Backfill safe defaults for missing required fields so older/demo
        #    documents (like ones created by tools/reset_products.py) don't
        #    crash Product.__init__.

        # Ensure we always have a unit
        if 'unit' not in cleaned or cleaned['unit'] is None:
            cleaned['unit'] = 'pieces'

        # Ensure we always have normalized_name (fallback: lowercase name)
        if 'normalized_name' not in cleaned and 'name' in cleaned:
            try:
                cleaned['normalized_name'] = (cleaned['name'] or '').strip().lower()
            except Exception:
                cleaned['normalized_name'] = ''

        # Infer current_stock from batches if not explicitly stored.
        if 'current_stock' not in cleaned or cleaned['current_stock'] is None:
            total_qty = 0.0
            batches_obj = cleaned.get('batches') or normalized.get('batches')
            if isinstance(batches_obj, dict):
                for batch in batches_obj.values():
                    try:
                        if not isinstance(batch, dict):
                            continue
                        qty_raw = batch.get('qty') or batch.get('quantity')
                        if qty_raw is None:
                            continue
                        total_qty += float(qty_raw)
                    except Exception:
                        continue
            cleaned['current_stock'] = total_qty

        return Product(**cleaned)


@dataclass
class Transaction:
    """Transaction model for inventory changes"""
    transaction_id: str
    shop_id: str
    product_id: str
    product_name: str
    transaction_type: TransactionType
    quantity: float
    previous_stock: float
    new_stock: float
    user_phone: str
    timestamp: datetime
    unit_price: Optional[float] = None  # price per unit at time of transaction (in rupees)
    total_amount: Optional[float] = None  # quantity * unit_price
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['transaction_type'] = self.transaction_type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Transaction':
        data['transaction_type'] = TransactionType(data['transaction_type'])
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return Transaction(**data)




@dataclass
class UdharEntry:
    """Udhar (credit) entry for a customer.

    Positive amount -> customer owes shopkeeper (gave goods on credit).
    Negative amount -> customer paid back (reduces outstanding balance).
    """
    entry_id: str
    shop_id: str
    customer_key: str  # canonical lowercase key for matching
    customer_name: str
    amount: float
    timestamp: datetime
    user_phone: str
    note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "UdharEntry":
        d = dict(data or {})
        ts = d.get("timestamp")
        if isinstance(ts, str):
            try:
                d["timestamp"] = datetime.fromisoformat(ts)
            except Exception:
                d["timestamp"] = datetime.utcnow()
        elif not isinstance(ts, datetime):
            d["timestamp"] = datetime.utcnow()
        return UdharEntry(**d)

@dataclass
class ParsedCommand:
    """Parsed command from user message"""
    action: CommandAction
    product_name: Optional[str] = None  # reused for customer_name in udhar commands
    quantity: Optional[float] = None  # reused for amount in udhar commands
    confidence: float = 0.0
    raw_message: str = ""

    def is_valid(self) -> bool:
        """Check if command is valid for execution"""
        if self.action == CommandAction.CHECK_STOCK:
            return self.product_name is not None
        elif self.action in [
            CommandAction.ADD_STOCK,
            CommandAction.REDUCE_STOCK,
            CommandAction.ADJUST_STOCK,
            CommandAction.UPDATE_PRICE,
            CommandAction.ADD_UDHAR,
            CommandAction.PAY_UDHAR,
        ]:
            # For adjustments, quantity represents the correct quantity for the last entry
            # For udhar, quantity is the amount in rupees (always positive here).
            # For UPDATE_PRICE, quantity is the new selling price (per unit) in rupees.
            return self.product_name is not None and self.quantity is not None and self.quantity > 0
        elif self.action in [
            CommandAction.CUSTOMER_UDHAR,
        ]:
            # Customer-specific udhar history: only needs a customer name.
            return self.product_name is not None
        elif self.action in [
            CommandAction.TOTAL_SALES,
            CommandAction.TODAY_PROFIT,
            CommandAction.WEEKLY_PROFIT,
            CommandAction.MONTHLY_PROFIT,
            CommandAction.YEARLY_PROFIT,
            CommandAction.LIST_PRODUCTS,
            CommandAction.LOW_STOCK,
            CommandAction.TOP_PRODUCT_TODAY,
            CommandAction.ZERO_SALE_TODAY,
            CommandAction.EXPIRY_PRODUCTS,
            CommandAction.UNDO_LAST,
            CommandAction.HELP,
            CommandAction.LIST_UDHAR,
            CommandAction.REPORT_SUMMARY,
        ]:
            # These commands don't require product or quantity
            return True
        return False

