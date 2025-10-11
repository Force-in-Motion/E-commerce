from datetime import datetime
from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen, Ge
from pydantic import BaseModel, ConfigDict
from app.schemas import ProductResponse



class ProductInOrder(ProductResponse):
    """Класс описывающий объект, получаемый от пользователя,
    содержит аннотацию типов и ограничения ввода пользователем,
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    quantity: Annotated[int, Ge(0)]



class OrderRequest(BaseModel):
    """Класс описывающий объект, получаемый от пользователя,
    содержит аннотацию типов и ограничения ввода пользователем,
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    promo_code: Optional[Annotated[str, MinLen(10), MaxLen(10)]] = None
    comment: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None


class OrderResponse(OrderRequest):
    """Класс описывающий объект, возвращаемый пользователю, наследуется от UserInput
    для доступа ко всем полям UserInput, дополнительно содержит id
    поскольку в возвращаемом объекте он обязан быть,
    а так же объект класса ConfigDict и его настройку from_attributes=True,
    которая позволяет pydantic автоматически получать данные из объектов SQLAlchemy,
    полученных из БД и формировать из них объекты UserOutput для возврата клиенту"""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    user_id: Annotated[int, Ge(1)]
    total_price: Annotated[int, Ge(0)]
    comment: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None
    promo_code: Optional[Annotated[str, MinLen(10), MaxLen(10)]] = None
    created_at: datetime
    products: list[ProductInOrder]
