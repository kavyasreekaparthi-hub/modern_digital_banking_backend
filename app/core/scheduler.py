from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.alert_manager import AlertManager
from app.models.user import User

def run_automated_checks():
    """
    Main job that iterates through users and runs logic checks.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            # Every few hours logic: Check budget and balance [cite: 54]
            AlertManager.check_low_balance(db, user_id=user.id)
            AlertManager.check_budget_status(db, user_id=user.id)
            
            # Daily logic: Check bills [cite: 52]
            # Note: In a basic setup, these can run on the same interval 
            # or separate schedules.
            AlertManager.check_bill_deadlines(db, user_id=user.id)
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Basic interval-based setup: Runs every 4 hours [cite: 54, 56]
    scheduler.add_job(run_automated_checks, 'interval', hours=4)
    scheduler.start()