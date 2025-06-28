from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MaxLen, MinLen, Ge, Le, Gt


class Product(BaseModel):
    name: Annotated[str, ]
    description: Annotated[str]
    price: Annotated[int]