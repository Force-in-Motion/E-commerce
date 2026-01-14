from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProfileCreate, ProfileUpdate
from app.celery.tasks import send_msg_to_email_task
from app.models import Profile as Profile_model
from app.service import ProfileService
from app.tools import HTTPErrors


class ProfileDepends:

    @classmethod
    async def get_all_profiles(
        cls,
        session: AsyncSession,
    ) -> list[Profile_model]:
        """
        Возвращает все профили пользователей
        :param session: Асинхронная сессия
        :return: Список моделей профилей
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
    ) -> list[Profile_model]:
        """
        Возвращает профили, добавленные в указанном временном диапазоне
        :param dates: Определяет временной диапазон 
        :param session: Асинхронная сессия
        :return: Список моделей профилей, добавленных в указанном временном диапазоне
        """
        list_profile_models = await ProfileService.get_all_models_by_date(
            dates=dates,
            session=session,
        )

        if not list_profile_models:
            raise HTTPErrors.not_found

        return list_profile_models

    @classmethod
    async def get_profile(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        profile_id: Optional[int] = None,
    ) -> Profile_model:
        """
        Возвращает конкретный профиль пользователя
        :param user_id: Опциональный параметр, id продукта
        :param profile_id: Опциональный параметр, id продукта
        :param session: Асинхронная сессия
        :return: Модель профиля пользователя
        """
        profile_model = await ProfileService.get_model(
            user_id=user_id,
            model_id=profile_id,
            session=session,
        )

        if not profile_model:
            raise HTTPErrors.not_found

        return profile_model


    @classmethod
    async def create_profile(
        cls,
        user_id: int,
        session: AsyncSession,
        profile_scheme: ProfileCreate,
        login: Optional[EmailStr] = None
    ) -> Profile_model:
        """
        Создает профиль пользователя
        :param profile_scheme: Схема профиля, полученная от пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Модель профиля пользователя
        """
        profile_model = await ProfileService.register_model(
            scheme_in=profile_scheme,
            session=session,
            user_id=user_id,
        )

        if not profile_model:
            raise HTTPErrors.err_create_model

        send_msg_to_email_task.delay(
            key=cls.create_profile.__name__,
            to_email=login,
        )
            
        return profile_model

    @classmethod
    async def update_profile(
        cls,
        user_id: int,
        profile_scheme: ProfileUpdate,
        session: AsyncSession,
        partial: bool = False,
        login: Optional[EmailStr] = None,
    ) -> Profile_model:
        """
        Изменяет профиль пользователя
        :param profile_scheme: Схема профиля, полученная от пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :param partial: Флаг, определяющий полное или частичное изменение данных
        :return: Заказ пользователя
        """
        profile_model = await ProfileService.update_model(
            scheme_in=profile_scheme,
            session=session,
            partial=partial,
            user_id=user_id,
        )

        if not profile_model:
            raise HTTPErrors.err_update_model
        
        send_msg_to_email_task.delay(
            key=cls.update_profile.__name__,
            to_email=login,
        )

        return profile_model

    @classmethod
    async def delete_profile(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        post_id: Optional[int] = None,
        login: Optional[EmailStr] = None
    ) -> Profile_model:
        """
        Удаляет профиль пользователя
        :param post_id: Опциональный параметр, id профиля
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Модель профиля пользователя
        """
        profile_model = await ProfileService.delete_model(
            session=session,
            user_id=user_id,
            model_id=post_id,
        )

        if not profile_model:
            raise HTTPErrors.err_delete_model
        
        send_msg_to_email_task.delay(
            key=cls.delete_profile.__name__,
            to_email=login,
        )

        return profile_model

    @classmethod
    async def clear_profiles(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Полностью очищает таблицу профилей
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        cleared_table = await ProfileService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.clear_table

        return cleared_table
