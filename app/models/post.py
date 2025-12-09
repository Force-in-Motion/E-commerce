from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.models import Base, User, TimestampMixin


class Post(Base, TimestampMixin):
    """Класс, описывающий мета информацию таблицы Post"""

    __tablename__ = "posts"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="posts",
        lazy="select",
        uselist=False,
    )
