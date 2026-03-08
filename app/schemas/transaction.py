from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TransactionCreate(BaseModel):
    # Field aliases allow the API to accept "txn_type" but store it as "transaction_type"
    description: str
    amount: float
    
    transaction_type: str = Field(default="debit", validation_alias="txn_type")
    merchant: Optional[str] = None
    currency: Optional[str] = "USD"
    category: Optional[str] = None
    
    # Adding account_id to match your previous CSV import logic
    account_id: Optional[int] = None 

class TransactionOut(BaseModel):
    id: int
    user_id: int
    description: str
    amount: float
    category: str
    transaction_type: str
    merchant: Optional[str]
    currency: str
    transaction_date: datetime

    # Pydantic V2 configuration to read from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)