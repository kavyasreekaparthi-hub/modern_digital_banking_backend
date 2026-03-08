from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Link this account to a specific user (Foreign Key)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    bank_name = Column(String, nullable=False)
    account_type = Column(String) # e.g., Savings, Checking
    masked_account = Column(String) # e.g., ****6789
    currency = Column(String(3), default="USD")
    balance = Column(Numeric(precision=15, scale=2), default=0.00)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())