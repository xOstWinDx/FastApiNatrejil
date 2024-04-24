from src.fastapi_users.authentication import CookieTransport, AuthenticationBackend
from src.fastapi_users.authentication import JWTStrategy
from ..config import settings
cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

SECRET = settings.SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
