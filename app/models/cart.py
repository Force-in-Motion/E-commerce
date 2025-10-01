from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from . import CartProduct


class Cart(Base):
    __tablename__ = "Cart"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("User.id"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    products: Mapped[list["CartProduct"]] = relationship(
        back_populates="cart",
        lazy="select",
        cascade="all, delete-orphan",
    )
