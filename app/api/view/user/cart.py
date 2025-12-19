from fastapi import APIRouter, status, Path
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from app.api.depends.cart import CartDepends
from app.core import db_connector
from app.service.cart import CartService
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartResponse
from app.api.depends.user import UserAuth


router = APIRouter(prefix="/user/cart", tags=["User Cart"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/auth/login")



@router.get(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_cart(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> CartResponse:
    """

    :param cart_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.get_user_cart(
        user_id=user_model.id,
        session=session,
    )


@router.post(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_product(
    product_add: ProductAddOrUpdate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> CartResponse:
    """

    :param user_id:
    :param product_add:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_model.id,
        product_add=product_add,
        session=session,
    )


@router.patch(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_count_product(
    product_upd: ProductAddOrUpdate,
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> CartResponse:
    """

    :param user_id:
    :param product_upd:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_model.id,
        product_add=product_upd,
        session=session,
    )


@router.delete(
    "/{product_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: int = Path(..., description="Product ID"),
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> CartResponse:
    """

    :param user_id:
    :param product_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.del_product_from_cart(
        user_id=user_model.id,
        product_id=product_id,
        session=session,
    )


@router.delete(
    "/",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_my_cart(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_connector.get_session),
) -> list:
    """

    :param user_id:
    :param session:
    :return:
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.clear_cart_by_user_id(
        user_id=user_model.id,
        session=session,
    )
