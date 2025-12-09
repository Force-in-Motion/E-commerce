from typing import Annotated

from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.service import UserService
from app.schemas import UserResponse, UserCreate

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае UserResponse
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на добавление пользователя в БД
    :param user_in: Pydantic Схема - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Добавленного в БД пользователя в виде Pydantic схемы
    """

    return await UserService.register_model(
        scheme_in=user_in,
        session=session,
    )


@router.post("/login")
@router.post("/refresh")


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def full_update_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_in: Pydantic Схема - объект, содержащий новые данные пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Полностью обновленного в БД пользователя в виде Pydantic схемы
    """
    return await UserService.update_model(
        model_id=user_id,
        scheme_in=user_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_user(
    user_id: Annotated[int, Path(..., description="User id")],
    user_in: UserCreate,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_in: Pydantic Схема - объект, содержащий новые данные пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Частично обновленного в БД пользователя в виде Pydantic схемы
    """
    return await UserService.update_model(
        model_id=user_id,
        scheme_in=user_in,
        session=session,
        partial=True,
    )


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на удаление пользователя из БД
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Удаленного пользователя в виде Pydantic схемы
    """
    return await UserService.delete_model(
        model_id=user_id,
        session=session,
    )
