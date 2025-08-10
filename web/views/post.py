

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database import db_connector
from service.database.crud.post import PostAdapter
from web.schemas import PostOutput

router = APIRouter()


@router.get('/', response_model=list[PostOutput], status_code=status.HTTP_200_OK)
async def get_posts(
        session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[PostOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех профилей пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех профилей пользователей
    """
    return await PostAdapter.get_all_posts(session)