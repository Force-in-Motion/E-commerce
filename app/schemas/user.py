from datetime import datetime
from app.tools.types import UserRole
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen, Ge
from pydantic import BaseModel, EmailStr, ConfigDict, SecretStr


class UserCreate(BaseModel):
    login: Annotated[EmailStr, MinLen(5), MaxLen(30)]
    password: Annotated[SecretStr, MinLen(7), MaxLen(120)]


class UserUpdate(BaseModel):
    login: Optional[Annotated[EmailStr, MinLen(5), MaxLen(30)]]
    password: Optional[Annotated[SecretStr, MinLen(7), MaxLen(120)]]


class UserUpdateForAdmin(BaseModel):
    login: Optional[Annotated[EmailStr, MinLen(5), MaxLen(30)]]
    password: Optional[Annotated[SecretStr, MinLen(7), MaxLen(120)]]
    role: Optional[UserRole]
    is_active: Optional[bool]


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
