from pydantic import EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import jwt_settings
from app.tools import HTTPErrors
from app.service import UserService, TokenService
from app.utils import JWTUtils, AuthUtils
from app.models import User as User_model, RefreshToken as Refresh_model
from app.schemas import UserCreate, UserUpdate, TokenResponse, RefreshCreate


class UserDepends:


    @classmethod
    async def get_all_users(
        cls,
        session: AsyncSession,
    ) -> Optional[list[User_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        list_user_models = await UserService.get_all_models(session=session)

        if not list_user_models:
            raise HTTPErrors.not_found

        return list_user_models
    

    @classmethod
    async def get_user_by_login(
        cls,
        login: EmailStr,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """

        :param param:
        :param param:
        :return:
        """
        user_model = await UserService.get_user_by_login(
            login=login,
            session=session,
        )

        if not user_model:
            raise HTTPErrors.not_found

        return user_model

    @classmethod
    async def get_user_by_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """

        :param param:
        :param param:
        :return:
        """
        user_model = await UserService.get_model(
            user_id=user_id,
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
    ) -> Optional[list[User_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        list_user_models = await UserService.get_all_models_by_date(
            dates=dates,
            session=session,
        )

        if not list_user_models:
            raise HTTPErrors.not_found

        return list_user_models

    @classmethod
    async def create_user(
        cls,
        user_scheme: UserCreate,
        session: AsyncSession,
    ) -> User_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        created_user_model = await UserService.register_model(
            scheme_in=user_scheme,
            session=session,
        )

        if not created_user_model:
            raise HTTPErrors.db_error

        return created_user_model

    @classmethod
    async def get_refresh(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Refresh_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
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
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        refresh_schema = RefreshCreate(token=refresh)

        refresh_model = await TokenService.register_model(
            scheme_in=refresh,
            user_id=user_id,
            session=session,
        )

        if not refresh_model:
            raise HTTPErrors.db_error

        return refresh_model

    @classmethod
    async def delete_refresh(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Refresh_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        refresh_model = await TokenService.delete_model(
            session=session,
            user_id=user_id,
        )

        if not refresh_model:
            raise HTTPErrors.db_error

        return refresh_model

    @classmethod
    async def update_user(
        cls,
        user_id: int,
        user_scheme: UserUpdate,
        session: AsyncSession,
        partial: bool = False,
    ) -> User_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        updated_user_model = await UserService.update_model(
            model_id=user_id,
            scheme_in=user_scheme,
            session=session,
            partial=partial,
        )

        if not updated_user_model:
            raise HTTPErrors.db_error

        return updated_user_model

    @classmethod
    async def delete_user(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> User_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        deleted_user_model = await UserService.delete_model(
            model_id=user_id,
            session=session,
        )

        if not deleted_user_model:
            raise HTTPErrors.db_error

        return deleted_user_model

    @classmethod
    async def clear_users(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        cleared_table = await UserService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.db_error

        return cleared_table


class UserAuth:

    @classmethod
    async def validate_user(
        cls,
        login: str,
        password: str,
        session: AsyncSession,
    ) -> User_model:
        """
        Выполняет валидацию пользователя, если все проверки пройдены то возвращает его
        :param form_data: При помощи Depends() создается объект OAuth2PasswordRequestForm, содержащий данные, введенные в форме клиента form_data.username и form_data.password
        :return: Пользователя
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

        return user_model

    @classmethod
    async def create_access(
        cls,
        user_model: User_model,
    ) -> str:
        """
        Создает конкретно access_token
        :param user: схема пользователя с данными изи БД
        :return: access_token
        """
        return JWTUtils.create_access_token(user_model=user_model)

    @classmethod
    async def update_refresh(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> str:
        """
        Создает конкретно refresh_token
        :param user: схема пользователя с данными изи БД
        :return: refresh_token
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

        :param param:
        :param param:
        :return:
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
        )

    @classmethod
    async def get_current_user_by_access(
        cls,
        token: str,
        session: AsyncSession,
    ) -> User_model:
        """
        Через зависимость oauth2_scheme извлекает токен из заголовка запроса, затем парсит данные, извлеченные из токена и выполняет проверки
        :param token: Токен, полученный через зависимость из заголовка запроса
        :return: Возвращает пользователя, если такой существует в БД
        """
        payload = JWTUtils.decode_jwt(token)

        AuthUtils.check_token_type(
            payload=payload,
            token_type=jwt_settings.access_name,
        )

        user_id = int(payload.get("sub"))

        user_model = await UserDepends.get_user_by_id(
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
        Через зависимость oauth2_scheme извлекает токен из заголовка запроса, затем парсит данные, извлеченные из токена и выполняет проверки
        :return: Возвращает пользователя, если такой существует в БД
        """
        payload = JWTUtils.decode_jwt(token)

        AuthUtils.check_token_type(
            payload=payload,
            token_type=jwt_settings.refresh_name,
        )

        user_id = int(payload.get("sub"))

        refresh_model = await UserDepends.get_refresh(
            user_id=user_id,
            session=session,
        )

        if not refresh_model or refresh_model.token != token:
            raise HTTPErrors.token_invalid

        user_model = await UserDepends.get_user_by_id(
            user_id=user_id,
            session=session,
        )

        if not AuthUtils.check_user_status(user_model=user_model):
            raise HTTPErrors.user_inactive

        return user_model
