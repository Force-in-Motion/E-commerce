from datetime import datetime
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Depends, Path

from app.core import db_connector
from app.api.depends.inspect import Inspector
from app.api.depends.security import admin_guard
from app.api.depends.product import ProductDepends
from app.schemas import ProductCreate, ProductResponse, ProductUpdate


router = APIRouter(
    prefix="/admin/products",
    tags=["Admin Products"],
    dependencies=[Depends(admin_guard)],
)


@router.get(
    "/all",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[ProductResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Список всех продуктов в виде Pydantic схем
    """
    return await ProductDepends.get_all_products(session=session)


@router.get(
    "/date",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_products_by_date(
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[ProductResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: список всех продуктов, добавленных за указанный интервал времени в виде Pydantic схем
    """
    return await ProductDepends.get_products_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на получение продукта по его id
    :param product_id: id конкретного продукта в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Объект продукта в виде Pydantic схемы
    """
    return await ProductDepends.get_product(
        product_id=product_id,
        session=session,
    )


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_product(
    product_scheme: ProductCreate,
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на добавление продукта в БД
    :param product_scheme: ProductCreate - объект, содержащий данные продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Объект продукта в виде Pydantic схемы, добавленного в БД
    """
    return await ProductDepends.create_product(
        product_scheme=product_scheme,
        session=session,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_scheme: ProductUpdate,
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на полную замену данных продукта по его id
    :param product_id: id конкретного продукта в БД
    :param product_scheme: ProductUpdate - объект, содержащий новые данные конкретного продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Объект продукта в виде Pydantic схемы, обновленного в БД
    """
    return await ProductDepends.update_product(
        product_id=product_id,
        product_scheme=product_scheme,
        session=session,
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product_partial(
    product_scheme: ProductUpdate,
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param product_id: id конкретного продукта в БД
    :param product_scheme: ProductUpdate - объект, содержащий новые данные конкретного продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Объект продукта в виде Pydantic схемы, обновленного в БД
    """
    return await ProductDepends.update_product(
        product_id=product_id,
        product_scheme=product_scheme,
        session=session,
        partial=True,
    )


@router.delete(
    "/clear",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_products(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех продуктов
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Пустой список
    """
    return await ProductDepends.clear_products(session=session)


@router.delete(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного продукта
    :param product_id: id конкретного продукта в БД
    :param session: объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Объект продукта в виде Pydantic схемы, удаленного из БД
    """
    return await ProductDepends.delete_product(
        product_id=product_id,
        session=session,
    )
