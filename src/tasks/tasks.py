import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
from starlette.templating import Jinja2Templates

from src.config import settings
from email.mime.image import MIMEImage

SMTP_HOST = "smtp.yandex.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')
celery.broker_connection()
templates = Jinja2Templates(directory="src/templates")


async def get_email_template(token: str, username: str, email_address: str):
    page = templates.get_template('email.html').render({'token': token})
    email = MIMEMultipart()
    email['Subject'] = f'Специальное письмо для {username}'
    email['From'] = settings.SMTP_USER
    email['To'] = email_address
    email.attach(MIMEText(page, 'html', 'utf-8'))
    return email


@celery.task
async def send_email_report_dashboard(token: str, username: str, email_address: str):
    email = await get_email_template(token, username, email_address)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
