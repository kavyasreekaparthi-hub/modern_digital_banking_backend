from sqlalchemy.orm import Session
from app.models import Transaction, CategoryRule

def auto_categorize(db: Session, transaction: Transaction, user_id: int):
    """
    Attempts to categorize a transaction based on user-defined rules.
    """
    # Fetch all keyword rules for the current user
    rules = db.query(CategoryRule).filter(CategoryRule.user_id == user_id).all()
    
    # Check if the description matches any keyword rule
    for rule in rules:
        if rule.keyword_pattern.lower() in transaction.description.lower():
            transaction.category = rule.category
            break  # Stop at the first rule matched