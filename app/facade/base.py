from datetime import datetime
from typing import Type, Generic, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserAdapter
from app.interface.facade import Facade
from app.models import User as User_model, Base

from app.types import DBModel, PDScheme, Adapter


class BaseFacade(Generic[DBModel, PDScheme, Adapter], Facade):

    model: Type[DBModel]
    scheme: Type[PDScheme]
    adapter: Type[Adapter]

    @classmethod
    async def _check_adapter(cls, adapter: Optional[Type[Adapter]]) -> Type[Adapter]:

        if adapter is None:
            raise NotImplementedError(f"{cls.__name__} must defined this attribute")

        return adapter

    @classmethod
    async def get_all_models(
        cls,
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает результат выполнения метода получения всех моделей пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """
        cls_adapter = await cls._check_adapter(cls.adapter)

        models = await cls_adapter.get_all(session)

        if not models:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error, {cls_adapter.model.__name__} table is empty",
            )

        return models

    @classmethod
    async def get_model_by_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода получения модели пользователя по ее id из БД
        :param user_id: id модели конкретного пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Модель конкретного пользователя
        """
        cls_adapter = await cls._check_adapter(cls.adapter)

        user_model = await cls_adapter.get_by_id(user_id, session)

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error, {cls_adapter.model.__name__} with this id not found",
            )

        return user_model

    @classmethod
    async def get_models_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает результат выполнения метода получения моделей пользователей из БД, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список моделей всех пользователей, добавленных за указанный интервал времени
        """
        cls_adapter = await cls._check_adapter(cls.adapter)

        user_models = await cls_adapter.get_by_date(dates, session)

        if not user_models:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error, There are no added {cls_adapter.model.__name__} in this range",
            )

        return user_models

    @classmethod
    async def register_model(
        cls,
        user_input: PDScheme,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода добавления модели пользователя в БД
        :param user_input: Pydantic Схема - объект, содержащий данные модели пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        cls_adapter = await cls._check_adapter(cls.adapter)

        user_model = await cls_adapter.create(user_input, session)

        if not user_model:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error, adding {cls_adapter.model.__name__}",
            )

        return user_model

    @classmethod
    async def update_model(
        cls,
        user_input: BaseModel,
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
                detail="Error updating model",
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
                detail="Error deleting model",
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
                detail="Error clearing model",
            )

        return result
