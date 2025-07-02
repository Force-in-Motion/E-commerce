from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MaxLen, MinLen, Ge, Le, Gt


class Product(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(30)]
    description: Annotated[str, MinLen(3), MaxLen(200)]
    price: Annotated[int, Ge(1), Le(1_000_000)]