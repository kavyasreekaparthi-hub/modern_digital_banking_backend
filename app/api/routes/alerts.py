from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, MarkReadRequest
from app.api.routes.auth import get_demo_user  # Helper from previous milestones

router = APIRouter(prefix="/alerts", tags=["Alert Center"])

@router.get("/", response_model=List[AlertResponse])
def get_all_alerts(db: Session = Depends(get_db)):
    """Retrieve all alerts for the user, sorted latest first[cite: 38, 42, 43]."""
    user = get_demo_user(db)
    return db.query(Alert).filter(Alert.user_id == user.id)\
             .order_by(Alert.created_at.desc()).all()

@router.get("/unread", response_model=List[AlertResponse])
def get_unread_alerts(db: Session = Depends(get_db)):
    """Retrieve only alerts that haven't been read[cite: 39, 42]."""
    user = get_demo_user(db)
    return db.query(Alert).filter(Alert.user_id == user.id, Alert.is_read == False)\
             .order_by(Alert.created_at.desc()).all()

@router.post("/mark-read")
def mark_alert_as_read(request: MarkReadRequest, db: Session = Depends(get_db)):
    """Update an alert's status to read[cite: 40]."""
    user = get_demo_user(db)
    alert = db.query(Alert).filter(Alert.id == request.alert_id, Alert.user_id == user.id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_read = True
    db.commit()
    return {"message": "Alert marked as read"}