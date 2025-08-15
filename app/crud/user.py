from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, text, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User as User_model
from app.schemas import UserInput


class UserAdapter:

    @classmethod
    async def get_all_users(
        cls,
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает всех пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: list[User_model]
        """
        try:
            stmt = select(User_model).order_by(User_model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_user_by_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает пользователя по его id из БД
        :param user_id: id конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: User_model | None
        """
        try:
            return await session.get(User_model, user_id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_user_by_name(
        cls,
        name: str,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает пользователя по его имени если существует в БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: User_model | None
        """
        try:
            return await session.get(User_model, name)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_added_users_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает список всех пользователей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех пользователей, добавленных за указанный интервал времени
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
            await session.rollback()
            return []

    @classmethod
    async def add_user(
        cls,
        user_input: UserInput,
        session: AsyncSession,
    ) -> User_model:
        """
        Добавляет пользователя в БД
        :param user_input: UserInput - объект, содержащий данные пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            user_model = User_model(**user_input.model_dump())
            session.add(user_model)
            await session.commit()
            await session.refresh(
                user_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что post_model содержит актуальное состояние из базы.
            return user_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error added User",
            )

    @classmethod
    async def update_user(
        cls,
        user_input: UserInput,
        user_model: User_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> User_model:
        """
        Обновляет данные пользователя в БД полностью или частично
        :param user_input: UserInput - объект, содержащий данные пользователя
        :param user_model: User_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        try:
            for key, value in user_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(user_model, key, value)

            await session.commit()
            await session.refresh(
                user_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что post_model содержит актуальное состояние из базы.
            return user_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error updated User",
            )

    @classmethod
    async def del_user(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> User_model:
        """
        Удаляет пользователя из БД
        :param user_model: User_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            await session.delete(user_model)
            await session.commit()
            return user_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted User",
            )

    @classmethod
    async def clear_users(cls, session: AsyncSession) -> list:
        """
        Очищает базу данных пользователя и сбрасывает последовательность id пользователей
        :param session: Объект сессии, полученный в качестве аргумента
        :return:
        """
        try:
            await session.execute(delete(User_model))
            await session.execute(text('ALTER SEQUENCE "User_id_seq" RESTART WITH 1'))
            await session.commit()
            return []

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted all Users",
            )
