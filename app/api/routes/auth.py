from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# --- Registration Endpoint ---
@router.post("/register", status_code=status.HTTP_201_CREATED) 
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user and hashes their password."""
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        name=user_in.name,
        phone=user_in.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "email": new_user.email}

# --- Login Endpoint ---
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Handles login by verifying hashed credentials and issuing a JWT."""
    
    # 1. Fetch user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # 2. Secure Verification
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    # 3. Generate the JWT Token
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Corrected payload syntax: Using dictionary curly braces
    payload = {
        "sub": str(user.id), 
        "email": user.email,
        "exp": expire
    } 
    
    access_token = jwt.encode(
        payload, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- Milestone 4 Helper Function ---
def get_demo_user(db: Session):
    """
    Helper function for Milestone 4 to provide a 'current_user' 
    without requiring a real JWT token during testing.
    Essential for logic-heavy services like Insights and Alerts.
    """
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No users found in database. Please register a user first."
        )
    return user