from datetime import datetime

from fastapi import APIRouter, status, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core import db_connector
from app.api.depends.security import admin_guard
from app.api.depends.cart import CartDepends
from app.api.depends.inspect import Inspector
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartResponse


router = APIRouter(
    prefix="/admin/carts",
    tags=["Admin Cart"],
    dependencies=[Depends(admin_guard)],
)


@router.get(
    "/all",
    response_model=list[CartResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_carts(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[CartResponse]:
    """

    :param session:
    :return:
    """
    return await CartDepends.get_all_cart(session=session)


@router.get(
    "/date",
    response_model=list[CartResponse],
    status_code=status.HTTP_200_OK,
)
async def get_carts_by_date(
    dates: datetime = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.get_session),
) -> list[CartResponse]:
    """

    :param dates:
    :param session:
    :return:
    """
    return await CartDepends.get_all_cart_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart_by_user_id(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await CartDepends.get_cart(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_product(
    product_add: ProductAddOrUpdate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """

    :param user_id:
    :param product_add:
    :param session:
    :return:
    """
    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_id,
        session=session,
        product_add=product_add,
    )


@router.patch(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_count_product(
    product_upd: ProductAddOrUpdate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """

    :param user_id:
    :param product_upd:
    :param session:
    :return:
    """
    return CartDepends.add_or_update_product_in_cart(
        user_id=user_id,
        product_add=product_upd,
        session=session,
    )


@router.delete(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    user_id: Annotated[int, Path(..., description="User ID")],
    product_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """

    :param user_id:
    :param product_id:
    :param session:
    :return:
    """
    return await CartDepends.del_product_from_cart(
        user_id=user_id,
        product_id=product_id,
        session=session,
    )


@router.delete(
    "/user/{user_id}/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_user_cart(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await CartDepends.clear_cart(
        user_id=user_id,
        session=session,
    )
