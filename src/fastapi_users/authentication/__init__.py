from src.fastapi_users.authentication.authenticator import Authenticator
from src.fastapi_users.authentication.backend import AuthenticationBackend
from src.fastapi_users.authentication.strategy import JWTStrategy, Strategy

try:
    from fastapi_users.authentication.strategy import RedisStrategy
except ImportError:  # pragma: no cover
    pass

from src.fastapi_users.authentication.transport import (
    BearerTransport,
    CookieTransport,
    Transport,
)

__all__ = [
    "Authenticator",
    "AuthenticationBackend",
    "BearerTransport",
    "CookieTransport",
    "JWTStrategy",
    "RedisStrategy",
    "Strategy",
    "Transport",
]
