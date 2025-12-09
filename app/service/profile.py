from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ProfileRepo
from app.service import BaseService
from app.models import Profile as Profile_model
from app.schemas import ProfileRequest


class ProfileFacade(BaseService[Profile_model, ProfileRepo]):

    model: Profile_model
    repo: ProfileRepo

    @classmethod
    async def get_model_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Profile_model:
        """

        :param user_id:
        :param session:
        :return:
        """
        return await cls.repo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def register_model_by_user_id(
        cls,
        user_id: int,
        scheme_in: ProfileRequest,
        session: AsyncSession,
    ) -> Profile_model:
        """

        :param user_id:
        :param scheme_in:
        :param session:
        :return:
        """
        return await cls.repo.create_for_user(
            user_id=user_id,
            profile_in=scheme_in,
            session=session,
        )

    @classmethod
    async def update_model_by_user_id(
        cls,
        user_id: int,
        scheme_in: ProfileRequest,
        session: AsyncSession,
        partial: bool = False,
    ) -> Profile_model:
        """

        :param user_id:
        :param scheme_in:
        :param session:
        :param partial:
        :return:
        """
        model = await cls.repo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        return await cls.repo.update(
            scheme_in=scheme_in,
            update_model=model,
            session=session,
            partial=partial,
        )

    @classmethod
    async def delete_model_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Profile_model:
        """

        :param user_id:
        :param session:
        :return:
        """
        model = await cls.repo.get_by_user_id(
            user_id=user_id,
            session=session,
        )

        return await cls.repo.delete(
            del_model=model,
            session=session,
        )
