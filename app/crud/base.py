from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession


class BaseCrud(ABC):

    @abstractmethod
    async def get_all(self) -> list[object]:
        """
        Возвращает все модели категории из БД
        :return: Список всех моделей
        """
        pass

    @abstractmethod
    async def get_by_id(
        self,
        id: int,
    ) -> Optional[object]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @abstractmethod
    async def get_by_date(
        self,
        dates: tuple[datetime, datetime],
    ) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @abstractmethod
    async def create(
        self,
        schema,
    ) -> object:
        """
        Добавляет схему в БД
        :param schema: схема, содержащая данные полученного объекта, преобразуется в модель и добавляется в БД
        :return: dict
        """
        pass

    @abstractmethod
    async def update(
        self,
        schema,
        model,
        partial: bool = False,
    ) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :param schema: схема, содержащая данные полученного объекта
        :param model: модель - конкретный объект в БД, найденный по id
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        pass

    @abstractmethod
    async def delete(self, model) -> object:
        """
        Удаляет модель из БД
        :param model: модель - конкретный объект в БД, найденный по id
        :return: dict
        """
        pass

    @abstractmethod
    async def clear(self) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :return: []
        """
        pass
