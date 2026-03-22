from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    # --- Primary Key ---
    id = Column(Integer, primary_key=True, index=True)
    
    # --- Auth & Profile ---
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # --- Banking Specifics ---
    kyc_status = Column(String, default="unverified")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # --- Intelligence Engine Relationships ---
    # Using back_populates to explicitly link with the 'user' attribute in child models
    transactions = relationship(
        "app.models.transaction.Transaction", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    rules = relationship(
        "app.models.category_rule.CategoryRule", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    budgets = relationship(
        "app.models.budget.Budget", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )