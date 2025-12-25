from datetime import datetime
from typing import Annotated
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, Query, Path

from app.core import db_connector
from app.api.depends.user import UserDepends
from app.api.depends.inspect import Inspector
from app.api.depends.security import admin_guard
from app.schemas import UserResponse, UserCreate, UserUpdateForAdmin


router = APIRouter(
    prefix="/admin/users",
    tags=['Users'],
    dependencies=[admin_guard],
)


@router.get(
    "/all",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[UserResponse]:
    """
    Обрабатывает запрос с fontend на получение списка всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех пользователей в виде Pydantic схем
    """
    return await UserDepends.get_all_users(session=session)


@router.get(
    "/date",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users_by_date(
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
) -> list[UserResponse]:
    """
    Обрабатывает запрос с fontend на получение всех добавленных в БД пользователей за указанный интервал времени
    :param dates:  кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список пользователей в виде Pydantic схем за указанную дату в виде Pydantic схем
    """
    return await UserDepends.get_users_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/name",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_login(
    login: Annotated[EmailStr, Query(..., description="User login")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на получение пользователя по его имени
    :param user_name: Имя пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Пользователя в виде Pydantic схемы
    """
    return await UserDepends.get_user_by_login(
        login=login,
        session=session,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на получение пользователя по его id
    :param user_id: конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Пользователя по его id в виде Pydantic схемы
    """
    return await UserDepends.get_user_by_id(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_scheme: UserCreate,
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на добавление пользователя в БД
    :param user_in: Pydantic Схема - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Добавленного в БД пользователя в виде Pydantic схемы
    """

    return await UserDepends.create_user(
        user_scheme=user_scheme,
        session=session,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_user(
    user_scheme: UserUpdateForAdmin,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_in: Pydantic Схема - объект, содержащий новые данные пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Полностью обновленного в БД пользователя в виде Pydantic схемы
    """
    return await UserDepends.update_user(
        user_id=user_id,
        user_scheme=user_scheme,
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
    user_scheme: UserUpdateForAdmin,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_in: Pydantic Схема - объект, содержащий новые данные пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Частично обновленного в БД пользователя в виде Pydantic схемы
    """
    return await UserDepends.update_user(
        user_id=user_id,
        user_scheme=user_scheme,
        session=session,
        partial=True,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_users(
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list:
    """
    Обрабатывает запрос с fontend на полную очистку таблицы пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Пустой список
    """
    return await UserDepends.clear_users(session=session)


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на удаление пользователя из БД
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Удаленного пользователя в виде Pydantic схемы
    """
    return await UserDepends.delete_user(
        user_id=user_id,
        session=session,
    )
