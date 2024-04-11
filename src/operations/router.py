import time

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from src.auth.base_config import current_user_optional
from src.auth.models import User
from src.operations.schemas import Operations as PDOperations
from src.operations.models import Operations

from src.database import get_async_session
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)


@router.get('/')
@cache(expire=60)
async def get_operations(operation_type: str,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user_optional)):
    if user is None:
        return RedirectResponse('/')
    query = select(Operations).where(and_(Operations.type == operation_type.strip(), Operations.user_id == user.id))
    res = await session.execute(query)

    return res.scalars().all()


@router.post('/')
async def add_operations(new_operation: PDOperations, session: AsyncSession = Depends(get_async_session)):
    data = {**new_operation.model_dump()}
    data['type'] = data['type'].strip()
    query = insert(Operations).values(**data)
    await session.execute(query)
    await session.commit()
    return {'message': 'success'}
