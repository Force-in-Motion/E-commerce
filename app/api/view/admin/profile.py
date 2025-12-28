from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.security import admin_guard
from app.api.depends.profile import ProfileDepends
from app.api.depends.inspect import Inspector
from app.schemas import ProfileResponse, ProfileCreate, ProfileUpdate
from app.schemas.profile import ProfileCreate



router = APIRouter(
    prefix="/admin/profiles",
    tags=["Profiles"],
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
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех профилей пользователей
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
    Возвращает всех добавленных в БД пользователей за указанный интервал времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param dates: окончание интервала времени
    :return: Список пользователей за указанную дату
    """
    return await ProfileDepends.get_profiles_by_date(
        dates=dates,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
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
    :param user_id: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Профиль конкретного пользователя
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
    :param profile_id: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Профиль конкретного пользователя
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
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param profile_in: ProfileInput - объект, содержащий данные профиля пользователя
    :param user_id: Profile_model - объект, содержащий данные профиля пользователя
    :return: dict
    """
    return await ProfileDepends.create_user_profile(
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
    :param profile_in: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param user_id: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileDepends.update_user_profile(
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
    :param user_id: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_in: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileDepends.update_user_profile(
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
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
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
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param user_id: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileDepends.delete_user_profile(
        user_id=user_id,
        session=session,
    )
