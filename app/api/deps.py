from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User # Ensure this import is correct
import os

# Ensure this matches your auth.py secret key exactly!
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # --- DEBUGGING PRINTS ---
    print(f"DEBUG: Token received: {token[:10]}...")
    print(f"DEBUG: Using Secret Key: {SECRET_KEY}")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"DEBUG: Decoded email from token: {email}")
        
        if email is None:
            raise credentials_exception
            
    except JWTError as e:
        print(f"DEBUG: JWT Decode Error: {e}")
        raise credentials_exception
        
    # Query database by email
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        print("DEBUG: User not found in database")
        raise credentials_exception
        
    return user