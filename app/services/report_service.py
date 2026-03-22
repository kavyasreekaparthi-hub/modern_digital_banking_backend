from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate
from app.services.alert_engine import AlertService

class ReportService:
    @staticmethod
    def create_budget(db: Session, budget_in: BudgetCreate, user_id: int):
        try:
            # 1. Business Rule: Check for existing budget
            existing_budget = db.query(Budget).filter(
                Budget.category == budget_in.category,
                Budget.month == budget_in.month,
                Budget.year == budget_in.year,
                Budget.user_id == user_id
            ).first()
            
            if existing_budget:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Budget for '{budget_in.category}' already exists for {budget_in.month}/{budget_in.year}."
                )
            
            # 2. Create new budget record with explicit mapping
            # We take the values and map 'monthly_limit' -> 'limit_amount'
            new_budget = Budget(
                user_id=user_id,
                category=budget_in.category,
                limit_amount=budget_in.monthly_limit,  # Explicit mapping
                month=budget_in.month,
                year=budget_in.year
            )
            
            db.add(new_budget)
            db.commit()
            db.refresh(new_budget)
            
            # 3. Trigger Intelligence: Check spending against new limit
            alert = AlertService.check_and_generate_alert(db, new_budget)
            
            # 4. Construct response
            response = {
                "message": "Budget limit established", 
                "budget_id": new_budget.id,
                "category": new_budget.category,
                "limit": new_budget.limit_amount
            }
            
            if alert:
                response["alert"] = f"Warning: Current spending for {new_budget.category} exceeds this limit!"
                
            return response
            
        except HTTPException as he:
            # Re-raise known HTTP exceptions
            raise he
        except Exception as e:
            # Handle unexpected database or logic errors
            db.rollback()
            print(f"CRITICAL ERROR IN CREATE_BUDGET: {str(e)}") 
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    @staticmethod
    def get_spending_summary(db: Session, user_id: int, month: int, year: int):
        return {"summary": "Spending data retrieved", "month": month, "year": year}