from fastapi import APIRouter, Depends

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from src.auth.base_config import current_user_verified
from src.auth.models import User

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
templates = Jinja2Templates(directory="src/templates")

@router.get('/')
def reg(request: Request, user: User = Depends(current_user_verified)):
    if user is not None:
        return RedirectResponse('/')
    error = request.cookies.get('error', '')
    return templates.TemplateResponse("auth.html", {"request": request, "error": error})
