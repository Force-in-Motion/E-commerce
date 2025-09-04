from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models import Profile as Profile_model
from app.schemas import ProfileInput
from app.tools.custom_err import DatabaseError


class ProfileAdapter(BaseCrud):

    @staticmethod
    async def get_all(
        session: AsyncSession,
    ) -> list[Profile_model]:
        """
        Возвращает все модели профилей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей профилей
        """
        try:
            stmt = select(Profile_model).order_by(Profile_model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError("Profile table is empty")

    @staticmethod
    async def get_by_id(
        profile_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """
        Возвращает модель профиля по ее id из БД
        :param profile_id: id модели профиля в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель профиля | None
        """
        try:
            return await session.get(Profile_model, profile_id)

        except SQLAlchemyError:
            raise DatabaseError("Profile model with this id not found")

    @staticmethod
    async def get_by_user_id(
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """
        Возвращает модель профиля, соответствующую id пользователя в БД
        :param user_id: id Модели конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель профиля | None
        """
        try:
            stmt = select(Profile_model).where(Profile_model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().first()

        except SQLAlchemyError:
            raise DatabaseError("Profile model with this user id not found")

    @staticmethod
    async def get_by_date(
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Profile_model]:
        """
        Возвращает список всех моделей профилей пользователей, добавленных за указанный интервал времени
        :param dates: кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей профилей пользователей, добавленных за указанный интервал времени
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
            raise DatabaseError("There are no added profile model in this range")

    @staticmethod
    async def create(
        profile_input: ProfileInput,
        user_id: int,
        session: AsyncSession,
    ) -> Profile_model:
        """
        Создает модель профиля конкретного пользователя в БД
        :param profile_input: Pydantic Схема - объект, содержащий данные модели профиля пользователя
        :param user_id: id Модели конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель профиля пользователя, созданную в БД
        """

        try:
            profile_model = Profile_model(user_id=user_id, **profile_input.model_dump())

            session.add(profile_model)
            await session.commit()
            await session.refresh(profile_model)
            return profile_model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error adding profile model")

    @staticmethod
    async def update(
        session: AsyncSession,
        profile_input: ProfileInput,
        profile_model: Profile_model,
        partial: bool = False,
    ) -> Profile_model:
        """
        Обновляет данные модели профиля пользователя в БД полностью или частично
        :param session: Объект сессии, полученный в качестве аргумента
        :param profile_input: Pydantic Схема - объект, содержащий новые данные профиля пользователя
        :param profile_model: ORM Модель - конкретный объект в БД, найденный по id
        :param partial: partial: Флаг, передаваемое значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: Модель профиля пользователя, обновленную в БД
        """
        try:
            for key, value in profile_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(profile_model, key, value)

            await session.commit()
            await session.refresh(profile_model)
            return profile_model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error updating profile model")

    @staticmethod
    async def delete(
        session: AsyncSession,
        profile_model: Profile_model,
    ) -> Profile_model:
        """
        Удаляет модель профиля из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param profile_model: ORM Модель - конкретный объект в БД, найденный по id
        :return: Модель профиля пользователя, удаленную из БД
        """
        try:
            await session.delete(profile_model)
            await session.commit()
            return profile_model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error deleting profile model")

    @staticmethod
    async def clear(session: AsyncSession) -> list:
        """
        Очищает таблицу профилей пользователей и сбрасывает последовательность id пользователей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Пустой список
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
            raise DatabaseError("Error clearing profile table")
