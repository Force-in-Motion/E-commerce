from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.service import UserFacade
from app.schemas import UserResponse, UserRequest
from app.tools import Inspector

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/all",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[UserResponse]:
    """
    Обрабатывает запрос с fontend на получение списка всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех пользователей в виде Pydantic схем
    """
    return await UserFacade.get_all_models(session=session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users_by_date(
    dates: tuple[datetime, datetime] = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[UserResponse]:
    """
    Обрабатывает запрос с fontend на получение всех добавленных в БД пользователей за указанный интервал времени
    :param dates:  кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список пользователей в виде Pydantic схем за указанную дату в виде Pydantic схем
    """
    return await UserFacade.get_models_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/name",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_name(
    user_name: Annotated[str, Query(..., description="User name")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на получение пользователя по его имени
    :param user_name: Имя пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Пользователя в виде Pydantic схемы
    """
    return await UserFacade.get_user_by_name(
        name=user_name,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на получение пользователя по его id
    :param user_id: конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Пользователя по его id в виде Pydantic схемы
    """
    return await UserFacade.get_model_by_id(
        model_id=user_id,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserRequest,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на добавление пользователя в БД
    :param user_in: Pydantic Схема - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Добавленного в БД пользователя в виде Pydantic схемы
    """

    return await UserFacade.register_model(
        scheme_in=user_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def full_update_user(
    user_id: Annotated[int, Path(..., description="User id")],
    user_in: UserRequest,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_in: Pydantic Схема - объект, содержащий новые данные пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Полностью обновленного в БД пользователя в виде Pydantic схемы
    """
    return await UserFacade.update_model(
        model_id=user_id,
        scheme_in=user_in,
        session=session,
    )


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_user(
    user_id: Annotated[int, Path(..., description="User id")],
    user_in: UserRequest,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на полную замену данных пользователя по его id
    :param user_in: Pydantic Схема - объект, содержащий новые данные пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Частично обновленного в БД пользователя в виде Pydantic схемы
    """
    return await UserFacade.update_model(
        model_id=user_id,
        scheme_in=user_in,
        session=session,
        partial=True,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_users(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """
    Обрабатывает запрос с fontend на полную очистку таблицы пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Пустой список
    """
    return await UserFacade.clear_table(session)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserResponse:
    """
    Обрабатывает запрос с fontend на удаление пользователя из БД
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Удаленного пользователя в виде Pydantic схемы
    """
    return await UserFacade.delete_model(
        model_id=user_id,
        session=session,
    )
