from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools import HTTPErrors
from app.service import CartService, UserService
from app.celery.tasks import send_msg_to_email_task
from app.schemas import ProductAddOrUpdate, CartResponse

class CartDepends:

    @classmethod
    async def get_all_cart(
        cls,
        session: AsyncSession,
        dates: Optional[tuple[datetime, datetime]] = None,
    ) -> list[CartResponse]:
        """
        Возвращает все созданные корзины в зависимости от переданных параметров
        :param dates: Опциональный параметр, определяет временной диапазон для поиска
        :param session: Асинхронная сессия
        :return: Список схем корзин пользователей, созданных в указанном временном диапазоне
        """
        cart_schemes = await CartService.get_all_carts(dates=dates, session=session)

        if cart_schemes is None:
            raise HTTPErrors.not_found

        return cart_schemes

    @classmethod
    async def get_cart(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """
        Возвращает корзину пользователя, поиск корзины осуществляется в зависимости от переданных параметров
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id корзины
        :param session: Асинхронная сессия
        :return: Схему корзины пользователя
        """
        cart_scheme = await CartService.get_or_create_cart(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
        )

        if cart_scheme is None:
            raise HTTPErrors.not_found

        return cart_scheme

    @classmethod
    async def add_or_update_product_in_cart(
        cls,
        session: AsyncSession,
        product_scheme: ProductAddOrUpdate,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """
        Добавляет продукт в корзину или изменяет его количество, если он уже есть в корзине, а так же уведомляет пользователя об этом
        :param product_scheme: Схема продукта, полученная от пользователя
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id корзины
        :param session: Асинхронная сессия
        :return: Схему корзины пользователя
        """
        cart_scheme = await CartService.add_or_update_product_in_cart(
            user_id=user_id,
            cart_id=cart_id,
            session=session,
            product_scheme=product_scheme,
        )

        if cart_scheme is None:
            raise HTTPErrors.err_update_model

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.add_or_update_product_in_cart.__name__,
            user_email=user_model.login,
        )

        return cart_scheme

    @classmethod
    async def del_product_from_cart(
        cls,
        product_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """
        Удаляет продукт из корзины, а так же уведомляет пользователя об этом
        :param product_id: id продукта
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id корзины
        :param session: Асинхронная сессия
        :return: Схему корзины пользователя
        """
        cart_scheme = await CartService.del_product_from_cart(
            user_id=user_id,
            cart_id=cart_id,
            product_id=product_id,
            session=session,
        )

        if cart_scheme is None:
            raise HTTPErrors.err_delete_model

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.del_product_from_cart.__name__,
            user_email=user_model.login,
        )

        return cart_scheme

    @classmethod
    async def clear_cart(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        cart_id: Optional[int] = None,
    ) -> CartResponse:
        """
        Очищает полностью корзину пользователя, а так же уведомляет пользователя об этом
        :param user_id: Опциональный параметр, id пользователя
        :param cart_id: Опциональный параметр, id корзины
        :param session: Асинхронная сессия
        :return: Схему корзины пользователя
        """
        cart_scheme = await CartService.clear_user_cart(
            cart_id=cart_id,
            user_id=user_id,
            session=session,
        )

        if cart_scheme is None:
            raise HTTPErrors.clear_table

        user_model = await UserService.get_model(
            session=session,
            model_id=user_id,
        )
            
        send_msg_to_email_task.delay(
            key=cls.clear_cart.__name__,
            user_email=user_model.login,
        )

        return cart_scheme
