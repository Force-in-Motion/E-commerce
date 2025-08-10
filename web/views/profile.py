from datetime import datetime

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import Profile as ProfileModel
from service.database.crud import ProfileAdapter
from service.database import db_connector
from web.schemas import ProfileOutput, ProfileInput
from tools import profile_by_user_id, profile_by_id

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/",
    response_model=list[ProfileOutput],
    status_code=status.HTTP_200_OK,
)
async def get_profiles(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProfileOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех профилей пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех профилей пользователей
    """
    return await ProfileAdapter.get_profiles(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/{id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_id(
    profile: ProfileOutput = Depends(profile_by_id),
) -> ProfileOutput:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по его id
    :param profile: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Профиль конкретного пользователя
    """
    return profile


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/{user_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_user_id(profile: ProfileOutput = Depends(profile_by_user_id)):
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по id пользователя
    :param profile: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Профиль конкретного пользователя
    """
    return profile


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date",
    response_model=list[ProfileOutput],
    status_code=status.HTTP_200_OK,
)
async def get_profiles_by_date(
    date_start: datetime = Query(
        ..., description="Начальная дата (формат: YYYY-MM-DD HH:MM:SS)"
    ),
    date_end: datetime = Query(
        ..., description="Конечная дата (формат: YYYY-MM-DD HH:MM:SS)"
    ),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProfileOutput]:
    """
    Возвращает всех добавленных в БД пользователей за указанный интервал времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :param date_start: начало интервала времени
    :param date_end: окончание интервала времени
    :return: Список пользователей за указанную дату
    """
    return await ProfileAdapter.get_added_profiles_by_date(
        session, date_start, date_end
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def add_profile(
    profile_input: ProfileInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
    :return: dict
    """
    return await ProfileAdapter.add_profile(session, profile_input)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    profile_input: ProfileInput,
    profile_model: ProfileModel = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на полную замену данных профиля конкретного пользователя
    :param profile_input: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_model: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.update_profile(session, profile_input, profile_model)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def update_profile_partial(
    profile_input: ProfileInput,
    profile_model: ProfileModel = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных профиля конкретного пользователя
    :param profile_input: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_model: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.update_profile(
        session, profile_input, profile_model, partial=True
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/clear",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def clear_profiles(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.clear_profile_db(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def del_profile(
    profile_model: ProfileModel = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param profile_model: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.del_profile(session, profile_model)
