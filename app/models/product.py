from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.mixin import TimestampMixin


if TYPE_CHECKING:
    from app.models import OrderProducts, CartProduct


class Product(Base, TimestampMixin):
    """Класс, описывающий мета информацию таблицы Product"""

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    orders: Mapped[list["OrderProducts"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select",
        uselist=True,
    )

    carts: Mapped[list["CartProduct"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="select",
        uselist=True,
    )
