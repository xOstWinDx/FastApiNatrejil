from typing import Optional

from fastapi import Depends, Request
from src.fastapi_users import BaseUserManager, IntegerIDMixin, models, schemas
from ..fastapi_users import exceptions
from src.fastapi_users.models import UP
from starlette.responses import Response
from ..config import settings
from src.auth.models import User, get_user_db
from src.tasks.tasks import send_email_report_dashboard

SECRET = settings.SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UP, request: Optional[Request] = None):
        await self.request_verify(user, request)

    async def on_after_login(self, user: User, request: Optional[Request] = None, response: Response = None):
        response.status_code = 303
        response.headers["Location"] = "http://127.0.0.1:8000/"
        response.set_cookie(key='error', value='', max_age=1)

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        await send_email_report_dashboard(token, user.username, user.email)


    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
