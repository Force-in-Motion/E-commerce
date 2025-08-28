from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import User


class Post(Base):
    """Класс, описывающий мета информацию таблицы Post"""

    __tablename__ = "Post"  # Название таблицы в БД

    # Описание мета информации таблицы
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # default="" используется когда экземпляр этого класса создается в алхимии, server_default="" используется когда создается колонка в базе данных
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        server_default="",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Внешний ключ на id таблицы User, пишется в кавычках чтобы не импортировать сюда User и не было циклического импорта
    user_id: Mapped[int] = mapped_column(
        ForeignKey("User.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Позволяет получать пользователя конкретного поста через атрибут класса user
    user: Mapped["User"] = relationship(back_populates="posts")


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
# server_default="1" -  Дефолтное значение, работает только на стороне БД, если указывается одно то должно указываться и другое
