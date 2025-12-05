from sqlalchemy.util import await_only

from app.repositories.cart import CartAdapter
from app.service import BaseFacade

from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProductAdapter
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
    Product as Product_model,
)
from app.schemas import ProductAddOrUpdate


class CartFacade(BaseFacade[Cart_model, CartAdapter]):

    model = Cart_model
    adapter = CartAdapter

    @classmethod
    async def get_cart_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
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
    ) -> dict[str, int]:
        """

        :param user_id:
        :param session:
        :return:
        """
        cart_model = await cls.adapter.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        result = await cls.adapter.get_count_products(cart_in=cart_model)

        return {"count products in cart": result}

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
        cart_model = await cls.adapter.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        result = await cls.adapter.get_total_price(cart_in=cart_model)

        return {"total sum cart": result}

    @classmethod
    async def add_or_update_product_in_cart(
        cls,
        user_id: int,
        product_scheme: ProductAddOrUpdate,
        session: AsyncSession,
    ) -> Cart_Product_model:
        """

        :param user_id:
        :param product_add:
        :param session:
        :return:
        """
        async with session.begin():
            
            cart_model = await cls.adapter.get_or_create_cart(
                user_id=user_id,
                session=session,
            )

            cart_product = await cls.adapter.get_product(
                product_id=product_scheme.product_id,
                cart_model=cart_model,
            )

            if not cart_product:
                product_model = await ProductAdapter.get_by_id(
                    product_scheme.product_id, session=session
                )

                cart_product = await cls.adapter.add_product(
                    quantity=product_scheme.quantity,
                    product_model=product_model,
                    cart_model=cart_model,
                    session=session,
                )
            else:
                cart_product = await cls.adapter.update_count_product(
                    product_scheme=product_scheme,
                    cart_model=cart_model,
                    session=session,
                )

            
            
            return cart_product

    @classmethod
    async def del_product_from_cart(
        cls,
        user_id: int,
        product_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_Product_model]:
        """

        :param user_id:
        :param product_id:
        :param session:
        :return:
        """
        async with session.begin():
            
            cart_model = await cls.adapter.get_by_user_id(
                user_id=user_id,
                session=session,
            )

            return await cls.adapter.delete_product(
                product_id=product_id,
                cart_model=cart_model,
                session=session,
            )

    @classmethod
    async def clear_cart_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        async with session.begin():

            cart_model = await cls.adapter.get_by_user_id(user_id=user_id, session=session)

            if not cart_model:
                return None

            return await cls.adapter.clear_cart(
                cart_model=cart_model,
                session=session,
            )
