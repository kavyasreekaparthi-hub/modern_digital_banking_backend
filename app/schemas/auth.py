from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

# If you have a Login model, it usually lives here too:
class LoginRequest(BaseModel):
    username: str
    password: str