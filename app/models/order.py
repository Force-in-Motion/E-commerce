from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    CheckConstraint,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.mixin import TimestampMixin


if TYPE_CHECKING:
    from app.models import User, OrderProducts


class Order(Base, TimestampMixin):
    """Класс, описывающий мета информацию таблицы Order"""

    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "promo_code IS NULL OR char_length(promo_code) = 10",
            name="err_promo_code_length",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    total_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    promo_code: Mapped[str | None] = mapped_column(
        String(10),
        unique=True,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="orders",
        lazy="select",
        uselist=False,
    )

    products: Mapped[list["OrderProducts"]] = relationship(
        back_populates="order",
        lazy="select",
        cascade="all, delete-orphan",
        uselist=True,
    )
