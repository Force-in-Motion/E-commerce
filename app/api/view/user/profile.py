from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.schemas import ProfileResponse
from app.api.depends.user import UserAuth
from app.api.depends.security import oauth2_scheme
from app.api.depends.profile import ProfileDepends
from app.schemas.profile import ProfileCreate, ProfileUpdate


router = APIRouter(
    prefix="/user/profile",
    tags=["My profile"],
)


@router.get(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_profile(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по его id 
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return:  Профиль конкретного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileDepends.get_profile(
        user_id=user_model.id,
        session=session,
    )


@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_profile(
    profile_scheme: ProfileCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param profile_scheme: ProfileCreate - схема, содержащая данные профиля пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Созданный профиль конкретного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileDepends.create_profile(
        user_id=user_model.id,
        profile_scheme=profile_scheme,
        session=session,
    )


@router.put(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_my_profile(
    profile_scheme: ProfileUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на полную замену данных профиля конкретного пользователя
    :param profile_scheme: ProfileUpdate - схема, содержащая данные профиля пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Измененный профиль конкретного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileDepends.update_profile(
        user_id=user_model.id,
        profile_scheme=profile_scheme,
        session=session,
    )


@router.patch(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_my_profile(
    profile_scheme: ProfileUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных профиля конкретного пользователя
    :param profile_scheme: ProfileUpdate - схема, содержащая данные профиля пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Измененный профиль конкретного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileDepends.update_profile(
        user_id=user_model.id,
        profile_scheme=profile_scheme,
        session=session,
        partial=True,
    )


@router.delete(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_my_profile(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Удаленный профиль конкретного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileDepends.delete_profile(
        user_id=user_model.id,
        session=session,
    )
