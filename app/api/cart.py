from datetime import datetime

from fastapi import APIRouter, status, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.core import db_connector
from app.facade.cart import CartFacade
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartResponse
from app.tools import Inspector

router = APIRouter()


@router.get(
    "/all",
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
    return await CartFacade.get_all_models(session=session)


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
    return await CartFacade.get_models_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/count/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def get_count_products(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, int]:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await CartFacade.get_count_products_in_cart(
        user_id=user_id,
        session=session,
    )


@router.get(
    "/sum/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def get_total_sum(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> dict[str, int]:
    """

    :param user_id:
    :param session:
    :return:
    """
    await CartFacade.get_total_sum_cart(
        user_id=user_id,
        session=session,
    )


@router.get(
    "/{cart_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart_by_id(
    cart_id: Annotated[int, Path(..., description="Cart id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param cart_id:
    :param session:
    :return:
    """
    return await CartFacade.get_model_by_id(
        model_id=cart_id,
        session=session,
    )


@router.get(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart_by_user_id(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param session:
    :return:
    """
    return await CartFacade.get_cart_by_user_id(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_product(
    user_id: Annotated[int, Path(..., description="User id")],
    product_add: ProductAddOrUpdate,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param product_add:
    :param session:
    :return:
    """
    return await CartFacade.add_or_update_product_in_cart(
        user_id=user_id,
        product_add=product_add,
        session=session,
    )


@router.patch(
    "/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_count_product(
    user_id: int,
    product_upd: ProductAddOrUpdate,
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> CartResponse:
    """

    :param user_id:
    :param product_upd:
    :param session:
    :return:
    """
    return CartFacade.add_or_update_product_in_cart(
        user_id=user_id,
        product_add=product_upd,
        session=session,
    )


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
    return await CartFacade.del_product_from_cart(
        user_id=user_id,
        product_id=product_id,
        session=session,
    )


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
    return await CartFacade.clear_cart_by_user_id(
        user_id=user_id,
        session=session,
    )
