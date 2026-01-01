from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge, Le
from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    """Класс описывающий объект, получаемый от пользователя, для создания
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    # Аннотация определена как Optional поскольку пользователь не обязательно должен передавать все поля в каждом запросе
    name: Annotated[str, MinLen(3), MaxLen(35)]
    address: Annotated[str, MinLen(8), MaxLen(255)]
    floor: Optional[Annotated[str, MinLen(3), MaxLen(12)]] = None
    age: Optional[Annotated[int, Ge(7), Le(120)]] = None
    bio: Optional[Annotated[str, MinLen(5), MaxLen(700)]] = None


class ProfileUpdate(BaseModel):
    """Класс описывающий объект, получаемый от пользователя, для обновления данных
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    # Аннотация определена как Optional поскольку пользователь не обязательно должен передавать все поля в каждом запросе
    name: Optional[Annotated[str, MinLen(3), MaxLen(35)]] = None
    address: Optional[Annotated[str, MinLen(8), MaxLen(255)]] = None
    floor: Optional[Annotated[str, MinLen(3), MaxLen(12)]] = None
    age: Optional[Annotated[int, Ge(7), Le(120)]] = None
    bio: Optional[Annotated[str, MinLen(5), MaxLen(700)]] = None


class ProfileResponse(ProfileCreate):
    """Класс описывающий объект, возвращаемый пользователю, наследуется от ProfileCreate
    для доступа ко всем полям ProfileCreate, дополнительно содержит id
    поскольку в возвращаемом объекте он обязан быть и другие данные модели,
    а так же объект класса ConfigDict и его настройку from_attributes=True,
    которая позволяет pydantic автоматически получать данные из объектов SQLAlchemy,
    полученных из БД и формировать из них объекты ProfileResponse для возврата клиенту"""
    model_config = ConfigDict(from_attributes=True)

    user_id: Annotated[int, Ge(1)]
    id: Annotated[int, Ge(1)]
    created_at: datetime
    updated_at: datetime
