from sqlalchemy.orm import Session
from ..models.alert import Alert
from ..models.budget import Budget

class AlertService:
    @staticmethod
    def check_and_generate_alert(db: Session, budget: Budget):
        """
        Milestone 2 Requirement: Overspending Detection (Step 8)
        1. Check if spent > limit
        2. Prevent duplicate alerts for the same category/month
        """
        if budget.spent_amount > budget.limit_amount:
            # Check if an alert already exists for this specific budget this month
            # We look for a message containing the category and month/year to ensure idempotency
            alert_msg = f"Limit exceeded for {budget.category} in {budget.month}/{budget.year}"
            
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
                return new_alert
        return None