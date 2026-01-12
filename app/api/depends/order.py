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
    ) -> list[OrderResponse]:
        """
        Возвращает все созданные заказы, поиск заказов осуществляется в зависимости от переданных параметров
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Список схем заказов пользователей
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
    ) -> list[OrderResponse]:
        """
        Возвращает все созданные заказы, созданные в указанном временном диапазоне
        :param dates: Определяет временной диапазон 
        :param session: Асинхронная сессия
        :return: Список схем заказов пользователей, созданных в указанном временном диапазоне
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
    ) -> OrderResponse:
        """
        Возвращает заказ пользователя, поиск заказа осуществляется в зависимости от переданных параметров
        :param user_id: Опциональный параметр, id пользователя
        :param order_id: id заказа
        :param session: Асинхронная сессия
        :return: Схема заказа пользователя
        """
        order_scheme = await OrderService.get_order_scheme(
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
        Создает заказ пользователя
        :param order_scheme: Схема заказа, полученная от пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Схема заказа пользователя
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
        Изменяет заказ пользователя
        :param order_scheme: Схема заказа, полученная от пользователя
        :param order_id: id заказа
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Схема заказа пользователя
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
    ) -> OrderResponse:
        """
        Удаляет заказ пользователя
        :param order_id: id заказа
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Схема заказа пользователя
        """
        order_scheme = await OrderService.delete_order(
            user_id=user_id,
            order_id=order_id,
            session=session,
        )
        if not order_scheme:
            raise HTTPErrors.err_delete_model

        return order_scheme

    @classmethod
    async def delete_all_user_orders(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """
        Удаляет все заказы пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Пустой список
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
        Полностью очищает таблицу заказов
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        cleared_table = await OrderService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.clear_table

        return cleared_table
