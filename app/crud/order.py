from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.crud import BaseCrud
from app.models import Order as Order_model
from app.schemas.order import OrderRequest


class OrderAdapter(BaseCrud[Order_model, OrderRequest]):

    model: Order_model
    scheme: OrderRequest

    @classmethod
    async def create_for_user(
        cls,
        order_in: OrderRequest,
        session: AsyncSession,
    ) -> Order_model:
        """

        :param order_in:
        :param session:
        :return:
        """
