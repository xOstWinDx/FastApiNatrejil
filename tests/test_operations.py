from httpx import AsyncClient
from conftest import async_session_maker
from sqlalchemy import insert
from src.auth.models import User


async def test_add_user(ac: AsyncClient):
    async with async_session_maker() as session:
        stmt = insert(User).values(id=0, email='Starkatya0@yandex.ru', username='BO$$', hashed_password="",
                                   is_active=True,
                                   is_superuser=True, is_verified=True, role_id=1)

        await session.execute(stmt)
        await session.commit()


async def test_add_specific_operation(ac: AsyncClient):
    response = await ac.post('/operations/', json=
    {
        "type": "SOLD",
        "quantity": "234",
        "date": "2024-04-08T22:49:34.510",
        "user_id": 0
    })
    assert response.status_code == 200
