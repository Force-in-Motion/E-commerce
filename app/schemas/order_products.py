from typing import Annotated

from annotated_types import Ge
from pydantic import BaseModel, ConfigDict


class OrderProductOutput(BaseModel):
    """Класс описывающий объект, получаемый от пользователя,
    содержит аннотацию типов и ограничения ввода пользователем,
    не содержит id потому как id присваивается на уровне логики работы с БД
    и пользователь не должен иметь к нему доступ и определять его,
    этот класс не требует настройки ConfigDict, т.к. его задача это валидация данных,
    полученных от пользователя"""

    product_id: Annotated[int, Ge(1)]
    quantity: Annotated[int, Ge(1)]

    model_config = ConfigDict(from_attributes=True)
