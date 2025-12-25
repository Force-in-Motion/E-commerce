# cart_depends.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order as Order_model
from app.schemas import OrderResponse, OrderRequest
from app.service.order import OrderService
from app.tools import HTTPErrors


class OrderDepends:

    @classmethod
    async def get_all_oreders(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[list[Order_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        list_order_model = await OrderService.get_all_orders(
            user_id=user_id,
            session=session,
        )

        if not list_order_model:

            raise HTTPErrors.not_found

        return list_order_model

    @classmethod
    async def get_oreder(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[Order_model]:
        """

        :param param:
        :param param:
        :return:
        """
        order_model = await OrderService.get_order(
            order_id=order_id,
            user_id=user_id,
            session=session,
        )

        if not order_model:
            raise HTTPErrors.not_found

        return order_model

    @classmethod
    async def create_oreder(
        cls,
        user_id: int,
        session: AsyncSession,
        order_schema: OrderRequest,
    ) -> Order_model:
        """

        :param param:
        :param param:
        :return:
        """
        created_order_model = await OrderService.create_order(
            user_id=user_id,
            order_schema=order_schema,
            session=session,
        )

        if not created_order_model:
            raise HTTPErrors.db_error

        return created_order_model

    @classmethod
    async def update_oreder(
        cls,
        order_id: int,
        session: AsyncSession,
        order_schema: OrderRequest,
        user_id: Optional[int] = None,
    ) -> Order_model:
        """

        :param param:
        :param param:
        :return:
        """
        updated_order_model = await OrderService.update_order_partial(
            user_id=user_id,
            order_id=order_id,
            order_schema=order_schema,
            session=session,
        )

        if not updated_order_model:
            raise HTTPErrors.db_error

        return updated_order_model

    @classmethod
    async def delete_order(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> OrderResponse:
        """

        :param param:
        :param param:
        :return:
        """
        deleted_order_model = await OrderService.delete_model(
            user_id=user_id,
            model_id=order_id,
            session=session,
        )
        if not deleted_order_model:
            raise HTTPErrors.db_error

        return deleted_order_model
