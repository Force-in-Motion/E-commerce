from datetime import datetime
from typing import Type, Generic, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.interface.facade import Facade
from app.tools import Utils
from app.types import DBModel, PDScheme, Adapter


class BaseFacade(Generic[DBModel, PDScheme, Adapter], Facade):

    model: Type[DBModel]
    scheme: Type[PDScheme]
    adapter: Type[Adapter]

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def get_all_models(
        cls,
        adapter: Type[Adapter],
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает результат выполнения метода получения всех моделей пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param adapter: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """

        return await adapter.get_all(session)

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def get_model_by_id(
        cls,
        adapter: Type[Adapter],
        model_id: int,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода получения модели пользователя по ее id из БД
        :param model_id: id модели конкретного пользователя
        :param adapter: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Модель конкретного пользователя
        """
        return await adapter.get_by_id(model_id, session)

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def get_models_by_date(
        cls,
        adapter: Type[Adapter],
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает результат выполнения метода получения моделей пользователей из БД, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param adapter: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список моделей всех пользователей, добавленных за указанный интервал времени
        """
        return await adapter.get_by_date(dates, session)

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def register_model(
        cls,
        adapter: Type[Adapter],
        scheme_in: PDScheme,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода добавления модели пользователя в БД
        :param scheme_in: Pydantic Схема - объект, содержащий данные модели пользователя
        :param adapter: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        return await adapter.create(scheme_in, session)

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def update_model(
        cls,
        adapter: Type[Adapter],
        scheme_in: PDScheme,
        model_id: int,
        session: AsyncSession,
        partial: bool = False,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода обновления данных модели пользователя в БД полностью или частично
        :param scheme_in: Pydantic Схема - объект, содержащий данные пользователя
        :param model_id: ORM Модель - конкретный объект модели в БД, найденный по id
        :param adapter: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
        :return: Модель пользователя, обновленную в БД
        """
        model = await adapter.get_by_id(model_id, session)

        return await adapter.update(scheme_in, model, session, partial)

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def delete_model(
        cls,
        adapter: Type[Adapter],
        model_id: int,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода удаления модели пользователя из БД
        :param model_id: ORM Модель - конкретный объект модели в БД, найденный по id
        :param adapter: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """

        model = await adapter.get_by_id(model_id, session)

        return await adapter.delete(model, session)

    @classmethod
    @Utils.ensure_adapter
    @Utils.map_crud_errors_auto
    async def clear_table(
        cls,
        adapter: Type[Adapter],
        session: AsyncSession,
    ) -> list:
        """
        Возвращает результат выполнения метода очищения таблицы данных моделей пользователя и сбрасывает последовательность id моделей
        :param adapter: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Пустой список
        """
        return await adapter.clear(session)
