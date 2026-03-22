from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.reward import Reward
from app.models.bill import Bill
from app.models.user import User
from app.schemas.reward import RewardResponse, RewardUpdate

router = APIRouter(tags=["Rewards Tracking"])

# Helper to ensure we have a user context for the demo
def get_demo_user(db: Session):
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No users found. Register via /auth/register first."
        )
    return user

@router.get("/balance", response_model=dict)
def get_rewards_balance(db: Session = Depends(get_db)):
    """
    Calculates total reward points based on paid bills for the demo user.
    """
    user = get_demo_user(db)
    
    # Counting paid bills
    paid_bills_count = db.query(Bill).filter(
        Bill.user_id == user.id, 
        Bill.status == "paid" 
    ).count()
    
    return {
        "user_id": user.id,
        "paid_bills": paid_bills_count,
        "points_balance": paid_bills_count * 10
    }

@router.get("/", response_model=List[RewardResponse])
def get_all_rewards(db: Session = Depends(get_db)):
    """Retrieve all reward programs associated with the demo user."""
    user = get_demo_user(db)
    return db.query(Reward).filter(Reward.user_id == user.id).all()

@router.put("/{reward_id}", response_model=RewardResponse)
def update_reward_program(
    reward_id: int, 
    reward_update: RewardUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update metadata for a specific reward program for the demo user.
    Uses model_dump(exclude_unset=True) for flexible partial updates.
    """
    user = get_demo_user(db)
    reward = db.query(Reward).filter(
        Reward.id == reward_id, 
        Reward.user_id == user.id
    ).first()
    
    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Reward program not found"
        )
    
    # Map the update dictionary, excluding unset fields
    # This automatically maps JSON fields like 'points_cost' to the reward model
    update_data = reward_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reward, key, value)
    
    db.commit()
    db.refresh(reward)
    return reward