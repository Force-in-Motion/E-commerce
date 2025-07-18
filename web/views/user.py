from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from web.schemas.user import UserOutput, UserInput
from service.database.crud import UserAdapter as ua
from service.database.models import User as User_model
from service.database import db_connector
from tools import user_by_id


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
    :return: list[ProductOutput]
    """
    return await ua.get_users(session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.get("/{id}", response_model=UserOutput, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user: UserOutput = Depends(user_by_id),
) -> UserOutput:
    """
    Обрабатывает запрос с фронт энда на получение пользователя по его id
    :param user: объект UserOutput, который получается путем выполнения зависимости (метода product_by_id)
    :return: UserOutput
    """
    return user


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_user(
    user: UserInput, session: AsyncSession = Depends(db_connector.session_dependency)
) -> dict:
    """
    Обрабатывает запрос с фронт энда на добавление пользователя в БД
    :param user: UserInput - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ua.add_user(session, user)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.put("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_user(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на полную замену данных продукта по его id
    :param user_input: UserInput - объект, содержащий новые данные конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ua.update_user(user_input, user_model, session)


# response_model определяет модель ответа пользователю, в данном случае список объектов UserOutput,
# status_code определяет какой статус вернется пользователю в случае успешного выполнения запроса с фронт энда
@router.patch("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_product(
    user_input: UserInput,
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param user_input: UserInput - объект, содержащий новые данные конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ua.update_user(user_input, user_model, session, partial=True)


@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def del_user_by_id(
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного пользователя
    :param user_model: User_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ua.del_user(user_model, session)
