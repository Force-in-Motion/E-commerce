import yaml
from pydantic import EmailStr
from email.message import EmailMessage

from app.schemas import EmailScheme
from app.core.config import PROJECT


class EmailUtils:
    """Содержит служебные утилиты для работы с фоновыми задачами токеном"""

    @classmethod
    def _read_text(cls) -> dict:
        """
        Считывает данные из templates.yaml , преобразует в словарь
        :return: словарь с данными
        """
        with open(PROJECT / "templates.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)  # преобразует YAML в dict Python

    @classmethod
    def _email(cls, email_scheme: EmailScheme) -> EmailMessage:
        """
        Формирует данные письма из полученных компонентов схемы
        :param message_scheme: Схема письма для отправки клиенту
        :return: готовое сообщение
        """
        data = email_scheme.model_dump()

        message = EmailMessage()
        message["From"] = data.get("service_email")
        message["To"] = data.get("user_email")
        message["Subject"] = data.get("theme_msg")
        message.set_content(data.get("body_msg"))

        return message

    @classmethod
    def create_email_message(
        cls,
        key: str,
        user_email: EmailStr,
        service_email: EmailStr,
    ) -> EmailMessage:
        """
        Создает письмо для отправки на email
        :param key: Ключ словаря, служит для получения данных, отправляемых в письме
        :param user_email: почта, на которую отправляется письмо
        :param service_email: сервисная почта, с которой отправляется письмо
        :param subject:
        :return:
        """
        templates = cls._read_text()

        data = templates.get(key)

        email_scheme = EmailScheme(
            user_email=user_email,
            service_email=service_email,
            theme_msg=data.get("theme_msg"),
            body_msg=data.get("body_msg").format(username=user_email),
        )

        return cls._email(email_scheme=email_scheme)
