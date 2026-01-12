from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import PostCreate, PostUpdate, PostResponse
from app.models import Post as Post_model
from app.service import PostService
from app.tools import HTTPErrors


class PostDepends:

    @classmethod
    async def get_all_posts(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
    ) -> list[Post_model]:
        """
        Возвращает все посты, поиск постов осуществляется в зависимости от переданных параметров
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Список моделей постов
        """
        post_models = await PostService.get_all_models(
            user_id=user_id,
            session=session,
        )

        if not post_models:
            raise HTTPErrors.not_found

        return post_models

    @classmethod
    async def get_all_posts_by_date(
        cls,
        dates: datetime,
        session: AsyncSession,
    ) -> list[Post_model]:
        """
        Возвращает все посты, созданные в указанном временном диапазоне
        :param dates: Определяет временной диапазон 
        :param session: Асинхронная сессия
        :return: Список моделей постов, созданных в указанном временном диапазоне
        """
        post_models = await PostService.get_all_models_by_date(
            dates=dates,
            session=session,
        )

        if not post_models:
            raise HTTPErrors.not_found

        return post_models

    @classmethod
    async def get_post(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        post_id: Optional[int] = None,
    ) -> Post_model:
        """
        Возвращает пост, поиск поста осуществляется в зависимости от переданных параметров
        :param user_id: Опциональный параметр, id пользователя
        :param post_id: Опциональный параметр, id поста
        :param session: Асинхронная сессия
        :return: Модель поста пользователя
        """
        post_model = await PostService.get_model(
            user_id=user_id,
            model_id=post_id,
            session=session,
        )

        if not post_model:
            raise HTTPErrors.not_found

        return post_model

    @classmethod
    async def create_post(
        cls,
        user_id: int,
        post_scheme: PostCreate,
        session: AsyncSession,
    ) -> Post_model:
        """
        Создает пост пользователя
        :param post_scheme: Схема поста, полученная от пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Модель поста пользователя 
        """
        post_model = await PostService.register_model(
            scheme_in=post_scheme,
            session=session,
            user_id=user_id,
        )

        if not post_model:
            raise HTTPErrors.err_create_model

        return post_model

    @classmethod
    async def update_post(
        cls,
        session: AsyncSession,
        post_scheme: PostUpdate,
        user_id: Optional[int] = None,
        post_id: Optional[int] = None,
        partial: bool = False,
    ) -> Post_model:
        """
        Изменяет пост пользователя
        :param post_scheme: Схема поста, полученная от пользователя
        :param post_id: Опциональный параметр, id поста
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :param partial: Флаг, определяющий полное или частичное изменение данных
        :return: Модель поста пользователя
        """
        post_model = await PostService.update_model(
            scheme_in=post_scheme,
            session=session,
            user_id=user_id,
            model_id=post_id,
            partial=partial,
        )

        if not post_model:
            raise HTTPErrors.err_update_model

        return post_model

    @classmethod
    async def delete_post(
        cls,
        session: AsyncSession,
        user_id: Optional[int] = None,
        post_id: Optional[int] = None,
    ) -> Post_model:
        """
        Удаляет пост пользователя
        :param post_id: Опциональный параметр, id поста
        :param user_id: Опциональный параметр, id пользователя
        :param session: Асинхронная сессия
        :return: Модель поста пользователя
        """
        post_model = await PostService.delete_model(
            user_id=user_id,
            model_id=post_id,
            session=session,
        )
        if not post_model:
            raise HTTPErrors.err_delete_model

        return post_model

    @classmethod
    async def delete_all_user_posts(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """
        Удаляет все посты пользователя
        :param user_id: id пользователя
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        result = await PostService.delete_all_models(
            user_id=user_id,
            session=session,
        )

        if result != []:
            raise HTTPErrors.err_delete_model

        return result

    @classmethod
    async def clear_posts(
        cls,
        session: AsyncSession,
    ) -> list:
        """
        Полностью очищает таблицу постов
        :param session: Асинхронная сессия
        :return: Пустой список
        """
        cleared_table = await PostService.clear_table(session=session)

        if cleared_table != []:
            raise HTTPErrors.clear_table

        return cleared_table
