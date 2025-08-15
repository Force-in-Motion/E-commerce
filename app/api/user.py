from datetime import datetime

from fastapi import APIRouter, status, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.crud import UserAdapter
from app.models import User as User_model
from app.schemas import UserOutput, UserInput
from app.tools import user_by_id, date_checker

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/",
    response_model=list[UserOutput],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[UserOutput]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех пользователей в БД
    """
    return await UserAdapter.get_all_users(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date",
    response_model=list[UserOutput],
    status_code=status.HTTP_200_OK,
)
async def get_users_by_date(
    dates: tuple[datetime, datetime] = Depends(date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[UserOutput]:
    """
    Возвращает всех добавленных в БД пользователей за указанный интервал времени
    :param dates:  кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список пользователей за указанную дату
    """
    return await UserAdapter.get_added_users_by_date(dates, session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/{user_id}",
    response_model=UserOutput,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_output: UserOutput = Depends(user_by_id),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на получение пользователя по его id
    :param user_output: объект UserOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Конкретного пользователя по его id
    """
    return user_output


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post(
    "/",
    response_model=UserOutput,
    status_code=status.HTTP_201_CREATED,
)
async def add_user(
    user_input: UserInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на добавление пользователя в БД
    :param user_input: UserInput - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.add_user(user_input, session)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put(
    "/{user_id}",
    response_model=UserOutput,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на полную замену данных продукта по его id
    :param user_input: UserInput - объект, содержащий новые данные конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.update_user(user_input, user_model, session)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch(
    "/{user_id}",
    response_model=UserOutput,
    status_code=status.HTTP_200_OK,
)
async def update_user_partial(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param user_input: UserInput - объект, содержащий новые данные конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.update_user(user_input, user_model, session, partial=True)


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_users(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.clear_users(session)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete(
    "/{user_id}",
    response_model=UserOutput,
    status_code=status.HTTP_200_OK,
)
async def del_user(
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.del_user(user_model, session)
