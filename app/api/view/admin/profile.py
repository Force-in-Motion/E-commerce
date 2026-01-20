from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.inspect import Inspector
from app.api.depends.security import admin_guard
from app.api.depends.profile import ProfileDepends
from app.schemas import ProfileResponse, ProfileCreate, ProfileUpdate




router = APIRouter(
    prefix="/admin/profiles",
    tags=["Admin Profiles"],
    dependencies=[Depends(admin_guard)],
)


@router.get(
    "/all",
    response_model=list[ProfileResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_profiles(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[ProfileResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех профилей пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Список всех профилей пользователей в виде Pydantic схем
    """
    return await ProfileDepends.get_all_profiles(session=session)


@router.get(
    "/date",
    response_model=list[ProfileResponse],
    status_code=status.HTTP_200_OK,
)
async def get_profiles_by_date(
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[ProfileResponse]:
    """
    Возвращает всех добавленных в БД профилей пользователей за указанный интервал времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :return: Список профилей пользователей за указанную дату в виде Pydantic схем
    """
    return await ProfileDepends.get_profiles_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_user_id(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по id пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Профиль конкретного пользователя в виде Pydantic схемы
    """
    return await ProfileDepends.get_profile(
        user_id=user_id,
        session=session,
    )


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_id(
    profile_id: Annotated[int, Path(..., description="Profile ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по его id
    :param profile_id: id конкретного профиля в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Профиль конкретного пользователя в виде Pydantic схемы
    """
    return await ProfileDepends.get_profile(
        profile_id=profile_id,
        session=session,
    )


@router.post(
    "/user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_profile(
    profile_scheme: ProfileCreate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :param profile_scheme: ProfileCreate - объект, содержащий данные профиля пользователя
    :param user_id: id конкретного пользователя в БД
    :return: Добавленный в БД профиль пользователя в виде Pydantic схемы
    """
    return await ProfileDepends.create_profile(
        user_id=user_id,
        profile_scheme=profile_scheme,
        session=session,
    )


@router.put(
    "/user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_profile(
    profile_scheme: ProfileUpdate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на полную замену данных профиля конкретного пользователя
    :param profile_scheme: ProfileUpdate - объект, содержащий новые данные профиля конкретного пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Обновленный в БД профиль пользователя в виде Pydantic схемы
    """
    return await ProfileDepends.update_profile(
        user_id=user_id,
        profile_scheme=profile_scheme,
        session=session,
    )


@router.patch(
    "/user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_profile(
    profile_scheme: ProfileUpdate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных профиля конкретного пользователя
    :param user_id: id конкретного пользователя в БД
    :param profile_scheme: ProfileUpdate - объект, содержащий новые данные профиля конкретного пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Обновленный в БД профиль пользователя в виде Pydantic схемы
    """
    return await ProfileDepends.update_profile(
        user_id=user_id,
        profile_scheme=profile_scheme,
        session=session,
        partial=True,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_profiles(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех профилей
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Пустой список
    """
    return await ProfileDepends.clear_profiles(session=session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного профиля
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Удаленный из БД профиль пользователя в виде Pydantic схемы
    """
    return await ProfileDepends.delete_profile(
        user_id=user_id,
        session=session,
    )
