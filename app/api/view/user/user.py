from typing import Annotated

from fastapi import APIRouter, status, Depends, Path
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.service import UserService
from app.models import User as User_model
from app.api.depends.user import UserDepends
from app.schemas import UserResponse, UserCreate, TokenResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    user_model: User_model = Depends(UserDepends.validate_user),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> TokenResponse:
    """

    :param param:
    :param param:
    :return:
    """
    return UserDepends.generate_tokens(
        user_model=user_model,
        session=session,
        refresh_status=True,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def give_access(
    user_model: User_model = Depends(UserDepends.get_current_user_by_refresh),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> TokenResponse:
    """

    :param param:
    :param param:
    :return:
    """
    return UserDepends.generate_tokens(
        user_model=user_model,
        session=session,
    )


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

    return await UserDepends.create_user(
        user_in=user_in,
        session=session,
    )


@router.put(
    "/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def full_update_user(
    user_in: UserCreate,
    user_model: User_model = Depends(UserDepends.get_current_user_by_access),
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
        model_id=user_model.id,
        scheme_in=user_in,
        session=session,
    )


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_user(
    user_in: UserCreate,
    user_model: User_model = Depends(UserDepends.get_current_user_by_refresh),
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
        model_id=user_model.id,
        scheme_in=user_in,
        session=session,
        partial=True,
    )


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_model: User_model = Depends(UserDepends.get_current_user_by_refresh),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на удаление пользователя из БД
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Удаленного пользователя в виде Pydantic схемы
    """
    return await UserService.delete_model(
        model_id=user_model.id,
        session=session,
    )
