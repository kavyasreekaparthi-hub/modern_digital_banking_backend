from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, UniqueConstraint
from ..database import Base  # Use .. to go up to the app level from the models folder

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)
    
    # Financial Requirement: Use Numeric(12, 2) to prevent rounding errors
    limit_amount = Column(Numeric(12, 2), nullable=False, default=0.00)
    spent_amount = Column(Numeric(12, 2), default=0.00)
    
    # Month/Year filtering for the Budget Engine
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)

    # Constraint Requirement: One budget per category per month per user
    __table_args__ = (
        UniqueConstraint('user_id', 'category', 'month', 'year', name='_user_budget_uc'),
    )