from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge, Le
from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(30)]
    description: Annotated[str, MinLen(3), MaxLen(200)]
    price: Annotated[int, Ge(1), Le(1_000_000)]


class ProductUpdate(BaseModel):
    name: Optional[Annotated[str, MinLen(3), MaxLen(30)]] = None
    description: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None
    price: Optional[Annotated[int, Ge(1), Le(1_000_000)]] = None


class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    created_at: datetime
    updated_at: datetime
