from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from service.database.models.base import Base

if TYPE_CHECKING:
    from service.database.models import User


class Profile(Base):
    """Класс, описывающий мета информацию таблицы Profile"""

    __tablename__ = "Profile"

    # Описание мета информации таблицы
    floor: Mapped[str] = mapped_column(
        String, nullable=True, default=None, server_default=None
    )
    age: Mapped[int] = mapped_column(
        Integer, nullable=True, default=None, server_default=None
    )
    married: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=None, server_default=None
    )
    bio: Mapped[str] = mapped_column(
        String, nullable=True, default=None, server_default=None
    )

    # Автоматически записывает дату создания профиля пользователя
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Внешний ключ на id таблицы User, пишется в кавычках чтобы не импортировать сюда User и не было циклического импорта
    # ondelete="CASCADE" Говорит о том, что при удалении пользователя с указанным id удалится и его профиль, на который ссылается эта запись через ForeignKey
    # Удаление записи из Profile (например, профиля с user_id=1) не влияет на таблицу User. Внешний ключ и ON DELETE CASCADE работают только в направлении от родительской таблицы (User) к дочерней (Profile).
    # Это означает, что пользователь с id=1 останется в таблице User, даже если его профиль удален.
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id", ondelete="CASCADE"))

    # Позволяет получать профиль пользователя через атрибут класса user
    user: Mapped["User"] = relationship(back_populates="profile")


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
