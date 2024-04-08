from datetime import datetime

from pydantic import BaseModel
from src.operations.models import OpType
class Operations(BaseModel):
    __tablename__ = 'operations'
    id: int
    type: OpType
    quantity: str
    date: datetime
    user_id: int