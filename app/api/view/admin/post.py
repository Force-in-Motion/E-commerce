from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.post import PostDepends
from app.api.depends.security import admin_guard
from app.api.depends.inspect import Inspector
from app.schemas import PostCreate, PostUpdate, PostResponse


router = APIRouter(
    prefix="/admin/posts",
    tags=["Admin Posts"],
    dependencies=[Depends(admin_guard)],
)


@router.get(
    "/all",
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Список всех постов пользователей в виде Pydantic схем
    """
    return await PostDepends.get_all_posts(session=session)


@router.get(
    "/date",
    response_model=list[PostResponse],
    status_code=status.HTTP_201_CREATED,
)
async def get_posts_by_date(
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: список всех постов, созданных за указанный интервал времени в виде Pydantic схем
    """
    return await PostDepends.get_all_posts_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_post_by_id(
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> PostResponse:
    """
     Обрабатывает запрос с фронт энда на получение конкретного поста по его id
    :param post_id: id конкретного поста в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: пост пользователя в виде Pydantic схемы
    """
    return await PostDepends.get_post(
        post_id=post_id,
        session=session,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user_id(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение всех постов конкретного пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: список всех постов пользователя в виде Pydantic схем
    """
    return await PostDepends.get_all_posts(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/user/{user_id}",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_post(
    post_scheme: PostCreate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на добавление нового поста пользователя в БД
    :param post_scheme: PostCreate - объект, содержащий данные поста пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Добавленный в БД пост пользователя в виде Pydantic схемы
    """
    return await PostDepends.create_post(
        user_id=user_id,
        post_scheme=post_scheme,
        session=session,
    )


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_post(
    post_scheme: PostUpdate,
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на полное обновление конкретного поста пользователя в БД
    :param post_id: id конкретного поста в БД
    :param post_scheme:  PostUpdate - объект, содержащий новые данные поста пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Обновленный в БД пост пользователя в виде Pydantic схемы
    """
    return await PostDepends.update_post(
        post_id=post_id,
        post_scheme=post_scheme,
        session=session,
    )


@router.patch(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_post_partial(
    post_scheme: PostUpdate,
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на частичное обновление конкретного поста пользователя в БД
    :param post_id: id конкретного поста в БД
    :param post_scheme: PostUpdate - объект, содержащий новые данные поста пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Обновленный в БД пост пользователя в виде Pydantic схемы
    """
    return await PostDepends.update_post(
        post_id=post_id,
        post_scheme=post_scheme,
        session=session,
        partial=True,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_all_posts(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех постов пользователей из БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Пустой список
    """
    return await PostDepends.clear_posts(session=session)


@router.delete(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_id: id конкретного поста в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Удаленный из БД пост пользователя в виде Pydantic схемы
    """
    return await PostDepends.delete_post(
        post_id=post_id,
        session=session,
    )


@router.delete(
    "/user/{user_id}",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def delete_all_user_posts(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех постов пользователей из БД
    :param post_id: id конкретного поста в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Пустой список
    """
    return await PostDepends.delete_all_user_posts(
        user_id=user_id,
        session=session,
    )
