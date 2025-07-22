from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import Post as Post_model
from web.schemas import PostInput


class PostAdapter:

    @classmethod
    async def get_all_posts(cls, session: AsyncSession) -> list[Post_model]:
        """
        Возвращает все посты, существующие в БД, и имена их создателей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех постов пользователей
        """

    @classmethod
    async def get_post_by_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> Post_model:
        """
        Возвращает конкретный пост, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного поста
        :return: один пост
        """

    @classmethod
    async def get_posts_by_user_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> list[Post_model]:
        """
        Возвращает посты, соответствующие id пользователя в БД и имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: список всех постов конкретного пользователя
        """

    @classmethod
    async def get_posts_by_date(
        cls,
        session: AsyncSession,
        input_date: date,
    ) -> list[Post_model]:
        """
        Возвращает посты, соответствующие полученному интервалу времени и их создателей
        :param input_date: полученный интервал времени
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех постов пользователей за указанный интервал времени
        """

    @classmethod
    async def add_post(
        cls,
        session: AsyncSession,
        post_input: PostInput,
    ) -> dict:
        """
        Добавляет пост пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_input: PostInput - объект, содержащий данные поста пользователя
        :return: dict
        """

    @classmethod
    async def update_post(
        cls,
        session: AsyncSession,
        post_input: PostInput,
        post_model: Post_model,
        partial: bool = False,
    ):
        """
        Обновляет пост в БД полностью или частично
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_input: PostInput - объект, содержащий данные поста пользователя
        :param post_model: Post_model - конкретный объект в БД, найденный по id
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """

    @classmethod
    async def del_post(
        cls,
        session: AsyncSession,
        post_model: Post_model,
    ) -> dict:
        """
        Удаляет пост из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_model: Post_model - конкретный объект в БД, найденный по id
        :return: dict
        """
