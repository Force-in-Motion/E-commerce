from datetime import datetime, timedelta, timezone
import jwt
from app.models import User as User_model
from app.core import jwt_settings



class JWTUtils:
    """Содержит служебные утилиты для работы с jwt токеном"""

    @classmethod
    def expire_jwt(
        cls,
        expire_minuts: int,
    ) -> dict:
        """
        Возвращает время действия refresh  или access токена
        :param expire_minuts: Определяет время действия токена в минутах в зависимости от от переданных настроек
        :return: время действия токена в минутах и текущее время
        """
        now = datetime.now(timezone.utc)

        expire = now + timedelta(minutes=expire_minuts)

        return {
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
        }

    
    @classmethod
    def create_jwt(
        cls,
        user_model: User_model,
        token_type: str,
        expire_minuts: int,
    ) -> str:
        """
        Создает access или refresh токен, в записимости от полученного типа и срока действия
        :param user: схема пользователя с данными изи БД
        :return: Закодированный токен
        """
        payload = {
            "type": token_type,
            "sub": str(user_model.id),
            "role": user_model.role,
            "is_active": user_model.is_active,
        }

        payload.update(cls.expire_jwt(expire_minuts=expire_minuts))

        return cls.encode_jwt(payload)
    

    @classmethod
    def encode_jwt(
        cls,
        payload: dict,
    ) -> str:
        """
        Собирает токен из полученных данных и кодирует его в base64
        :param payload: Полезная нагрузка, данные, которые должны быть переданы в токене
        :return: Готовый закодированный токен
        """
        token = jwt.encode(
            payload=payload,
            key=jwt_settings.private_key.read_text(),
            algorithm=jwt_settings.algorithm,
        )

        return token

    @classmethod
    def decode_jwt(
        cls,
        token: str,
    ) -> str:
        """
        Декодирует полученный токен
        :param token: Закодированный в base64 токен
        :return: Раскодированные данные, переданные в токене payload
        """
        payload = jwt.decode(
            jwt=token,
            key=jwt_settings.public_key.read_text(),
            algorithms=[jwt_settings.algorithm],
        )

        return payload


    @classmethod
    def create_access_token(cls, user_model: User_model) -> str:
        """
        Создает конкретно access_token
        :param user: схема пользователя с данными изи БД
        :return: access_token
        """
        return cls.create_jwt(
            user_model=user_model,
            token_type=jwt_settings.access_name,
            expire_minuts=jwt_settings.access_token_expire,
        )

    @classmethod
    def create_refresh_token(cls, user_model: User_model) -> str:
        """
        Создает конкретно refresh_token
        :param user: схема пользователя с данными изи БД
        :return: refresh_token
        """
        return cls.create_jwt(
            user_model=user_model,
            token_type=jwt_settings.refresh_name,
            expire_minuts=jwt_settings.refresh_token_expire,
        )
