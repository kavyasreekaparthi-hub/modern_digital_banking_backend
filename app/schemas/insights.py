# app/schemas/insights.py
from pydantic import BaseModel
from typing import List

class CashFlowResponse(BaseModel):
    """Schema for monthly income vs. expense tracking."""
    month: str
    income: float
    expense: float

class CategorySpend(BaseModel):
    """Schema for spending breakdown by transaction category."""
    category: str
    total_amount: float

class TopMerchant(BaseModel):
    """Schema for identifying where the user spends the most."""
    merchant: str
    total_spent: float

class BurnRateResponse(BaseModel):
    """Schema for real-time budget utilization tracking."""
    budget_limit: float
    spent_so_far: float
    burn_percentage: float