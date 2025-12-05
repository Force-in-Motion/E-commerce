from datetime import datetime
from typing import Optional, Type, Generic, cast

from sqlalchemy import select, text, delete, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.interface import ARepo
from app.tools.custom_err import DatabaseError
from app.tools.types import DBModel, PDScheme


# DBModel - будет подставляться конкретная ORM модель, наследуемая от Base напрямую или через других предков
# PDScheme - будет подставляться конкретная Pydantic схема, наследуемая от BaseModel напрямую или через других предков


class BaseCrud(Generic[DBModel], ARepo):
    """
    Базовый CRUD.
    model должен быть определён в наследнике.
    """

    # Optional нужен для типовой корректности и работы статического анализа
    # базовый CRUD не может знать заранее модель и схему, которые будут определены в дочерних классах.
    model: Type[DBModel]  # Будет переопределено в наследниках

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
        try:
            stmt = select(cls.model).order_by(cls.model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving all {cls.model.__name__}s"
            ) from e

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
        try:
            return await session.get(cls.model, model_id)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by id"
            ) from e

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
        scheme_in: PDScheme,
        session: AsyncSession,
    ) -> DBModel:
        """
        Добавляет модель пользователя в БД
        :param scheme_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, добавленную в БД
        """
        try:
            model = cls.model(**scheme_in.model_dump())

            session.add(model)
            await session.commit()
            await session.refresh(
                model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что User_model содержит актуальное состояние из базы.
            return model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when adding {cls.model.__name__}") from e

    @classmethod
    async def update(
        cls,
        scheme_in: PDScheme,
        update_model: DBModel,
        session: AsyncSession,
        partial: bool = False,
    ) -> DBModel:
        """
        Обновляет данные модели пользователя в БД полностью или частично
        :param scheme_in: Pydantic Схема - объект, содержащий данные пользователя
        :param update_model: ORM Модель - конкретный объект в БД, найденный по id
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
            for key, value in scheme_in.model_dump(exclude_unset=partial).items():
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
            raise DatabaseError(f"Error when updating {cls.model.__name__}") from e

    @classmethod
    async def delete(
        cls,
        del_model: DBModel,
        session: AsyncSession,
    ) -> DBModel:
        """
        Удаляет модель пользователя из БД
        :param del_model: ORM Модель - конкретный объект в БД, найденный по id для удаления
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя, удаленную из БД
        """
        try:
            await session.delete(del_model)
            await session.commit()
            return del_model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when deleting {cls.model.__name__}") from e

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
        # Имя таблицы.
        # Получаем список первичных ключей и берем колонку id.
        # Формируем строку из названия таблицы, название столбца, счетчик которого нужно сбросить и добавляем _seq
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
            raise DatabaseError(
                f"Error when clearing table {cls.model.__name__}"
            ) from e
