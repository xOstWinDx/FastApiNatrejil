from typing import Optional

from src.fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class ConfigDict:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: Optional[int] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False