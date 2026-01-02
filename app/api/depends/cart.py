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
    ) -> list[CartResponse]:
        """

        :param param:
        :param param:
        :return:
        """
        cart_schemes = await CartService.get_all_carts(session=session)

        if not cart_schemes:
            raise HTTPErrors.db_error

        return cart_schemes

    @classmethod
    async def get_all_cart_by_date(
        cls,
        session: AsyncSession,
        dates: tuple[datetime, datetime] = None,
    ) -> list[CartResponse]:
        """

        :param param:
        :param param:
        :return:
        """
        cart_schemes = await CartService.get_all_carts_by_date(
            dates=dates,
            session=session,
        )

        if not cart_schemes:
            raise HTTPErrors.db_error

        return cart_schemes

    @classmethod
    async def get_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        cart_scheme = await CartService.get_or_create_cart(
            user_id=user_id,
            session=session,
        )

        if not cart_scheme:

            raise HTTPErrors.db_error

        return cart_scheme

    @classmethod
    async def add_or_update_product_in_cart(
        cls,
        user_id: int,
        product_add: ProductAddOrUpdate,
        session: AsyncSession,
    ) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        cart_scheme = await CartService.add_or_update_product_in_cart(
            user_id=user_id,
            session=session,
            product_scheme=product_add,
        )

        if not cart_scheme:
            raise HTTPErrors.db_error

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

        if not cart_scheme:
            raise HTTPErrors.db_error

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
        empty_list = await CartService.clear_cart_by_user_id(
            user_id=user_id,
            session=session,
        )

        if not empty_list:
            raise HTTPErrors.db_error

        return empty_list
