import yaml
from pydantic import EmailStr
from email.message import EmailMessage

from app.schemas import EmailScheme
from app.core.config import PROJECT
from app.core import smtp_settings


class EmailUtils:
    """Содержит служебные утилиты для работы с фоновыми задачами токеном"""

    @classmethod
    def _read_text(cls) -> dict:
        """

        :param param:
        :param param:
        :return:
        """
        with open(PROJECT / "templates.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)  # преобразует YAML в dict Python

    @classmethod
    def _email(email_scheme: EmailScheme) -> EmailMessage:
        """
        Создает письмо из полученных компонентов схемы
        :param message_scheme: Схема письма для отправки клиенту
        :param subject:
        :return:
        """
        data = email_scheme.model_dump()

        message = EmailMessage()
        message["From"] = data.get("from_email")
        message["To"] = data.get("to_email")
        message["Subject"] = data.get("theme_msg")
        message.set_content(data.get("body_msg"))

        return message

    @classmethod
    def create_email_message(
        cls,
        key: str,
        to_email: EmailStr,
        from_email: EmailStr,
    ) -> EmailMessage:
        """
        Создает письмо из полученных компонентов схемы
        :param message_scheme: Схема письма для отправки клиенту
        :param subject:
        :return:
        """
        templates = cls._read_text()

        data = templates.get(key)

        email_scheme = EmailScheme(
            from_email=from_email,
            to_email=to_email,
            theme_msg=data.get("theme_msg"),
            body_msg=data.get("body_msg").format(username=to_email),
        )

        return cls._email(email_scheme=email_scheme)
