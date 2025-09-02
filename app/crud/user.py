from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, text, delete
from sqlalchemy.exc import SQLAlchemyError

from app.crud import BaseCrud
from app.models import User as User_model
from app.schemas import UserInput


class UserAdapter(BaseCrud):

    def __init__(self, session):
        self.__session = session

    async def get_all(self) -> list[User_model]:
        """
        Возвращает всех пользователей из БД
        :return: list[User_model]
        """
        try:
            stmt = select(User_model).order_by(User_model.id)
            result = await self.__session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    async def get_by_id(
        self,
        user_id: int,
    ) -> Optional[User_model]:
        """
        Возвращает пользователя по его id из БД
        :param user_id: id конкретного пользователя
        :return: User_model | None
        """
        try:
            return await self.__session.get(User_model, user_id)

        except SQLAlchemyError:
            return None

    async def get_by_name(
        self,
        name: str,
    ) -> Optional[User_model]:
        """
        Возвращает пользователя по его имени если существует в БД
        :param name: Имя пользователя
        :return: User_model | None
        """
        try:
            return await self.__session.get(User_model, name)

        except SQLAlchemyError:
            return None

    async def get_by_date(
        self,
        dates: tuple[datetime, datetime],
    ) -> list[User_model]:
        """
        Возвращает список всех пользователей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :return: список всех пользователей, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(User_model)
                .where(User_model.created_at.between(*dates))
                .order_by(User_model.created_at.desc())
            )
            result = await self.__session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    async def create(
        self,
        user_input: UserInput,
    ) -> User_model:
        """
        Добавляет пользователя в БД
        :param user_input: UserInput - объект, содержащий данные пользователя
        :return: dict
        """
        try:
            user_model = User_model(**user_input.model_dump())
            self.__session.add(user_model)
            await self.__session.commit()
            await self.__session.refresh(
                user_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return user_model

        except SQLAlchemyError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error added User",
            )

    async def update(
        self,
        user_input: UserInput,
        user_model: User_model,
        partial: bool = False,
    ) -> User_model:
        """
        Обновляет данные пользователя в БД полностью или частично
        :param user_input: UserInput - объект, содержащий данные пользователя
        :param user_model: User_model - конкретный объект в БД, найденный по id
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

            await self.__session.commit()
            await self.__session.refresh(
                user_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return user_model

        except SQLAlchemyError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error updated User",
            )

    async def delete(
        self,
        user_model: User_model,
    ) -> User_model:
        """
        Удаляет пользователя из БД
        :param user_model: User_model - конкретный объект в БД, найденный по id
        :return: dict
        """
        try:
            await self.__session.delete(user_model)
            await self.__session.commit()
            return user_model

        except SQLAlchemyError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted User",
            )

    async def clear(self) -> list:
        """
        Очищает базу данных пользователя и сбрасывает последовательность id пользователей
        :return:
        """
        try:
            await self.__session.execute(delete(User_model))
            await self.__session.execute(
                text('ALTER SEQUENCE "User_id_seq" RESTART WITH 1')
            )
            await self.__session.commit()
            return []

        except SQLAlchemyError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted all Users",
            )
