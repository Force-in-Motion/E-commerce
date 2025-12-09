from datetime import datetime
from typing import Type, Generic

from sqlalchemy.ext.asyncio import AsyncSession

from app.interface.service import AService
from app.tools.types import DBModel, PDScheme, Adapter


class BaseService(Generic[DBModel, Adapter], AService):

    model: Type[DBModel]
    repo: Type[Adapter]

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
        return await cls.repo.get_all(session=session)

    @classmethod
    async def get_model_by_id(
        cls,
        model_id: int,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода получения модели пользователя по ее id из БД
        :param model_id: id модели конкретного пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Модель конкретного пользователя
        """
        return await cls.repo.get_by_id(
            model_id=model_id,
            session=session,
        )

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
        return await cls.repo.get_by_date(
            dates=dates,
            session=session,
        )

    @classmethod
    async def register_model(
        cls,
        scheme_in: PDScheme,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода добавления модели пользователя в БД
        :param scheme_in: Pydantic Схема - объект, содержащий данные модели пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        return await cls.repo.create(
            scheme_in=scheme_in,
            session=session,
        )

    @classmethod
    async def update_model(
        cls,
        model_id: int,
        scheme_in: PDScheme,
        session: AsyncSession,
        partial: bool = False,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода обновления данных модели пользователя в БД полностью или частично
        :param scheme_in: Pydantic Схема - объект, содержащий данные пользователя
        :param model_id: ORM Модель - конкретный объект модели в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
        :return: Модель пользователя, обновленную в БД
        """
        model = await cls.repo.get_by_id(
            model_id=model_id,
            session=session,
        )

        return await cls.repo.update(
            scheme_in=scheme_in,
            update_model=model,
            session=session,
            partial=partial,
        )

    @classmethod
    async def delete_model(
        cls,
        model_id: int,
        session: AsyncSession,
    ) -> DBModel:
        """
        Возвращает результат выполнения метода удаления модели пользователя из БД
        :param model_id: ORM Модель - конкретный объект модели в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """

        model = await cls.repo.get_by_id(
            model_id=model_id,
            session=session,
        )

        return await cls.repo.delete(
            del_model=model,
            session=session,
        )

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
        return await cls.repo.clear(session=session)
