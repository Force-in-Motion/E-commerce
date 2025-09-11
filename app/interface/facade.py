from abc import ABC, abstractmethod
from typing import Optional


class Facade(ABC):

    @abstractmethod
    async def get_all_models(*args, **kwargs) -> list[object]:
        """
        Возвращает все модели категории из БД
        :return: Список всех моделей
        """
        pass

    @abstractmethod
    async def get_model_by_id(*args, **kwargs) -> Optional[object]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @abstractmethod
    async def get_model_by_date(*args, **kwargs) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @abstractmethod
    async def register_model(*args, **kwargs) -> object:
        """
        Добавляет модель в БД
        :return: Модель пользователя, добавленную в БД
        """
        pass

    @abstractmethod
    async def update_model(*args, **kwargs) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :return: Модель, обновленную в БД
        """
        pass

    @abstractmethod
    async def delete_model(*args, **kwargs) -> object:
        """
        Удаляет модель из БД
        :return: Модель, удаленную из БД
        """
        pass

    @abstractmethod
    async def clear_table(*args, **kwargs) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :return: Пустой список
        """
        pass
