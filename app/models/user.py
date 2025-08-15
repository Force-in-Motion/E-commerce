from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    pass


class User(Base):
    """Класс, описывающий мета информацию таблицы User"""

    __tablename__ = "User"  # Название таблицы в БД

    # Описание мета информации таблицы
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    # Автоматически записывает дату создания пользователя
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Позволяет получать список постов пользователя через атрибут класса posts
    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
    )

    # Позволяет получать профиль пользователя через атрибут класса profile
    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        uselist=False,  # uselist: Указывает, является ли связь коллекцией (True для один-ко-многим, False для один-к-одному)
        lazy="select",
        cascade="all, delete",
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

# Это говорит SQLAlchemy, что у объекта User есть атрибут posts, который возвращает список объектов Post, связанных с этим пользователем.
# back_populates="user" указывает обратную связь: в модели Post есть атрибут user, который ссылается на объект User.

# cascade="all, delete-orphan", Это настройка в relationship на стороне родительской таблицы (User), которая управляет каскадом при операциях с объектами в сессии (например, session.delete(user)).
# Она определяет, что делать с связанными объектами в памяти. Это обеспечивает, что связанные объекты (posts, profile) удаляются в памяти Python и синхронизируются с БД.
# предназначен для коллекций (один-ко-многим, как posts), а не для отношений один-к-одному (profile)

# cascade="all, delete" Используется для каскадного удаления при связи один к одному.
# lazy="joined Выполняет LEFT OUTER JOIN при загрузке объекта, загружая связанные данные сразу. # Для один-к-одному (User.profile) или небольших коллекций (User.posts).
