from pydantic import BaseModel, EmailStr
from typing import Annotated
from annotated_types import MaxLen, MinLen


class EmailScheme(BaseModel):

    from_email: EmailStr  # От кого письмо
    to_email: EmailStr  # Кому письмо
    theme_msg: Annotated[str, MinLen(3), MaxLen(200)]  # Тема письма
    body_msg: Annotated[str, MinLen(20), MaxLen(2000)]  # Текст письма
