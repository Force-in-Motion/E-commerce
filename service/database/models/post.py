from sqlalchemy import String, Text, ForeignKey

from service.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Post(Base):
    """Класс, описывающий мета информацию таблицы Post"""

    __tablename__ = "Post"  # Название таблицы в БД

    # Описание мета информации таблицы
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    # default="" используется когда экземпляр этого класса создается в алхимии, server_default="" используется когда создается колонка в базе данных
    body: Mapped[str] = mapped_column(
        Text, nullable=False, default="", server_default=""
    )
    # Внешний ключ на id таблицы User, пишется в кавычках чтобы не импортировать сюда User и не было циклического импорта
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))


# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.
