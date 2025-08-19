from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from app.models import Order
    from app.models import OrderProducts


class Product(Base):
    """Класс, описывающий мета информацию таблицы Product"""

    __tablename__ = "Product"  # Название таблицы в БД

    # Описание мета информации таблицы
    name: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str] = mapped_column(String, nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(  # Связка на сквозь
        DateTime(timezone=True),
        server_default=func.now(),
    )

    orders: Mapped[list["Order"]] = relationship(
        secondary="OrderProducts",
        back_populates="products",
    )

    product_detail: Mapped["OrderProducts"] = relationship(
        back_populates="product"
    )  # Полноценная модель-связка


# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.

# relationship создаёт атрибут в классе модели, который позволяет:
# Получать связанные объекты (например, список постов пользователя через user.posts).
# Автоматически загружать связанные данные из базы, когда ты обращаешься к этому атрибуту.

# Это говорит SQLAlchemy, что у объекта Product есть атрибут orders, который возвращает список объектов Order, связанные с этим продуктом.
# back_populates="products" указывает обратную связь: в модели Order есть атрибут products, который ссылается на список объектов Product.


# Сквозная связь через secondary - Удобно, когда таблица-связка (OrderProducts) ничего больше не хранит, кроме order_id и product_id.
# Тогда ты просто работаешь через order.products или product.orders, и тебе не важно, как устроена связка.
# Минус: ты не можешь добавить дополнительные данные (например, count или скидку на товар в заказе). Таблица не содержит ничего кроме внешних ключей

# Полноценная модель-связка - Этот вариант нужен, если у связки есть дополнительные поля — например:
# count (количество товара в заказе),
# price на момент заказа,
# discount,
# статус (например, "подарок").
# В этом случае OrderProducts становится полноценной ассоциативной сущностью, а не просто связкой.
