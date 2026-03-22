# 1. Import the shared Base from your database configuration
from app.database import Base

# 2. Import all your model classes
from .user import User
from .transaction import Transaction
from .budget import Budget
from .category_rule import CategoryRule
from .alert import Alert
from .account import Account
from .bill import Bill
from .reward import Reward

# 3. Export them using __all__ for clean imports
# This ensures that these classes are visible when you do: from app.models import Bill
__all__ = [
    "Base", 
    "User", 
    "Transaction", 
    "Budget", 
    "CategoryRule", 
    "Alert", 
    "Account", 
    "Bill", 
    "Reward"
]