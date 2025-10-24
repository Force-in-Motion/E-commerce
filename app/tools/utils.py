from functools import wraps
import jwt
from typing import Callable

from app.core.config import JWTSettings


class Utils:

    @staticmethod
    def singleton(cls):
        instance = None

        class Wrapper(cls):
            def __new__(cls_, *args, **kwargs):
                nonlocal instance
                if instance is None:
                    instance = super().__new__(cls_, *args, **kwargs)
                else:
                    raise Exception(f"Instance of {cls.__name__} already created")
                return instance

        return Wrapper


class JWTOperations:

    @staticmethod
    async def jwt_encode(
        payload: dict,
        privat_key: str = JWTSettings.private_key.read_text(),
        algoritm: str = JWTSettings.algoritm,
    ):
        """
        Кодирует токен
        :param param:
        :param param:
        :return:
        """
        return jwt.encode(
            payload=payload,
            key=privat_key,
            algorithm=algoritm,
        )

    @staticmethod
    async def jwt_decode(
        token,
        public_key: str = JWTSettings.public_key.read_text(),
        algoritm=JWTSettings.algoritm,
    ):
        """
        Кодирует токен
        :param param:
        :param param:
        :return:
        """
        return jwt.decode(
            token=token,
            key=public_key,
            algorithms=[algoritm],
        )
