from datetime import datetime
from typing import Optional

from sqlalchemy import select, text, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models import User as User_model
from app.schemas import UserInput
from app.tools.custom_err import DatabaseError


class UserAdapter(BaseCrud):

    @staticmethod
    async def get_all(
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает всех моделей пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """
        try:
            stmt = select(User_model).order_by(User_model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError("User table is empty")

    @staticmethod
    async def get_by_id(
        user_id: int,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает модель пользователя по его id из БД
        :param user_id: id модели конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        try:
            return await session.get(User_model, user_id)

        except SQLAlchemyError:
            raise DatabaseError("User model with this id not found")

    @staticmethod
    async def get_by_name(
        name: str,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        try:
            return await session.get(User_model, name)

        except SQLAlchemyError:
            raise DatabaseError("User model with this name not found")

    @staticmethod
    async def get_by_date(
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает список всех моделей пользователей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех моделей пользователей, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(User_model)
                .where(User_model.created_at.between(*dates))
                .order_by(User_model.created_at.desc())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError("There are no added users models in this range")

    @staticmethod
    async def create(
        user_input,
        session: AsyncSession,
    ) -> User_model:
        """
        Добавляет модель пользователя в БД
        :param user_input: Pydantic Схема - объект, содержащий данные пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        try:
            user_model = User_model(**user_input.model_dump())

            session.add(user_model)
            await session.commit()
            await session.refresh(
                user_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return user_model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error adding user model")

    @staticmethod
    async def update(
        user_input: UserInput,
        user_model: User_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> User_model:
        """
        Обновляет данные модели пользователя в БД полностью или частично
        :param user_input: Pydantic Схема - объект, содержащий данные пользователя
        :param user_model: ORM Модель - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: Модель пользователя, обновленную в БД
        """
        try:
            for key, value in user_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(user_model, key, value)

            await session.commit()
            await session.refresh(
                user_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return user_model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error updating user model")

    @staticmethod
    async def delete(
        user_model: User_model,
        session: AsyncSession,
    ) -> User_model:
        """
        Удаляет модель пользователя из БД
        :param user_model: ORM Модель - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """
        try:
            await session.delete(user_model)
            await session.commit()
            return user_model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error deleting user model")

    @staticmethod
    async def clear(
        session: AsyncSession,
    ) -> list:
        """
        Очищает таблицу моделей пользователей и сбрасывает последовательность id моделей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Пустой список
        """
        try:
            await session.execute(delete(User_model))
            await session.execute(text('ALTER SEQUENCE "User_id_seq" RESTART WITH 1'))
            await session.commit()
            return []

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError("Error clearing user table")
