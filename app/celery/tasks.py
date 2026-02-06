import asyncio
from pydantic import EmailStr

from app.celery.app import celery
from app.service.message import MessagesService


@celery.task
def send_msg_to_email_task(
    key: str, 
    user_email: EmailStr,
) -> None:
    """
    Создает задачу на откравку письма на почту пользователя
    :param key: Название метода, где была поставлена задача,
    название метода так же является ключем словаря с текстом письма пользователю,
    хранящимся в файле template.yaml
    :param user_email: адрес почты, на который задача отправляет письмо
    :return: Словарь с результатом выполнения задачи
    """
    asyncio.run(MessagesService.send_msg_to_email(key=key, user_email=user_email))


#  celery -A app.celery.app.celery flower --port=5555

# Запуск воркеров стандартным способом через delay 
# celery -A app.celery.app worker --loglevel=info --concurrency=4

# Запуск воркеров через celery.conf.beat_schedule
# celery -A app.core.celery worker --beat --loglevel=info --concurrency=4
