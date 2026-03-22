from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.bill import Bill

def check_upcoming_bills(db: Session):
    """Logic to find bills due within 2 days."""
    today = datetime.now().date()
    reminder_window = today + timedelta(days=2)
    
    # Query for bills due soon that aren't paid
    upcoming_bills = db.query(Bill).filter(
        Bill.due_date <= reminder_window,
        Bill.due_date >= today,
        Bill.status != "paid"
    ).all()
    
    for bill in upcoming_bills:
        print(f"NOTIFICATION: Bill for {bill.biller_name} is due on {bill.due_date}!")
        # Here is where you would call an Email/SMS API in a real app
    
    return len(upcoming_bills)