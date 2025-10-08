from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import OrderAdapter
from app.facade import BaseFacade
from app.models import Order as Order_model
from app.schemas import OrderRequest


class OrderFacade(BaseFacade[Order_model, OrderAdapter]):
    model: Order_model
    adapter: OrderAdapter

    @classmethod
    async def get_order_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[Order_model]:
        """

        :param user_id:
        :param session:
        :return:
        """

    @classmethod
    async def create_order_for_user(
        cls,
        order_in: OrderRequest,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param order_in:
        :param session:
        :return:
        """
        return await OrderAdapter.create_for_user(
            order_in=order_in,
            session=session,
        )
