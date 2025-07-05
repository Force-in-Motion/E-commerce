from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from web.schemas import ProductInput
from service.database.models import Product as Product_model



class ProductAdapter:

    @classmethod
    async def get_products(cls, session: AsyncSession) -> list[Product_model]:
        try:
            request = select(Product_model).order_by(Product_model.id)
            result = await session.execute(request)
            products = result.scalars().all()
            return list(products)

        except SQLAlchemyError:
            return []



    @classmethod
    async def get_product_by_id(cls, id: int, session: AsyncSession) -> Product_model | None:
        try:
            return await session.get(Product_model, id)

        except SQLAlchemyError:
            return None



    @classmethod
    async def add_product(cls, product: ProductInput, session: AsyncSession) -> dict:
        try:
            product_model = Product_model(**product.model_dump())
            session.add(product_model)
            await session.commit()
            return {'status': 'ok', 'detail': 'product has been added'}

        except SQLAlchemyError:
            await session.rollback()
            return {'status': 'False', 'detail': 'Error added product'}



    @classmethod
    async def update_product(cls,
                             product_input: ProductInput,
                             product_model: Product_model,
                             session: AsyncSession, partial: bool = False) -> dict:
        try:
            for key, value in product_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(product_model, key, value)

            await session.commit()
            return {'status': 'ok', 'detail': 'product has been updated'}

        except SQLAlchemyError:
            await session.rollback()
            return {'status': 'False', 'detail': 'Error updating product'}



    @classmethod
    async def del_product(cls, product_model: Product_model, session: AsyncSession) -> dict:
        try:
            await session.delete(product_model)
            await  session.commit()
            return {'status': 'ok', 'detail': 'Product has been removing'}

        except SQLAlchemyError:
            await session.rollback()
            return {'status': 'False', 'detail': 'Error removing product'}