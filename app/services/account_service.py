from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate

def create_user_account(db: Session, account_data: AccountCreate, user_id: int):
    # Creates a new account linked to the provided user_id
    db_account = Account(**account_data.model_dump(), user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_user_accounts(db: Session, user_id: int):
    # Retrieves all accounts associated with a specific user
    return db.query(Account).filter(Account.user_id == user_id).all()
