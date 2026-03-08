from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from ..database import Base
import datetime

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, default="budget_exceeded")
    message = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)