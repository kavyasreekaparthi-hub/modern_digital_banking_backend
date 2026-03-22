from pydantic import BaseModel
from typing import Optional

class CategoryRuleCreate(BaseModel):
    """
    Schema for creating a new categorization rule.
    Matches the 'pattern' field now used in the Database and RuleEngine.
    """
    pattern: str                 # Renamed from 'keyword_pattern' to match DB model
    category: str
    match_type: Optional[str] = "keyword" # Defaulted to match your RuleEngine logic