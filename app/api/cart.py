from datetime import datetime

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.schemas.cart import CartResponse
from app.tools import Inspector

router = APIRouter()


@router.get(
    "/",
    response_model=list[CartResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_carts(
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[CartResponse]:
    """

    :param session:
    :return:
    """


@router.get(
    "/date",
    response_model=list[CartResponse],
    status_code=status.HTTP_200_OK,
)
async def get_carts_by_date(
    dates: datetime = Depends(Inspector.date_checker),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[CartResponse]:
    """

    :param dates:
    :param session:
    :return:
    """
    pass


@router.get(
    "/count/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def get_count_products(
    user_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, int]:
    """

    :param user_id:
    :param session:
    :return:
    """


@router.get(
    "/sum/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def get_total_sum(
    user_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, int]:
    """

    :param user_id:
    :param session:
    :return:
    """


@router.get(
    "/{cart_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart_by_id(
    cart_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param cart_id:
    :param session:
    :return:
    """


@router.get(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart_by_user_id(
    user_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param session:
    :return:
    """


@router.post(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_product(
    user_id: int,
    product_id: int,
    quantity: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param product_id:
    :param quantity:
    :param session:
    :return:
    """


@router.patch(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_count_product(
    user_id: int,
    product_id: int,
    quantity: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param product_id:
    :param quantity:
    :param session:
    :return:
    """


@router.delete(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    user_id: int,
    product_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param product_id:
    :param session:
    :return:
    """


@router.delete(
    "/{user_id}",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_user_cart(
    user_id: int,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list:
    """

    :param user_id:
    :param session:
    :return:
    """
