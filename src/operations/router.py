from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.operations.schemas import Operations as PDOperations
from src.operations.models import Operations

from src.database import get_async_session

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)


@router.get('/')
async def get_operations(session: AsyncSession = Depends(get_async_session)):
    query = select(Operations)
    res = await session.execute(query)
    return res.scalars().all()


@router.post('/')
async def add_operations(new_operation: PDOperations, session: AsyncSession = Depends(get_async_session)):
    query = insert(Operations).values(**new_operation.dict())
    await session.execute(query)
    await session.commit()
    return {'message': 'success'}
