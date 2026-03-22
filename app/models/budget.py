from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    category = Column(String, nullable=False)
    limit_amount = Column(Float, nullable=False) 
    
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    # Relationship to the User model
    # back_populates must match the 'budgets' relationship defined in the User model
    user = relationship("User", back_populates="budgets")