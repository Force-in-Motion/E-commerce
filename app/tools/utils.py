import jwt
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


class JWTUtils:

    @staticmethod
    async def jwt_encode(
        payload: dict,
        private_key: str = JWTSettings.private_key.read_text(),
        algoritm: str = JWTSettings.algoritm,
    ):
        """
        Кодирует (подписывает) данные payload в JWT-токен.
        :param param:
        :param param:
        :return:
        """
        return jwt.encode(
            payload=payload,
            key=private_key,
            algorithm=algoritm,
        )

    @staticmethod
    async def jwt_decode(
        jwt_token,
        public_key: str = JWTSettings.public_key.read_text(),
        algoritm=JWTSettings.algoritm,
    ):
        """
        Декодирует (проверяет) JWT-токен и возвращает payload.
        :param param:
        :param param:
        :return:
        """
        return jwt.decode(
            token=jwt_token,
            key=public_key,
            algorithms=[algoritm],
        )
