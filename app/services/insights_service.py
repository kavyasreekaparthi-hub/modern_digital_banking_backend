from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.models.transaction import Transaction
from app.models.budget import Budget

class InsightsService:
    
    @staticmethod
    def get_category_spending(db: Session, user_id: int):
        """
        Calculates total spending grouped by category.
        Useful for Pie Charts in the Frontend.
        """
        results = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total_amount")
        ).filter(
            Transaction.user_id == user_id
        ).group_by(
            Transaction.category
        ).all()
        
        # Convert SQLAlchemy objects to a list of dictionaries for the Pydantic schema
        return [{"category": r.category, "total_amount": float(r.total_amount)} for r in results]

    @staticmethod
    def get_top_merchants(db: Session, user_id: int, limit: int = 5):
        """
        Identifies the top merchants by spending volume.
        Logic: Filter by user -> Group by Merchant -> Sum Amount -> Order Descending.
        """
        results = db.query(
            Transaction.merchant,
            func.sum(Transaction.amount).label("total_spent")
        ).filter(
            Transaction.user_id == user_id
        ).group_by(
            Transaction.merchant
        ).order_by(
            func.sum(Transaction.amount).desc()
        ).limit(limit).all()
        
        return [{"merchant": r.merchant, "total_spent": float(r.total_spent)} for r in results]

    @staticmethod
    def calculate_burn_rate(db: Session, user_id: int):
        """
        Calculates how much of the monthly budget has been consumed.
        Formula: (Spent / Limit) * 100
        """
        # 1. Fetch the user's budget
        budget = db.query(Budget).filter(Budget.user_id == user_id).first()
        
        if not budget or budget.limit == 0:
            return {
                "budget_limit": 0.0, 
                "spent_so_far": 0.0, 
                "burn_percentage": 0.0
            }

        # 2. Dynamically calculate spending for the current month
        # This ensures the burn rate is always 'live' data
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        total_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            func.extract('month', Transaction.date) == current_month,
            func.extract('year', Transaction.date) == current_year
        ).scalar() or 0.0
        
        # 3. Calculate percentage
        percentage = (float(total_spent) / float(budget.limit)) * 100
        
        return {
            "budget_limit": float(budget.limit),
            "spent_so_far": float(total_spent),
            "burn_percentage": round(percentage, 2)
        }

    @staticmethod
    def get_cash_flow(db: Session, user_id: int):
        """
        Logic for Milestone 4 Export: Calculates monthly Income vs Expense.
        """
        # This can be expanded to return a List[CashFlowResponse]
        pass