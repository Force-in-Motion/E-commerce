from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from app.core import db_connector
from app.schemas import ProfileResponse
from app.api.depends.user.user import UserAuth
from app.api.depends.user.profile import ProfileCrud
from app.schemas.profile import ProfileCreate, ProfileUpdate


router = APIRouter(prefix="/user/profile")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.get(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_profile(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по id пользователя
    :param user_id: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Профиль конкретного пользователя
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileCrud.get_profile_by_user_id(
        user_model=user_model,
        session=session,
    )


@router.post(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile_in: ProfileCreate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param profile_in: ProfileInput - объект, содержащий данные профиля пользователя
    :param user_id: Profile_model - объект, содержащий данные профиля пользователя
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileCrud.create_user_profile(
        user_model=user_model,
        profile_in=profile_in,
        session=session,
    )


@router.put(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_profile(
    profile_in: ProfileUpdate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на полную замену данных профиля конкретного пользователя
    :param profile_in: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param user_id: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileCrud.update_user_profile(
        user_model=user_model,
        profile_in=profile_in,
        session=session,
        partial=True,
    )


@router.patch(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_profile(
    profile_in: ProfileUpdate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных профиля конкретного пользователя
    :param user_id: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_in: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileCrud.update_user_profile(
        user_model=user_model, profile_in=profile_in, session=session
    )


@router.delete(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param user_id: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await ProfileCrud.delete_user_profile(
        user_model=user_model,
        session=session,
    )
