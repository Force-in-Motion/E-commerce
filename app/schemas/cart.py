from typing import Annotated
from datetime import datetime
from annotated_types import Ge
from pydantic import BaseModel, ConfigDict
from app.schemas.product import ProductResponse


class ProductAddOrUpdate(BaseModel):
    product_id: Annotated[int, Ge(1)]
    quantity: Annotated[int, Ge(0)] = 0


class ProductInCart(ProductResponse):
    quantity: Annotated[int, Ge(0)] = 0


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    user_id: Annotated[int, Ge(1)]
    products: list[ProductInCart]
    total_price: Annotated[int, Ge(0)] = 0
    total_quantity: Annotated[int, Ge(0)] = 0
    created_at: datetime
    updated_at: datetime
