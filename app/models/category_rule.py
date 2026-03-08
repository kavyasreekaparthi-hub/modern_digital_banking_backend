from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from app.database import Base

class CategoryRule(Base):
    """
    Intelligence Engine Model:
    Stores user-defined rules for automated transaction categorization.
    """
    __tablename__ = "category_rules"

    # --- Safety & Constraints ---
    __table_args__ = (
        # 1. Prevents a user from creating the exact same rule twice
        UniqueConstraint('user_id', 'pattern', name='_user_pattern_uc'),
        # 2. Fixes the 'Multiple classes found' / 'Already defined' registry errors
        {'extend_existing': True} 
    )

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The text to look for in transaction descriptions (e.g., 'Starbucks')
    pattern = Column(String, nullable=False) 
    
    # The label to apply (e.g., 'Food & Dining')
    category = Column(String, nullable=False)

    # How to match: 'keyword' (partial) or 'exact'
    match_type = Column(String, default="keyword")