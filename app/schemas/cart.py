from typing import Annotated
from datetime import datetime
from annotated_types import Ge
from pydantic import BaseModel, ConfigDict, computed_field



class ProductAddOrUpdate(BaseModel):
    product_id: Annotated[int, Ge(1)]
    quantity: Annotated[int, Ge(0)] = 0


class ProductInCart(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: Annotated[int, Ge(1)]
    name: str
    description: str
    price: int
    quantity: Annotated[int, Ge(0)] = 0



class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    user_id: Annotated[int, Ge(1)]
    products: list[ProductInCart] = []
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def total_price(self) -> int:
        """ Вычисляет общую стоимость всех продуктов в корзине """
        return sum(pic.price * pic.quantity for pic in self.products)

    @computed_field
    @property
    def total_quantity(self) -> int:
        """ Вычисляет общее количество всех продуктов в корзине """
        return sum(pic.quantity for pic in self.products)
