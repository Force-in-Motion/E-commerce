from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MaxLen, MinLen


class EmailScheme(BaseModel):

    user_email: EmailStr  # Кому письмо
    service_email: EmailStr  # От кого письмо
    theme_msg: Annotated[str, MinLen(3), MaxLen(200)]  # Тема письма
    body_msg: Annotated[str, MinLen(20), MaxLen(2000)]  # Текст письма
