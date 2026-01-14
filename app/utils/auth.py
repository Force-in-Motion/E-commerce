import bcrypt
from pydantic import SecretStr
from app.models.user import User as User_model



class AuthUtils:

    @staticmethod
    def hash_password(password: SecretStr) -> bytes:
        """
        Хэширует полученный пароль
        :param password: Пароль в виде строки
        :return: Пароль в байтах
        """
        return bcrypt.hashpw(
            password=password.get_secret_value().encode(),
            salt=bcrypt.gensalt(),
        )

    @staticmethod
    def check_password(
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

    @staticmethod
    def check_user_status(user_model: User_model) -> bool:
        """

        :param param:
        :param param:
        :return:
        """
        return user_model.is_active

    @staticmethod
    def check_token_type(
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
