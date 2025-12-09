from sqlalchemy.util import await_only

from app.repositories.cart import CartRepo
from app.service import BaseService

from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProductRepo
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
    Product as Product_model,
)
from app.schemas import ProductAddOrUpdate


class CartFacade(BaseService[Cart_model, CartRepo]):

    model = Cart_model
    repo = CartRepo

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

        return await cls.repo.get_by_user_id(
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
        cart_model = await cls.repo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        result = await cls.repo.get_count_products(cart_in=cart_model)

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
        cart_model = await cls.repo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        result = await cls.repo.get_total_price(cart_in=cart_model)

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

            cart_model = await cls.repo.get_or_create_cart(
                user_id=user_id,
                session=session,
            )

            cart_product = await cls.repo.get_product(
                product_id=product_scheme.product_id,
                cart_model=cart_model,
            )

            if not cart_product:
                product_model = await ProductRepo.get_by_id(
                    product_scheme.product_id, session=session
                )

                cart_product = await cls.repo.add_product(
                    quantity=product_scheme.quantity,
                    product_model=product_model,
                    cart_model=cart_model,
                    session=session,
                )
            else:
                cart_product = await cls.repo.update_count_product(
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

            cart_model = await cls.repo.get_by_user_id(
                user_id=user_id,
                session=session,
            )

            return await cls.repo.delete_product(
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

            cart_model = await cls.repo.get_by_user_id(user_id=user_id, session=session)

            if not cart_model:
                return None

            return await cls.repo.clear_cart(
                cart_model=cart_model,
                session=session,
            )
