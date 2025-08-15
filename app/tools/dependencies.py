from datetime import datetime
from typing import Annotated

from fastapi import Path, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_connector
from app.crud import ProductAdapter, UserAdapter, ProfileAdapter
from app.crud.post import PostAdapter
from app.models import (
    Product as Product_model,
    User as User_model,
    Profile as Profile_model,
    Post as Post_model,
)


async def product_by_id(
    product_id: Annotated[int, Path(..., description="Product id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Product_model:
    """
    Возвращает продукт по его id из БД, работает в качестве зависимости для другой логики
    :param product_id: id конкретного продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Product_model
    """
    product_model = await ProductAdapter.get_product_by_id(product_id, session)

    if product_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with this id not found",
        )

    return product_model


async def user_by_id(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> User_model:
    """
    Возвращает пользователя по его id из БД, работает в качестве зависимости для другой логики
    :param user_id: id конкретного пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: User_model
    """
    user_model = await UserAdapter.get_user_by_id(session, user_id)

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with this id not found"
        )

    return user_model


async def profile_by_id(
    profile_id: Annotated[int, Path(..., description="Profile id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Profile_model:
    """
    Возвращает профиль пользователя по его id
    :param profile_id: id конкретного профиля пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Profile_model
    """
    profile_model = await ProfileAdapter.get_profile_by_id(profile_id, session)

    if profile_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile with this id not found",
        )

    return profile_model


async def profile_by_user_id(
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Profile_model:
    """
    Возвращает профиль пользователя по его id
    :param user_model: UserModel - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Profile_model
    """
    profile_model = await ProfileAdapter.get_profile_by_user_id(session, user_model.id)

    if profile_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile with this user_id not found",
        )

    return profile_model


async def post_by_id(
    post_id: Annotated[int, Path(..., description="Post id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Post_model:
    """
    Возвращает конкретный пост по его id
    :param post_id:
    :param session:
    :return:
    """
    post_model = await PostAdapter.get_post_by_id(session, post_id)

    if post_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post with this id not found"
        )

    return post_model


async def posts_by_user_id(
    user_model: User_model = Depends(user_by_id),
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[Post_model]:
    """
    Возвращает все посты пользователя по его id
    :param user_model: UserModel - объект, содержащий данные пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: list[PostOutput]
    """
    posts_model = await PostAdapter.get_posts_by_user_id(session, user_model.id)

    if not posts_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posts with this user_id not found",
        )

    return posts_model


async def date_checker(
    date_start: Annotated[
        datetime,
        Query(..., description="Start date (формат: YYYY-MM-DD HH:MM:SS)"),
    ],
    date_end: Annotated[
        datetime,
        Query(..., description="End date (формат: YYYY-MM-DD HH:MM:SS)"),
    ],
):
    if date_start >= date_end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_start must be less than date_end",
        )

    return date_start, date_end


async def profile_checker(
    user_id: Annotated[int, Path(..., description="User id")],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> int:
    profile_model = await cls.get_profile_by_user_id(user_id, session)

    if profile_model:
        raise HTTPException(
            status_code=500,
            detail="Error user profile already exists",
        )

    return user_id
