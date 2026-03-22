from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
from fastapi.security import HTTPBearer # New import

# 1. Setup Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Setup Security Scheme (Replaces OAuth2PasswordBearer)
security_scheme = HTTPBearer()

# 3. Secret Keys for JWT
SECRET_KEY = "your-secret-key-here" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    """
    Hashes a password with bcrypt. 
    Truncates to 72 bytes to avoid bcrypt's hard limit and 
    associated ValueErrors.
    """
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(truncated_password)

def verify_password(plain_password: str, hashed_password: str):
    truncated_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(truncated_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt