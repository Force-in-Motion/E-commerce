from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order as Order_model
from app.schemas.order import OrderInput, OrderOutput


class OrderAdapter:

    @classmethod
    async def get_all_orders(
        cls,
        session: AsyncSession,
    ) -> list[Order_model]:
        pass

    @classmethod
    async def get_order_by_id(
        cls,
        order_id: int,
        session: AsyncSession,
    ) -> Order_model:
        pass

    @classmethod
    async def get_added_orders_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Order_model]:
        pass

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
