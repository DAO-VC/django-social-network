import random

from django.core.mail import get_connection, EmailMessage

from main import settings


def send_emails(recipient_email: str, message_url: str):
    """Простейшая функция отправки сообщений"""
    with get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls=settings.EMAIL_USE_TLS,
    ) as connection:
        subject = "DAO"
        email_from = settings.EMAIL_HOST_USER

        EmailMessage(
            subject, message_url, email_from, [recipient_email], connection=connection
        ).send()

    return


def generate_activation_code():
    return int("".join([str(random.randint(0, 10)) for _ in range(6)]))


def send_verification_mail(email):
    generated_code = generate_activation_code()
    subject = "DAO verification code"
    message = f"Your verification code:\n{generated_code}\nThanks for using DAO."
    send_emails(recipient_email=email, message_url=message)
    return generated_code
