from datetime import datetime
from fastapi import Depends
from fastapi import APIRouter, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.api.depends.order import OrderDepends
from app.core import db_connector
from app.api.depends.security import admin_guard
from app.api.depends.inspect import Inspector
from app.schemas import OrderResponse, OrderCreate, OrderUpdate

router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin Orders"],
    dependencies=[Depends(admin_guard)],
)


@router.get(
    "/all",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_orders(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[OrderResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех заказов пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех заказов пользователей в виде Pydantic схем
    """
    return await OrderDepends.get_all_oreders(session=session)


@router.get(
    "/date",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_orders_by_date(
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[OrderResponse]:
    """
    Возвращает все добавленные в БД заказы пользователей за указанный интервал времени
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :return: Список пользователей за указанную дату в виде Pydantic схем
    """
    return await OrderDepends.get_all_oreders_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_user_orders(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[OrderResponse]:
    """
    Обрабатывает запрос с фронт энда на получение заказа пользователя по id пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: заказ конкретного пользователя в виде Pydantic схемы
    """
    return await OrderDepends.get_all_oreders(
        user_id=user_id,
        session=session,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_by_id(
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на получение заказа пользователя по его id
    :param order_id: id конкретного заказа в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Профиль конкретного пользователя в виде Pydantic схемы
    """
    return await OrderDepends.get_oreder(
        order_id=order_id,
        session=session,
    )


@router.post(
    "/user/{user_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    order_scheme: OrderCreate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на создание заказа пользователя в БД
    :param user_id: id конкретного пользователя в БД
    :param order_scheme: OrderCreate - объект, содержащий данные заказа пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Добавленный в БД заказ пользователя в виде Pydantic схемы
    """
    return await OrderDepends.create_oreder(
        user_id=user_id,
        session=session,
        order_scheme=order_scheme,
    )


@router.patch(
    "/user/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order_partial(
    order_scheme: OrderUpdate,
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных заказа конкретного пользователя
    :param order_id: id конкретного заказа в БД
    :param order_scheme: OrderUpdate - объект, содержащий новые данные заказа конкретного пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Обновленный в БД заказ пользователя в виде Pydantic схемы
    """
    return await OrderDepends.update_oreder(
        order_id=order_id,
        session=session,
        order_schema=order_scheme,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_orders(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех заказов
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Пустой список
    """
    return await OrderDepends.clear_orders(session=session)


@router.delete(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_order(
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного заказа
    :param order_id: id конкретного заказа в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Удаленный из БД заказ пользователя в виде Pydantic схемы
    """
    return await OrderDepends.delete_order(
        order_id=order_id,
        session=session,
    )


@router.delete(
    "/user/{user_id}",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def delete_user_orders(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех заказов конкретного пользователя
    :param user_id: id конкретного пользователя в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Пустой список
    """
    return await OrderDepends.delete_all_user_orders(
        user_id=user_id,
        session=session,
    )
