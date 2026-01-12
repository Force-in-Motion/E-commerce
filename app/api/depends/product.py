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
    ) -> list[Product_model]:
        """
        Возвращает все продукты
        :param session: Асинхронная сессия
        :return: Список моделей продуктов
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
    ) -> Product_model:
        """
        Возвращает конкретный продукт
        :param product_id: id продукта
        :param session: Асинхронная сессия
        :return: Модель поста 
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
    ) -> list[Product_model]:
        """
        Возвращает все продукты, добавленные в указанном временном диапазоне
        :param dates: Определяет временной диапазон 
        :param session: Асинхронная сессия
        :return: Список моделей продуктов, добавленных в указанном временном диапазоне
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
        Добавляет продукт
        :param product_scheme: Схема продукта, полученная от пользователя
        :param session: Асинхронная сессия
        :return: Модель продукта 
        """
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
        Изменяет данные продукта
        :param product_scheme: Схема прподукта, полученная от пользователя
        :param product_id:  id поспродукта
        :param session: Асинхронная сессия
        :param partial: Флаг, определяющий полное или частичное изменение данных
        :return: Модель продукта 
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
        Удаляет продукт
        :param product_id: id поста
        :param session: Асинхронная сессия
        :return: Модель продукта 
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
        Полностью очищает таблицу продуктов
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        cleared_table = await ProductService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.db_error

        return cleared_table
