from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from app.models import Order
    from app.models import Product


class OrderProducts(Base):
    """Класс, описывающий мета информацию таблицы OrderProducts, таблица связывающая заказы и продукты
    Ассоциативная модель, поскольку содержит не только внешние ключи, но и дополнительные личные поля и параметры
    """

    __tablename__ = "OrderProducts"  # Название таблицы в БД

    __table_args = UniqueConstraint(
        "order_id",
        "product_id",
        name="idx_unique_order_product",
    )
    # Описание мета информации таблицы
    order_id: Mapped[int] = mapped_column(
        ForeignKey("Order.id", ondelete="CASCADE"),
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE"),
    )
    count: Mapped[int] = mapped_column(default=1, server_default="1")

    order: Mapped[list["Order"]] = relationship(back_populates="order_detail")
    product: Mapped[list["Product"]] = relationship(back_populates="product_detail")


# UniqueConstraint Гарантирует что order_id и product_id в таблице в одной строке будут уникальны,
# другими словами в одном заказе не может быть одинаковых продуктов, добавленных разными строками,
# будет только одна позиция одного товара, но количество его может быть любым.
# Таким же образом это гарантирует что один и тот же товар может повторяться в разных заказах только один раз

# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.
