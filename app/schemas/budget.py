from pydantic import BaseModel, Field

class BudgetCreate(BaseModel):
    """
    Schema for creating a monthly budget limit for a specific category.
    Matches the database model fields (month: int, year: int).
    """
    category: str
    monthly_limit: float = Field(..., gt=0, description="The maximum amount to spend in this category")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    year: int = Field(..., ge=2020, description="Year (e.g., 2026)")