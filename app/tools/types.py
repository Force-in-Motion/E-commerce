from typing import TypeVar, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from pydantic import BaseModel
    from app.interface import ARepo
    from app.models import Base


# Абстрактные типы модели, схемы, адаптера
DBModel = TypeVar("DBModel", bound="Base")
Adapter = TypeVar("Adapter", bound="ARepo")
PDScheme = TypeVar("PDScheme", bound="BaseModel")


# Определяет возможные роли пользователей
class UserRole(str, enum.Enum):
    god = 'god'
    user = "user"
    admin = "admin"
    moderator = "moderator"
