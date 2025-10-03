from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.tools.custom_err import DatabaseError, NotFoundError

# Словарь соответствия CRUD ошибок → HTTPException
CRUD_TO_HTTP_MAP = {
    IntegrityError: lambda e, model: HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{model.__name__} already exists",
    ),
    NotFoundError: lambda e, model: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e),
    ),
    DatabaseError: lambda e, model: HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database error: {str(e)}",
    ),
    SQLAlchemyError: lambda e, model: HTTPException(  # fallback
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"SQLAlchemy error: {type(e).__name__} ({str(e)})",
    ),
}


# Создаём словарь (dict) под названием CRUD_TO_HTTP_MAP.
# Он будет хранить сопоставления ошибок из CRUD → HTTPException,
# которые нужно вернуть во внешнем слое (например, FastAPI).

# Ключ: IntegrityError — ошибка SQLAlchemy (например, нарушен уникальный индекс).
# Значение: lambda e, model: ... — анонимная функция, которая:
# Принимает e (само исключение) и model (класс модели, например User).
# Возвращает объект HTTPException с кодом 400 Bad Request.
# В detail пишет что-то вроде "User already exists", используя имя модели.

# Ключ: DatabaseError — общая ошибка работы с базой данных.
# Значение: функция, которая возвращает HTTPException с кодом 500 Internal Server Error.
# detail = текст ошибки из CRUD.
