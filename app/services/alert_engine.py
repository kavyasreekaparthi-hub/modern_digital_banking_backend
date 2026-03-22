from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.budget import Budget
from app.models.transaction import Transaction

class AlertService:
    @staticmethod
    def check_and_generate_alert(db: Session, budget: Budget):
        """
        Calculates real-time spending and generates an alert if the 
        budget limit for the category/month has been exceeded.
        """
        # 1. Calculate actual spent amount for this category in the given month/year
        # We use func.sum for database-side efficiency
        total_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == budget.user_id,
            Transaction.category == budget.category,
            func.extract('month', Transaction.transaction_date) == budget.month,
            func.extract('year', Transaction.transaction_date) == budget.year
        ).scalar() or 0.0

        # 2. Check if spent > limit (Using limit_amount from your Budget model)
        if total_spent > float(budget.limit_amount):
            alert_msg = f"Limit exceeded for {budget.category} in {budget.month}/{budget.year}"
            
            # 3. Prevent duplicate alerts (idempotency)
            existing_alert = db.query(Alert).filter(
                Alert.user_id == budget.user_id,
                Alert.message == alert_msg
            ).first()

            if not existing_alert:
                new_alert = Alert(
                    user_id=budget.user_id,
                    type="budget_exceeded",
                    message=alert_msg
                )
                db.add(new_alert)
                db.commit()
                db.refresh(new_alert)
                return new_alert
        
        return None