from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.post import PostDepends
from app.api.depends.security import admin_guard
from app.schemas import PostCreate, PostUpdate, PostResponse
from app.tools import Inspector

router = APIRouter(
    prefix="/admin/posts",
    tags=["Posts"],
    dependencies=[admin_guard],
)


@router.get(
    "/all",
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех постов пользователей
    """
    return await PostDepends.get_all_posts(session=session)


@router.get(
    "/date",
    response_model=list[PostResponse],
    status_code=status.HTTP_201_CREATED,
)
async def get_posts_by_date(
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов, созданных за указанный интервал времени
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
     Обрабатывает запрос с фронт энда на получение конкретного поста по его id
    :param post_id: объект PostOutput, который получается путем выполнения зависимости (метода post_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: конкретный пост по его id
    """
    return await PostDepends.get_post(
        post_id=post_id,
        session=session,
    )


@router.get(
    "/{post_id}user/{user_id}",
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user_id(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[PostResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов конкретного пользователя
    :param user_id: список объектов PostOutput, который получается путем выполнения зависимости (метода posts_by_user_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов пользователя
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на добавление нового поста пользователя в БД
    :param post_in: PostInput - объект, содержащий данные поста пользователя
    :param user_id: UserModel - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostDepends.create_post(
        user_id=user_id,
        post_scheme=post_scheme,
        session=session,
    )


@router.put(
    "/{post_id}/user/{user_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_post(
    post_scheme: PostUpdate,
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
    return await PostDepends.update_post(
        post_id=post_id,
        post_scheme=post_scheme,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/{post_id}/user/{user_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_post_partial(
    post_scheme: PostUpdate,
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
    return await PostDepends.update_user_post(
        post_id=post_id,
        post_scheme=post_scheme,
        session=session,
        partial=True,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_all_posts(
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех постов пользователей из БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostDepends.clear_post(session=session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/{post_id}/user/{user_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_id: Annotated[int, Path(..., description="Post ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> PostResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    return await PostDepends.delete_post(
        post_id=post_id,
        session=session,
    )


@router.delete(
    "/{post_id}/user/{user_id}",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def delete_all_user_posts(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_id: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    return await PostDepends.delete_all_post(
        user_id=user_id,
        session=session,
    )
