from pydantic import BaseModel, EmailStr



class Message(BaseModel):

    from_email: EmailStr                        # От кого письмо
    to_email: EmailStr                          # Кому письмо
    theme_msg: str                              # Тема письма
    body_msg: str                               # Текст письма