from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProfileCreate, ProfileUpdate
from app.models import Profile as Profile_model
from app.service import ProfileService
from app.tools import HTTPErrors


class ProfileDepends:

    @classmethod
    async def get_all_profiles(
        cls,
        session: AsyncSession,
    ) -> Optional[list[Profile_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        list_profile_models = await ProfileService.get_all_models(session=session)

        if not list_profile_models:
            raise HTTPErrors.not_found

        return list_profile_models

    @classmethod
    async def get_profiles_by_date(
        cls,
        dates: datetime,
        session: AsyncSession,
    ) -> Optional[list[Profile_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        list_profile_models = await ProfileService.get_all_models_by_date(
            dates=dates,
            session=session,
        )

        if not list_profile_models:
            raise HTTPErrors.not_found

        return list_profile_models

    @classmethod
    async def get_profile_by_id(
        cls,
        profile_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """

        :param param:
        :param param:
        :return:
        """
        profile_model = await ProfileService.get_model(
            model_id=profile_id,
            session=session,
        )

        if not profile_model:
            raise HTTPErrors.not_found

        return profile_model

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
            raise HTTPErrors.not_found

        return profile_model

    @classmethod
    async def create_user_profile(
        cls,
        user_id: int,
        profile_scheme: ProfileCreate,
        session: AsyncSession,
    ) -> Profile_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        created_profile_model = await ProfileService.register_model(
            scheme_in=profile_scheme,
            session=session,
            user_id=user_id,
        )

        if not created_profile_model:
            raise HTTPErrors.db_error

        return created_profile_model

    @classmethod
    async def update_user_profile(
        cls,
        user_id: int,
        profile_scheme: ProfileUpdate,
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
            scheme_in=profile_scheme,
            session=session,
            partial=partial,
            user_id=user_id,
        )

        if not updated_profile_model:
            raise HTTPErrors.db_error

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
            raise HTTPErrors.db_error

        return deleted_profile_model
    

    @classmethod
    async def clear_profiles(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        cleared_table = await ProfileService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.db_error

        return cleared_table
