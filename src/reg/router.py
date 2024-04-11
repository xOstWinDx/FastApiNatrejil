from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.base_config import current_user_optional
from src.auth.models import User

router = APIRouter(
    prefix='/reg',
    tags=['auth']
)
templates = Jinja2Templates(directory="src/templates")


@router.get('/')
def reg(request: Request, user:User = Depends(current_user_optional)):
    if user is not None:
        return RedirectResponse('/')
    return templates.TemplateResponse("register.html", {"request": request})
