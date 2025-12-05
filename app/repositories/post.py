from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseCrud
from app.models import Post as Post_model
from app.schemas import PostRequest
from app.tools import DatabaseError


class PostAdapter(BaseCrud[Post_model]):

    model = Post_model

    @classmethod
    async def get_by_user_id(
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

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Database operation failed for {cls.model.__name__}"
            ) from e

    @classmethod
    async def create_for_user(
        cls,
        user_id: int,
        post_in: PostRequest,
        session: AsyncSession,
    ) -> Post_model:
        """
        Добавляет пост пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param post_in: PostInput - объект, содержащий данные поста пользователя
        :param user_id: UserModel - объект, содержащий данные пользователя
        :return: dict
        """
        post_in = post_in.model_dump()
        post_in["user_id"] = (user_id,)

        return await cls.create(
            scheme_in=post_in,
            session=session,
        )
