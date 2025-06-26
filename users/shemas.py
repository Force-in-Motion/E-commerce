from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MaxLen, MinLen, Ge, Le, Gt


class User(BaseModel):
    id: Annotated[int, Ge(1)]
    name: Annotated[str, MinLen(3), MaxLen(30)]
    floor: Annotated[str, MinLen(3), MaxLen(12)]
    age: Annotated[int, Ge(12), Le(120)]
    email: EmailStr