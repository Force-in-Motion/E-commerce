from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession


class BaseCrud(ABC):

    @staticmethod
    @abstractmethod
    async def get_all(*args, **kwargs) -> list[object]:
        """
        Возвращает все модели категории из БД
        :return: Список всех моделей
        """
        pass

    @staticmethod
    @abstractmethod
    async def get_by_id(*args, **kwargs) -> Optional[object]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @staticmethod
    @abstractmethod
    async def get_by_date(*args, **kwargs) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @staticmethod
    @abstractmethod
    async def create(*args, **kwargs) -> object:
        """
        Добавляет модель в БД
        :return: Модель пользователя, добавленную в БД
        """
        pass

    @staticmethod
    @abstractmethod
    async def update(*args, **kwargs) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :return: Модель, обновленную в БД
        """
        pass

    @staticmethod
    @abstractmethod
    async def delete(*args, **kwargs) -> object:
        """
        Удаляет модель из БД
        :return: Модель, удаленную из БД
        """
        pass

    @staticmethod
    @abstractmethod
    async def clear(*args, **kwargs) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :return: Пустой список
        """
        pass
