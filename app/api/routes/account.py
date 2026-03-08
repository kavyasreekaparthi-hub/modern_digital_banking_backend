from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction, User
from app.schemas.transaction import TransactionCreate
from app.api.deps import get_current_user
from app.services.rule_engine import RuleEngine

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new transaction, runs it through the Intelligence Engine, 
    and links it to the authenticated user.
    """
    
    # 1. INTELLIGENCE ENGINE: Categorize based on description
    assigned_category = RuleEngine.match_category(
        transaction_in.description, 
        db, 
        current_user.id
    )

    # 2. DATA PREPARATION: Map Pydantic schema to Database columns
    txn_data = transaction_in.model_dump() if hasattr(transaction_in, 'model_dump') else transaction_in.dict()
    
    # Handle Aliases (Cleaning data for the DB)
    if "txn_type" in txn_data: txn_data["transaction_type"] = txn_data.pop("txn_type")
    if "txn_date" in txn_data: txn_data["transaction_date"] = txn_data.pop("txn_date")

    # 3. CRITICAL CLEANING: Remove extra fields to prevent SQL errors
    txn_data.pop("category", None)
    txn_data.pop("account_id", None) 

    # 4. SAVE: Link to current user and save to DB
    try:
        new_txn = Transaction(
            **txn_data,
            user_id=current_user.id,
            category=assigned_category
        )
        
        db.add(new_txn)
        db.commit()
        db.refresh(new_txn)
        return new_txn
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transaction processing failed: {str(e)}"
        )

@router.get("/")
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetch all transactions specifically for the logged-in user."""
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).all()