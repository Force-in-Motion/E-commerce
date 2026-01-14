import aiosmtplib
from pydantic import EmailStr

from app.core.config import smtp_settings
from app.utils.email import EmailUtils


class MessagesService:
    """Класс, содержащий фоновые задачи для отправки сообщений пользователю"""

    @classmethod
    async def send_msg_to_email(
        cls,
        key: str,
        to_email: EmailStr,
    ) -> dict:
        """

        :param param:
        :param param:
        :return:
        """
        email_message = EmailUtils.create_email_message(
            key=key,
            to_email=to_email,
            from_email=smtp_settings.username,
        )

        await aiosmtplib.send(
            email_message,
            hostname=smtp_settings.hostname,
            port=smtp_settings.port,
            username=smtp_settings.username,
            password=smtp_settings.password,
            start_tls=smtp_settings.start_tls,
        )
