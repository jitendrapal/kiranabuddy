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
        if 'created_at' in data and data['created_at']:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and data['updated_at']:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return Product(**data)


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
class ParsedCommand:
    """Parsed command from user message"""
    action: CommandAction
    product_name: Optional[str] = None
    quantity: Optional[float] = None
    confidence: float = 0.0
    raw_message: str = ""
    
    def is_valid(self) -> bool:
        """Check if command is valid for execution"""
        if self.action == CommandAction.CHECK_STOCK:
            return self.product_name is not None
        elif self.action in [CommandAction.ADD_STOCK, CommandAction.REDUCE_STOCK]:
            return self.product_name is not None and self.quantity is not None and self.quantity > 0
        return False

