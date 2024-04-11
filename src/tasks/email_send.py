from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from src.auth.base_config import current_user
from src.tasks.tasks import send_email_report_dashboard


def get_dashboard_report(user=Depends(current_user)):
    if current_user is None:
        return HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    send_email_report_dashboard.delay(user.username, user.email)

