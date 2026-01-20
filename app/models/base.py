from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Родительский класс для всех таблицы базы данных"""

    __abstract__ = True  # Указывает алхимии, что такой таблицы в БД быть не должно, она абстрактная

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
