from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import PostCreate, PostUpdate, PostResponse
from app.models import Post as Post_model
from app.service import PostService
from app.tools import HTTPExeption


class PostCrud:

    @classmethod
    async def get_all_user_posts(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[Post_model]:
        """

        :param param:
        :param param:
        :return:
        """
        list_post_models = await PostService.get_all_models(
            user_id=user_id,
            session=session,
        )

        if not list_post_models:
            raise HTTPExeption.not_found

        return list_post_models

    @classmethod
    async def get_user_post(
        cls,
        post_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Post_model]:
        """

        :param param:
        :param param:
        :return:
        """
        post_model = await PostService.get_model(
            user_id=user_id,
            model_id=post_id,
            session=session,
        )

        if not post_model:
            raise HTTPExeption.not_found

        return post_model

    @classmethod
    async def create_user_post(
        cls,
        user_id: int,
        post_in: PostCreate,
        session: AsyncSession,
    ) -> Post_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        created_post_model = await PostService.register_model(
            scheme_in=post_in,
            session=session,
            user_id=user_id,
        )

        if not created_post_model:
            raise HTTPExeption.db_error

        return created_post_model

    @classmethod
    async def update_user_post(
        cls,
        user_id: int,
        post_id: int,
        post_in: PostUpdate,
        session: AsyncSession,
        partial: bool = False,
    ) -> Post_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        updated_post_model = await PostService.update_model(
            scheme_in=post_in,
            session=session,
            user_id=user_id,
            model_id=post_id,
            partial=partial,
        )

        if not updated_post_model:
            raise HTTPExeption.db_error

        return updated_post_model

    @classmethod
    async def delete_user_post(
        cls,
        user_id: int,
        post_id: int,
        session: AsyncSession,
    ) -> Post_model:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        deleted_post_model = await PostService.delete_model(
            user_id=user_id,
            model_id=post_id,
            session=session,
        )
        if not deleted_post_model:
            raise HTTPExeption.db_error

        return deleted_post_model

    @classmethod
    async def delete_all_user_post(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """
        Обрабатывает запрос с fontend на добавление пользователя в БД
        :param user_in: Pydantic Схема - объект, содержащий данные пользователя
        :param session: объект сессии, который получается путем выполнения зависимости (метода session_dependency объекта db_connector)
        :return: Добавленного в БД пользователя в виде Pydantic схемы
        """
        result = await PostService.delete_all_user_posts(
            user_id=user_id,
            session=session,
        )

        if result != []:
            raise HTTPExeption.db_error

        return result
