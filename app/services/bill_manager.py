from datetime import date, timedelta
from app.models.bill import Bill
from app.database import SessionLocal

class BillManager:
    @staticmethod
    def get_updated_status(bill: Bill):
        """
        Logic for Step 2: Auto-detect status.
        Ensures bills are correctly marked as 'upcoming', 'overdue', or 'paid'.
        """
        if bill.status == "paid":
            return "paid"
        
        today = date.today()
        if today > bill.due_date:
            return "overdue"
        return "upcoming"

    @staticmethod
    def send_bill_reminders():
        """
        Logic for Step 3: Scan and notify.
        Queries the database for bills due within the next 2 days
        that are still in 'upcoming' status.
        """
        db = SessionLocal()
        try:
            today = date.today()
            threshold = today + timedelta(days=2)
            
            # Query for bills needing attention
            upcoming_bills = db.query(Bill).filter(
                Bill.due_date <= threshold,
                Bill.due_date >= today,
                Bill.status == "upcoming"
            ).all()
            
            for bill in upcoming_bills:
                # Placeholder for your Email/SMS Service integration
                print(f"Triggering reminder for: {bill.biller_name}, due on {bill.due_date}")
                
        finally:
            # Always close the session to prevent memory leaks
            db.close()