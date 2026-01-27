from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge, Le
from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(35)]

    address: Annotated[str, MinLen(8), MaxLen(255)]

    floor: Optional[Annotated[str, MinLen(3), MaxLen(12)]] = None

    age: Optional[Annotated[int, Ge(7), Le(120)]] = None
    
    bio: Optional[Annotated[str, MinLen(5), MaxLen(700)]] = None


class ProfileUpdate(BaseModel):
    name: Optional[Annotated[str, MinLen(3), MaxLen(35)]] = None
    address: Optional[Annotated[str, MinLen(8), MaxLen(255)]] = None
    floor: Optional[Annotated[str, MinLen(3), MaxLen(12)]] = None
    age: Optional[Annotated[int, Ge(7), Le(120)]] = None
    bio: Optional[Annotated[str, MinLen(5), MaxLen(700)]] = None


class ProfileResponse(ProfileCreate):
    model_config = ConfigDict(from_attributes=True)

    user_id: Annotated[int, Ge(1)]
    id: Annotated[int, Ge(1)]
    created_at: datetime
    updated_at: datetime
