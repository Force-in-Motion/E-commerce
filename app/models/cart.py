from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from . import CartItem


class Cart(Base):
    __tablename__ = "Cart"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("User.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    items: Mapped[list["CartItem"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
    )
