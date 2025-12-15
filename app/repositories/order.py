from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepo
from app.models import (
    Order as Order_model,
    OrderProducts as OrderProducts_model,
    Cart as Cart_model,
)
from app.tools import DatabaseError


class OrderRepo(BaseRepo[Order_model]):

    model: Order_model


    @classmethod
    async def create_order(
        cls,
        user_id: int,
        total_price: int,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param order_in:
        :param session:
        :return:
        """
        try:
            order_model = Order_model(
                user_id=user_id,
                total_price=total_price,
            )

            session.add(order_model)

            await session.flush()
            await session.refresh(order_model)

            return order_model

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when adding {cls.model.__name__}") from e

    @classmethod
    async def add_product_to_order(
        cls,
        cart_model: Cart_model,
        order_model: Order_model,
        session: AsyncSession,
    ) -> None:
        """

        :param order_id:
        :param product_id:
        :param quantity:
        :param current_price:
        :param session:
        :return:
        """

        try:
            for cart_product in cart_model.products:

                order_product = OrderProducts_model(
                    order_id=order_model.id,
                    product_id=cart_product.product_id,
                    quantity=cart_product.quantity,
                    current_price=cart_product.current_price,
                )

                session.add(order_product)

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when adding product to {cls.model.__name__}"
            ) from e
