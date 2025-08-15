from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.crud import PostAdapter
from app.models import Post as Post_model, User as User_model
from app.schemas import PostOutput, PostInput
from app.tools import date_checker
from app.tools.dependencies import posts_by_user_id, post_by_id, user_by_id

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/",
    response_model=list[PostOutput],
    status_code=status.HTTP_200_OK,
)
async def get_posts(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех постов пользователей
    """
    return await PostAdapter.get_all_posts(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date",
    response_model=list[PostOutput],
    status_code=status.HTTP_201_CREATED,
)
async def get_posts_by_date(
    dates: tuple[datetime, datetime] = Depends(date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов, созданных за указанный интервал времени
    """
    return await PostAdapter.get_added_posts_by_date(dates, session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def get_post_by_id(
    post: PostOutput = Depends(post_by_id),
) -> PostOutput:
    """
     Обрабатывает запрос с фронт энда на получение конкретного поста по его id
    :param post: объект PostOutput, который получается путем выполнения зависимости (метода post_by_id)
    :return: конкретный пост по его id
    """
    return post


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-user/{user_id}",
    response_model=list[PostOutput],
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user_id(
    posts: list[PostOutput] = Depends(posts_by_user_id),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов конкретного пользователя
    :param posts: список объектов PostOutput, который получается путем выполнения зависимости (метода posts_by_user_id)
    :return: список всех постов пользователя
    """
    return posts


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/by-user/{user_id}",
    response_model=PostOutput,
    status_code=status.HTTP_201_CREATED,
)
async def add_post(
    post_input: PostInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на добавление нового поста пользователя в БД
    :param post_input: PostInput - объект, содержащий данные поста пользователя
    :param user_model: UserModel - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostAdapter.add_post(session, post_input, user_model)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def full_update_post(
    post_input: PostInput,
    post_model: Post_model = Depends(post_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на полное обновление конкретного поста пользователя в БД
    :param post_input:  PostInput - объект, содержащий данные поста пользователя
    :param post_model: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostAdapter.update_post(session, post_input, post_model)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def partial_update_post(
    post_input: PostInput,
    post_model: Post_model = Depends(post_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на частичное обновление конкретного поста пользователя в БД
    :param post_input:  PostInput - объект, содержащий данные поста пользователя
    :param post_model: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostAdapter.update_post(session, post_input, post_model, partial=True)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_posts(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех постов пользователей из БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostAdapter.clear_posts(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/by-id/{post_id}",
    response_model=PostOutput,
    status_code=status.HTTP_200_OK,
)
async def delete_post(
    post_model: Post_model = Depends(post_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> PostOutput:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_model: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    return await PostAdapter.del_post(session, post_model)
