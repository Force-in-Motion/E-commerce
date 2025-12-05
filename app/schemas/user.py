from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen, Ge
from pydantic import BaseModel, EmailStr, ConfigDict

from app.tools.types import UserRole


class UserCreate(BaseModel):
    """Класс описывающий объект, получаемый от пользователя, для его создания
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    login: Annotated[EmailStr, MinLen(5), MaxLen(30)]
    password: Annotated[str, MinLen(7), MaxLen(120)]


class UserUpdate(BaseModel):
    """Класс описывающий объект, получаемый от пользователя, для изменения логина или пароля
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    # Аннотация определена как Optional поскольку пользователь не обязательно должен передавать все поля для изменения
    login: Optional[Annotated[EmailStr, MinLen(5), MaxLen(30)]]
    password: Optional[Annotated[str, MinLen(7), MaxLen(120)]]


class UserResponse(BaseModel):
    """Класс описывающий объект, возвращаемый администратору, наследуется от UserCreate
    для доступа ко всем полям UserCreate, дополнительно содержит id
    поскольку в возвращаемом объекте он обязан быть и остальные поля из таблицы
    а так же объект класса ConfigDict и его настройку from_attributes=True,
    которая позволяет pydantic автоматически получать данные из объектов SQLAlchemy,
    полученных из БД и формировать из них объекты UserResponse для возврата клиенту"""

    model_config = ConfigDict(from_attributes=True)

    id: Annotated[int, Ge(1)]
    role: UserRole
    is_active: bool
    created_at: datetime
