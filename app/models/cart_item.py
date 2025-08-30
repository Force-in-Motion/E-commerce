from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .cart import Cart
    from . import Product


class CartItem(Base):
    __tablename__ = "CartItem"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("Cart.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("Product.id", ondelete="CASCADE")
    )
    quantity: Mapped[int] = mapped_column(default=1, server_default="1", nullable=False)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
