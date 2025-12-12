from fastapi import HTTPException, status


class DatabaseError(Exception):
    """Ошибка работы с базой данных."""

    pass


class HTTPExeption(Exception):
    """Ошибка нахождения данных."""

    db_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error adding data to DB",
    )

    not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Data not found",
    )

    bad_request = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad request",
    )

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid login or password",
    )

    user_inactive = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )


    token_invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )