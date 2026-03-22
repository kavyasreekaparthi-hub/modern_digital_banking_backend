from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Alert(Base):
    """
    Database model for the Alert system. 
    Supports low_balance, bill_due, and budget_exceeded types.
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Ensure every alert is tied to a user for secure filtering [cite: 17, 42, 273]
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Stores the alert type: low_balance, bill_due, or budget_exceeded [cite: 22, 106, 267]
    type = Column(String, nullable=False, default="budget_exceeded")
    
    # Descriptive message for the UI [cite: 167, 268]
    message = Column(String, nullable=False)
    
    # Tracks if the user has seen the alert; critical for GET /alerts/unread [cite: 39, 170, 272]
    is_read = Column(Boolean, default=False, nullable=False)
    
    # Automated timestamp for sorting (latest first) [cite: 43, 270, 302]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Alert(id={self.id}, type='{self.type}', is_read={self.is_read})>"