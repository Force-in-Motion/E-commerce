from datetime import datetime

from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Order(Base):
    """Класс, описывающий мета информацию таблицы Order"""

    __tablename__ = "Order"  # Название таблицы в БД

    # Описание мета информации таблицы
    promo_code: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    total_sum: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.

# relationship создаёт атрибут в классе модели, который позволяет:
# Получать связанные объекты (например, список постов пользователя через user.posts).
# Автоматически загружать связанные данные из базы, когда ты обращаешься к этому атрибуту.

# Это говорит SQLAlchemy, что у объекта Post есть атрибут user, который возвращает объект User, связанный с этим постом.
# back_populates="posts" указывает обратную связь: в модели User есть атрибут posts, который ссылается на объект User.
