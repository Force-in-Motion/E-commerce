from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.api.depends.security import admin_guard
from app.api.depends.product import ProductDepends
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.tools import Inspector

router = APIRouter(
    prefix="/admin/products",
    tags=["Products"],
    dependencies=[admin_guard],
)


@router.get(
    "/all",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_products(
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[ProductResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: list[ProductOutput]
    """
    return await ProductDepends.get_all_products(session=session)


@router.get(
    "/date",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_products_by_date(
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list[ProductResponse]:
    """
    Обрабатывает запрос с фронт энда на получение списка всех продуктов, добавленных за указанный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: список всех продуктов, добавленных за указанный интервал времени
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на получение продукта по его id
    :param product_id: объект ProductOutput, который получается путем выполнения зависимости (метода product_by_id)
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: ProductOutput
    """
    return ProductDepends.get_product_by_id(
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на добавление продукта в БД
    :param product_in: ProductInput - объект, содержащий данные продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на полную замену данных продукта по его id
    :param product_in: ProductInput - объект, содержащий новые данные конкретного продукта
    :param product_id: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на частичную замену данных продукта по его id
    :param product_in: ProductInput - объект, содержащий новые данные конкретного продукта
    :param product_id: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
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
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех пользователей
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductDepends.clear_products(session=session)


@router.delete(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.session_dependency)],
) -> ProductResponse:
    """
    Обрабатывает запрос с фронт энда на удаление конкретного продукта
    :param product_id: Product_model - конкретный объект в БД, найденный по id
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: dict
    """
    return await ProductDepends.delete_product(
        product_id=product_id,
        session=session,
    )
