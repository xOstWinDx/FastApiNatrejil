from typing import Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from src.fastapi_users import models
from src.fastapi_users.authentication import AuthenticationBackend, Authenticator, Strategy
from src.fastapi_users.manager import BaseUserManager, UserManagerDependency
from src.fastapi_users.openapi import OpenAPIResponseType
from src.fastapi_users.router.common import ErrorCode, ErrorModel


def get_auth_router(
        backend: AuthenticationBackend,
        get_user_manager: UserManagerDependency[models.UP, models.ID],
        authenticator: Authenticator,
        requires_verification: bool = False,
) -> APIRouter:
    """Generate a router with login/logout routes for an authentication backend."""
    router = APIRouter()
    get_current_user_token = authenticator.current_user_token(
        active=True, verified=requires_verification
    )

    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post(
        "/login",
        name=f"auth:{backend.name}.login",
        responses=login_responses,
    )
    async def login(
            request: Request,
            credentials: OAuth2PasswordRequestForm = Depends(),
            user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
            strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        user = await user_manager.authenticate(credentials)
        templates = Jinja2Templates(directory="src/templates")
        if user is None or not user.is_active:
            error = 'LOGIN_BAD_CREDENTIALS'
            response = Response()
            response.set_cookie(key='error', value='LOGIN_BAD_CREDENTIALS', max_age=5)
            response.status_code = 303
            response.headers["Location"] = "http://127.0.0.1:8000/"
            return response

        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/logout", name=f"auth:{backend.name}.logout", responses=logout_responses
    )
    async def logout(
            user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
            strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        user, token = user_token
        res = await backend.logout(strategy, user, token)
        res.status_code = 303
        res.headers["Location"] = "http://127.0.0.1:8000/"
        return res

    return router
