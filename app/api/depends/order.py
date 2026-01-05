from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools import HTTPErrors
from app.service.order import OrderService
from app.models import Order as Order_model
from app.schemas.order import OrderResponse
from app.schemas import OrderCreate, OrderUpdate


class OrderDepends:

    @classmethod
    async def get_all_oreders(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[list[OrderResponse]]:
        """

        :param param:
        :param param:
        :return:
        """
        order_schemes = await OrderService.get_all_orders(
            user_id=user_id,
            session=session,
        )

        if not order_schemes:

            raise HTTPErrors.not_found

        return order_schemes

    @classmethod
    async def get_all_oreders_by_date(
        cls,
        session: AsyncSession,
        dates: tuple[datetime, datetime],
    ) -> Optional[list[OrderResponse]]:
        """

        :param param:
        :param param:
        :return:
        """
        order_schemes = await OrderService.get_orders_by_date(
            dates=dates,
            session=session,
        )

        if not order_schemes:

            raise HTTPErrors.not_found

        return order_schemes

    @classmethod
    async def get_oreder(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[OrderResponse]:
        """

        :param param:
        :param param:
        :return:
        """
        order_scheme = await OrderService.get_order_response(
            order_id=order_id,
            user_id=user_id,
            session=session,
        )

        if not order_scheme:
            raise HTTPErrors.not_found

        return order_scheme

    @classmethod
    async def create_oreder(
        cls,
        user_id: int,
        session: AsyncSession,
        order_scheme: OrderCreate,
    ) -> OrderResponse:
        """

        :param param:
        :param param:
        :return:
        """
        order_scheme = await OrderService.create_order(
            user_id=user_id,
            order_scheme=order_scheme,
            session=session,
        )

        if not order_scheme:
            raise HTTPErrors.err_create_model

        return order_scheme

    @classmethod
    async def update_oreder(
        cls,
        order_id: int,
        session: AsyncSession,
        order_scheme: OrderUpdate,
        user_id: Optional[int] = None,
    ) -> OrderResponse:
        """

        :param param:
        :param param:
        :return:
        """
        order_scheme = await OrderService.update_order_partial(
            user_id=user_id,
            order_id=order_id,
            order_scheme=order_scheme,
            session=session,
        )

        if not order_scheme:
            raise HTTPErrors.err_update_model

        return order_scheme

    @classmethod
    async def delete_order(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Order_model:
        """

        :param param:
        :param param:
        :return:
        """
        order_scheme = await OrderService.delete_order(
            user_id=user_id,
            order_id=order_id,
            session=session,
        )
        if not order_scheme:
            raise HTTPErrors.err_delete_model

        return order_scheme

    classmethod

    async def delete_all_user_orders(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> list:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        result = await OrderService.delete_all_models(
            user_id=user_id,
            session=session,
        )

        if result != []:
            raise HTTPErrors.err_delete_model

        return result

    @classmethod
    async def clear_orders(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        result = await OrderService.clear_table(session=session)

        if result != []:
            raise HTTPErrors.clear_table

        return result
