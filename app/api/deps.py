from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

# This scheme is required for Swagger UI to show the 'Authorize' padlock
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    PRESENTATION OVERRIDE:
    Bypasses JWT validation entirely to ensure the demo is not blocked.
    Always returns the first user found in the database.
    """
    user = db.query(User).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found in database to simulate login."
        )
        
    return user