from datetime import datetime

from fastapi import APIRouter, status, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.core import db_connector
from app.service.order import OrderService
from app.schemas import OrderResponse, OrderRequest, UserResponse
from app.tools import Inspector

router = APIRouter()


@router.get(
    "/all",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_orders(
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[OrderResponse]:
    """

    :param session:
    :return:
    """
    return await OrderService.get_all_models(session=session)


@router.get(
    "/date",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_orders_by_date(
    dates: tuple[datetime, datetime] = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[OrderResponse]:
    """

    :param dates:
    :param session:
    :return:
    """
    return await OrderService.get_all_models_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_by_id(
    order_id: Annotated[int, Path(..., description="Order id")],
    session: AsyncSession = Depends(db_connector.get_session),
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    return await OrderService.get_model_by_id(
        model_id=order_id,
        session=session,
    )


@router.get(
    "/{user_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_orders_by_user_id(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[OrderResponse]:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await OrderService.get_orders_by_user_id(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/{user_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.get_session),
) -> OrderResponse:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await OrderService.create_order_for_user(
        user_id=user_id,
        session=session,
    )


@router.patch(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order_partial(
    order_id: Annotated[int, Path(..., description="Order id")],
    order_scheme: OrderRequest,
    session: AsyncSession = Depends(db_connector.get_session),
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    return await OrderService.update_order_partial(
        model_id=order_id,
        order_scheme=order_scheme,
        session=session,
    )


@router.delete(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_order(
    order_id: Annotated[int, Path(..., description="Order id")],
    session: AsyncSession = Depends(db_connector.get_session),
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    return await OrderService.delete_model(
        model_id=order_id,
        session=session,
    )
