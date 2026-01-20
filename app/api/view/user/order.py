from typing import Annotated
from fastapi.params import Depends
from fastapi import APIRouter, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.schemas import OrderResponse
from app.api.depends.user import UserAuth
from app.api.depends.order import OrderDepends
from app.api.depends.security import oauth2_scheme
from app.schemas.order import OrderCreate, OrderUpdate


router = APIRouter(
    prefix="/user/orders",
    tags=["My Orders"],
)


@router.get(
    "/all",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_my_orders(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[OrderResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех заказов пользователей
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Список всех заказов пользователей в виде Pydantic схем
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await OrderDepends.get_all_oreders(
        user_id=user_model.id,
        session=session,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_order(
    token: Annotated[str, Depends(oauth2_scheme)],
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[OrderResponse]:
    """
    Обрабатывает запрос с фронт энда на получение заказа пользователя по его id
    :param order_id: id конкретного заказа в БД
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Профиль конкретного пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await OrderDepends.get_oreder(
        user_id=user_model.id,
        order_id=order_id,
        session=session,
    )


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_my_order(
    order_scheme: OrderCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на создание заказа пользователя в БД
    :param order_scheme: OrderCreate - объект, содержащий данные заказа пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Добавленный в БД заказ пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await OrderDepends.create_oreder(
        user_id=user_model.id,
        session=session,
        order_scheme=order_scheme,
    )


@router.patch(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def update_my_order_partial(
    order_scheme: OrderUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных заказа конкретного пользователя
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param order_scheme: OrderUpdate - объект, содержащий новые данные заказа конкретного пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Обновленный в БД заказ пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await OrderDepends.update_oreder(
        user_id=user_model.id,
        order_id=order_id,
        session=session,
        order_response=order_scheme,
    )


@router.delete(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_my_order(
    token: Annotated[str, Depends(oauth2_scheme)],
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> OrderResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного заказа
    :param order_id: id конкретного заказа в БД
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Удаленный из БД заказ пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await OrderDepends.delete_order(
        user_id=user_model.id,
        order_id=order_id,
        session=session,
    )
