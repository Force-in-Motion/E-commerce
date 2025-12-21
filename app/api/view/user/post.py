from typing import Annotated

from fastapi import APIRouter, status, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.user import PostCrud, UserAuth
from app.schemas import PostResponse, PostCreate, PostUpdate


router = APIRouter(prefix="/user/posts", tags=["User posts"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/login")


@router.get(
    "/all",
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_my_posts(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех постов пользователей
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.get_all_user_posts(
        user_id=user_model.id,
        session=session,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_post(
    token: Annotated[str, Depends(oauth2_scheme)],
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов конкретного пользователя
    :param user_id: список объектов PostOutput, который получается путем выполнения зависимости (метода posts_by_user_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов пользователя
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.get_user_post(
        post_id=post_id,
        user_id=user_model.id,
        session=session,
    )


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_my_post(
    post_in: PostCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на добавление нового поста пользователя в БД
    :param post_in: PostInput - объект, содержащий данные поста пользователя
    :param user_id: UserModel - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.create_user_post(
        user_id=user_model.id,
        post_in=post_in,
        session=session,
    )


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_my_post(
    post_in: PostUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на полное обновление конкретного поста пользователя в БД
    :param post_in:  PostInput - объект, содержащий данные поста пользователя
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.update_user_post(
        user_id=user_model.id,
        post_id=post_id,
        post_in=post_in,
        session=session,
    )


@router.patch(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_my_post(
    post_in: PostUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на частичное обновление конкретного поста пользователя в БД
    :param post_in:  PostInput - объект, содержащий данные поста пользователя
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.update_user_post(
        user_id=user_model.id,
        post_id=post_id,
        post_in=post_in,
        session=session,
        partial=True,
    )


@router.delete(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_my_post(
    token: Annotated[str, Depends(oauth2_scheme)],
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.delete_user_post(
        user_id=user_model.id,
        post_id=post_id,
        session=session,
    )


@router.delete(
    "/all",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def delete_all_my_post(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await PostCrud.delete_all_user_post(
        user_id=user_model.id,
        session=session,
    )
