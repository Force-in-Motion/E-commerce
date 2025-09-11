from typing import Optional
from abc import ABC, abstractmethod


class Crud(ABC):

    @classmethod
    @abstractmethod
    async def get_all(cls, *args, **kwargs) -> list[object]:
        """
        Возвращает все модели категории из БД
        :return: Список всех моделей
        """
        pass

    @classmethod
    @abstractmethod
    async def get_by_id(cls, *args, **kwargs) -> Optional[object]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @classmethod
    @abstractmethod
    async def get_by_date(cls, *args, **kwargs) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @classmethod
    @abstractmethod
    async def create(cls, *args, **kwargs) -> object:
        """
        Добавляет модель в БД
        :return: Модель пользователя, добавленную в БД
        """
        pass

    @classmethod
    @abstractmethod
    async def update(cls, *args, **kwargs) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :return: Модель, обновленную в БД
        """
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, *args, **kwargs) -> object:
        """
        Удаляет модель из БД
        :return: Модель, удаленную из БД
        """
        pass

    @classmethod
    @abstractmethod
    async def clear(cls, *args, **kwargs) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :return: Пустой список
        """
        pass
