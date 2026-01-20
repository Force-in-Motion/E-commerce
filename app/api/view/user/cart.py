from fastapi import APIRouter, status, Path
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core import db_connector
from app.api.depends.user import UserAuth
from app.api.depends.cart import CartDepends
from app.api.depends.security import oauth2_scheme
from app.schemas import CartResponse
from app.schemas import ProductAddOrUpdate


router = APIRouter(
    prefix="/user/cart",
    tags=["My Cart"],
)


@router.get(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def get_my_cart(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на получение корзины пользователеля по его id
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.get_cart(
        user_id=user_model.id,
        session=session,
    )


@router.post(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def add_product(
    product_scheme: ProductAddOrUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на добавление продукта в корзину пользователеля
    :param product_scheme: Схема продукта для добавления
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_model.id,
        product_scheme=product_scheme,
        session=session,
    )


@router.patch(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def update_count_product(
    product_scheme: ProductAddOrUpdate,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на изменение количества продукта в корзине пользователеля
    :param product_scheme: Схема продукта для изменения
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.add_or_update_product_in_cart(
        user_id=user_model.id,
        product_scheme=product_scheme,
        session=session,
    )


@router.delete(
    "/{product_id}",
    response_model=CartResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: Annotated[int, Path(..., description="Product ID")],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> CartResponse:
    """
    Обрабатывает запрос с фронт энда на удаление продукта из корзины пользователеля
    :param product_id: id конкретного продукта в БД
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.del_product_from_cart(
        user_id=user_model.id,
        product_id=product_id,
        session=session,
    )


@router.delete(
    "/",
    response_model=list,
    status_code=status.HTTP_200_OK,
)
async def clear_my_cart(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(db_connector.get_session)],
) -> list:
    """
    Обрабатывает запрос с фронт энда на удаление всех продуктов из корзины пользователеля
    :param token:  объект токена, полученный из заголовка запроса при помощи зависимости oauth2_scheme
    :param session: Объект сессии, который получается путем выполнения зависимости (метода get_session объекта db_connector)
    :return: Корзина пользователя в виде Pydantic схемы
    """
    user_model = await UserAuth.get_current_user_by_access(
        token=token,
        session=session,
    )

    return await CartDepends.clear_cart(
        user_id=user_model.id,
        session=session,
    )
