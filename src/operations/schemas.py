from datetime import datetime

from pydantic import BaseModel



class Operations(BaseModel):
    __tablename__ = 'operations'
    id: int
    quantity: str
    figi: str
    date: datetime
    type: str
    user_id:int