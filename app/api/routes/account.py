from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Import local database and auth dependencies
from app.database import get_db
from app.api.routes.auth import get_demo_user  # Essential for Milestone 4 Testing
from app.services.currency import CurrencyService

# Initialize the router - Variable name MUST be 'router'
router = APIRouter()

@router.get("/", tags=["Account Management"])
def get_account_status():
    """
    Verification endpoint to confirm the Account Management service is operational.
    """
    return {
        "status": "online", 
        "module": "Account Management", 
        "version": "4.0.0"
    }

@router.get("/summary/{currency}", tags=["Account Summary"])
def get_currency_summary(
    currency: str, 
    db: Session = Depends(get_db)
):
    """
    Returns the user's total account balance converted to a requested currency.
    Example: GET /accounts/summary/EUR
    """
    # 1. Fetch the demo user context (Shortcut for Milestone 4 dashboard)
    current_user = get_demo_user(db)
    
    # 2. Access the 'balance' field from your User model.
    # We use 1000.0 as a fallback if the user balance is not set.
    total_usd_balance = getattr(current_user, "balance", 1000.0)
    
    # 3. Perform conversion via the CurrencyService logic layer
    converted_total = CurrencyService.convert(total_usd_balance, currency.upper())
    
    # 4. Handle unsupported or invalid currency codes
    if converted_total is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Currency '{currency.upper()}' is not supported or the conversion service is down."
        )
        
    return {
        "user_id": current_user.id,
        "name": getattr(current_user, "name", "Demo User"),
        "base_currency": "USD",
        "target_currency": currency.upper(),
        "original_balance": round(float(total_usd_balance), 2),
        "converted_total": round(float(converted_total), 2)
    }