import asyncio
from pydantic import EmailStr

from app.celery.app import celery
from app.celery.service import MessagesService


@celery.task
def send_msg_to_email_task(
    key: str,
    to_email: EmailStr,
):
    """

    :param param:
    :param param:
    :return:
    """
    asyncio.run(MessagesService.send_msg_to_email(key=key, to_email=to_email))


#  celery -A app.celery.app.celery flower --port=5555

# celery -A app.celery.app worker --loglevel=info --concurrency=4
