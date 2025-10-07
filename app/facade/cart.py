from sqlalchemy.util import await_only

from app.crud.cart import CartAdapter
from app.facade import BaseFacade

from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
    Product as Product_model,
)
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartRequest


class CartFacade(BaseFacade[Cart_model, CartAdapter]):

    model = Cart_model
    adapter = CartAdapter

    @classmethod
    async def get_cart_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Cart_model:
        """

        :param user_id:
        :param session:
        :return:
        """

        return await cls.adapter.get_by_user_id(
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def get_count_products_in_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Cart_model:
        """

        :param user_id:
        :param session:
        :return:
        """
        cart = await cls.adapter.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        return await cls.adapter.get_count_products(cart_in=cart)

    @classmethod
    async def get_total_sum_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> dict[str, int]:
        """

        :param user_id:
        :param session:
        :return:
        """
        cart = await cls.adapter.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        return await cls.adapter.get_total_sum(cart_in=cart)

    @classmethod
    async def add_product_in_cart(
        cls,
        user_id: int,
        product_add: ProductAddOrUpdate,
        session: AsyncSession,
    ) -> Cart_Product_model:
        """

        :param user_id:
        :param product_add:
        :param session:
        :return:
        """
        cart_model = await cls.adapter.get_or_create_cart(
            user_id=user_id,
            session=session,
        )

        cart_product = await cls.adapter.get_product(
            product_id=product_add.product_id,
            cart_in=cart_model,
        )

        if not cart_product:
            return await cls.adapter.add_product(
                quantity=product_add.quantity,
                product_in=cart_product.product,
                cart_in=cart_model,
                session=session,
            )

        else:
            return await cls.adapter.update_count_product(
                product_upd=product_add,
                cart_in=cart_model,
                session=session,
            )
