from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order as Order_model
from app.schemas.order import OrderInput, OrderOutput


class OrderAdapter:

    @classmethod
    async def get_all_orders(
        cls,
        session: AsyncSession,
    ) -> list[Order_model]:
        """
        Возвращает все объекты заказов, существующие в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Список моделей Order
        """
        try:
            stmt = select(Order_model).order_by(Order_model.id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_order_by_id(
        cls,
        order_id: int,
        session: AsyncSession,
    ) -> Optional[Order_model]:
        """
        Возвращает объект конкретного заказа по его id из БД
        :param order_id: id конкретного заказа
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Объект конкретного заказа | None
        """
        try:
            return await session.get(Order_model, order_id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_added_orders_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Order_model]:
        """
        Возвращает список всех заказов, добавленных за указанный интервал времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех заказов, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(Order_model)
                .where(Order_model.created_at.between(*dates))
                .order_by(Order_model.created_at.desc())
            )

            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def add_order(
        cls,
        order_input: OrderInput,
        session: AsyncSession,
    ) -> Order_model:
        pass

    @classmethod
    async def update_order(
        cls,
        order_input: OrderInput,
        order_model: Order_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> Order_model:
        pass

    @classmethod
    async def delete_order(
        cls,
        order_model: Order_model,
        session: AsyncSession,
    ) -> Order_model:
        pass

    @classmethod
    async def clear_order_db(
        cls,
        session: AsyncSession,
    ) -> Order_model:
        pass
