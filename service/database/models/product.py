from sqlalchemy import String, Integer

from service.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    """Класс, описывающий мета информацию таблицы Product"""

    __tablename__ = "Product"  # Название таблицы в БД

    # Описание мета информации таблицы
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.
