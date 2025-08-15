from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.crud import ProfileAdapter
from app.models import Profile as Profile_model, User as UserModel
from app.schemas import ProfileOutput, ProfileInput
from app.tools import (
    profile_by_user_id,
    profile_by_id,
    user_by_id,
    date_checker,
    profile_checker,
)

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


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date",
    response_model=list[ProfileOutput],
    status_code=status.HTTP_200_OK,
)
async def get_profiles_by_date(
    dates: tuple[datetime, datetime] = Depends(date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[ProfileOutput]:
    """
    Возвращает всех добавленных в БД пользователей за указанный интервал времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param dates: окончание интервала времени
    :return: Список пользователей за указанную дату
    """
    return await ProfileAdapter.get_added_profiles_by_date(session, dates)


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-user/{user_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_user_id(
    profile_output: ProfileOutput = Depends(profile_by_user_id),
):
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по id пользователя
    :param profile_output: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Профиль конкретного пользователя
    """
    return profile_output


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-id/{profile_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_id(
    profile_output: ProfileOutput = Depends(profile_by_id),
) -> ProfileOutput:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по его id
    :param profile_output: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Профиль конкретного пользователя
    """
    return profile_output


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/by-user/{user_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_201_CREATED,
)
async def add_profile(
    profile_input: ProfileInput,
    user_id: int = Depends(profile_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProfileOutput:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
    :param user_id: Profile_model - объект, содержащий данные профиля пользователя
    :return: dict
    """
    return await ProfileAdapter.add_profile(
        profile_input,
        user_id,
        session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/by-user/{user_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def update_profile(
    profile_input: ProfileInput,
    profile_model: Profile_model = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProfileOutput:
    """
    Обрабатывает запрос с фронт энда на полную замену данных профиля конкретного пользователя
    :param profile_input: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_model: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.update_profile(
        profile_input,
        profile_model,
        session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/by-user/{user_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def update_profile_partial(
    profile_input: ProfileInput,
    profile_model: Profile_model = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProfileOutput:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных профиля конкретного пользователя
    :param profile_input: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_model: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.update_profile(
        profile_input,
        profile_model,
        session,
        partial=True,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_profiles(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.clear_profile_db(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/by-user/{user_id}",
    response_model=ProfileOutput,
    status_code=status.HTTP_200_OK,
)
async def del_profile(
    profile_model: Profile_model = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> ProfileOutput:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param profile_model: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileAdapter.del_profile(profile_model, session)
