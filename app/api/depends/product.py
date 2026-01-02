from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProductCreate, ProductUpdate
from app.tools import HTTPErrors
from app.service import ProductService
from app.models import Product as Product_model


class ProductDepends:

    @classmethod
    async def get_all_products(
        cls,
        session: AsyncSession,
    ) -> Optional[list[Product_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        product_models = await ProductService.get_all_models(session=session)

        if not product_models:
            raise HTTPErrors.not_found

        return product_models

    @classmethod
    async def get_product(
        cls,
        product_id: int,
        session: AsyncSession,
    ) -> Optional[Product_model]:
        """

        :param param:
        :param param:
        :return:
        """
        product_model = await ProductService.get_model(
            model_id=product_id,
            session=session,
        )

        if not product_model:
            raise HTTPErrors.not_found

        return product_model

    @classmethod
    async def get_products_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> Optional[list[Product_model]]:
        """

        :param param:
        :param param:
        :return:
        """
        product_models = await ProductService.get_all_models_by_date(
            dates=dates,
            session=session,
        )

        if not product_models:
            raise HTTPErrors.not_found

        return product_models

    @classmethod
    async def create_product(
        cls,
        product_scheme: ProductCreate,
        session: AsyncSession,
    ) -> Product_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        product_scheme.price = str(product_scheme.price)

        product_model = await ProductService.register_model(
            scheme_in=product_scheme,
            session=session,
        )

        if not product_model:
            raise HTTPErrors.db_error

        return product_model

    @classmethod
    async def update_product(
        cls,
        product_id: int,
        product_scheme: ProductUpdate,
        session: AsyncSession,
        partial: bool = False,
    ) -> Product_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        product_model = await ProductService.update_model(
            model_id=product_id,
            scheme_in=product_scheme,
            session=session,
            partial=partial,
        )

        if not product_model:
            raise HTTPErrors.db_error

        return product_model

    @classmethod
    async def delete_product(
        cls,
        product_id: int,
        session: AsyncSession,
    ) -> Product_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        product_model = await ProductService.delete_model(
            model_id=product_id,
            session=session,
        )

        if not product_model:
            raise HTTPErrors.db_error

        return product_model

    @classmethod
    async def clear_products(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        cleared_table = await ProductService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.db_error

        return cleared_table
