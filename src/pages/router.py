from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from src.operations.router import get_operations


router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/search/{operation_type}")
def get_search_page(request: Request, operations=Depends(get_operations)):
    return templates.TemplateResponse("main_page.html", {"request": request, "operations": operations})
