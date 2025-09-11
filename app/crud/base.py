from datetime import datetime
from typing import Optional, Type, TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy import select, text, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.interface import Crud
from app.tools.custom_err import DatabaseError

# DBModel - будет подставляться конкретная ORM модель, наследуемая от Base напрямую или через других предков
# PDScheme - будет подставляться конкретная Pydantic схема, наследуемая от BaseModel напрямую или через других предков
DBModel = TypeVar("DBModel", bound=DeclarativeBase)
PDScheme = TypeVar("PDScheme", bound=BaseModel)


class BaseCrud(Generic[DBModel, PDScheme], Crud):

    model: Optional[Type[DBModel]]
    scheme: Optional[Type[PDScheme]]

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает всех моделей пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список всех моделей пользователей
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        try:
            stmt = select(cls.model).order_by(cls.model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError(f"{cls.model.__name__} table is empty")

    @classmethod
    async def get_by_id(
        cls,
        model_id: int,
        session: AsyncSession,
    ) -> Optional[DBModel]:
        """
        Возвращает модель пользователя по его id из БД
        :param model_id: id модели конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        try:
            return await session.get(cls.model, model_id)

        except SQLAlchemyError:
            raise DatabaseError(f"{cls.model.__name__} model with this id not found")

    @classmethod
    async def get_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[DBModel]:
        """
        Возвращает список всех моделей пользователей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех моделей пользователей, добавленных за указанный интервал времени
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        try:
            stmt = (
                select(cls.model)
                .where(cls.model.created_at.between(*dates))
                .order_by(cls.model.created_at.desc())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError(
                f"{cls.model.__name__}There are no added models in this range"
            )

    @classmethod
    async def create(
        cls,
        scheme_input: PDScheme,
        session: AsyncSession,
    ) -> DBModel:
        """
        Добавляет модель пользователя в БД
        :param scheme_input: Pydantic Схема - объект, содержащий данные пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        try:
            model = cls.model(**scheme_input.model_dump())

            session.add(model)
            await session.commit()
            await session.refresh(
                model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"{cls.model.__name__}Error adding model")

    @classmethod
    async def update(
        cls,
        scheme_input: PDScheme,
        model: DBModel,
        session: AsyncSession,
        partial: bool = False,
    ) -> DBModel:
        """
        Обновляет данные модели пользователя в БД полностью или частично
        :param scheme_input: Pydantic Схема - объект, содержащий данные пользователя
        :param model: ORM Модель - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: Модель пользователя, обновленную в БД
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        try:
            for key, value in scheme_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(model, key, value)

            await session.commit()
            await session.refresh(
                model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"{cls.model.__name__}Error updating model")

    @classmethod
    async def delete(
        cls,
        model: DBModel,
        session: AsyncSession,
    ) -> DBModel:
        """
        Удаляет модель пользователя из БД
        :param model: ORM Модель - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        try:
            await session.delete(model)
            await session.commit()
            return model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"{cls.model.__name__}Error deleting model")

    @classmethod
    async def clear(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Очищает таблицу моделей пользователей и сбрасывает последовательность id моделей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Пустой список
        """
        if cls.model is None:
            raise NotImplementedError("cls.model must be defined in subclass")

        # Имя таблицы.
        # Получаем список первичных ключей и берем колонку id.
        # Формируем строку из названия таблицы, название столбца, счетчик которого нужно сбросить и добавляем _seq
        table = cls.model.__table__
        pk = list(table.primary_key)[0]
        seq_name = f"{table.name}_{pk.name}_seq"

        try:
            await session.execute(delete(cls.model))
            await session.execute(text(f'ALTER SEQUENCE "{seq_name}" RESTART WITH 1'))
            await session.commit()
            return []

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"{cls.model.__name__}Error clearing table")
