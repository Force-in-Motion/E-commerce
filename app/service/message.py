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
        user_email: EmailStr,
    ) -> dict:
        """
        Отправляет письмо на полученный email
        :param key: Ключ словаря, служит для получения данных, отправляемых в письме
        :param user_email: почта, на которую отправляется письмо
        :return: Словарь с данными об успешной отправке
        """

        email_message = EmailUtils.create_email_message(
            key=key,
            user_email=user_email,
            service_email=smtp_settings.username,
        )

        await aiosmtplib.send(
            email_message,
            hostname=smtp_settings.hostname,
            port=smtp_settings.port,
            username=smtp_settings.username,
            password=smtp_settings.password,
            start_tls=smtp_settings.start_tls,
        )

        return {
            "status": "SUCCESS",
            "message": f"Письмо отправлено на {user_email}",
            "called": key,
        }
