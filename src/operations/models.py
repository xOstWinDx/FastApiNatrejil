from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship, relationship
from sqlalchemy import ForeignKey, TIMESTAMP, Column
from enum import Enum

from src.auth.models import User
from src.database import Base


class Operations(Base):
    __tablename__ = 'operations'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    quantity: Mapped[str] = mapped_column(nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    figi: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id,ondelete='CASCADE'), nullable=False)

    user: Mapped[User] = relationship()
