from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.annotation import Annotated
from annotated_types import MaxLen, MinLen, Ge
from app.schemas import ProductResponse


class ProductAddOrUpdate(BaseModel):
    product_id: Annotated[int, Ge(1)]
    quantity: Annotated[int, Ge(0)] = 0


class ProductInCart(ProductResponse):
    quantity: Annotated[int, Ge(0)] = 0


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    user_id: Annotated[int, Ge(1)]
    created_at: datetime
    updated_at: datetime
    products: list[ProductInCart]
    total_price: Annotated[int, Ge(0)] = 0
    total_quantity: Annotated[int, Ge(0)] = 0
