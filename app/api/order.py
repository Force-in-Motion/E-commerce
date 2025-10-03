from datetime import datetime

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.facade.order import OrderFacade
from app.schemas import OrderResponse, OrderRequest, UserResponse
from app.tools import Inspector

router = APIRouter()


@router.get(
    "/all",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_orders(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[OrderResponse]:
    """

    :param session:
    :return:
    """
    return await OrderFacade.get_all_models(session=session)


@router.get(
    "/date",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_orders_by_date(
    dates: tuple[datetime, datetime] = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[OrderResponse]:
    """

    :param dates:
    :param session:
    :return:
    """
    return await OrderFacade.get_models_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    return await OrderFacade.get_model_by_id(
        model_id=order_id,
        session=session,
    )


@router.get(
    "/{user_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def get_orders_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[OrderResponse]:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await OrderFacade.get_orders_by_user_id(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_order(
    order_in: OrderRequest,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> OrderResponse:
    """

    :param order_in:
    :param session:
    :return:
    """
    return await OrderFacade.register_model_for_user(
        session=session,
    )


@router.delete(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    return await OrderFacade.delete_model(
        model_id=order_id,
        session=session,
    )
