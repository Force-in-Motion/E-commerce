# cart_depends.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Cart as Cart_model, CartProduct as Cart_Product_model
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartResponse
from app.service.cart import CartService
from app.tools import HTTPExeption


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
        schema_cart = await CartService.get_or_create_cart(
            user_id=user_id,
            session=session,
        )

        if not schema_cart:

            raise HTTPExeption.db_error
        
        return schema_cart

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
        schema_cart = await CartService.add_or_update_product_in_cart(
            user_id=user_id,
            product_scheme=product_add,
            session=session,
        )

        if not schema_cart:
            raise HTTPExeption.db_error

        return schema_cart

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
        schema_cart = await CartService.del_product_from_cart(
            user_id=user_id,
            product_id=product_id,
            session=session,
        )

        if not schema_cart:
            raise HTTPExeption.db_error

        return schema_cart

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
        schema_cart = await CartService.clear_cart_by_user_id(
            user_id=user_id,
            session=session,
        )

        if not schema_cart:
            raise HTTPExeption.db_error

        return schema_cart
