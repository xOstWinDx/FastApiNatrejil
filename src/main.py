from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache

from fastapi_cache.backends.redis import RedisBackend
from fastapi.responses import RedirectResponse
from redis import asyncio as aioredis
from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from src.auth.base_config import current_user_verified
from src.pages.router import router as search_router

from src.auth.base_config import fastapi_users
from src.reg.router import router as router_reg
from src.operations.router import router as router_operation
from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.schemas import UserCreate, UserRead
from fastapi.templating import Jinja2Templates
from src.config import settings

from src.auth.routers import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)

app.include_router(router_reg)
app.include_router(router_auth)
app.include_router(search_router)

templates = Jinja2Templates(directory="src/templates")

origins = [
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")


@app.get("/")
def main_page(request: Request = None, user: User = Depends(current_user_verified)):
    if user is None:
        return RedirectResponse('/auth/')
    else:
        return templates.TemplateResponse("main_page.html", {"request": request})
