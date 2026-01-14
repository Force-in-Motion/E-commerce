import asyncio
from pydantic import EmailStr

from app.celery.app import celery
from app.celery.service import MessagesService


@celery.task
def send_msg_to_email_task(
    key: str,
    to_email: EmailStr,
) -> dict:
    """
    Создает задачу на откравку письма на почту пользователя
    :param key: Название метода, где была поставлена задача,
    название метода так же является ключем словаря с текстом письма пользователю, 
    хранящимся в файле template.yaml
    :param to_email: адрес почты, куда задача отправляет письмо
    :return: Словарь с результатом выполнения задачи
    """
    asyncio.run(MessagesService.send_msg_to_email(key=key, to_email=to_email))

    return {
        "status": "SUCCESS",
        "message": f"Письмо отправлено на {to_email}",
        "called": key,
    }


#  celery -A app.celery.app.celery flower --port=5555

# celery -A app.celery.app worker --loglevel=info --concurrency=4
