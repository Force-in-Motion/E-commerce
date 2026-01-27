from datetime import datetime
from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen, Ge
from pydantic import BaseModel, ConfigDict,computed_field
from app.schemas.product import ProductResponse



class ProductInOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Annotated[int, Ge(1)]
    name: str
    description: str
    price: int
    quantity: Annotated[int, Ge(0)] = 0


class OrderCreate(BaseModel):
    promo_code: Optional[Annotated[int, Ge(5)]] = None
    comment: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None
    

class OrderUpdate(BaseModel):
    comment: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None


class OrderResponse(OrderCreate):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    user_id: Annotated[int, Ge(1)]
    products: list[ProductInOrder]
    comment: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None
    promo_code: Optional[Annotated[int, Ge(5)]] = None
    discount: Optional[Annotated[int, Ge(0)]] = None
    original_price: Annotated[int, Ge(0)] = 0
    total_price: Annotated[int, Ge(0)] = 0
    total_quantity: Annotated[int, Ge(0)] = 0
    created_at: datetime
    updated_at: datetime


