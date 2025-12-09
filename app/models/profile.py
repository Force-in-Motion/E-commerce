from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, TimestampMixin


if TYPE_CHECKING:
    from app.models import User


class Profile(Base, TimestampMixin):
    """Класс, описывающий мета информацию таблицы Profile"""

    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    floor: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    age: Mapped[int] = mapped_column(
        Integer(120),
        nullable=True,
    )

    bio: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="profile",
        lazy="select",
        uselist=False,
    )
