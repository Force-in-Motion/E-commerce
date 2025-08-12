from datetime import datetime

from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from service.database import db_connector
from service.database.crud import ProfileAdapter
from service.database.models import Profile as ProfileModel, User as UserModel
from tools import profile_by_user_id, profile_by_id, user_by_id, date_checker
from web.schemas import ProfileOutput, ProfileInput

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
async def get_profile_by_user_id(profile: ProfileOutput = Depends(profile_by_user_id)):
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по id пользователя
    :param profile: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Профиль конкретного пользователя
    """
    return profile


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-id/{id}",
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


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/by-user/{user_id}",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def add_profile(
    profile_input: ProfileInput,
    user_model: UserModel = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
    :param user_model: UserModel - объект, содержащий данные пользователя
    :return: dict
    """
    return await ProfileAdapter.add_profile(user_model, session, profile_input)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/by-user/{user_id}",
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
    return await ProfileAdapter.update_profile(
        session,
        profile_input,
        profile_model,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/by-user/{user_id}",
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
        session,
        profile_input,
        profile_model,
        partial=True,
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
    "/by-user/{user_id}",
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
