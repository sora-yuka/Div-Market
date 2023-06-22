import smtplib
from email.message import EmailMessage
from celery import Celery
from decouple import config


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')

def verification_code(user_email: str):
    email = EmailMessage()
    email["Subject"] = "Account verification"
    email["From"] = config("EMAIL_HOST")
    email["To"] = user_email
    
    email.set_content(
        "This is verification leter, here is your code. Don't tell"
    )
    return email

@celery.task
def send_email_confirmation(user_email: str):
    email = verification_code(user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(config("EMAIL_HOST"), config("EMAIL_PASSWORD"))
        server.send_message(email)