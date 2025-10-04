from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import PostAdapter
from app.facade import BaseFacade
from app.models import Post as PostModel
from app.schemas import PostRequest


class PostFacade(BaseFacade[PostModel, PostAdapter]):

    model: PostModel
    adapter: PostAdapter

    @classmethod
    async def get_models_by_user_id(
        cls, user_id: int, session: AsyncSession
    ) -> PostModel:
        """

        :param user_id:
        :param session:
        :return:
        """
        return await cls.adapter.get_by_user_id(
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def register_model_by_user_id(
        cls,
        user_id: int,
        post_in: PostRequest,
        session: AsyncSession,
    ) -> PostModel:
        """

        :param user_id:
        :param post_in:
        :param session:
        :return:
        """
        return await PostAdapter.create_for_user(
            user_id=user_id,
            post_in=post_in,
            session=session,
        )
