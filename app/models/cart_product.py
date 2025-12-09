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
        default=0,
        server_default="0",
        nullable=False,
    )

    current_price: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default="0",
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

