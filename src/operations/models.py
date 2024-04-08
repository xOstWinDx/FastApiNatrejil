from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship, relationship
from sqlalchemy import ForeignKey, TIMESTAMP, Column
from enum import Enum

from src.auth.models import User


class Base(DeclarativeBase):
    pass


class OpType(Enum):
    SELL = 'SOLD'
    BUY = 'BUY'
    SEND = 'SEND'
    SPEND = 'SPEND'


class Operations(Base):
    __tablename__ = 'operations'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[OpType] = mapped_column(nullable=False)
    quantity: Mapped[str] = mapped_column(nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)

    user: Mapped[User] = relationship()
