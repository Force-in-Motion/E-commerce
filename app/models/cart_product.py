from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from . import Cart
    from . import Product


class CartProduct(Base):
    __tablename__ = "cart_products"

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="idx_unique_cart_product",
        ),
    )

    cart_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("carts.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default="1",
        nullable=False,
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="products",
        lazy="select",
    )
    product: Mapped["Product"] = relationship(
        back_populates="carts",
        lazy="select",
    )


# UniqueConstraint Гарантирует что cart_id и product_id в таблице в одной строке будут уникальны,
# другими словами в одной корзине не может быть одинаковых продуктов, добавленных разными строками,
# будет только одна позиция одного товара, но количество его может быть любым.
# Таким же образом это гарантирует что один и тот же товар может повторяться в разных корзинах только один раз

# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.

# default=1 - Дефолтное значение, работает только на стороне Алхимии
# server_default="1" -  Дефолтное значение, работает только на стороне БД, если указывается одно то должно указываться и другое
