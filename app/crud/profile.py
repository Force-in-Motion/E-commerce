from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrud
from app.models import Profile as Profile_model
from app.schemas import ProfileRequest
from app.tools.custom_err import DatabaseError


class ProfileAdapter(BaseCrud[Profile_model, ProfileRequest]):

    model = Profile_model
    schema = ProfileRequest

    @classmethod
    async def get_by_user_id(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[Profile_model]:
        """
        Возвращает модель профиля, соответствующую id пользователя в БД
        :param user_id: id Модели конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель профиля | None
        """
        try:
            stmt = select(Profile_model).where(Profile_model.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().first()

        except SQLAlchemyError as e:
            raise DatabaseError(
                f"Database operation failed for {cls.model.__name__}"
            ) from e

    @classmethod
    async def create_for_user(
        cls,
        user_id: int,
        profile_in: ProfileRequest,
        session: AsyncSession,
    ) -> Profile_model:
        """
        Создает модель профиля конкретного пользователя в БД
        :param profile_in: Pydantic Схема - объект, содержащий данные модели профиля пользователя
        :param user_id: id Модели конкретного пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель профиля пользователя, созданную в БД
        """
        profile_in = profile_in.model_dump()
        profile_in["user_id"] = user_id

        return cls.create(profile_in=profile_in, session=session)
