from datetime import datetime

from fastapi import APIRouter, status, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core import db_connector
from app.api.depends.cart import CartDepends
from app.api.depends.inspect import Inspector
from app.api.depends.security import admin_guard
from app.schemas import ProductAddOrUpdate
from app.schemas.cart import CartResponse


router = APIRouter(
    prefix="/admin/carts",
    tags=["Admin Carts"],
    dependencies=[Depends(admin_guard)],
)


@router.get(
    "/all",
    response_model=list[CartResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_carts(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list[CartResponse]:
    """
    Обрабатывает запрос с фронт энда на получение всех корзин пользователей
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Список корзин пользователей в виде Pydantic схем
    """
    return await CartDepends.get_all_cart(session=session)


@router.get(
    "/date",
    response_model=list[CartResponse],
    status_code=status.HTTP_200_OK,
)
async def get_carts_by_date(
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
    dates: Annotated[tuple[datetime, datetime], Depends(Inspector.date_checker)],
) -> list[CartResponse]:
    """
    Обрабатывает запрос с фронт энда на получение всех корзин пользователей, созданных в полученный интервал времени
    :param dates: кортеж, содержащий начало интервала времени и его окончание
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Список корзин пользователей в виде Pydantic схем
    """
    return await CartDepends.get_all_cart_by_date(
        dates=dates,
        session=session,
    )


@router.get(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cart_by_user_id(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на получение корзины пользователеля по его id
    :param user_id: id конкретного пользователя в БД
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    return await CartDepends.get_cart(
        user_id=user_id,
        session=session,
    )


@router.post(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_product(
    product_scheme: ProductAddOrUpdate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на добавление продукта в корзину пользователеля
    :param user_id: iid конкретного пользователя в БД
    :param product_scheme: Схема продукта для добавления
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_id,
        session=session,
        product_scheme=product_scheme,
    )


@router.patch(
    "/user/{user_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_count_product(
    product_scheme: ProductAddOrUpdate,
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на изменение количества продукта в корзине пользователеля
    :param user_id: id конкретного пользователя в БД
    :param product_scheme: Схема продукта для изменения
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_id,
        product_scheme=product_scheme,
        session=session,
    )


@router.delete(
    "/user/{user_id}/product_id{product_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    user_id: Annotated[int, Path(..., description="User ID")],
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на удаление продукта из корзины пользователеля
    :param user_id: id конкретного пользователя в БД
    :param product_id: id конкретного продукта в БД
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    return await CartDepends.del_product_from_cart(
        user_id=user_id,
        product_id=product_id,
        session=session,
    )


@router.delete(
    "/user/{user_id}/clear",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def clear_user_cart(
    user_id: Annotated[int, Path(..., description="User ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на удаление всех продуктов из корзины пользователеля
    :param user_id: id пользователя
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    return await CartDepends.clear_cart(
        user_id=user_id,
        session=session,
    )
