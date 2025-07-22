from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database.crud import ProfileAdapter
from service.database import db_connector
from web.schemas import ProfileOutput, ProfileInput
from tools import profile_by_user_id

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/", response_model=list[ProfileOutput], status_code=status.HTTP_200_OK)
async def get_profiles(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProfileOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех профилей пользователей
    """
    return await ProfileAdapter.get_profiles(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/{id}", response_model=ProfileOutput, status_code=status.HTTP_200_OK)
async def get_profile_by_user_id(profile: ProfileOutput = Depends(profile_by_user_id)):
    """
    Обрабатывает запрос с фронт энда на получение пользователя по его id
    :param profile: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Профиль конкретного пользователя
    """
    return profile
