from pydantic import BaseModel
from typing import Optional

class RewardBase(BaseModel):
    name: str
    points_cost: int
    description: Optional[str] = None
    is_active: bool = True

class RewardUpdate(BaseModel):
    """
    Schema for PATCH/PUT operations. 
    All fields are optional so you can update individual attributes 
    without needing to provide the full object.
    """
    name: Optional[str] = None
    points_cost: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class RewardResponse(RewardBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True