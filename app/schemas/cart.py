from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas import ProductResponse


class CartRequest(BaseModel):
    user_id: int
    product_id: str
    quantity: int


class ProductInCart(ProductResponse):
    quantity: int


class CartResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    product: list[ProductInCart]
    total_price: int

    model_config = ConfigDict(from_attributes=True)
