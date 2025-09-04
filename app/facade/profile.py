from typing import Optional

from app.facade import BaseFacade
from app.models import Profile as Profile_model


class ProfileFacade(BaseFacade):

    @staticmethod
    async def get_all(*args, **kwargs) -> list[object]:
        """
        Возвращает все модели категории из БД
        :return: Список всех моделей
        """
        pass

    @staticmethod
    async def get_by_id(*args, **kwargs) -> Optional[object]:
        """
        Возвращает модель по её id из БД
        :return: Модель | None
        """
        pass

    @staticmethod
    async def get_by_user_id(*args, **kwargs) -> Optional[Profile_model]:
        """
        Возвращает модель профиля, соответствующую id пользователя в БД
        :return: Модель профиля | None
        """

    @staticmethod
    async def get_by_date(*args, **kwargs) -> list[object]:
        """
        Возвращает список всех моделей, добавленных за указанный интервал времени
        :return: список всех моделей, добавленных за указанный интервал времени
        """
        pass

    @staticmethod
    async def create(*args, **kwargs) -> object:
        """
        Добавляет модель в БД
        :return: Модель пользователя, добавленную в БД
        """
        pass

    @staticmethod
    async def update(*args, **kwargs) -> object:
        """
        Обновляет данные модели в БД полностью или частично
        :return: Модель, обновленную в БД
        """
        pass

    @staticmethod
    async def delete(*args, **kwargs) -> object:
        """
        Удаляет модель из БД
        :return: Модель, удаленную из БД
        """
        pass

    @staticmethod
    async def clear(*args, **kwargs) -> list:
        """
        Очищает базу данных моделей определенной категории и сбрасывает последовательность id моделей
        :return: Пустой список
        """
        pass
