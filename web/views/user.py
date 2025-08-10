from datetime import datetime

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.database import db_connector
from service.database.crud import UserAdapter
from service.database.models import User as User_model
from tools import user_by_id
from web.schemas import UserOutput, UserInput

router = APIRouter()


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/", response_model=list[UserOutput], status_code=status.HTTP_200_OK)
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
@router.get("/id{id}", response_model=UserOutput, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user: UserOutput = Depends(user_by_id),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на получение пользователя по его id
    :param user: объект UserOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: Конкретного пользователя по его id
    """
    return user


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get(
    "/date{date}", response_model=list[UserOutput], status_code=status.HTTP_200_OK
)
async def get_users_by_date(
    date: datetime,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[UserOutput]:
    """
    Возвращает всех добавленных в БД пользователей за указанный интервал времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :param date: конкретная дата, по которой нужно распарсить всех пользователей
    :return: Список пользователей за указанную дату
    """
    return await UserAdapter.get_added_users_by_date(session, date)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserInput,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на добавление пользователя в БД
    :param user: UserInput - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.add_user(session, user)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_user(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
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
@router.patch("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_user_partial(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param user_input: UserInput - объект, содержащий новые данные конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.update_user(user_input, user_model, session, partial=True)


@router.delete("/clear", response_model=dict, status_code=status.HTTP_200_OK)
async def clear_users(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.clear_user_db(session)


# response_model определяет модель ответа пользователю, в данном случае словарь
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def del_user(
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, str]:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await UserAdapter.del_user(user_model, session)
