from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.budget import Budget

class BudgetService:
    @staticmethod
    def recalculate_budget(db: Session, user_id: int, category: str, month: int, year: int):
        """
        Milestone 2 Requirement: Aggregation Logic.
        Sums all 'debit' transactions for a specific user, category, and month.
        """
        # 1. Calculate total spending using SQL SUM
        total_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == category,
            Transaction.transaction_type == 'debit',
            func.extract('month', Transaction.transaction_date) == month,
            func.extract('year', Transaction.transaction_date) == year
        ).scalar() or 0

        # 2. Find the budget record to update
        budget = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category == category,
            Budget.month == month,
            Budget.year == year
        ).first()

        # 3. If budget exists, update the spent_amount column
        if budget:
            budget.spent_amount = total_spent
            db.commit()
            db.refresh(budget)
            return budget
        
        return None

    @staticmethod
    def get_budget_status(spent: float, limit: float):
        """
        Calculates the percentage of the budget used.
        """
        if not limit or limit == 0:
            return 0.0
        
        # Rounding to 2 decimal places as per requirement
        progress = (float(spent) / float(limit)) * 100
        return round(progress, 2)