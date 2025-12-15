from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepo
from app.models import Post as Post_model
from app.tools.exeptions import DatabaseError


class PostRepo(BaseRepo[Post_model]):

    model = Post_model

    @classmethod
    async def delete_all_posts(
        cls,
        list_post_models: list[Post_model],
        session: AsyncSession,
    ) -> list:
        """

        :param user_id:
        :param post_in:
        :param session:
        :return:
        """
        try:
            for post in list_post_models:
                await session.delete(post)
            await session.commit()
            return []


        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError(f"Error when deleting list {cls.model.__name__}") from e