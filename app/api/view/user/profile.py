from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.service.profile import ProfileFacade
from app.schemas import ProfileResponse, ProfileRequest
from app.tools import Inspector

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/me",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по id пользователя
    :param user_id: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Профиль конкретного пользователя
    """
    return await ProfileFacade.get_model_by_user_id(
        user_id=user_id,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов ProfileOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/by-id/{profile_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profile_by_id(
    profile_id: int,
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на получение профиля пользователя по его id
    :param profile_id: объект ProfileOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Профиль конкретного пользователя
    """
    return await ProfileFacade.get_model_by_id(
        model_id=profile_id,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_profile(
    user_id: int,
    profile_in: ProfileRequest,
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на создание профиля пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param profile_in: ProfileInput - объект, содержащий данные профиля пользователя
    :param user_id: Profile_model - объект, содержащий данные профиля пользователя
    :return: dict
    """
    return await ProfileFacade.register_model_by_user_id(
        user_id=user_id,
        scheme_in=profile_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_profile(
    user_id: int,
    profile_in: ProfileRequest,
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на полную замену данных профиля конкретного пользователя
    :param profile_in: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param user_id: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileFacade.update_model_by_user_id(
        user_id=user_id,
        scheme_in=profile_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_profile(
    user_id: int,
    profile_in: ProfileRequest,
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных профиля конкретного пользователя
    :param user_id: ProfileInput - объект, содержащий новые данные профиля конкретного пользователя
    :param profile_in: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileFacade.update_model_by_user_id(
        user_id=user_id,
        scheme_in=profile_in,
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
async def clear_profiles(
    session: AsyncSession = Depends(db_connector.get_session),
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileFacade.clear_table(session=session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/by-user/{user_id}",
    response_model=ProfileResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_profile(
    user_id: int,
    session: AsyncSession = Depends(db_connector.get_session),
) -> ProfileResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param user_id: ProfileModel - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProfileFacade.delete_model_by_user_id(
        user_id=user_id,
        session=session,
    )
