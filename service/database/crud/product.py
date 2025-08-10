from datetime import datetime
from typing import Annotated

from fastapi import Path, HTTPException, status
from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


from web.schemas import ProductInput
from service.database.models import Product as Product_model


class ProductAdapter:

    @classmethod
    async def get_products(cls, session: AsyncSession) -> list[Product_model]:
        """
        Возвращает все продукты из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: list[Product_model]
        """
        try:
            request = select(Product_model).order_by(Product_model.id)
            response = await session.execute(request)
            products = response.scalars().all()
            return list(products)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_product_by_id(
        cls,
        id: Annotated[int, Path],
        session: AsyncSession,
    ) -> Product_model | None:
        """
        Возвращает продукт по его id из БД
        :param id: id конкретного продукта
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Product_model | None
        """
        try:
            return await session.get(Product_model, id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_added_product_by_date(
        cls,
        date_start: datetime,
        date_end: datetime,
        session: AsyncSession,
    ) -> list[Product_model]:
        """
        Возвращает продукты, добавленные в указанный интервал времени
        :param date_start: начало интервала времени
        :param date_end: окончание интервала времени
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех продуктов, добавленных за указанный интервал времени
        """
        if date_start >= date_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_start must be less than date_end",
            )

        try:
            request = (
                select(Product_model)
                .where(Product_model.created_at.between(date_start, date_end))
                .order_by(Product_model.created_at.desc())
            )
            result = await session.execute(request)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def add_product(
        cls,
        product_input: ProductInput,
        session: AsyncSession,
    ) -> dict:
        """
        Добавляет продукт в БД
        :param product_input: ProductInput - объект, содержащий данные продукта
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            product_model = Product_model(**product_input.model_dump())
            session.add(product_model)
            await session.commit()
            return {
                "status": "ok",
                "detail": "Product has been added",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error added Product",
            )

    @classmethod
    async def update_product(
        cls,
        product_input: ProductInput,
        product_model: Product_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> dict:
        """
        Обновляет данные продукта в БД полностью или частично
        :param product_input: ProductInput - объект, содержащий данные продукта
        :param product_model: Product_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта ProductInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        try:
            for key, value in product_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(product_model, key, value)

            await session.commit()
            return {
                "status": "ok",
                "detail": "Product has been updated",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error updating Product",
            )

    @classmethod
    async def del_product(
        cls,
        product_model: Product_model,
        session: AsyncSession,
    ) -> dict:
        """
        Удаляет продукт из БД
        :param product_model: Product_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            await session.delete(product_model)
            await session.commit()
            return {
                "status": "ok",
                "detail": "Product has been removing",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error removing Product",
            )

    @classmethod
    async def clear_product_db(cls, session: AsyncSession) -> dict[str, str]:
        """
        Очищает базу данных продуктов и сбрасывает последовательность id пользователей
        :param session: Объект сессии, полученный в качестве аргумента
        :return:
        """
        try:
            await session.execute(delete(Product_model))
            await session.execute(text('ALTER SEQUENCE "User_id_seq" RESTART WITH 1'))
            await session.commit()
            return {
                "status": "ok",
                "detail": "All users have been deleted",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted all Users",
            )
