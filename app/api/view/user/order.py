from typing import Annotated

from fastapi.params import Depends
from fastapi import APIRouter, status, Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.user import UserAuth
from app.api.depends.order import OrderDepends
from app.api.depends.security import oauth2_scheme
from app.schemas import OrderResponse, OrderRequest, UserResponse


router = APIRouter(prefix="/user/orders", tags=["User Orders"])


@router.get(
    "/all",
    response_model=list[OrderResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_my_orders(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[OrderResponse]:
    """

    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_refresh(
        token=token,
        session=session,
    )

    return await OrderDepends.get_all_user_oreders(
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[OrderResponse]:
    """

    :param user_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_refresh(
        token=token,
        session=session,
    )

    return await OrderDepends.get_user_oreder(
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
    order_schema: OrderRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> OrderResponse:
    """

    :param user_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_refresh(
        token=token,
        session=session,
    )

    return await OrderDepends.create_user_oreder(
        user_id=user_model.id,
        session=session,
        order_schema=order_schema,
    )


@router.patch(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def update_my_order_partial(
    order_schema: OrderRequest,
    token: Annotated[str, Depends(oauth2_scheme)],
    order_id: Annotated[int, Path(..., description="Order ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_refresh(
        token=token,
        session=session,
    )

    return await OrderDepends.update_user_oreder(
        user_id=user_model.id,
        order_id=order_id,
        session=session,
        order_schema=order_schema,
    )


@router.delete(
    "/{order_id}",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_my_order(
    token: Annotated[str, Depends(oauth2_scheme)],
    order_id: Annotated[int, Path(..., description="Order id")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> OrderResponse:
    """

    :param order_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_refresh(
        token=token,
        session=session,
    )

    return await OrderDepends.del_user_order(
        user_id=user_model.id,
        order_id=order_id,
        session=session,
    )
