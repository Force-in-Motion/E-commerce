from pydantic import EmailStr
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import jwt_settings
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.schemas.user import UserUpdate
from app.service.profile import ProfileService
from app.tools import HTTPExeption
from app.service.user import UserService
from app.utils import JWTUtils, AuthUtils
from app.models import User as User_model
from app.schemas import UserResponse, UserCreate, TokenResponse


class ProfileCrud:

    @classmethod
    async def get_profile_by_user_id(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> Optional[ProfileResponse]:
        """

        :param param:
        :param param:
        :return:
        """
        profile_model = await ProfileService.get_model_by_user_id(
            user_id=user_model.id,
            session=session,
        )

        if not profile_model:
            raise HTTPExeption.unauthorized

        return profile_model

    @classmethod
    async def create_user_profile(
        cls,
        user_model: User_model,
        profile_in: ProfileCreate,
        session: AsyncSession,
    ) -> ProfileResponse:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        created_profile_model = await ProfileService.register_model_by_user_id(
            user_id=user_model.id,
            scheme_in=profile_in,
            session=session,
        )

        if not created_profile_model:
            raise HTTPExeption.db_error

        return created_profile_model

    @classmethod
    async def update_user_profile(
        cls,
        profile_in: ProfileUpdate,
        user_model: User_model,
        session: AsyncSession,
        partial: bool,
    ) -> ProfileResponse:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        updated_profile_model = await ProfileService.update_model_by_user_id(
            user_id=user_model.id,
            scheme_in=profile_in,
            session=session,
            partial=partial,
        )

        if not updated_profile_model:
            raise HTTPExeption.db_error

        return updated_profile_model

    @classmethod
    async def delete_user_profile(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> ProfileResponse:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        deleted_profile_model = await ProfileService.delete_model_by_user_id(
            user_id=user_model.id,
            session=session,
        )

        if not deleted_profile_model:
            raise HTTPExeption.db_error

        return deleted_profile_model
