from sqlalchemy.orm import Session
from ..models.category_rule import CategoryRule
from app.schemas.category_rule import CategoryRuleCreate

class RuleEngine:
    @staticmethod
    def create_rule(db: Session, rule_in: CategoryRuleCreate, user_id: int):
        """
        Saves a new user-defined categorization rule to the database.
        Called by the POST /reports/rules endpoint.
        """
        new_rule = CategoryRule(
            user_id=user_id,
            pattern=rule_in.pattern,
            category=rule_in.category,
            match_type=rule_in.match_type
        )
        try:
            db.add(new_rule)
            db.commit()
            db.refresh(new_rule)
            return {"message": "Intelligence Engine rule created", "rule_id": new_rule.id}
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def match_category(merchant_description: str, db: Session, user_id: int) -> str:
        """
        Intelligence Engine Logic:
        Priority 1: Exact Merchant Match (Deterministic)
        Priority 2: Keyword/Partial Match
        Fallback: 'Uncategorized'
        """
        # Step 0: Clean the input
        clean_desc = merchant_description.strip().lower()
        
        # Step 1: Fetch all rules for the user
        rules = db.query(CategoryRule).filter(CategoryRule.user_id == user_id).all()
        
        # --- STEP 2: Priority 1 - Exact Matches ---
        for rule in rules:
            pattern = rule.pattern.strip().lower() 
            if pattern == clean_desc:
                return rule.category

        # --- STEP 3: Priority 2 - Keyword/Partial Matches ---
        for rule in rules:
            pattern = rule.pattern.strip().lower()
            if pattern in clean_desc:
                return rule.category
        
        # --- STEP 4: Default Fallback ---
        return "Uncategorized"