from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.alert import Alert
from app.models.account import Account
from app.models.budget import Budget
from app.models.bill import Bill

class AlertManager:
    @staticmethod
    def check_low_balance(db: Session, user_id: int, threshold: float = 500.0):
        """
        Check if balance < threshold 
        """
        account = db.query(Account).filter(Account.user_id == user_id).first()
        if account and account.balance < threshold:
            new_alert = Alert(
                user_id=user_id,
                type="low_balance",
                message=f"Warning: Your balance is below {threshold}. Current balance: {account.balance}."
            )
            db.add(new_alert)
            db.commit() [cite: 33]

    @staticmethod
    def check_budget_status(db: Session, user_id: int):
        """
        Check if budget exceeded 
        """
        budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
        for budget in budgets:
            if budget.spent_amount > budget.limit:
                new_alert = Alert(
                    user_id=user_id,
                    type="budget_exceeded",
                    message=f"Alert: Budget exceeded for {budget.category}."
                )
                db.add(new_alert)
        db.commit() [cite: 33]

    @staticmethod
    def check_bill_deadlines(db: Session, user_id: int, x_days: int = 3):
        """
        Check if bill due in next X days 
        """
        upcoming_date = datetime.now() + timedelta(days=x_days)
        upcoming_bills = db.query(Bill).filter(
            Bill.user_id == user_id,
            Bill.status != "paid",
            Bill.due_date <= upcoming_date
        ).all()

        for bill in upcoming_bills:
            new_alert = Alert(
                user_id=user_id,
                type="bill_due",
                message=f"Reminder: {bill.biller_name} bill is due on {bill.due_date}."
            )
            db.add(new_alert)
        db.commit() [cite: 33]