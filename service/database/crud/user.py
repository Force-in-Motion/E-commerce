from datetime import datetime, time
from fastapi import HTTPException, Query

from sqlalchemy import select, text, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import User as User_model
from web.schemas import UserInput


class UserAdapter:

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> list[User_model]:
        """
        Возвращает всех пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: list[User_model]
        """
        try:
            request = select(User_model).order_by(User_model.created_at)
            response = await session.execute(request)
            users = response.scalars().all()
            return list(users)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_user_by_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> User_model | None:
        """
        Возвращает пользователя по его id из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: User_model | None
        """
        try:
            return await session.get(User_model, id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_added_users_by_date(
        cls,
        session: AsyncSession,
        date_start: datetime = Query(),
        date_end: datetime = Query(),
    ) -> list[User_model]:
        """
        Возвращает список всех пользователей, добавленных за указанный интервал времени
        :param session: Объект сессии, полученный в качестве аргумента
        :param date_start: начало интервала времени
        :param date_end: окончание интервала времени
        :return: список всех пользователей, добавленных за указанный интервал времени
        """
        if date_start >= date_end:
            raise ValueError("date_start must be less than date_end")

        try:
            request = (
                select(User_model)
                .where(User_model.created_at.between(date_start, date_end))
                .order_by(User_model.created_at.desc())
            )
            response = await session.execute(request)
            return list(response.scalars().all())

        except SQLAlchemyError:
            await session.rollback()
            return []

    @classmethod
    async def add_user(
        cls,
        session: AsyncSession,
        user_input: UserInput,
    ) -> dict[str, str]:
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
            return {"status": "ok", "detail": "User has been added"}

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Error added User")

    @classmethod
    async def update_user(
        cls,
        user_input: UserInput,
        user_model: User_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> dict[str, str]:
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
            return {"status": "ok", "detail": "User has been updated"}

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Error updated User")

    @classmethod
    async def del_user(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> dict[str, str]:
        """
        Удаляет пользователя из БД
        :param user_model: User_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            await session.delete(user_model)
            await session.commit()
            return {"status": "ok", "detail": "User has been deleted"}

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Error deleted User")

    @classmethod
    async def clear_user_db(cls, session: AsyncSession) -> dict[str, str]:
        """
        Очищает базу данных пользователя и сбрасывает последовательность id пользователей
        :param session: Объект сессии, полученный в качестве аргумента
        :return:
        """
        try:
            await session.execute(delete(User_model))
            await session.execute(text('ALTER SEQUENCE "User_id_seq" RESTART WITH 1'))
            await session.commit()
            return {"status": "ok", "detail": "All users have been deleted"}

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Error deleted all Users")
