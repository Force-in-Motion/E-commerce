from abc import ABC, abstractmethod
from ctypes import c_char_p
from typing import Optional


class Facade(ABC):

    @classmethod
    @abstractmethod
    async def _get_all_models(cls, *args, **kwargs) -> list[object]:
        """
        Возвращает все модели категории из БД
        :return: Список всех моделей
        """
        pass

    @classmethod
    @abstractmethod
    async def _get_model_by_id(cls, *args, **kwargs) -> Optional[object]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @classmethod
    @abstractmethod
    async def _get_models_by_date(cls, *args, **kwargs) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @classmethod
    @abstractmethod
    async def _register_model(cls, *args, **kwargs) -> object:
        """
        Добавляет модель в БД
        :return: Модель пользователя, добавленную в БД
        """
        pass

    @classmethod
    @abstractmethod
    async def _update_model(cls, *args, **kwargs) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :return: Модель, обновленную в БД
        """
        pass

    @classmethod
    @abstractmethod
    async def _delete_model(cls, *args, **kwargs) -> object:
        """
        Удаляет модель из БД
        :return: Модель, удаленную из БД
        """
        pass

    @classmethod
    @abstractmethod
    async def _clear_table(cls, *args, **kwargs) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :return: Пустой список
        """
        pass
