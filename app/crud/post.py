from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, delete, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post as Post_model, User as User_model
from app.schemas import PostInput


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
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_post_by_id(
        cls,
        post_id: int,
        session: AsyncSession,
    ) -> Optional[Post_model]:
        """
        Возвращает конкретный пост, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_id: id конкретного поста
        :return: один пост
        """
        try:
            return await session.get(Post_model, post_id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_posts_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list[Post_model]:
        """
        Возвращает посты, соответствующие id пользователя в БД и имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :param user_id: id конкретного пользователя
        :return: список всех постов конкретного пользователя
        """
        try:
            stmt = select(Post_model).where(Post_model.user_id == user_id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

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
            stmt = (
                select(Post_model)
                .where(Post_model.created_at.between(*dates))
                .order_by(Post_model.created_at.desc())
            )

            result = await session.execute(stmt)
            return list(result.scalars().all())

        except SQLAlchemyError:
            return []

    @classmethod
    async def add_post(
        cls,
        post_input: PostInput,
        user_model: User_model,
        session: AsyncSession,
    ) -> Post_model:
        """
        Добавляет пост пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_input: PostInput - объект, содержащий данные поста пользователя
        :param user_model: UserModel - объект, содержащий данные пользователя
        :return: dict
        """
        try:
            post_model = Post_model(user_id=user_model.id, **post_input.model_dump())
            session.add(post_model)
            await session.commit()
            await session.refresh(
                post_model
            )  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
            # refresh гарантирует, что post_model содержит актуальное состояние из базы.
            return post_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error added Post",
            )

    @classmethod
    async def update_post(
        cls,
        post_input: PostInput,
        post_model: Post_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> Post_model:
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
            update_data = post_input.model_dump(exclude_unset=partial)

            for key, value in update_data.items():
                if value is not None:
                    setattr(post_model, key, value)

            await session.commit()
            await session.refresh(
                post_model  # После commit SQLAlchemy не всегда подгружает свежие данные из базы (например, если БД автоматически меняет created_at или триггеры что-то обновляют).
                # refresh гарантирует, что post_model содержит актуальное состояние из базы.
            )
            return post_model

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
    ) -> list:
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
            return []

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error cleared Post",
            )

    @classmethod
    async def del_post(
        cls,
        post_model: Post_model,
        session: AsyncSession,
    ) -> Post_model:
        """
        Удаляет пост из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_model: Post_model - конкретный объект в БД, найденный по id
        :return: dict
        """
        try:
            await session.delete(post_model)
            await session.commit()
            return post_model

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail="Error deleted Post",
            )
