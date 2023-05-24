import random

from django.core.mail import get_connection, EmailMessage
from django.template.loader import get_template

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

        msg = EmailMessage(
            subject, message_url, email_from, [recipient_email], connection=connection
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

    return


def generate_activation_code():
    """Генерация кода проверки"""
    return int("".join([str(random.randint(0, 9)) for _ in range(6)]))


def send_verification_mail(email):
    """Отправка email с проверочным кодом"""
    generated_code = generate_activation_code()
    ctx = {"code": generated_code}

    message = get_template("letter-code.html").render(ctx)

    send_emails(recipient_email=email, message_url=message)
    return generated_code
