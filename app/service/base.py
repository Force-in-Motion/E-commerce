from datetime import datetime
from typing import Type, Generic, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.interface.service import AService
from app.tools.types import DBModel, PDScheme, Repo


class BaseService(Generic[Repo], AService):

    repo: Type[Repo]

    @classmethod
    async def get_all_models(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> list[DBModel]:
        """
        Возвращает результат выполнения метода получения всех моделей пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """
        if user_id is not None:
            return await cls.repo.get_all_by_user_id(
                user_id=user_id,
                session=session,
            )

        return await cls.repo.get_all(session=session)

    @classmethod
    async def get_model(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        model_id: Optional[int] = None,
    ) -> Optional[DBModel]:
        """
        Универсальный метод получения модели по user_id, model_id или обоим сразу.
        :param session: AsyncSession
        :param user_id: id пользователя
        :param model_id: id модели
        :return: Найденная модель или None
        """
        if user_id is not None and model_id is not None:
            return await cls.repo.get_by_user_and_model_id(
                model_id=model_id,
                user_id=user_id,
                session=session,
            )

        if model_id is not None:
            return await cls.repo.get_by_id(model_id=model_id, session=session)

        if user_id is not None:
            return await cls.repo.get_by_user_id(user_id=user_id, session=session)

        return None

    @classmethod
    async def get_all_models_by_date(
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
        cls, scheme_in: PDScheme, session: AsyncSession, user_id: Optional[int] = None
    ) -> DBModel:
        """
        Возвращает результат выполнения метода добавления модели пользователя в БД
        :param scheme_in: Pydantic Схема - объект, содержащий данные модели пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        async with session.begin():

            data = scheme_in.model_dump()

            if user_id:
                data["user_id"] = user_id

            return await cls.repo.create(
                model=cls.repo.model(**data),
                session=session,
            )

    @classmethod
    async def update_model(
        cls,
        scheme_in: PDScheme,
        session: AsyncSession,
        user_id: Optional[int] = None,
        model_id: Optional[int] = None,
        partial: bool = False,
    ) -> Optional[DBModel]:
        """
        Возвращает результат выполнения метода обновления данных модели пользователя в БД полностью или частично
        :param scheme_in: Pydantic Схема - объект, содержащий данные пользователя
        :param model_id: ORM Модель - конкретный объект модели в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
        :return: Модель пользователя, обновленную в БД
        """
        async with session.begin():

            new_data = scheme_in.model_dump(
                exclude_unset=partial,
                exclude_none=True,
            )

            model = await cls.get_model(
                session=session,
                user_id=user_id,
                model_id=model_id,
            )

            if not model:
                return None

            return await cls.repo.update(
                new_data=new_data,
                update_model=model,
                session=session,
            )

    @classmethod
    async def delete_model(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        model_id: Optional[int] = None,
    ) -> Optional[DBModel]:
        """
        Возвращает результат выполнения метода удаления модели пользователя из БД
        :param model_id: ORM Модель - конкретный объект модели в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """
        async with session.begin():

            model = await cls.get_model(
                session=session,
                user_id=user_id,
                model_id=model_id,
            )

            if not model:
                return None

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
