from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    Product as Product_model,
    Order as Order_model,
    OrderProducts as OrderProducts_model,
)


class OrderProductAdapter:

    @classmethod
    async def get_products_contained_in_order(
        cls,
        order: Order_model,
        session: AsyncSession,
    ) -> list[Product_model]:
        """
        Возвращает список продуктов содержащихся в конкретном заказе
        :param order: id заказа
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список продуктов содержащихся в конкретном заказе
        """
        try:
            order = await session.get(
                Order_model,
                order_id,
                options=[
                    selectinload(Order_model.products_contained).selectinload(
                        OrderProducts_model.product
                    )
                ],
            )

            if not order:
                return []

            products = []
            for order_product in order.products_contained:
                products.append(order_product.product)

            return products

        except SQLAlchemyError:
            return []
