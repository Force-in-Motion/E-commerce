from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepo
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
    Product as Product_model,
)
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartRequest

from app.tools import DatabaseError


class CartRepo(BaseRepo[Cart_model]):

    model = Cart_model

    @classmethod
    async def get_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        try:
            stmt = select(cls.model).where(cls.model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().first()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by user id"
            ) from e

    @classmethod
    async def get_count_products(
        cls,
        cart_in: Cart_model,
    ) -> int:
        """
        Считает суммарное количество продуктов в корзине из уже найденной модели.
        :param cart_in: ORM-модель корзины с уже загруженными продуктами
        :return: сумма quantity
        """
        try:
            return sum(product.quantity for product in cart_in.products)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving count products in {cls.model.__name__}"
            ) from e

    @classmethod
    async def get_total_price(
        cls,
        cart_in: Cart_model,
    ) -> int:
        """
        Считает суммарное количество продуктов в корзине из уже найденной модели.
        :param cart_in: ORM-модель корзины с уже загруженными продуктами
        :return: сумма quantity
        """
        try:
            return sum(cp.quantity * cp.current_price for cp in cart_in.products)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving total sum in {cls.model.__name__}"
            ) from e

    @classmethod
    async def get_product(
        cls,
        product_id: int,
        cart_in: Cart_model,
    ) -> Optional[Cart_Product_model]:
        """

        :param cart_in:
        :param product_id:
        :return:
        """
        try:
            for assoc in cart_in.products:
                if assoc.product_id == product_id:
                    return assoc

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving product by id from {cls.model.__name__}"
            ) from e

    @classmethod
    async def get_or_create_cart(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Cart_model:
        """

        :param user_id:
        :param session:
        :return:
        """
        cart_model = await cls.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        if not cart_model:

            cart_schema = CartRequest(user_id=user_id)

            cart_model = await cls.create(
                scheme_in=cart_schema,
                session=session,
            )

        return cart_model

    @classmethod
    async def add_product(
        cls,
        quantity: int,
        product_model: Product_model,
        cart_in: Cart_model,
        session: AsyncSession,
    ) -> Cart_Product_model:
        """

        :param quantity:
        :param product_in:
        :param cart_in:
        :param session:
        :return:
        """
        try:
            assoc = Cart_Product_model(
                cart_id=cart_in.id,
                product_id=product_model.id,
                quantity=quantity,
                current_price=product_model.price,
            )

            session.add(assoc)
            await session.refresh(assoc)

            return assoc

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error adding product in {cls.model.__name__}") from e

    @classmethod
    async def update_count_product(
        cls,
        product_scheme: ProductAddOrUpdate,
        cart_model: Cart_model,
        session: AsyncSession,
    ) -> Cart_Product_model:
        """

        :param product_scheme:
        :param cart_in:
        :param session:
        :return:
        """
        try:
            for assoc in cart_model.products:
                if assoc.product_id == product_scheme.product_id:
                    assoc.quantity = product_scheme.quantity
                    await session.refresh(assoc)

                    return assoc

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error updating count product in {cls.model.__name__}"
            ) from e

    @classmethod
    async def delete_product(
        cls,
        product_id: int,
        cart_model: Cart_model,
        session: AsyncSession,
    ) -> Optional[Cart_Product_model]:
        """

        :param product_id:
        :param cart_in:
        :param session:
        :return:
        """
        try:
            for assoc in cart_model.products:
                if assoc.product_id == product_id:
                    await session.delete(assoc)

                    return assoc

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error deleting count product in {cls.model.__name__}"
            ) from e

    @classmethod
    async def clear_cart(
        cls,
        cart_model: Cart_model,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
        """
        Очищает корзину пользователя, удаляя все продукты,
        но сохраняя саму корзину.
        """
        try:
            # Удаляем все связанные продукты из корзины
            for assoc in list(cart_model.products):
                await session.delete(assoc)

            await session.refresh(cart_model)

            return cart_model

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error clearing cart in {cls.model.__name__}") from e
