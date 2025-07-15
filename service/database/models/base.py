from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """Родительский класс для всех таблицы базы данных"""

    __abstract__ = True  # Указывает алхимии, что такой таблицы в БД быть не должно, она абстрактная

    @classmethod
    # Декоратор позволяет автоматически генерировать названия таблиц исходя из названия моделей SQLAlchemy
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.title()

    # id присутствует во всех таблицах, поэтому его можно указать в родительской,
    # чтобы при наследовании он по умолчанию был уже во всех дочерних таблицах
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
