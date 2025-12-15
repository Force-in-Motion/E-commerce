from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import OrderRepo
from app.repositories.cart import CartRepo
from app.service import BaseService
from app.models import Order as Order_model
from app.schemas import OrderRequest


class OrderService(BaseService[Order_model, OrderRepo]):
    model: Order_model
    repo: OrderRepo

    @classmethod
    async def get_orders_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[Order_model]:
        """

        :param user_id:
        :param session:
        :return:
        """
        return await cls.repo.get_all_by_user_id(
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def create_order_for_user(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param user_id:
        :param session:
        :return:
        """
        async with session.begin():

            cart_model = await CartRepo.get_all_by_user_id(
                user_id=user_id,
                session=session,
            )

            total_price = await CartRepo.get_total_price(cart_model)

            order_model = await cls.repo.create_order(
                user_id=user_id,
                total_price=total_price,
                session=session,
            )

            await cls.repo.add_product_to_order(
                cart_in=cart_model,
                order_in=order_model,
                session=session,
            )

            await CartRepo.clear_cart(
                cart_id=cart_model.id,
                session=session,
            )

            return order_model

    @classmethod
    async def update_order_partial(
        cls,
        order_id: int,
        order_scheme: OrderRequest,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param model_id:
        :param order_in:
        :param session:
        :return:
        """
        async with session.begin():

            order_model = await cls.get_model_by_id(
                model_id=order_id,
                session=session,
            )

            updated_order_model = cls.repo.update(
                scheme_in=order_scheme,
                update_model=order_model,
                session=session,
                partial=True,
            )

            return updated_order_model
