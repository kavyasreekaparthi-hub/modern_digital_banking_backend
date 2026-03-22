from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.bill import Bill

class ReminderService:
    @staticmethod
    def process_bill_reminders(db: Session, user_id: int):
        """
        Identifies bills due within the next 2 days that are not yet marked as 'paid'.
        This fulfills the Step 3: Bill Reminder System requirement for Milestone 3.
        """
        today = datetime.now().date()
        reminder_window = today + timedelta(days=2)
        
        # Query: Filter for bills belonging to the user that are NOT paid
        # and fall within the 2-day reminder window
        upcoming_bills = db.query(Bill).filter(
            Bill.user_id == user_id,
            Bill.status != "paid",
            Bill.due_date >= today,
            Bill.due_date <= reminder_window
        ).all()
        
        processed_reminders = []
        
        # Simulated Notification Output
        for bill in upcoming_bills:
            msg = f"NOTIFICATION: Your bill '{bill.biller_name}' for {bill.amount_due} is due on {bill.due_date}!"
            # This print statement will show in your terminal when the task runs
            print(f"--- [M3 REMINDER SYSTEM] {msg} ---")
            processed_reminders.append(msg)
            
        return processed_reminders