from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    account_id: int
    amount: float
    transaction_type: str  # e.g., 'debit' or 'credit'
    category: str
    description: Optional[str] = None
    transaction_date: datetime