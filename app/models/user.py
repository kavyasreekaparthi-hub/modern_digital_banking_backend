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
    # Using the full module path (app.models.filename.ClassName) solves 
    # the "Multiple classes found" registry error.
    transactions = relationship(
        "app.models.transaction.Transaction", 
        backref="user", 
        cascade="all, delete-orphan"
    )
    rules = relationship(
        "app.models.category_rule.CategoryRule", 
        backref="user", 
        cascade="all, delete-orphan"
    )
    budgets = relationship(
        "app.models.budget.Budget", 
        backref="user", 
        cascade="all, delete-orphan"
    )