from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate

def create_user_account(db: Session, account_data: AccountCreate, user_id: int):
    db_account = Account(**account_data.model_dump(), user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_user_accounts(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()