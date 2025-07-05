from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional
from annotated_types import MaxLen, MinLen, Ge, Le




class ProductInput(BaseModel):

    name: Optional[Annotated[str, MinLen(3), MaxLen(30)]] = None
    description: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None
    price: Optional[Annotated[int, Ge(1), Le(1_000_000)]] = None



class ProductOutput(ProductInput):
    model_config = ConfigDict(from_attributes=True)

    id: int