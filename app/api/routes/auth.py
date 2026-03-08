from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from app.database import get_db
from app.models import User
from app.schemas.user import UserCreate
# Importing both hashing and verification functions
from app.core.security import get_password_hash, verify_password

SECRET_KEY = "your-secret-key-here" 
ALGORITHM = "HS256"

router = APIRouter()

# --- Registration Endpoint ---
@router.post("/register", status_code=201) 
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Registers a new user including profile details."""
    
    # 1. Check if user already exists
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Create new user with hashed password
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
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Secure Verification: Compares raw password with the stored hash
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    # Generate the JWT Token
    access_token = jwt.encode({"sub": user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}