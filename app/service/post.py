from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import PostRepo
from app.schemas.post import PostUpdate
from app.service import BaseService
from app.models import Post as PostModel


class PostService(BaseService[PostModel]):

    repo: PostRepo

    @classmethod
    async def get_user_post(
        cls,
        user_id: int,
        post_id: int,
        session: AsyncSession,
    ) -> PostModel:
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

        return next((post for post in list_post_models if post.id == post_id), None)

    @classmethod
    async def update_user_post(
        cls,
        user_id: int,
        post_id: int,
        post_in: PostUpdate,
        session: AsyncSession,
        partial: bool = False,
    ) -> PostModel:
        """

        :param user_id:
        :param post_in:
        :param session:
        :return:
        """
        post_model = await cls.get_user_post(
            user_id=user_id,
            post_id=post_id,
            session=session,
        )

        return cls.repo.update(
            scheme_in=post_in,
            update_model=post_model,
            session=session,
            partial=partial,
        )

    @classmethod
    async def delete_user_post(
        cls,
        user_id: int,
        post_id: int,
        session: AsyncSession,
    ) -> PostModel:
        """

        :param user_id:
        :param post_in:
        :param session:
        :return:
        """
        post_model = await cls.get_user_post(
            user_id=user_id,
            post_id=post_id,
            session=session,
        )

        return cls.repo.delete(
            del_model=post_model,
            session=session,
        )

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
