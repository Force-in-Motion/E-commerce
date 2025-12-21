from app.repositories.cart import CartRepo
from app.schemas.cart import CartResponse
from app.service import BaseService

from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProductRepo
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
)
from app.schemas import ProductAddOrUpdate


class CartService(BaseService[CartRepo]):

    repo = CartRepo

    classmethod

    async def get_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[CartResponse]:
        """

        :param user_id:
        :param session:
        :return:
        """
        cart_model = await cls.repo.get_by_user_id(user_id, session)

        if cart_model:
            total_quantity = sum(cp.quantity for cp in cart_model.products)
            total_price = sum(
                int(cp.current_price) * cp.quantity for cp in cart_model.products
            )

            cart_schema = CartResponse.model_validate(cart_model)

            cart_schema.total_price = total_price
            cart_schema.total_quantity = total_quantity

            return cart_schema

    @classmethod
    async def get_or_create_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> CartResponse:
        """

        :param user_id:
        :param session:
        :return:
        """
        async with session.begin():

            cart_schema = await cls.get_cart(
                user_id=user_id,
                session=session,
            )

            if not cart_schema:
                cart_model = await cls.repo.create_cart(
                    user_id=user_id,
                    session=session,
                )
                return CartResponse.model_validate(cart_model)

            return cart_schema

    @classmethod
    async def add_or_update_product_in_cart(
        cls,
        user_id: int,
        product_scheme: ProductAddOrUpdate,
        session: AsyncSession,
    ) -> CartResponse:
        """

        :param user_id:
        :param product_add:
        :param session:
        :return:
        """
        async with session.begin():

            cart_model = await cls.repo.get_by_user_id(
                user_id=user_id,
                session=session,
            )

            cart_product = await cls.repo.get_product(
                product_id=product_scheme.product_id,
                cart_model=cart_model,
            )

            if not cart_product:
                product_model = await ProductRepo.get_by_id(
                    model_id=product_scheme.product_id,
                    session=session,
                )

                await cls.repo.add_product(
                    quantity=product_scheme.quantity,
                    product_model=product_model,
                    cart_model=cart_model,
                    session=session,
                )
            else:
                await cls.repo.update_count_product(
                    product_scheme=product_scheme,
                    cart_model=cart_model,
                    session=session,
                )

            return cls.get_or_create_cart(
                user_id=user_id,
                session=session,
            )

    @classmethod
    async def del_product_from_cart(
        cls,
        user_id: int,
        product_id: int,
        session: AsyncSession,
    ) -> CartResponse:
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

            if not cart_model:
                return None

            await cls.repo.delete_product(
                product_id=product_id,
                cart_model=cart_model,
                session=session,
            )

            return cls.get_or_create_cart(
                user_id=user_id,
                session=session,
            )

    @classmethod
    async def clear_cart_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """

        :param user_id:
        :param session:
        :return:
        """
        async with session.begin():

            cart_model = await cls.repo.get_by_user_id(
                user_id=user_id,
                session=session,
            )

            if not cart_model:
                return None

            await cls.repo.clear_cart(
                cart_model=cart_model,
                session=session,
            )

            return cls.get_or_create_cart(
                user_id=user_id,
                session=session,
            )
