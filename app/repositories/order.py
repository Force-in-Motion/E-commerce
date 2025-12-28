from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepo
from app.models import (
    Order as Order_model,
    Cart as Cart_model,
    OrderProducts as OrderProducts_model,
)
from app.tools import DatabaseError


class OrderRepo(BaseRepo[Order_model]):

    model: Order_model

    @classmethod
    async def get_all_orders(
        cls,
        session: AsyncSession,
    ) -> list[Order_model]:
        """

        :param order_in:
        :param session:
        :return:
        """
        try:
            stmt = (
                select(cls.model).options(
                    selectinload(cls.model.products)
                    .selectinload(OrderProducts_model.product)
                )
                .order_by(cls.model.created_at.desc())
            )

            result = await session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} list"
            ) from e

    @classmethod
    async def get_all_orders_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[Order_model]:
        """

        :param order_in:
        :param session:
        :return:
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .options(
                    selectinload(cls.model.products).selectinload(
                        OrderProducts_model.product
                    )
                )
                .order_by(cls.model.created_at.desc())
            )

            result = await session.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} list"
            ) from e


    @classmethod
    async def get_orders_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Order_model]:
        """
        Возвращает список всех моделей пользователей, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех моделей пользователей, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.created_at.between(*dates))
                .options(
                    selectinload(cls.model.products).selectinload(
                        OrderProducts_model.product
                    )
                )
                .order_by(cls.model.created_at.desc())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving list {cls.model.__name__}s by dates"
            ) from e
        

    @classmethod
    async def get_by_user_id_and_order_id(
        cls,
        user_id: int,
        order_id: int,
        session: AsyncSession,
    ) -> Optional[Order_model]:
        try:
            stmt = (
                select(cls.model)
                .where(
                    cls.model.user_id == user_id,
                    cls.model.id == order_id,
                )
                .options(
                    selectinload(cls.model.products).selectinload(
                        OrderProducts_model.product
                    )
                )
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e

    @classmethod
    async def get_by_order_id(
        cls,
        order_id: int,
        session: AsyncSession,
    ) -> Optional[Order_model]:
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.id == order_id)
                .options(
                    selectinload(cls.model.products).selectinload(
                        OrderProducts_model.product
                    )
                )
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e

    @classmethod
    async def create_order(
        cls,
        user_id: int,
        total_price: int,
        total_quantity: int,
        session: AsyncSession,
        promo_code: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> Order_model:
        """

        :param order_in:
        :param session:
        :return:
        """
        try:
            order_model = Order_model(
                user_id=user_id,
                comment=comment,
                promo_code=promo_code,
                total_price=total_price,
                total_quantity=total_quantity,
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
