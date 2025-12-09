from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.mixin import TimestampMixin

if TYPE_CHECKING:
    from app.models import User, CartProduct


class Cart(Base, TimestampMixin):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="cart",
        uselist=False,
    )

    products: Mapped[list["CartProduct"]] = relationship(
        back_populates="cart",
        lazy="select",
        cascade="all, delete-orphan",
        uselist=True,
    )
