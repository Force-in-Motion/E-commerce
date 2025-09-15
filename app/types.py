from typing import TypeVar

from pydantic import BaseModel

from app.crud import BaseCrud
from app.models import Base

DBModel = TypeVar("DBModel", bound=Base)
Adapter = TypeVar("Adapter", bound=BaseCrud)
PDScheme = TypeVar("PDScheme", bound=BaseModel)