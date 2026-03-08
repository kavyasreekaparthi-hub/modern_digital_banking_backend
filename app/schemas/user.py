from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- 1. USER IDENTITY SCHEMAS ---

# This is used for POST /auth/register
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

# This is used for user responses (Security: No password returned)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    kyc_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- 2. AUTHENTICATION SCHEMAS ---

# This matches the OAuth2 standard for the login response
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# --- 3. INTELLIGENCE ENGINE SCHEMAS ---

# This is used for POST /api/reports/rules
# This is what fixed your ImportError!
class CategoryRuleCreate(BaseModel):
    pattern: str
    category: str
    match_type: str  # e.g., "exact", "partial", "keyword"

    class Config:
        from_attributes = True

# Used for returning rule details to the user
class CategoryRuleOut(BaseModel):
    id: int
    keyword: str
    category: str
    rule_type: str

    class Config:
        from_attributes = True