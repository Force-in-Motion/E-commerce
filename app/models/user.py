from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import Boolean, Enum, String, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
from app.models.mixin import TimestampMixin
from app.tools.types import UserRole

if TYPE_CHECKING:
    from app.models import Post, Profile, Order, Cart


class User(Base, TimestampMixin):
    """Класс, описывающий мета информацию таблицы User"""

    __tablename__ = "users"

    email: Mapped[EmailStr] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    password: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.user,
        server_default=UserRole.user.value,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
        uselist=True,
    )

    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        cascade="all, delete",
        lazy="select",
        uselist=False,
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
        uselist=True,
    )

    cart: Mapped["Cart"] = relationship(
        back_populates="user",
        cascade="all, delete",
        lazy="select",
        uselist=False,
    )
