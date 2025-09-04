from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector


class BaseFacade(ABC):

    @staticmethod
    @abstractmethod
    async def get_all(
        session: AsyncSession,
    ) -> list[object]:
        """
        Возвращает все модели категории из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей
        """
        pass

    @staticmethod
    @abstractmethod
    async def get_by_id(
        id: int,
        session: AsyncSession,
    ) -> object:
        """
        Возвращает модель по её id из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: Идентификатор объекта, полученный в качестве аргумента
        :return: Модель | None
        """
        pass

    @staticmethod
    @abstractmethod
    async def get_by_date(
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @staticmethod
    @abstractmethod
    async def create(
        schema,
        session: AsyncSession,
    ) -> object:
        """
        Добавляет схему в БД
        :param schema: схема, содержащая данные полученного объекта, преобразуется в модель и добавляется в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        pass

    @staticmethod
    @abstractmethod
    async def update(
        schema,
        model,
        session: AsyncSession,
        partial: bool = False,
    ) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :param schema: схема, содержащая данные полученного объекта
        :param model: модель - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        pass

    @staticmethod
    @abstractmethod
    async def delete(
        model,
        session: AsyncSession,
    ) -> object:
        """
        Удаляет модель из БД
        :param model: модель - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        pass

    @staticmethod
    @abstractmethod
    async def clear(
        session: AsyncSession,
    ) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: []
        """
        pass
