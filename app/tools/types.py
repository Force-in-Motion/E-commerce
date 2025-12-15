from typing import TypeVar, TYPE_CHECKING
import enum

if TYPE_CHECKING:
    from pydantic import BaseModel
    from app.interface import ARepo
    from app.models import Base


# Абстрактные типы модели, схемы, адаптера
DBModel = TypeVar("DBModel", bound="Base")
Repo = TypeVar("Repo", bound="ARepo")
PDScheme = TypeVar("PDScheme", bound="BaseModel")


# Определяет возможные роли пользователей
class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"
