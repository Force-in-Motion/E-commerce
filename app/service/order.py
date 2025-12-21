from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import OrderRepo
from app.repositories.cart import CartRepo
from app.service import BaseService
from app.models import Order as Order_model
from app.schemas import OrderRequest


class OrderService(BaseService[OrderRepo]):

    repo: OrderRepo

    @classmethod
    async def get_all_orders_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[Order_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        return await cls.repo.get_all_orders_by_user_id(
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def get_order_by_user_id(
        cls,
        user_id: int,
        order_id: int,
        session: AsyncSession,
    ) -> list[Order_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        return await cls.repo.get_by_user_id_and_order_id(
            user_id=user_id,
            order_id=order_id,
            session=session,
        )

    @classmethod
    async def create_order_for_user(
        cls,
        user_id: int,
        order_schema: OrderRequest,
        session: AsyncSession,
    ) -> Optional[Order_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        async with session.begin():

            cart_model = await CartRepo.get_by_user_id(
                user_id=user_id,
                session=session,
            )

            if not cart_model:
                return None

            total_quantity = sum(cp.quantity for cp in cart_model.products)

            total_price = sum(
                int(cp.current_price) * cp.quantity for cp in cart_model.products
            )

            order_model = await cls.repo.create_order(
                user_id=user_id,
                total_price=total_price,
                total_quantity=total_quantity,
                session=session,
                comment=order_schema.comment,
                promo_code=order_schema.promo_code,
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

            return order_model

    @classmethod
    async def update_order_partial(
        cls,
        user_id: int,
        order_id: int,
        order_schema: OrderRequest,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param model_id:
        :param order_in:
        :param session:
        :return:
        """
        async with session.begin():

            order_model = await cls.repo.get_by_user_and_model_id(
                model_id=order_id,
                user_id=user_id,
                session=session,
            )

            if not order_model:
                return None

            updated_order_model = cls.repo.update(
                new_data=order_schema.model_dump(exclude_unset=True),
                update_model=order_model,
                session=session,
            )

            return updated_order_model
