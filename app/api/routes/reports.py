from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Alert, User
from app.schemas.category_rule import CategoryRuleCreate 
from app.schemas.budget import BudgetCreate

# Service imports
from app.services.report_service import ReportService
from app.services.rule_engine import RuleEngine as RuleService
from app.services.currency import CurrencyService

router = APIRouter(prefix="/reports", tags=["Intelligence Engine"])

# Helper to get first user for demo bypass
def get_demo_user(db: Session):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found. Please register a user first.")
    return user

# --- 1. INTELLIGENCE ENGINE: Categorization Rules ---
@router.post("/rules", status_code=status.HTTP_201_CREATED)
def create_category_rule(
    rule_in: CategoryRuleCreate, 
    db: Session = Depends(get_db)
):
    user = get_demo_user(db)
    return RuleService.create_rule(db, rule_in, user.id)

# --- 2. BUDGET ENGINE: Spending Limits ---
@router.post("/budgets", status_code=status.HTTP_201_CREATED)
def create_budget(
    budget_in: BudgetCreate, 
    db: Session = Depends(get_db)
):
    user = get_demo_user(db)
    return ReportService.create_budget(db, budget_in, user.id)

# --- 3. ANALYTICS: Monthly Spending Summary ---
@router.get("/spending-summary")
def get_spending_report(
    month: int, 
    year: int, 
    db: Session = Depends(get_db)
):
    user = get_demo_user(db)
    return ReportService.get_spending_summary(db, user.id, month, year)

# --- 4. ALERT NOTIFICATIONS ---
@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    user = get_demo_user(db)
    return db.query(Alert).filter(Alert.user_id == user.id).all()

# --- 5. CURRENCY CONVERSION (Resilient Version) ---
@router.get("/currency-rates")
def get_currency_rates():
    rates = CurrencyService.get_latest_rates()
    
    if "error" in rates:
        return {
            "status": "warning",
            "message": "Live rates unavailable, using cached data.",
            "rates": {"USD": 1.0, "INR": 83.50}, 
            "note": "Service currently unreachable"
        }
    
    return rates