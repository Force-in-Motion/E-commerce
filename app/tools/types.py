from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel
    from app.interface import ARepo
    from app.models import Base

DBModel = TypeVar("DBModel", bound="Base")
Adapter = TypeVar("Adapter", bound="ARepo")
PDScheme = TypeVar("PDScheme", bound="BaseModel")
