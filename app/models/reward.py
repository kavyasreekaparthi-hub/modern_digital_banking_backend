from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database import Base

class Reward(Base):
    """
    SQLAlchemy model for the 'rewards' table.
    Tracks points balances across different loyalty programs.
    """
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Example: "HDFC Credit Card", "Amazon Pay", etc.
    program_name = Column(String, nullable=False)
    
    # Tracks the actual point count
    points_balance = Column(Integer, default=0)
    
    # Records the last time points were updated
    last_updated = Column(Date)