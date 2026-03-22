from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertResponse(BaseModel):
    id: int
    type: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class MarkReadRequest(BaseModel):
    alert_id: int