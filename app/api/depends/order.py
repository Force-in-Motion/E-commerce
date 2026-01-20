from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools import HTTPErrors
from app.service import OrderService, UserService
from app.celery.tasks import send_msg_to_email_task
from app.schemas import OrderCreate, OrderUpdate, OrderResponse


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
        Создает заказ пользователя, а так же уведомляет пользователя об этом
        :param order_scheme: Схема заказа, полученная от пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Схема заказа пользователя
        """
        order_response = await OrderService.create_order(
            user_id=user_id,
            order_scheme=order_scheme,
            session=session,
        )

        if not order_response:
            raise HTTPErrors.err_create_model

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.create_oreder.__name__,
            user_email=user_model.login,
        )

        return order_response

    @classmethod
    async def update_oreder(
        cls,
        order_id: int,
        session: AsyncSession,
        order_scheme: OrderUpdate,
        user_id: Optional[int] = None,
    ) -> OrderResponse:
        """
        Изменяет заказ пользователя, а так же уведомляет пользователя об этом
        :param order_scheme: Схема заказа, полученная от пользователя
        :param order_id: id заказа
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Схема заказа пользователя
        """
        order_response = await OrderService.update_order_partial(
            user_id=user_id,
            order_id=order_id,
            order_scheme=order_scheme,
            session=session,
        )

        if not order_response:
            raise HTTPErrors.err_update_model

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.update_oreder.__name__,
            user_email=user_model.login,
        )

        return order_response

    @classmethod
    async def delete_order(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> OrderResponse:
        """
        Удаляет заказ пользователя, а так же уведомляет пользователя об этом
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

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.delete_order.__name__,
            user_email=user_model.login,
        )

        return order_scheme

    @classmethod
    async def delete_all_user_orders(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """
        Удаляет все заказы пользователя, а так же уведомляет пользователя об этом
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

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.delete_all_user_orders.__name__,
            user_email=user_model.login,
        )

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
