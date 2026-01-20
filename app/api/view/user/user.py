from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.core import db_connector
from app.schemas import UserUpdate
from app.api.depends.security import oauth2_scheme
from app.api.depends.user import UserAuth, UserDepends
from app.schemas import UserResponse, UserCreate, TokenResponse


router = APIRouter(
    prefix="/user/auth",
    tags=["Me"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """
    Обрабатывает запрос с fontend на авторизацию пользователя, выдает токены
    :param form_data:  объект OAuth2PasswordRequestForm, содержит данные пользователя, считанные из формы
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: токены в виде Pydantic схемы
    """
    user_model = await UserAuth.validate_user(
        session=session,
        login=form_data.username,
        password=form_data.password,
    )

    return await UserAuth.generate_tokens(
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
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> TokenResponse:
    """
    Обрабатывает запрос с fontend на выдачу access токена по refresh токену
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: access токен в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_refresh(
        token=token,
        session=session,
    )

    return await UserAuth.generate_tokens(
        user_model=user_model,
        session=session,
    )


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_me(
    user_scheme: UserCreate,
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на добавление пользователя в БД
    :param user_scheme: Pydantic Схема - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Добавленного в БД пользователя в виде Pydantic схемы
    """
    return await UserDepends.create_user(
        user_scheme=user_scheme,
        session=session,
    )


@router.put(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_me(
    user_scheme: UserUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_scheme: Pydantic Схема - объект, содержащий новые данные пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Полностью обновленного в БД пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await UserDepends.update_user(
        user_id=user_model.id,
        user_scheme=user_scheme,
        session=session,
    )


@router.patch(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_me(
    user_scheme: UserUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_scheme: Pydantic Схема - объект, содержащий новые данные пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Частично обновленного в БД пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await UserDepends.update_user(
        user_id=user_model.id,
        user_scheme=user_scheme,
        session=session,
        partial=True,
    )


@router.delete(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на удаление пользователя из БД
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Удаленного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await UserDepends.delete_user(
        user_id=user_model.id,
        session=session,
    )
