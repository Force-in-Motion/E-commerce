import bcrypt
from app.models.user import User as User_model
from app.tools import HTTPErrors


class AuthUtils:

    @classmethod
    def hash_password(cls, password: str) -> bytes:
        """
        Хэширует полученный пароль
        :param password: Пароль в виде строки
        :return: Пароль в байтах
        """
        return bcrypt.hashpw(
            password=password.encode(),
            salt=bcrypt.gensalt(),
        )

    @classmethod
    def check_password(
        cls,
        password: str,
        hashed_password,
    ) -> bool:
        """
        Сравнивает полученный пароль пользователя с захешированным его паролем из БД
        :param password: Полученный от пользователя пароль
        :param hash_password: Пароль пользователя из БД
        :return: bool
        """
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )

    @classmethod
    def check_user_status(
        cls,
        user_model: User_model,
    ) -> bool:
        """

        :param param:
        :param param:
        :return:
        """
        return user_model.is_active

    @classmethod
    def check_token_type(
        cls,
        payload: dict,
        token_type: str,
    ) -> bool:
        """
        Проверяет тип полученного токена на соответствие тому, который указан в полученном payload
        :param payload: Полезная нагрузка, полученная из токена
        :return: bool
        """
        if payload.get("type") == token_type:
            return True

        return False
