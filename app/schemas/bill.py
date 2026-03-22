from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class BillBase(BaseModel):
    biller_name: str = Field(..., min_length=1)  # Ensure not empty
    amount_due: float = Field(..., gt=0)         # Ensure positive
    due_date: date
    auto_pay: bool = False

class BillCreate(BillBase):
    pass

class BillUpdate(BaseModel):
    biller_name: Optional[str] = None
    amount_due: Optional[float] = Field(None, gt=0)
    due_date: Optional[date] = None
    status: Optional[str] = None
    auto_pay: Optional[bool] = None

class BillResponse(BillBase):
    id: int
    user_id: int
    status: str

    class Config:
        from_attributes = True