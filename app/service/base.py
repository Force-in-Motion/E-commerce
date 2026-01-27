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
    ) -> Optional[list[DBModel]]:
        """
        Возвращает все модели согласно полученым параметрам
        :param session: Асинхронная сессия
        :param user_id: Опциональный параметр, id пользователя
        :return: Список всех ORM моделей | None
        """
        if user_id is not None:
            return await cls.repo.get_all_by_user_id(
                user_id=user_id,
                session=session,
            )

        return cls.repo.get_all(session=session)
        

    @classmethod
    async def get_model(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        model_id: Optional[int] = None,
    ) -> Optional[DBModel]:
        """
        Возвращает модель согласно полученым параметрам
        :param session: Асинхронная сессия
        :param user_id: Опциональный параметр, id пользователя
        :param model_id: Опциональный параметр, id  модели
        :return: ORM Модель | None
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
        

    @classmethod
    async def get_all_models_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> Optional[list[DBModel]]:
        """
        Возвращает все модели, созданные в указанном временном диапазоне
        :param dates: Определяет временной диапазон
        :param session: Асинхронная сессия
        :return: Список ORM  моделей, созданных в указанном временном диапазоне
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
        user_id: Optional[int] = None,
    ) -> DBModel:
        """
        Регистрирует модель в БД согласно полученым параметрам
        :param scheme_in: Pydantic схема - объект, содержащий данные для регистрации модели
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Зарегистрированную ORM модель
        """

        data = scheme_in.model_dump()

        if user_id is not None:
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
        Изменяет модель в БД, согласно полученым параметрам, полностью или частично
        :param scheme_in: Pydantic схема - объект, содержащий данные для изменения модели
        :param partial: Флаг, определяющий полное или частичное обновление
        :param user_id: Опциональный параметр, id пользователя
        :param model_id: Опциональный параметр, id модели
        :param session: Асинхронная сессия
        :return: Измененную ORM модель
        """
        new_data = scheme_in.model_dump(
            exclude_unset=partial,
            exclude_none=True,
        )

        model = await cls.get_model(
            session=session,
            user_id=user_id,
            model_id=model_id,
        )

        if model is None:
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
        Удаляет модель из БД согласно полученым параметрам
        :param user_id: Опциональный параметр, id пользователя
        :param model_id: Опциональный параметр, id модели
        :param session: Асинхронная сессия
        :return: Удаленную ORM модель
        """
        model = await cls.get_model(
            session=session,
            user_id=user_id,
            model_id=model_id,
        )

        if model is None:
            return None

        return await cls.repo.delete(
            del_model=model,
            session=session,
        )

    @classmethod
    async def delete_all_models(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> list:
        """
        Удаляет модель из БД согласно полученым параметрам
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        list_models = await cls.get_all_models(
            session=session,
            user_id=user_id,
        )

        if not list_models:
            return None

        return await cls.repo.delete_all(
            list_models=list_models,
            session=session,
        )

    @classmethod
    async def clear_table(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Очищает таблицу БД
        :param session: объект асинхронной сессии
        :return: Пустой список
        """
        return await cls.repo.clear(session=session)
