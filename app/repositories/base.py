from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Type, Generic, cast
from sqlalchemy import select, text, delete, Table

from app.interface import ARepo
from app.tools.exeptions import DatabaseError
from app.tools.types import DBModel


class BaseRepo(Generic[DBModel], ARepo):
    """
    Базовый Репозиторий.
    model должен быть определён в наследнике.
    """

    model: Type[DBModel]  # Будет переопределено в наследниках

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> Optional[list[DBModel]]:
        """
        Возвращает все модели, содержащиеся в конкретной таблице БД
        :param session: Объект асинхронной сессии
        :return: Список всех ORM моделей
        """
        try:
            stmt = select(cls.model).order_by(cls.model.id)
            result = await session.execute(stmt)

            return list(result.scalars().all())

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving all {cls.model.__name__}s"
            ) from e

    @classmethod
    async def get_all_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[list[DBModel]]:
        """
        Возвращает все модели, содержащиеся в конкретной таблице БД по user_id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: Список всех ORM моделей по user_id
        """
        try:
            stmt = select(cls.model).where(cls.model.user_id == user_id)
            result = await session.execute(stmt)

            return list(result.scalars().all())

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by user id"
            ) from e

    @classmethod
    async def get_by_id(
        cls,
        model_id: int,
        session: AsyncSession,
    ) -> Optional[DBModel]:
        """
        Возвращает модель по ее id из конкретной таблицы БД
        :param model_id: id модели
        :param session: объект асинхронной сессии
        :return: ORM модель по ее id
        """
        try:
            return await session.get(cls.model, model_id)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by id"
            ) from e

    @classmethod
    async def get_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[DBModel]:
        """
        Возвращает модель, содержащиеся в конкретной таблице БД по user_id
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: ORM модель по user_id
        """
        try:
            stmt = select(cls.model).where(cls.model.user_id == user_id)
            result = await session.execute(stmt)

            return result.scalars().one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by user id"
            ) from e

    @classmethod
    async def get_by_user_and_model_id(
        cls,
        model_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[DBModel]:
        """
        Возвращает модель, содержащиеся в конкретной таблице БД по user_id и id модели
        :param model_id: id модели
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: ORM модель по user_id и id модели
        """
        try:
            stmt = select(cls.model).where(
                cls.model.id == model_id,
                cls.model.user_id == user_id,
            )

            result = await session.execute(stmt)
            return result.scalars().one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by user and model id"
            ) from e

    @classmethod
    async def get_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> Optional[list[DBModel]]:
        """
        Возвращает список всех модель, содержащихся в конкретной таблице БД, добавленных за указанный интервал времени
        :param session: объект асинхронной сессии
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :return: список всех ORM моделей, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.created_at.between(*dates))
                .order_by(cls.model.created_at.desc())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving list {cls.model.__name__}s by dates"
            ) from e

    @classmethod
    async def create(
        cls,
        model: DBModel,
        session: AsyncSession,
    ) -> DBModel:
        """
        Добавляет модель пользователя в конкретную таблицу БД
        :param model: ORM модель
        :param session: объект асинхронной сессии
        :return: ORM модель, добавленную в БД
        """
        try:
            session.add(model)
            await session.commit()
            await session.refresh(model)

            return model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when adding {cls.model.__name__}") from e

    @classmethod
    async def update(
        cls,
        new_data: dict,
        update_model: DBModel,
        session: AsyncSession,
    ) -> DBModel:
        """
        Обновляет данные модели в конкретной таблице БД полностью или частично
        :param new_data: dict с новыми данными для изменения ORM модели
        :param update_model: ORM Модель - конкретный объект в БД
        :param session: объект асинхронной сессии
        :return: ORM модель, обновленную в БД
        """
        try:
            for key, value in new_data.items():
                if value is not None:
                    setattr(update_model, key, value)

            await session.commit()
            await session.refresh(update_model)
            return update_model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when updating {cls.model.__name__}") from e

    @classmethod
    async def delete(
        cls,
        del_model: DBModel,
        session: AsyncSession,
    ) -> DBModel:
        """
        Удаляет ORM модель из конкретной таблицы БД
        :param del_model: ORM Модель - конкретный объект в БД для удаления
        :param session: объект асинхронной сессии
        :return: ORM модель, удаленную из БД
        """
        try:
            await session.delete(del_model)
            await session.commit()
            return del_model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when deleting {cls.model.__name__}") from e

    @classmethod
    async def delete_all(
        cls,
        list_models: list[DBModel],
        session: AsyncSession,
    ) -> list:
        """
        Удаляет все ORM модели из полученного списка ORM моделей
        :param list_models: список ORM моделей для удаления
        :param session: объект асинхронной сессии
        :return: Пустой список
        """
        try:
            for model in list_models:
                await session.delete(model)
            await session.commit()
            return []

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when deleting list {cls.model.__name__}") from e

    @classmethod
    async def clear(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Очищает таблицу БД и сбрасывает последовательность id моделей
        :param session: объект асинхронной сессии
        :return: Пустой список
        """
        table = cast(Table, cls.model.__table__)
        pk_column = next(iter(table.primary_key.columns))
        seq_name = f"{table.name}_{pk_column.name}_seq"

        try:
            await session.execute(delete(cls.model))
            await session.execute(text(f'ALTER SEQUENCE "{seq_name}" RESTART WITH 1'))
            await session.commit()
            return []

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when clearing table {cls.model.__name__}") from e
