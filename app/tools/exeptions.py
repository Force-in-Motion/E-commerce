from fastapi import HTTPException, status


class DatabaseError(Exception):
    """Ошибка работы с базой данных."""

    pass


class HTTPErrors(Exception):
    """Ошибка нахождения данных."""

    db_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Database operation error",
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

    cart_empty = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cart empty or not found",
    )

    not_admin = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User not admin",
    )

    err_update_model = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error update model in DB",
    )

    err_create_model = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error create model in DB",
    )

    err_delete_model = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error delete model in DB",
    )

    clear_table = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error cleared table",
    )
