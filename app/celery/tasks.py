import aiosmtplib
from email.message import EmailMessage

from app.celery.app import celery
from app.core.config import SMTPSettings
from app.schemas.message import Message

def create_message(message: Message) -> EmailMessage:
    """
    Создает письмо из полученных компонентов схемы
    :param message_scheme: Схема письма для отправки клиенту
    :param subject:
    :return:
    """
    message = EmailMessage()
    message["From"] = message.from_email 
    message["To"] = message.to_email                      
    message["Subject"] = message.theme_msg             
    message.set_content(message.body_msg)                   

    return message

@celery.task
def send_email_task(message: EmailMessage) -> dict:
    """
    
    :param param:
    :param param:
    :return:
    """
    aiosmtplib.send(
        message,
        hostname=SMTPSettings.hostname,
        port=SMTPSettings.port,
        username=SMTPSettings.username,
        password=SMTPSettings.password,
        start_tls=SMTPSettings.start_tls,
    )

    return {'response': f"Message : {message} sent to {message.to_email}"}