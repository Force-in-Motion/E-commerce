from typing import Optional
from datetime import datetime
from app.service import BaseService
from app.repositories import OrderRepo
from app.repositories.cart import CartRepo
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Order as Order_model, Cart as Cart_model
from app.schemas import OrderCreate, OrderUpdate, ProductInOrder, OrderResponse


class OrderService(BaseService[OrderRepo]):

    repo = OrderRepo

    @classmethod
    def _collect_order(
        cls,
        user_id: int,
        cart_model: Cart_model,
        order_scheme: OrderCreate,
    ) -> Order_model:
        """

        :param param:
        :param param:
        :return:
        """
        discount: int | None = None

        total_quantity = sum(cp.quantity for cp in cart_model.products)

        original_price = sum(
            int(cp.current_price) * cp.quantity for cp in cart_model.products
        )

        if order_scheme.promo_code is not None:
            total_price = original_price * (100 - order_scheme.promo_code) // 100
            discount = original_price - total_price

        else:
            total_price = original_price

        return Order_model(
            user_id=user_id,
            promo_code=order_scheme.promo_code,
            original_price=original_price,
            discount=discount,
            total_price=total_price,
            total_quantity=total_quantity,
            comment=order_scheme.comment,
        )

    @classmethod
    def _to_order_response(cls, order_model: Order_model) -> OrderResponse:
        """

        :param param:
        :param param:
        :return:
        """
        if order_model is None:
            return None

        products = [
            ProductInOrder(
                id=op.product.id,
                name=op.product.name,
                description=op.product.description,
                price=op.current_price,
                quantity=op.quantity,
            )
            for op in order_model.products
        ]

        return OrderResponse(
            id=order_model.id,
            user_id=order_model.user_id,
            products=products,
            original_price=order_model.original_price,
            discount=order_model.discount,
            total_price=order_model.total_price,
            total_quantity=order_model.total_quantity,
            promo_code=order_model.promo_code,
            comment=order_model.comment,
            created_at=order_model.created_at,
            updated_at=order_model.updated_at,
        )

    @classmethod
    async def get_all_orders(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[list[OrderResponse]]:
        """

        :param user_id:
        :param session:
        :return:
        """
        if user_id is not None:
            order_models = await cls.repo.get_all_orders_by_user_id(
                user_id=user_id,
                session=session,
            )

        else:
            order_models = await cls.repo.get_all_orders(session=session)

        if order_models is None:
            return None

        return [cls._to_order_response(order) for order in order_models]

    @classmethod
    async def get_orders_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> Optional[list[OrderResponse]]:
        """

        :param user_id:
        :param session:
        :return:
        """
        order_models = await cls.repo.get_orders_by_date(
            dates=dates,
            session=session,
        )

        if order_models is None:
            return None

        return [cls._to_order_response(order) for order in order_models]

    @classmethod
    async def get_order_model(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[Order_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        if user_id is not None:
            order_model = await cls.repo.get_by_user_id_and_order_id(
                user_id=user_id,
                order_id=order_id,
                session=session,
            )

        else:
            order_model = await cls.repo.get_by_order_id(
                order_id=order_id,
                session=session,
            )

        if order_model is None:
            return None

        return order_model

    @classmethod
    async def get_order_scheme(
        cls,
        order_id: int,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> Optional[OrderResponse]:
        """

        :param user_id:
        :param session:
        :return:
        """
        order_model = await cls.get_order_model(
            order_id=order_id,
            user_id=user_id,
            session=session,
        )

        if order_model is None:
            return None

        return cls._to_order_response(order_model=order_model)

    @classmethod
    async def create_order(
        cls,
        user_id: int,
        order_scheme: OrderCreate,
        session: AsyncSession,
    ) -> Optional[OrderResponse]:
        """
        Создает заказ на основе корзины пользователя.
        Рассчитывает total_price с учетом промокода (если он есть),
        сохраняет все данные заказа в БД и очищает корзину.
        :param user_id:
        :param session:
        :return:
        """
        cart_model = await CartRepo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        if not cart_model or cart_model.products == []:
            return None

        order_model = cls._collect_order(
            user_id=user_id,
            cart_model=cart_model,
            order_scheme=order_scheme,
        )

        await cls.repo.create(
            model=order_model,
            session=session,
        )

        await cls.repo.add_product_to_order(
            cart_model=cart_model,
            order_model=order_model,
            session=session,
        )

        await CartRepo.clear_cart(
            cart_model=cart_model,
            session=session,
        )

        return await cls.get_order_scheme(
            order_id=order_model.id,
            session=session,
            user_id=user_id,
        )

    @classmethod
    async def update_order_partial(
        cls,
        order_id: int,
        session: AsyncSession,
        order_scheme: OrderUpdate,
        user_id: Optional[int] = None,
    ) -> Order_model:
        """

        :param model_id:
        :param order_in:
        :param session:
        :return:
        """

        order_model = await cls.get_order_model(
            order_id=order_id,
            session=session,
            user_id=user_id,
        )

        if not order_model:
            return None

        order_model = await cls.repo.update(
            new_data=order_scheme.model_dump(exclude_unset=True),
            update_model=order_model,
            session=session,
        )

        return await cls.get_order_scheme(
            order_id=order_model.id,
            session=session,
            user_id=user_id,
        )

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
        order_model = await OrderService.delete_model(
            user_id=user_id,
            model_id=order_id,
            session=session,
        )
        if not order_model:
            return None

        return cls._to_order_response(order_model=order_model)
