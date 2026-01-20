from typing import Optional
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools import DatabaseError
from app.repositories import BaseRepo
from app.models import Cart as Cart_model, CartProduct as Cart_Product_model


class CartRepo(BaseRepo[Cart_model]):

    model = Cart_model

    @classmethod
    async def get_all_carts(
        cls,
        session: AsyncSession,
    ) -> Optional[list[Cart_model]]:
        """
        Возвращает все модели корзин, содержащиеся в БД
        :param session: Объект асинхронной сессии
        :return: Список всех ORM моделей корзин
        """
        try:
            stmt = select(cls.model).options(
                selectinload(cls.model.products).selectinload(
                    Cart_Product_model.product
                )
            )

            result = await session.execute(stmt)

            return result.scalars().all()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e

    @classmethod
    async def get_all_carts_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> Optional[list[Cart_model]]:
        """
        Возвращает список всех моделей корзины, добавленных за указанный интервал времени
        :param session: объект асинхронной сессии
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :return: список всех ORM моделей корзин, добавленных за указанный интервал времени
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.created_at.between(**dates))
                .options(
                    selectinload(cls.model.products).selectinload(
                        Cart_Product_model.product
                    )
                )
                .execution_options(populate_existing=True)
            )

            result = await session.execute(stmt)

            return result.scalars().all()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e

    @classmethod
    async def get_product(
        cls,
        cart_id: int,
        product_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_Product_model]:
        """
        Возвращает продукт из конкретной, найденной по ее id
        :param cart_id: id корзины
        :param product_id: id продукта
        :param session: объект асинхронной сессии
        :return: ORM модель продукта по ее id
        """
        try:
            stmt = select(Cart_Product_model).where(
                Cart_Product_model.cart_id == cart_id,
                Cart_Product_model.product_id == product_id,
            )

            result = await session.execute(stmt)

            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Error when receiving product by id from {cls.model.__name__}"
            ) from e

    @classmethod
    async def get_by_id(
        cls,
        cart_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
        """
        Возвращает корзину по ее id
        :param cart_id: id корзины
        :param session: объект асинхронной сессии
        :return: ORM модель корзины по ее id
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.id == cart_id)
                .options(
                    selectinload(cls.model.products).selectinload(
                        Cart_Product_model.product
                    )
                )
                .execution_options(populate_existing=True)
            )

            result = await session.execute(stmt)

            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e

    @classmethod
    async def get_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Cart_model]:
        """
        Возвращает корзину по id пользователя
        :param user_id: id пользователя
        :param session: объект асинхронной сессии
        :return: ORM модель корзины по user_id
        """
        try:
            stmt = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .options(
                    selectinload(cls.model.products).selectinload(
                        Cart_Product_model.product
                    )
                )
                .execution_options(populate_existing=True)
            )

            result = await session.execute(stmt)

            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__}") from e



    @classmethod
    async def clear_cart(
        cls,
        cart_id: int,
        session: AsyncSession,
    ) -> list:
        """
        Очищает конкретную корзину от продуктов, найденную по id
        :param cart_id: id корзины
        :param session: объект асинхронной сессии
        :return: Пустой список
        """
        try:
            stmt = delete(Cart_Product_model).where(Cart_Product_model.cart_id == cart_id)

            await session.execute(stmt)
            await session.commit()
            return []

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error clearing cart {cart_id}") from e
