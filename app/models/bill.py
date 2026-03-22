from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from app.database import Base  # Ensure this points to your shared Base in app.database

class Bill(Base):
    """
    SQLAlchemy model for the 'bills' table.
    Tracks recurring or one-time payments due from the user.
    """
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Requirement: Biller name should not be empty (Handled by nullable=False)
    biller_name = Column(String, nullable=False)
    
    # Requirement: Amount due must be tracked (Validation happens in Schema)
    amount_due = Column(Float, nullable=False)
    
    # Requirement: Track due dates for status logic
    due_date = Column(Date, nullable=False)
    
    # Logic: Status can be 'upcoming', 'paid', or 'overdue'
    status = Column(String, default="upcoming") 
    
    # Feature: Boolean to check if auto-payment is enabled
    auto_pay = Column(Boolean, default=False)