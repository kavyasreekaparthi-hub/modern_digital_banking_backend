from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class CategoryRule(Base):
    """
    Intelligence Engine Model:
    Stores user-defined rules for automated transaction categorization.
    """
    __tablename__ = "category_rules"

    # --- Safety & Constraints ---
    __table_args__ = (
        # 1. Prevents a user from creating the exact same rule twice for the same user
        UniqueConstraint('user_id', 'pattern', name='_user_pattern_uc'),
        # 2. Fixes potential registry errors during hot-reloads
        {'extend_existing': True} 
    )

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 'pattern' is the primary field for the RuleEngine to match against
    pattern = Column(String, nullable=False) 
    category = Column(String, nullable=False)
    match_type = Column(String, default="keyword")

    # --- Relationships ---
    # Matches 'rules' defined in User model (app.models.user.User)
    user = relationship("User", back_populates="rules")