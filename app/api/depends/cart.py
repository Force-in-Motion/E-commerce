from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProductAddOrUpdate
from app.schemas import CartResponse
from app.service import CartService
from app.tools import HTTPErrors


class CartDepends:

    @classmethod
    async def get_user_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        cart_response = await CartService.get_or_create_cart(
            user_id=user_id,
            session=session,
        )

        if not cart_response:

            raise HTTPErrors.db_error

        return cart_response

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
        cart_response = await CartService.add_or_update_product_in_cart(
            user_id=user_id,
            product_scheme=product_add,
            session=session,
        )

        if not cart_response:
            raise HTTPErrors.db_error

        return cart_response

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
        cart_response = await CartService.del_product_from_cart(
            user_id=user_id,
            product_id=product_id,
            session=session,
        )

        if not cart_response:
            raise HTTPErrors.db_error

        return cart_response

    @classmethod
    async def clear_cart_by_user_id(
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
