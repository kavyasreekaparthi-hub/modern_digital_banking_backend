from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
    
    class Config:
        from_attributes = True 