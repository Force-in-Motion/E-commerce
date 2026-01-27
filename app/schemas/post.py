from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge
from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(100)]
    body: Annotated[str, MinLen(3), MaxLen(700)]


class PostUpdate(BaseModel):
    title: Optional[Annotated[str, MinLen(3), MaxLen(100)]] = None
    body: Optional[Annotated[str, MinLen(3), MaxLen(700)]] = None


class PostResponse(PostCreate):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    user_id: Annotated[int, Ge(1)]
    created_at: datetime
    updated_at: datetime