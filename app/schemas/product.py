from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge, Le
from pydantic import BaseModel, ConfigDict


class ProductRequest(BaseModel):
    """Класс описывающий объект, получаемый от пользователя,
    содержит аннотацию типов и ограничения ввода пользователем,
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    # Аннотация определена как Optional поскольку пользователь не обязательно должен передавать все поля в каждом запросе
    name: Optional[Annotated[str, MinLen(3), MaxLen(30)]] = None
    description: Optional[Annotated[str, MinLen(3), MaxLen(200)]] = None
    price: Optional[Annotated[int, Ge(1), Le(1_000_000)]] = None


class ProductResponse(ProductRequest):
    """Класс описывающий объект, возвращаемый пользователю, наследуется от ProductInput
    для доступа ко всем полям ProductInput, дополнительно содержит id
    поскольку в возвращаемом объекте он обязан быть,
    а так же объект класса ConfigDict и его настройку from_attributes=True,
    которая позволяет pydantic автоматически получать данные из объектов SQLAlchemy,
    полученных из БД и формировать из них объекты ProductOutput для возврата клиенту"""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    created_at: datetime
    updated_at: datetime
