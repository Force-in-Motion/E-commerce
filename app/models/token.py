from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixin import TimestampMixin

if TYPE_CHECKING:
    from app.models import User


class RefreshToken(Base, TimestampMixin):

    __tablename__ = "refresh_tokens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="refresh_tokens",
        lazy="select",
        uselist=False,
    )
