from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    func,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from app.models import Product
    from app.models import OrderProducts


class Order(Base):
    """Класс, описывающий мета информацию таблицы Order"""

    __tablename__ = "Order"  # Название таблицы в БД

    __table_args__ = (
        CheckConstraint("char_length(promo_code) = 10", name="ck_promo_code_length"),
    )

    # Описание мета информации таблицы
    promo_code: Mapped[str] = mapped_column(String(10), unique=True)

    comment: Mapped[str] = mapped_column(String)

    total_sum: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    products: Mapped[list["Product"]] = relationship(
        secondary="OrderProducts",
        back_populates="orders",
    )

    product_detail: Mapped["OrderProducts"] = relationship(
        back_populates="order_detail"
    )


# CheckConstraint("length(promo_code) = 10") → гарантирует, что значение будет ровно 10 символов.
# Если указать name=..., SQLAlchemy (или сама СУБД) сгенерирует при ошибке валидации constraint в БД вы получите ошибку с указанием этого имени
# Сразу ясно, что это проверка на длину промокода.


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
