import smtplib
from email.message import EmailMessage
from celery import Celery
from decouple import config


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')

def verification_code(user_email: str, code: str):
    email = EmailMessage()
    email["Subject"] = "Account verification"
    email["From"] = config("EMAIL_HOST")
    email["To"] = user_email
    
    email.set_content(
        f"Here is your code: {code}\nEnter verification code on this link: http://127.0.0.1:8000/docs#/Auth/profile_activation_api_v1_auth_confirm_post"
    )
    return email

@celery.task
def send_email_confirmation(user_email: str, code: str):
    email = verification_code(user_email, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(config("EMAIL_HOST"), config("EMAIL_PASSWORD"))
        server.send_message(email)
        

def recovery_code(user_email: str, code: str):
    email = EmailMessage()
    email["Subject"] = "Account recovery"
    email["From"] = config("EMAIL_HOST")
    email["To"] = user_email
    
    email.set_content(
        f"Here is your code: {code}\nEnter recovery code on this link: http://127.0.0.1:8000/docs#/Auth/profile_set_new_password_api_v1_auth_password_recovery_post"
    )
    
@celery.task
def send_email_recovery(user_email: str, code: str):
    email = recovery_code(user_email, code)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(config("EMAIL_HOST"), config("EMAIL_PASSWORD"))
        server.send_message(email)