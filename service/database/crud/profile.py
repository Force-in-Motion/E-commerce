from datetime import datetime, time

from fastapi import HTTPException
from sqlalchemy import select, Select, delete, text
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
    ) -> Profile_model | None:
        """
        Возвращает профиль, соответствующий id пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: модель конкретного профиля
        """
        response = await session.get(User_model, id)
        return response.profile if response else None

    @classmethod
    async def get_added_profiles_by_date(
        cls,
        session: AsyncSession,
        date: datetime,
    ) -> list[Profile_model]:
        """
        Возвращает список всех профилей пользователей, добавленных за указанный интервал времени
        :param session: Объект сессии, полученный в качестве аргумента
        :param date: полученный интервал времени
        :return: список всех профилей пользователей, добавленных за указанный интервал времени
        """
        start_of_day = datetime.combine(date, time(0, 0, 0))
        end_of_day = datetime.combine(date, time(23, 59, 59))

        try:
            request = select(Profile_model).where(
                User_model.created_at.between(start_of_day, end_of_day)
            )
            response = await session.execute(request)
            profiles = response.scalars().all()
            return list(profiles)

        except SQLAlchemyError:
            await session.rollback()
            return []

    @classmethod
    async def add_profile(
        cls,
        session: AsyncSession,
        profile_input: ProfileInput,
    ) -> dict:
        """
        Создает профиль конкретного пользователя в БД
        :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        # Проверка наличия уже существующего профиля у пользователя
        profile_model = await cls.get_profile_by_user_id(session, profile_input.user_id)

        # Если профиля у пользователя нет, то добавляем
        if profile_model is None:

            try:
                profile_model = Profile_model(**profile_input.model_dump())
                session.add(profile_model)
                await session.commit()
                return {"status": "ok", "detail": "Profile has been added"}

            except SQLAlchemyError:
                await session.rollback()
                raise HTTPException(status_code=500, detail="Error added Profile")

        else:
            raise HTTPException(
                status_code=500, detail="Error user profile already exists"
            )

    @classmethod
    async def update_profile(
        cls,
        session: AsyncSession,
        profile_input: ProfileInput,
        profile_model: Profile_model,
        partial: bool = False,
    ) -> dict[str, str] | None:
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
            raise HTTPException(status_code=500, detail="Error updated Profile")

    @classmethod
    async def del_profile(
        cls, session: AsyncSession, profile_model: Profile_model
    ) -> dict[str, str]:
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
            raise HTTPException(status_code=500, detail="Error deleted Profile")

    @classmethod
    async def clear_profile_db(cls, session: AsyncSession) -> dict[str, str]:
        """
        Очищает базу данных пользователя и сбрасывает последовательность id пользователей
        :param session: Объект сессии, полученный в качестве аргумента
        :return:
        """
        try:
            await session.execute(delete(Profile_model))
            await session.execute(
                text('ALTER SEQUENCE "Profile_id_seq" RESTART WITH 1')
            )
            await session.commit()
            return {"status": "ok", "detail": "All Profiles have been deleted"}

        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=500, detail="Error deleted all Profiles")
