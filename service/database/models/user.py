from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from service.database.models.base import Base


class User(Base):
    """Класс, описывающий мета информацию таблицы User"""

    __tablename__ = "User"  # Название таблицы в БД

    # Описание мета информации таблицы
    name: Mapped[str] = mapped_column(String, nullable=False)
    floor: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)


# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.
