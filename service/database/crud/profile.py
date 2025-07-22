from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from service.database.models import Profile as Profile_model
from service.database.models import User as User_model
from web.schemas import ProfileInput


class ProfileAdapter:

    @classmethod
    async def get_profiles(cls, session: AsyncSession) -> list[Profile_model]:
        """
        Возвращает все профили, существующие в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список моделей профилей
        """
        try:
            request = Select(Profile_model).order_by(Profile_model.created_at)
            response = await session.execute(request)
            profiles = response.scalars().all()
            return list(profiles)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_profile_by_user_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> Mapped[Profile_model] | None:
        """
        Возвращает профиль, соответствующий id пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: модель конкретного профиля
        """
        try:
            response = await session.get(User_model, id)
            return response.profile

        except SQLAlchemyError:
            return None

    @classmethod
    async def add_profile(
        cls, session: AsyncSession, profile_input: ProfileInput
    ) -> dict:
        """
        Создает профиль конкретного пользователя в БД
        :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: dict
        """
        try:
            profile_model = Profile_model(**profile_input.model_dump())
            session.add(profile_model)
            await session.commit()
            return {"status": "ok", "detail": "Profile has been added"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error added Profile"}

    @classmethod
    async def update_profile(
        cls,
        session: AsyncSession,
        profile_input: ProfileInput,
        profile_model: Profile_model,
        partial: bool = False,
    ) -> dict:
        """
        Обновляет данные профиля пользователя в БД полностью или частично
        :param session: Объект сессии, полученный в качестве аргумента
        :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
        :param profile_model: Profile_model -конкретный объект в БД, найденный по id
        :param partial: partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        try:
            for key, value in profile_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(profile_model, key, value)

                await session.commit()
                return {"status": "ok", "detail": "Profile has been updated"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error updated Profile"}

    @classmethod
    async def del_profile(
        cls, session: AsyncSession, profile_model: Profile_model
    ) -> dict:
        """
        Удаляет профиль из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param profile_model: Profile_model -конкретный объект в БД, найденный по id
        :return: dict
        """
        try:
            await session.delete(profile_model)
            await session.commit()
            return {"status": "ok", "detail": "Profile has been deleted"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error deleted Profile"}
