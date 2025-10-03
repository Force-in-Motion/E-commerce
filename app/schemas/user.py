from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge
from pydantic import BaseModel, EmailStr, ConfigDict


class UserRequest(BaseModel):
    """Класс описывающий объект, получаемый от пользователя,
    содержит аннотацию типов и ограничения ввода пользователем,
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    # Аннотация определена как Optional поскольку пользователь не обязательно должен передавать все поля в каждом запросе
    name: Optional[Annotated[str, MinLen(3), MaxLen(30)]] = None
    address: Optional[Annotated[str, MinLen(3), MaxLen(120)]] = None
    email: Optional[EmailStr] = None


class UserResponse(UserRequest):
    """Класс описывающий объект, возвращаемый пользователю, наследуется от UserInput
    для доступа ко всем полям UserInput, дополнительно содержит id
    поскольку в возвращаемом объекте он обязан быть,
    а так же объект класса ConfigDict и его настройку from_attributes=True,
    которая позволяет pydantic автоматически получать данные из объектов SQLAlchemy,
    полученных из БД и формировать из них объекты UserOutput для возврата клиенту"""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    created_at: datetime
