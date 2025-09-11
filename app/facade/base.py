from datetime import datetime
from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User as User_model
from app.schemas import UserInput
from app.crud import UserAdapter
from app.interface.facade import Facade


class BaseFacade(Facade):

    model: Type

    @classmethod
    async def get_all_models(
        cls,
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает результат выполнения метода получения всех моделей пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """
        user_models = await UserAdapter.get_all(session)

        if not user_models:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User table is empty",
            )

        return user_models

    @classmethod
    async def get_model_by_id(
        user_id: int,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает результат выполнения метода получения модели пользователя по ее id из БД
        :param user_id: id модели конкретного пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Модель конкретного пользователя
        """
        user_model = await UserAdapter.get_by_id(user_id, session)

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User model with this id not found",
            )

        return user_model

    @classmethod
    async def get_model_by_date(
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[User_model]:
        """
        Возвращает результат выполнения метода получения моделей пользователей из БД, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список моделей всех пользователей, добавленных за указанный интервал времени
        """

        user_models = await UserAdapter.get_by_date(dates, session)

        if not user_models:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no added users models in this range",
            )

        return user_models

    @classmethod
    async def create(
        user_input,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает результат выполнения метода добавления модели пользователя в БД
        :param user_input: Pydantic Схема - объект, содержащий данные модели пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        user_model = await UserAdapter.create(user_input, session)

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error adding user model",
            )

        return user_model

    @classmethod
    async def update(
        user_input: UserInput,
        user_model: User_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> User_model:
        """
        Возвращает результат выполнения метода обновления данных модели пользователя в БД полностью или частично
        :param user_input: Pydantic Схема - объект, содержащий данные пользователя
        :param user_model: ORM Модель - конкретный объект модели в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
        :return: Модель пользователя, обновленную в БД
        """
        user_model = await UserAdapter.update(user_input, user_model, session, partial)

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error updating user model",
            )

        return user_model

    @classmethod
    async def delete_model(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> User_model:
        """
        Возвращает результат выполнения метода удаления модели пользователя из БД
        :param user_model: ORM Модель - конкретный объект модели в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """
        user_model = await UserAdapter.delete(user_model, session)

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error deleting user model",
            )

        return user_model

    @classmethod
    async def clear_table(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Возвращает результат выполнения метода очищения таблицы данных моделей пользователя и сбрасывает последовательность id моделей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Пустой список
        """
        result = await cls.model.clear(session)

        if result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error clearing user model",
            )

        return result
