from datetime import datetime

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from service.database import db_connector
from service.database.models import Post as Post_model
from service.database.crud import PostAdapter
from tools.dependencies import posts_by_user_id, post_by_id
from web.schemas import PostOutput, PostInput

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/", response_model=list[PostOutput], status_code=status.HTTP_200_OK)
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
@router.get("/date", response_model=PostOutput, status_code=status.HTTP_201_CREATED)
async def get_posts_by_date(
    date_start: datetime = Query(),
    date_end: datetime = Query(),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех постов пользователей за указанный интервал времени
    :param date_start: начало интервала времени
    :param date_end: окончание интервала времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех постов, созданных за указанный интервал времени
    """
    return await PostAdapter.get_posts_by_date(date_start, date_end, session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/{id}", response_model=PostOutput, status_code=status.HTTP_200_OK)
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
@router.get("/{user_id}", response_model=PostOutput, status_code=status.HTTP_200_OK)
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
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_post(
    post_input: PostInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на добавление нового поста пользователя в БД
    :param post_input: PostInput - объект, содержащий данные поста пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostAdapter.add_post(session, post_input)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_post(
    post_input: PostInput,
    post_model: Post_model = Depends(post_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
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
@router.patch("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_post(
    post_input: PostInput,
    post_model: Post_model = Depends(post_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
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
@router.delete("/clear", response_model=dict, status_code=status.HTTP_200_OK)
async def clear_posts(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление всех постов пользователей из БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await PostAdapter.clear_posts(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_post(
    post_model: Post_model = Depends(post_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного поста пользователя из БД
    :param post_model: Post_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return:
    """
    return await PostAdapter.del_post(session, post_model)
