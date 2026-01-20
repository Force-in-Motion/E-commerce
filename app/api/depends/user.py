from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import jwt_settings
from app.tools import HTTPErrors
from app.utils import JWTUtils, AuthUtils
from app.service import UserService, TokenService
from app.celery.tasks import send_msg_to_email_task
from app.models import User as User_model, RefreshToken as Refresh_model
from app.schemas import (
    UserCreate,
    UserUpdate,
    TokenResponse,
    RefreshCreate,
)


class UserDepends:

    @classmethod
    async def get_all_users(
        cls,
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает всех пользователей
        :param session: Асинхронная сессия
        :return: Список моделей пользователей
        """
        user_models = await UserService.get_all_models(session=session)

        if not user_models:
            raise HTTPErrors.not_found

        return user_models

    @classmethod
    async def get_user_by_login(
        cls,
        login: EmailStr,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает пользователя по его логину
        :param login: Логин пользователя
        :param session: Асинхронная сессия
        :return: Модель пользователя
        """
        user_model = await UserService.get_user_by_login(
            login=login,
            session=session,
        )

        if not user_model:
            raise HTTPErrors.not_found

        return user_model

    @classmethod
    async def get_user(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает пользователя по его id
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Модель пользователя
        """
        user_model = await UserService.get_model(
            model_id=user_id,
            session=session,
        )

        if not user_model:
            raise HTTPErrors.not_found

        return user_model

    @classmethod
    async def get_users_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает пользователей, добавленных в указанном временном диапазоне
        :param session: Асинхронная сессия
        :param dates: Определяет временной диапазон
        :return: Список моделей пользователей, добавленных в указанном временном диапазоне
        """
        user_models = await UserService.get_all_models_by_date(
            dates=dates,
            session=session,
        )

        if not user_models:
            raise HTTPErrors.not_found

        return user_models

    @classmethod
    async def create_user(
        cls,
        user_scheme: UserCreate,
        session: AsyncSession,
    ) -> User_model:
        """
        Создает пользователя, а так же уведомляет пользователя об этом
        :param session: Асинхронная сессия
        :param user_scheme: Схема пользователя, полученная от клиента
        :return: Модель пользователя
        """
        user_scheme.password = AuthUtils.hash_password(user_scheme.password)

        user_model = await UserService.register_model(
            scheme_in=user_scheme,
            session=session,
        )

        if not user_model:
            raise HTTPErrors.err_create_model

        send_msg_to_email_task.delay(
            key=cls.create_user.__name__,
            user_email=user_scheme.login,
        )

        return user_model

    @classmethod
    async def update_user(
        cls,
        user_id: int,
        user_scheme: UserUpdate,
        session: AsyncSession,
        partial: bool = False,
    ) -> User_model:
        """
        Изменяет данные пользователя, а так же уведомляет пользователя об этом
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :param user_scheme: Схема пользователя, полученная от клиента
        :param partial: Флаг, определяющий полное или частичное изменение данных
        :return: Модель пользователя
        """
        if user_scheme.password is not None:
            user_scheme.password = AuthUtils.hash_password(user_scheme.password)

        user_model = await UserService.update_model(
            model_id=user_id,
            scheme_in=user_scheme,
            session=session,
            partial=partial,
        )

        if not user_model:
            raise HTTPErrors.err_update_model

        send_msg_to_email_task.delay(
            key=cls.update_user.__name__,
            user_email=user_scheme.login,
        )
            
        return user_model

    @classmethod
    async def delete_user(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> User_model:
        """
        Удаляет пользователя, а так же уведомляет пользователя об этом
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Модель пользователя
        """
        user_model = await UserService.delete_model(
            model_id=user_id,
            session=session,
        )

        if not user_model:
            raise HTTPErrors.err_delete_model

        send_msg_to_email_task.delay(
            key=cls.update_user.__name__,
            user_email=user_model.login,
        )
            
        return user_model

    @classmethod
    async def clear_users(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Полностью очищает таблицу профилей
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        cleared_table = await UserService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.clear_table

        return cleared_table

    @classmethod
    async def get_refresh(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Refresh_model:
        """
        Возвращает refresh токен по id пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Модель refresh токена
        """
        refresh_model = await TokenService.get_model(
            user_id=user_id,
            session=session,
        )

        return refresh_model

    @classmethod
    async def create_refresh(
        cls,
        user_id: int,
        refresh: str,
        session: AsyncSession,
    ) -> Refresh_model:
        """
        Добавляет refresh токен по id пользователя
        :param user_id: id пользователя
        :param refresh: Токен в виде строки
        :param session: Асинхронная сессия
        :return: Модель refresh токена
        """
        refresh_schema = RefreshCreate(token=refresh)

        refresh_model = await TokenService.register_model(
            scheme_in=refresh_schema,
            user_id=user_id,
            session=session,
        )

        if not refresh_model:
            raise HTTPErrors.err_create_model

        return refresh_model

    @classmethod
    async def delete_refresh(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Refresh_model:
        """
        Удаляет refresh токен по id пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Модель refresh токена
        """
        refresh_model = await TokenService.delete_model(
            session=session,
            user_id=user_id,
        )

        if not refresh_model:
            raise HTTPErrors.err_delete_model

        return refresh_model


class UserAuth:

    @classmethod
    async def validate_user(
        cls,
        login: str,
        password: str,
        session: AsyncSession,
    ) -> User_model:
        """
        Выполняет валидацию пользователя, а так же уведомляет пользователя об этом
        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param session: Асинхронная сессия
        :return: Модель пользователя
        """
        user_model = await UserDepends.get_user_by_login(
            login=login,
            session=session,
        )

        if not AuthUtils.check_password(
            password=password,
            hashed_password=user_model.password,
        ):
            raise HTTPErrors.unauthorized

        if not AuthUtils.check_user_status(user_model=user_model):
            raise HTTPErrors.user_inactive

        send_msg_to_email_task.delay(
            key=cls.validate_user.__name__,
            user_email=login,
        )
            
        return user_model

    @classmethod
    async def create_access(
        cls,
        user_model: User_model,
    ) -> str:
        """
        Создает access токен
        :param user_model: модель пользователя с данными изи БД
        :return: access_token в виде строки
        """
        return JWTUtils.create_access_token(user_model=user_model)

    @classmethod
    async def update_refresh(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> str:
        """
        Изменяет refresh токен в БД
        :param user: схема пользователя с данными изи БД
        :return: refresh_token в виде строки
        """
        refresh = JWTUtils.create_refresh_token(user_model=user_model)

        if await UserDepends.get_refresh(
            user_id=user_model.id,
            session=session,
        ):

            await UserDepends.delete_refresh(
                user_id=user_model.id,
                session=session,
            )

        await UserDepends.create_refresh(
            user_id=user_model.id,
            refresh=refresh,
            session=session,
        )

        return refresh

    @classmethod
    async def generate_tokens(
        cls,
        user_model: User_model,
        session: AsyncSession,
        refresh_status: bool = False,
    ) -> TokenResponse:
        """
        Создает схему TokenResponse
        :param session: Асинхронная сессия
        :param user_model: Модель пользователя с данными изи БД
        :param refresh_status: Флаг, который определяет количество создаваемых токенов
        :return: Схему токенов
        """
        refresh = None

        access = await cls.create_access(user_model)

        if refresh_status:
            refresh = await cls.update_refresh(
                user_model=user_model,
                session=session,
            )

        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            token_type=jwt_settings.token_type,
        )

    @classmethod
    async def get_current_user_by_access(
        cls,
        token: str,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает модель пользователя по его access токену
        :param session: Асинхронная сессия
        :param token: Токен в виде строки
        :return: Модель пользователя
        """
        payload = JWTUtils.decode_jwt(token)

        if not AuthUtils.check_token_type(
            payload=payload,
            token_type=jwt_settings.access_name,
        ):
            raise HTTPErrors.token_invalid

        user_id = int(payload.get("sub"))

        user_model = await UserDepends.get_user(
            user_id=user_id,
            session=session,
        )

        if not AuthUtils.check_user_status(user_model=user_model):
            raise HTTPErrors.user_inactive

        return user_model

    @classmethod
    async def get_current_user_by_refresh(
        cls,
        token: str,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает модель пользователя по его refresh токену
        :param session: Асинхронная сессия
        :param token: Токен в виде строки
        :return: Модель пользователя
        """
        payload = JWTUtils.decode_jwt(token)

        if not AuthUtils.check_token_type(
            payload=payload,
            token_type=jwt_settings.refresh_name,
        ):
            raise HTTPErrors.token_invalid

        user_id = int(payload.get("sub"))

        refresh_model = await UserDepends.get_refresh(
            user_id=user_id,
            session=session,
        )

        if refresh_model is None or refresh_model.token != token:
            raise HTTPErrors.token_invalid

        user_model = await UserDepends.get_user(
            user_id=user_id,
            session=session,
        )

        if not AuthUtils.check_user_status(user_model=user_model):
            raise HTTPErrors.user_inactive

        return user_model
