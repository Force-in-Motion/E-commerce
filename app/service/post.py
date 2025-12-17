from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import PostRepo
from app.schemas.post import PostUpdate
from app.service import BaseService
from app.models import Post as PostModel


class PostService(BaseService[PostModel]):

    repo: PostRepo

    @classmethod
    async def delete_all_user_posts(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> list:
        """

        :param user_id:
        :param post_in:
        :param session:
        :return:
        """
        list_post_models = await cls.repo.get_all_by_user_id(
            user_id=user_id,
            session=session,
        )

        return await cls.repo.delete_all_posts(
            list_post_models=list_post_models,
            session=session,
        )
