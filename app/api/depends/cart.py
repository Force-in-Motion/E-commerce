from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProductAddOrUpdate
from app.schemas import CartResponse
from app.service import CartService
from app.tools import HTTPErrors


class CartDepends:

    @classmethod
    async def get_all_cart(
        cls,
        session: AsyncSession,
        dates: tuple[datetime, datetime] = None,
    ) -> list[CartResponse]:
        """

        :param param:
        :param param:
        :return:
        """
        cart_schemes = await CartService.get_all_carts(dates=dates, session=session)

        if cart_schemes is None:
            raise HTTPErrors.not_found

        return cart_schemes

    @classmethod
    async def get_cart(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        cart_scheme = await CartService.get_or_create_cart(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
        )

        if cart_scheme is None:

            raise HTTPErrors.not_found

        return cart_scheme

    @classmethod
    async def add_or_update_product_in_cart(
        cls,
        session: AsyncSession,
        product_scheme: ProductAddOrUpdate,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        cart_scheme = await CartService.add_or_update_product_in_cart(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
            product_scheme=product_scheme,
        )

        if cart_scheme is None:
            raise HTTPErrors.err_update_model

        return cart_scheme

    @classmethod
    async def del_product_from_cart(
        cls,
        user_id: int,
        product_id: int,
        session: AsyncSession,
    ) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        cart_scheme = await CartService.del_product_from_cart(
            user_id=user_id,
            product_id=product_id,
            session=session,
        )

        if cart_scheme is None:
            raise HTTPErrors.err_delete_model

        return cart_scheme

    @classmethod
    async def clear_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """

        :param param:
        :param param:
        :return:
        """
        cart_table = await CartService.clear_user_cart(
            user_id=user_id,
            session=session,
        )

        if cart_table is None:
            raise HTTPErrors.clear_table

        return cart_table
