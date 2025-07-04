from pydantic import BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MaxLen, MinLen, Ge, Le




class ProductInput(BaseModel):

    name: Annotated[str, MinLen(3), MaxLen(30)]
    description: Annotated[str, MinLen(3), MaxLen(200)]
    price: Annotated[int, Ge(1), Le(1_000_000)]



class ProductOutput(ProductInput):
    model_config = ConfigDict(from_attributes=True)

    id: int