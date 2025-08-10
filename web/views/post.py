from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database import db_connector
from service.database.crud.post import PostAdapter
from tools.dependencies import posts_by_user_id, post_by_id
from web.schemas import PostOutput

router = APIRouter()


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
