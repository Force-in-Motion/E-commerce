from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from web.schemas.product import Product as Product_scheme
from service.database.models.product import Product as Product_model



class ProductAdapter:

    @classmethod
    async def get_products(cls, session: AsyncSession) -> list[Product_model]:
        try:
            request = select(Product_model).order_by(Product_model.id)
            result = await session.execute(request)
            products = result.scalars().all()
            return list(products)

        except SQLAlchemyError as e:
            print('Ошибка при получении списка всех продуктов', e)
            return []


    @classmethod
    async def get_product_by_id(cls, id: int, session: AsyncSession):
        try:
            return await session.get(Product_model, id)

        except SQLAlchemyError as e:
            print('Ошибка при получении продукта по id')
            return None


    @classmethod
    async def add_product(cls, product: Product_scheme, session: AsyncSession) -> bool:
        try:
            product_model = Product_model(**product.model_dump())
            session.add(product_model)
            await session.commit()
            return True

        except SQLAlchemyError as e:
            print('Ошибка при добавлении продукта')
            await session.rollback()
            return False


    @classmethod
    async def update_product(cls, id: int, data) -> bool:
        pass


    @classmethod
    async def del_product(cls, id: int, session: AsyncSession) -> bool:
        try:
            product_model = await session.get(Product_model, id)
            if product_model is None:
                return False

            await session.delete(product_model)
            await  session.commit()
            return True

        except SQLAlchemyError as e:
            print('Ошибка при удалении продукта')
            await session.rollback()
            return False