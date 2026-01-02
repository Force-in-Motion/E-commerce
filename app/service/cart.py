from app.repositories.cart import CartRepo
from app.schemas.cart import CartResponse
from app.service import BaseService
from datetime import datetime
from typing import Optional


from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProductRepo
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
)
from app.schemas import ProductAddOrUpdate, ProductInCart


class CartService(BaseService[CartRepo]):

    repo = CartRepo

    @classmethod
    def _to_cart_response(cls, cart_model: Cart_model) -> CartResponse:
        """

        :param param:
        :param param:
        :return:
        """
        products = [
            ProductInCart(
                id=cp.product.id,
                name=cp.product.name,
                description=cp.product.description,
                price=cp.current_price,
                quantity=cp.quantity,
            )
            for cp in cart_model.products
        ]

        return CartResponse(
            id=cart_model.id,
            user_id=cart_model.user_id,
            products=products,
            created_at=cart_model.created_at,
            updated_at=cart_model.updated_at,
        )


    @classmethod
    async def get_all_carts(
        cls,
        session: AsyncSession,
        dates: tuple[datetime, datetime] = None,
    ) -> list[CartResponse]:
        """ "

        :param user_id:
        :param session:
        :return:
        """
        cart_models = await cls.repo.get_all_carts(
            dates=dates,
            session=session,
        )

        return [CartResponse.model_validate(cart) for cart in cart_models]

    @classmethod
    async def get_all_carts_by_date(
        cls,
        session: AsyncSession,
        dates: tuple[datetime, datetime] = None,
    ) -> list[CartResponse]:
        """

        :param user_id:
        :param session:
        :return:
        """
        cart_models = await cls.repo.get_all_carts_by_date(
            dates=dates,
            session=session,
        )

        return [CartResponse.model_validate(cart) for cart in cart_models]

    @classmethod
    async def get_cart(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[Cart_model]:
        """

        :param user_id:
        :param session:
        :return:
        """

        cart_model = await cls.repo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        if not cart_model:
            return None

        return cart_model

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
        cart_model = await cls.get_cart(
            user_id=user_id,
            session=session,
        )

        if not cart_model:
            cart_model = Cart_model(user_id=user_id)

            cart_model = await cls.repo.create(
                model=cart_model,
                session=session,
            )

        return cls._to_cart_response(cart_model)

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

        return await cls.get_or_create_cart(
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

        return await cls.get_or_create_cart(
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

        return await cls.get_or_create_cart(
            user_id=user_id,
            session=session,
        )
