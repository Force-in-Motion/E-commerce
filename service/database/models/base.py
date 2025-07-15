from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """Родительский класс для всех таблицы базы данных"""

    __abstract__ = True  # Указывает алхимии, что такой таблицы в БД быть не должно, она абстрактная

    @classmethod
    # Этот декоратор позволяет реализовать логику, которая автоматически генерирует название таблицы в БД,
    # которое соответствует названию класса SQLAlchemy, в котором она описана
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.title()

    # id присутствует во всех таблицах, поэтому его можно указать в родительской,
    # чтобы при наследовании он по умолчанию был уже во всех дочерних таблицах
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
