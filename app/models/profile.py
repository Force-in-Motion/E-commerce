from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import User


class Profile(Base):
    """Класс, описывающий мета информацию таблицы Profile"""

    __tablename__ = "profiles"

    # Описание мета информации таблицы
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )


from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import User


class Profile(Base):
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
        String(150),
        nullable=False,
        default=None,
        server_default=None,
    )

    floor: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        server_default=None,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        server_default=None,
    )

    bio: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        server_default=None,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="profile",
        lazy="select",
        uselist=False,
    )

    address: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    floor: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        server_default=None,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        server_default=None,
    )

    bio: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        server_default=None,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


    user: Mapped["User"] = relationship(
        back_populates="profile",
        lazy="select",
        uselist=False,
    )


# Mapped — это обобщённый тип (generic type) из модуля sqlalchemy.orm,
# для аннотации типов атрибутов модели. Он указывает, что атрибут класса (например, name)
# связан с колонкой в базе данных и имеет определённый Python-тип (например, str).


# mapped_column — это функция из sqlalchemy.orm, для определения колонок и их параметров (тип, ограничения, индексы)
# в декларативных моделях. Она создаёт объект колонки и связывает его с атрибутом, аннотированным Mapped.

# Mapped и mapped_column используются для определения модели, которая регистрируется в Base.metadata.

# relationship создаёт атрибут в классе модели, который позволяет:
# Получать связанные объекты (например, список постов пользователя через user.posts).
# Автоматически загружать связанные данные из базы, когда ты обращаешься к этому атрибуту.

# Это говорит SQLAlchemy, что у объекта Post есть атрибут user, который возвращает объект User, связанный с этим постом.
# back_populates="posts" указывает обратную связь: в модели User есть атрибут posts, который ссылается на объект User.


# ondelete="CASCADE" Говорит о том, что при удалении пользователя с указанным id удалится и его профиль, на который ссылается эта запись через ForeignKey
# Удаление записи из Profile (например, профиля с user_id=1) не влияет на таблицу User. Внешний ключ и ON DELETE CASCADE работают только в направлении от родительской таблицы (User) к дочерней (Profile).
# Это означает, что пользователь с id=1 останется в таблице User, даже если его профиль удален.

# default=1 - Дефолтное значение, работает только на стороне Алхимии
# server_default="1" - Дефолтное значение, работает только на стороне БД, если указывается одно то должно указываться и другое
