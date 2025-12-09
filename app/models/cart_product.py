from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models import Cart, Product


class CartProduct(Base, TimestampMixin):
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
        nullable=False,
    )

    current_price: Mapped[str] = mapped_column(
        String(255),
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

