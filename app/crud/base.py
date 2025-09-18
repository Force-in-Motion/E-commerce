from datetime import datetime
from typing import Optional, Type, TypeVar, Generic, cast

from pydantic import BaseModel
from sqlalchemy import select, text, delete, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.interface import Crud
from app.tools import Utils
from app.tools.custom_err import DatabaseError
from app.types import DBModel, PDScheme


# DBModel - будет подставляться конкретная ORM модель, наследуемая от Base напрямую или через других предков
# PDScheme - будет подставляться конкретная Pydantic схема, наследуемая от BaseModel напрямую или через других предков


class BaseCrud(Generic[DBModel, PDScheme], Crud):
    """
    Базовый CRUD.
    model должен быть определён в наследнике.
    """

    # Optional нужен для типовой корректности и работы статического анализа
    # базовый CRUD не может знать заранее модель и схему, которые будут определены в дочерних классах.
    model: Type[DBModel]  # Будет переопределено в наследниках
    scheme: Type[PDScheme]  # Будет переопределено в наследниках

    @classmethod
    @Utils.ensure_model
    async def get_all(
        cls,
        model: Type[DBModel],
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает всех моделей пользователей из БД
        :param model: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """
        try:
            stmt = select(model).order_by(model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Database operation failed for {model.__name__}"
            ) from e

    @classmethod
    @Utils.ensure_model
    async def get_by_id(
        cls,
        model: Type[DBModel],
        model_id: int,
        session: AsyncSession,
    ) -> Optional[DBModel]:
        """
        Возвращает модель пользователя по его id из БД
        :param model_id: id модели конкретного пользователя
        :param model: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        try:
            return await session.get(model, model_id)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Database operation failed for {model.__name__}"
            ) from e

    @classmethod
    @Utils.ensure_model
    async def get_by_date(
        cls,
        model: Type[DBModel],
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает список всех моделей пользователей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param model: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех моделей пользователей, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(model)
                .where(model.created_at.between(*dates))
                .order_by(model.created_at.desc())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError as e:

            raise DatabaseError(
                f"Database operation failed for {model.__name__}"
            ) from e

    @classmethod
    @Utils.ensure_model
    async def create(
        cls,
        model: Type[DBModel],
        scheme_input: PDScheme,
        session: AsyncSession,
    ) -> DBModel:
        """
        Добавляет модель пользователя в БД
        :param scheme_input: Pydantic Схема - объект, содержащий данные пользователя
        :param model: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        try:
            model = model(**scheme_input.model_dump())

            session.add(model)
            await session.commit()
            await session.refresh(
                model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Failed to add {model.__name__}") from e

    @classmethod
    @Utils.ensure_model
    async def update(
        cls,
        model: Type[DBModel],
        scheme_input: PDScheme,
        update_model: DBModel,
        session: AsyncSession,
        partial: bool = False,
    ) -> DBModel:
        """
        Обновляет данные модели пользователя в БД полностью или частично
        :param scheme_input: Pydantic Схема - объект, содержащий данные пользователя
        :param update_model: ORM Модель - конкретный объект в БД, найденный по id
        :param model: Объект сессии, полученный в качестве аргумента
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: Модель пользователя, обновленную в БД
        """
        try:
            for key, value in scheme_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(update_model, key, value)

            await session.commit()
            await session.refresh(
                update_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return update_model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Failed to update {model.__name__}") from e

    @classmethod
    @Utils.ensure_model
    async def delete(
        cls,
        model: Type[DBModel],
        del_model: DBModel,
        session: AsyncSession,
    ) -> DBModel:
        """
        Удаляет модель пользователя из БД
        :param del_model: ORM Модель - конкретный объект в БД, найденный по id для удаления
        :param model: Модель, которая должна быть определена в потомках, чтобы методы базового CRUD, понимали с какой моделью они работают
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """
        try:
            await session.delete(del_model)
            await session.commit()
            return del_model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Failed to delete {model.__name__}") from e

    @classmethod
    @Utils.ensure_model
    async def clear(
        cls,
        model: Type[DBModel],
        session: AsyncSession,
    ) -> list:
        """
        Очищает таблицу моделей пользователей и сбрасывает последовательность id моделей
        :param model: Модель, которая должна быть определена в потомках, чтобы методы базового CRUD, понимали с какой моделью они работают
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Пустой список
        """
        # Имя таблицы.
        # Получаем список первичных ключей и берем колонку id.
        # Формируем строку из названия таблицы, название столбца, счетчик которого нужно сбросить и добавляем _seq
        table = cast(Table, model.__table__)
        pk_column = next(iter(table.primary_key.columns))
        seq_name = f"{table.name}_{pk_column.name}_seq"

        try:
            await session.execute(delete(model))
            await session.execute(text(f'ALTER SEQUENCE "{seq_name}" RESTART WITH 1'))
            await session.commit()
            return []

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Failed to clear {model.__name__}") from e
