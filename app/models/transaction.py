from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), index=True)
    
    # Financial Data
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    transaction_type = Column(String, default="debit")
    category = Column(String, default="Uncategorized")
    
    # Metadata for Intelligence Engine
    merchant = Column(String, index=True)
    description = Column(String)
    
    # Dates
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    posted_date = Column(DateTime, nullable=True)

    # Relationships
    # Link to Account
    account = relationship("Account", back_populates="transactions")
    # Link to User (Matches User.transactions)
    user = relationship("User", back_populates="transactions")