from typing import AsyncGenerator, Annotated
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.config import settings

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)

class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker(engine)() as session:
        yield session
