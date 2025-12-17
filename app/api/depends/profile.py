from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProfileCreate, ProfileUpdate
from app.models import Profile as Profile_model
from app.service import ProfileService
from app.tools import HTTPExeption


class ProfileCrud:

    @classmethod
    async def get_profile_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """

        :param param:
        :param param:
        :return:
        """
        profile_model = await ProfileService.get_model(
            user_id=user_id,
            session=session,
        )

        if not profile_model:
            raise HTTPExeption.not_found

        return profile_model

    @classmethod
    async def create_user_profile(
        cls,
        user_id: int,
        profile_in: ProfileCreate,
        session: AsyncSession,
    ) -> Profile_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        created_profile_model = await ProfileService.register_model(
            scheme_in=profile_in,
            session=session,
            user_id=user_id,
        )

        if not created_profile_model:
            raise HTTPExeption.db_error

        return created_profile_model

    @classmethod
    async def update_user_profile(
        cls,
        user_id: int,
        profile_in: ProfileUpdate,
        session: AsyncSession,
        partial: bool = False,
    ) -> Profile_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        updated_profile_model = await ProfileService.update_model(
            scheme_in=profile_in,
            session=session,
            partial=partial,
            user_id=user_id,
        )

        if not updated_profile_model:
            raise HTTPExeption.db_error

        return updated_profile_model

    @classmethod
    async def delete_user_profile(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Profile_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        deleted_profile_model = await ProfileService.delete_model(
            session=session,
            user_id=user_id,
        )

        if not deleted_profile_model:
            raise HTTPExeption.db_error

        return deleted_profile_model
