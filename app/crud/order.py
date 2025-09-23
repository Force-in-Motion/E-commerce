from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.crud import BaseCrud
from app.models import Order as Order_model
from app.schemas.order import OrderInput


class OrderAdapter(BaseCrud[Order_model, OrderInput]):

    model: Order_model
    scheme: OrderInput

    @classmethod
    async def create_for_user(
        cls,
        order_in: OrderInput,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param order_in:
        :param session:
        :return:
        """
