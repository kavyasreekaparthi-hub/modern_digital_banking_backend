from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.insights_service import InsightsService
from app.api.routes.auth import get_demo_user 

# Ensure these classes are defined in app/schemas/insights.py
from app.schemas.insights import CategorySpend, TopMerchant, BurnRateResponse

router = APIRouter(prefix="/insights", tags=["Insights Dashboard"])

@router.get("/category-spend", response_model=List[CategorySpend])
def get_category_spend(db: Session = Depends(get_db)):
    """Retrieve spending broken down by category for the current user."""
    user = get_demo_user(db)
    return InsightsService.get_category_spending(db, user.id)

@router.get("/top-merchants", response_model=List[TopMerchant])
def get_top_merchants(db: Session = Depends(get_db)):
    """Retrieve the merchants where the user spends the most."""
    user = get_demo_user(db)
    return InsightsService.get_top_merchants(db, user.id)

@router.get("/burn-rate", response_model=BurnRateResponse)
def get_burn_rate(db: Session = Depends(get_db)):
    """Calculate the percentage of the budget spent so far."""
    user = get_demo_user(db)
    return InsightsService.calculate_burn_rate(db, user.id)