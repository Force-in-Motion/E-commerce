from datetime import datetime
from typing import Optional, Type, TypeVar, Generic, cast

from pydantic import BaseModel
from sqlalchemy import select, text, delete, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.interface import Crud
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
    async def _check_model(cls, model: Optional[Type[DBModel]]) -> Type[DBModel]:
        """
        Выполняет проверку переопределения переменной окружения,
        в дочернем классе в данном случае модели
        :return: БД Модель
        """
        if model is None:
            raise NotImplementedError(f"{cls.__name__} must defined this attribute")

        return model

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
        cls_model = await cls._check_model(cls.model)

        try:
            stmt = select(cls_model).order_by(cls_model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError(f"{cls_model.__name__} table is empty")

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
        cls_model = await cls._check_model(cls.model)

        try:
            return await session.get(cls_model, model_id)

        except SQLAlchemyError:
            raise DatabaseError(f"{cls_model.__name__} model with this id not found")

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
        cls_model = await cls._check_model(cls.model)

        try:
            stmt = (
                select(cls_model)
                .where(cls_model.created_at.between(*dates))
                .order_by(cls_model.created_at.desc())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            raise DatabaseError(
                f"There are no added {cls_model.__name__} models in this range"
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
        cls_model = await cls._check_model(cls.model)

        try:
            model = cls_model(**scheme_input.model_dump())

            session.add(model)
            await session.commit()
            await session.refresh(
                model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"Error adding {cls_model.__name__} model")

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
        cls_model = await cls._check_model(cls.model)

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
            raise DatabaseError(f"Error updating {cls_model.__name__} model")

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
        cls_model = await cls._check_model(cls.model)

        try:
            await session.delete(model)
            await session.commit()
            return model

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"Error deleting {cls_model.__name__} model")

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
        cls_model = await cls._check_model(cls.model)

        # Имя таблицы.
        # Получаем список первичных ключей и берем колонку id.
        # Формируем строку из названия таблицы, название столбца, счетчик которого нужно сбросить и добавляем _seq
        table = cast(Table, cls_model.__table__)
        pk_column = next(iter(table.primary_key.columns))
        seq_name = f"{table.name}_{pk_column.name}_seq"

        try:
            await session.execute(delete(cls_model))
            await session.execute(text(f'ALTER SEQUENCE "{seq_name}" RESTART WITH 1'))
            await session.commit()
            return []

        except SQLAlchemyError:
            await session.rollback()
            raise DatabaseError(f"Error clearing {cls_model.__name__} table")
