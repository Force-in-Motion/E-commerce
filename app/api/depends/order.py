# cart_depends.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order as Order_model
from app.schemas import ProductAddOrUpdate
from app.schemas import OrderResponse, OrderRequest
from app.service.order import OrderService
from app.tools import HTTPExeption


class OrderDepends:

    @classmethod
    async def get_all_user_oreders(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[OrderResponse]:
        """

        :param param:
        :param param:
        :return:
        """
        list_order_model = await OrderService.get_all_models(
            user_id=user_id,
            session=session,
        )

        if not list_order_model:

            raise HTTPExeption.not_found

        return list_order_model

    @classmethod
    async def get_user_oreder(
        cls,
        user_id: int,
        order_id: int,
        session: AsyncSession,
    ) -> OrderResponse:
        """

        :param param:
        :param param:
        :return:
        """
        order_model = await OrderService.get_order_by_user_id(
            user_id=user_id,
            order_id=order_id,
            session=session,
        )

        if not order_model:
            raise HTTPExeption.not_found

        return order_model

    @classmethod
    async def create_user_oreder(
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
        created_order_model = await OrderService.create_order_for_user(
            user_id=user_id,
            order_schema=order_schema,
            session=session,
        )

        if not created_order_model:
            raise HTTPExeption.db_error

        return created_order_model

    @classmethod
    async def update_user_oreder(
        cls,
        user_id: int,
        order_id: int,
        session: AsyncSession,
        order_schema: OrderRequest,
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
            raise HTTPExeption.db_error

        return updated_order_model

    @classmethod
    async def del_user_order(
        cls,
        user_id: int,
        order_id: int,
        session: AsyncSession,
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
            raise HTTPExeption.db_error

        return deleted_order_model
