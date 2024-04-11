from src.fastapi_users import FastAPIUsers
from src.fastapi_users.authentication import AuthenticationBackend,CookieTransport, JWTStrategy

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import settings

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user_optional = fastapi_users.current_user(optional=True)
current_user = fastapi_users.current_user()
current_user_verified = fastapi_users.current_user(verified=True, optional=True)
