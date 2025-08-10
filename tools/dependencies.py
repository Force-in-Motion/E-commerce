from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from service.database import db_connector
from service.database.crud.post import PostAdapter
from service.database.models import (
    Product as Product_model,
    User as User_model,
    Profile as Profile_model,
    Post as Post_model,
)
from service.database.crud import ProductAdapter, UserAdapter, ProfileAdapter
from web.schemas import PostOutput


async def product_by_id(
    id: Annotated[int, Path],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Product_model:
    """
    Возвращает продукт по его id из БД, работает в качестве зависимости для другой логики
    :param id: id конкретного продукта
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Product_model
    """
    product_model = await ProductAdapter.get_product_by_id(id, session)

    if product_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with this id not found",
        )

    return product_model


async def user_by_id(
    user_id: Annotated[int, Path],
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


async def profile_by_user_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Profile_model:
    """
    Возвращает профиль пользователя по его id
    :param user_id: id конкретного пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: Profile_model
    """
    profile_model = await ProfileAdapter.get_profile_by_user_id(session, user_id)

    if profile_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile with this user_id not found",
        )

    return profile_model


async def post_by_id(
    id: Annotated[int, Path],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> Post_model:
    """
    Возвращает конкретный пост по его id
    :param id:
    :param session:
    :return:
    """
    post_model = await PostAdapter.get_post_by_id(session, id)

    if post_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post with this id not found"
        )

    return post_model


async def posts_by_user_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_connector.session_dependency),
) -> list[Post_model]:
    """
    Возвращает все посты пользователя по его id
    :param user_id: id конкретного пользователя
    :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
    :return: list[PostOutput]
    """
    list_user_posts = await PostAdapter.get_posts_by_user_id(session, user_id)

    if list_user_posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posts with this user_id not found",
        )

    return list(list_user_posts)
