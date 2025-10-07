from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas import ProductResponse


class ProductAddOrUpdate(BaseModel):
    product_id: int
    quantity: int


class CartRequest(BaseModel):
    user_id: int


class ProductInCart(ProductResponse):
    quantity: int


class CartResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    products: list[ProductInCart]
    total_price: int

    model_config = ConfigDict(from_attributes=True)
