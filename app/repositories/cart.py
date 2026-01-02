from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepo
from app.models import (
    Cart as Cart_model,
    CartProduct as Cart_Product_model,
    Product as Product_model,
)
from app.schemas import ProductAddOrUpdate
from app.tools import DatabaseError


class CartRepo(BaseRepo[Cart_model]):

    model = Cart_model


    @classmethod
    async def get_all_carts(
        cls,
        session: AsyncSession,
    ) -> list[Cart_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        try:
            stmt = (
                select(cls.model)
                .options(
                    selectinload(cls.model.products)
                    .selectinload(Cart_Product_model.product)
                )
            )

            result = await session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e
        

    @classmethod
    async def get_all_carts_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Cart_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.created_at.between(**dates))
                .options(
                    selectinload(cls.model.products)
                    .selectinload(Cart_Product_model.product)
                )
            )

            result = await session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e
        

    @classmethod
    async def get_product(
        cls,
        product_id: int,
        cart_model: Cart_model,
    ) -> Optional[Cart_Product_model]:
        """

        :param cart_in:
        :param product_id:
        :return:
        """
        try:
            for assoc in cart_model.products:
                if assoc.product_id == product_id:
                    return assoc

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving product by id from {cls.model.__name__}"
            ) from e


    @classmethod
    async def get_by_id(
        cls,
        cart_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.id == cart_id)
                .options(
                    selectinload(cls.model.products)
                    .selectinload(Cart_Product_model.product)
                )
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e
        

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
            stmt = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .options(
                    selectinload(cls.model.products)
                    .selectinload(Cart_Product_model.product)
                )
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e


    @classmethod
    async def add_product(
        cls,
        quantity: int,
        product_model: Product_model,
        cart_model: Cart_model,
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
                cart_id=cart_model.id,
                product_id=product_model.id,
                quantity=quantity,
                current_price=product_model.price,
            )

            session.add(assoc)
            await session.commit()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error adding product in {cls.model.__name__}") from e

    @classmethod
    async def update_count_product(
        cls,
        product_scheme: ProductAddOrUpdate,
        cart_model: Cart_model,
        session: AsyncSession,
    ) -> None:
        """

        :param product_scheme:
        :param cart_in:
        :param session:
        :return:
        """
        try:
            for assoc in cart_model.products:
                if assoc.product_id == product_scheme.product_id:
                    assoc.quantity += product_scheme.quantity

            await session.commit()


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
    ) -> None:
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

            await session.commit()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error deleting count product in {cls.model.__name__}"
            ) from e

    @classmethod
    async def clear_cart(
        cls,
        cart_model: Cart_model,
        session: AsyncSession,
    ) -> list:
        """
        Очищает корзину пользователя, удаляя все продукты,
        но сохраняя саму корзину.
        """
        try:
            for assoc in cart_model.products:
                await session.delete(assoc)

            await session.commit()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error clearing cart in {cls.model.__name__}") from e
