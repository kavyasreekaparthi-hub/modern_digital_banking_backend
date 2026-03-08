from sqlalchemy.orm import Session
from ..models.category_rule import CategoryRule

class RuleEngine:
    @staticmethod
    def match_category(merchant_description: str, db: Session, user_id: int) -> str:
        """
        Milestone 2 Final Intelligence Engine:
        Priority 1: Exact Merchant Match (Deterministic)
        Priority 2: Keyword/Partial Match
        Fallback: 'Uncategorized'
        """
        # Requirement 3.1: Case-insensitive and whitespace trimmed normalization
        clean_desc = merchant_description.strip().lower()
        
        # Requirement 3.2: Fetch all rules once to avoid N+1 queries
        rules = db.query(CategoryRule).filter(CategoryRule.user_id == user_id).all()
        
        # --- STEP 1: Check for Exact Matches First ---
        # (Professional logic: prevents 'Amazon Prime' rule from being skipped for 'Amazon')
        for rule in rules:
            # We use rule.keyword or rule.rule_value depending on your Model attribute name
            pattern = rule.keyword.strip().lower() 
            if pattern == clean_desc:
                return rule.category

        # --- STEP 2: Check for Partial/Keyword Matches ---
        for rule in rules:
            pattern = rule.keyword.strip().lower()
            if pattern in clean_desc:
                return rule.category
        
        # --- STEP 3: Default Fallback ---
        return "Uncategorized"