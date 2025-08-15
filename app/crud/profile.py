from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, delete, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Profile as Profile_model
from app.schemas import ProfileInput


class ProfileAdapter:

    @classmethod
    async def get_profiles(
        cls,
        session: AsyncSession,
    ) -> list[Profile_model]:
        """
        Возвращает все профили, существующие в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список моделей профилей
        """
        try:
            stmt = select(Profile_model).order_by(Profile_model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @staticmethod
    async def get_profile_by_id(
        profile_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """
        Возвращает профиль по его id
        :param profile_id: id профиля в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: модель конкретного профиля
        """
        try:
            return await session.get(Profile_model, profile_id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_profile_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """
        Возвращает профиль, соответствующий id пользователя в БД
        :param user_id: id конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: модель конкретного профиля
        """
        try:
            stmt = select(Profile_model).where(Profile_model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().first()

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_added_profiles_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Profile_model]:
        """
        Возвращает список всех профилей пользователей, добавленных за указанный интервал времени
        :param dates: кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех профилей пользователей, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(Profile_model)
                .where(Profile_model.created_at.between(*dates))
                .order_by(Profile_model.created_at.desc())
            )

            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def add_profile(
        cls,
        profile_input: ProfileInput,
        user_id: int,
        session: AsyncSession,
    ) -> Profile_model:
        """
        Создает профиль конкретного пользователя в БД
        :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
        :param user_id: UserModel - объект, содержащий данные пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        # Проверка наличия уже существующего профиля у пользователя

        # Если профиля у пользователя нет, то добавляем

        try:
            profile_model = Profile_model(user_id=user_id, **profile_input.model_dump())

            session.add(profile_model)
            await session.commit()
            return profile_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error added Profile",
            )

    @classmethod
    async def update_profile(
        cls,
        session: AsyncSession,
        profile_input: ProfileInput,
        profile_model: Profile_model,
        partial: bool = False,
    ) -> Profile_model:
        """
        Обновляет данные профиля пользователя в БД полностью или частично
        :param session: Объект сессии, полученный в качестве аргумента
        :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
        :param profile_model: Profile_model -конкретный объект в БД, найденный по id
        :param partial: partial: Флаг, передаваемое значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        try:
            for key, value in profile_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(profile_model, key, value)

            await session.commit()
            return profile_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error updated Profile",
            )

    @classmethod
    async def del_profile(
        cls,
        session: AsyncSession,
        profile_model: Profile_model,
    ) -> Profile_model:
        """
        Удаляет профиль из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param profile_model: Profile_model -конкретный объект в БД, найденный по id
        :return: dict
        """
        try:
            await session.delete(profile_model)
            await session.commit()
            return profile_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted Profile",
            )

    @classmethod
    async def clear_profile_db(cls, session: AsyncSession) -> list:
        """
        Очищает базу данных пользователя и сбрасывает последовательность id пользователей
        :param session: Объект сессии, полученный в качестве аргумента
        :return:
        """
        try:
            await session.execute(delete(Profile_model))
            await session.execute(
                text('ALTER SEQUENCE "Profile_id_seq" RESTART WITH 1')
            )
            await session.commit()
            return []

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted all Profiles",
            )
