from datetime import datetime

from typing import Optional


from fastapi import HTTPException, status
from sqlalchemy import select, delete, text, Result
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from service.database.models import Post as Post_model, User as User_model
from web.schemas import PostInput


class PostAdapter:

    @classmethod
    async def get_all_posts(
        cls,
        session: AsyncSession,
    ) -> list[Post_model]:
        """
        Возвращает все посты, существующие в БД, и имена их создателей
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех постов пользователей
        """
        try:
            stmt = select(Post_model).order_by(Post_model.id)
            result = await session.execute(stmt)
            posts = result.scalars().all()
            return list(posts)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_post_by_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> Optional[Post_model]:
        """
        Возвращает конкретный пост, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного поста
        :return: один пост
        """
        try:
            result = await session.get(Post_model, id)
            return result

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_posts_by_user_id(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> Optional[list[Post_model]]:
        """
        Возвращает посты, соответствующие id пользователя в БД и имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :param user_id: id конкретного пользователя
        :return: список всех постов конкретного пользователя
        """
        try:
            stmt = select(Post_model).where(Post_model.user_id == user_id)

            result = await session.execute(stmt)
            posts = result.scalars().all()

            return list(posts)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_added_posts_by_date(
        cls,
        dates: tuple[datetime, datetime],
        session: AsyncSession,
    ) -> list[Post_model]:
        """
        Возвращает посты, соответствующие полученному интервалу времени
        :param dates:  кортеж, содержащий начало интервала времени и его окончание
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список всех постов пользователей, добавленных за указанный интервал времени
        """
        try:
            date_start, date_end = dates
            request = (
                select(Post_model)
                .where(Post_model.created_at.between(date_start, date_end))
                .order_by(Post_model.created_at.desc())
            )

            result = await session.execute(request)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def add_post(
        cls,
        session: AsyncSession,
        post_input: PostInput,
    ) -> dict[str, str]:
        """
        Добавляет пост пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_input: PostInput - объект, содержащий данные поста пользователя
        :return: dict
        """
        try:
            post_model = Post_model(**post_input.model_dump())
            session.add(post_model)
            await session.commit()
            return {
                "status": "ok",
                "detail": "Post has been added",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error added User",
            )

    @classmethod
    async def update_post(
        cls,
        session: AsyncSession,
        post_input: PostInput,
        post_model: Post_model,
        partial: bool = False,
    ) -> dict[str, str]:
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
        try:
            for key, value in post_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(post_model, key, value)

            await session.commit()
            return {
                "status": "ok",
                "detail": "Post has been updated",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error updated Post",
            )

    @classmethod
    async def clear_posts(
        cls,
        session: AsyncSession,
    ) -> dict[str, str]:
        """
        Удаляет все посты пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            await session.execute(delete(Post_model))
            await session.execute(
                text('ALTER SEQUENCE "Profile_id_seq" RESTART WITH 1')
            )
            await session.commit()
            return {
                "status": "ok",
                "detail": "Post has been cleared",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error cleared Post",
            )

    @classmethod
    async def del_post(
        cls,
        session: AsyncSession,
        post_model: Post_model,
    ) -> dict[str, str]:
        """
        Удаляет пост из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_model: Post_model - конкретный объект в БД, найденный по id
        :return: dict
        """
        try:
            await session.execute(delete(post_model))
            await session.commit()
            return {
                "status": "ok",
                "detail": "Post has been deleted",
            }

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted Post",
            )
