from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.bill import Bill
from app.models.user import User
from app.schemas.bill import BillCreate, BillUpdate, BillResponse
from app.services.bill_manager import BillManager
from app.services.reminder_service import ReminderService

# REMOVED: prefix="/bills" from here
router = APIRouter(tags=["Bills Management"])

# Helper to ensure we have a user context for the demo
def get_demo_user(db: Session):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found. Register via /auth/register first.")
    return user

@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
def create_bill(bill_in: BillCreate, db: Session = Depends(get_db)):
    """Creates a new bill for the demo user."""
    user = get_demo_user(db)
    new_bill = Bill(**bill_in.model_dump(), user_id=user.id)
    new_bill.status = BillManager.get_updated_status(new_bill)
    
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill

@router.get("/", response_model=List[BillResponse])
def get_bills(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Fetches all bills for the demo user and triggers background reminders."""
    user = get_demo_user(db)
    bills = db.query(Bill).filter(Bill.user_id == user.id).all()
    
    for bill in bills:
        bill.status = BillManager.get_updated_status(bill)
    
    db.commit() 
    background_tasks.add_task(ReminderService.process_bill_reminders, db, user.id)
    
    return bills

@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(bill_id: int, bill_update: BillUpdate, db: Session = Depends(get_db)):
    """Updates bill details and re-calculates status."""
    user = get_demo_user(db)
    db_bill = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == user.id).first()
    
    if not db_bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found.")
    
    update_data = bill_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bill, key, value)
    
    db_bill.status = BillManager.get_updated_status(db_bill)
    
    db.commit()
    db.refresh(db_bill)
    return db_bill

@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    """Deletes a specific bill."""
    user = get_demo_user(db)
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == user.id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    db.delete(bill)
    db.commit()
    return None