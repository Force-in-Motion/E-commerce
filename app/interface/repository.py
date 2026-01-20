from typing import Optional
from abc import ABC, abstractmethod
from app.tools.types import DBModel


class ARepo(ABC):

    @classmethod
    @abstractmethod
    async def get_all(cls, *args, **kwargs) -> Optional[list[DBModel]]:
        """
        Возвращает все модели из БД
        :return: Список всех моделей | None
        """
        pass

    @classmethod
    @abstractmethod
    async def get_all_by_user_id(cls, *args, **kwargs) -> Optional[list[DBModel]]:
        """
        Возвращает список моделей по user id из БД
        :return: Список всех моделей | None
        """
        pass

    @classmethod
    @abstractmethod
    async def get_by_id(cls, *args, **kwargs) -> Optional[DBModel]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @classmethod
    @abstractmethod
    async def get_by_user_id(cls, *args, **kwargs) -> Optional[DBModel]:
        """
        Возвращает модель по user id из БД
        :return: Модель | None
        """
        pass

    @classmethod
    @abstractmethod
    async def get_by_user_and_model_id(cls, *args, **kwargs) -> Optional[DBModel]:
        """
        Возвращает модель по её id и user id из БД
        :return: Модель | None
        """
        pass

    @classmethod
    @abstractmethod
    async def get_by_date(cls, *args, **kwargs) -> list[DBModel]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :return: Список всех моделей | None
        """
        pass

    @classmethod
    @abstractmethod
    async def create(cls, *args, **kwargs) -> DBModel:
        """
        Добавляет модель в БД
        :return: Модель, добавленную в БД
        """
        pass

    @classmethod
    @abstractmethod
    async def update(cls, *args, **kwargs) -> DBModel:
        """
        Обновляет данные модели в БД полностью или частично
        :return: Модель, обновленную в БД
        """
        pass

    @classmethod
    @abstractmethod
    async def delete(cls, *args, **kwargs) -> DBModel:
        """
        Удаляет модель из БД
        :return: Модель, удаленную из БД
        """
        pass

    @classmethod
    @abstractmethod
    async def delete_all(cls, *args, **kwargs) -> list:
        """
        Удаляет модель из БД
        :return: Пустой список
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
