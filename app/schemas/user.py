from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- 1. USER IDENTITY SCHEMAS ---

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None  # Now correctly defined

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    kyc_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- 2. AUTHENTICATION SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- 3. INTELLIGENCE ENGINE SCHEMAS ---

class CategoryRuleCreate(BaseModel):
    keyword_pattern: str  # Updated to match the attribute name in models.py
    category: str
    match_type: Optional[str] = "partial" # Defaulting for easier API usage

    class Config:
        from_attributes = True

class CategoryRuleOut(BaseModel):
    id: int
    keyword_pattern: str
    category: str
    match_type: str

    class Config:
        from_attributes = True