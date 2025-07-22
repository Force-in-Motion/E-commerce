from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import Profile as Profile_model
from web.schemas.profile import ProfileInput


class ProfileAdapter:

    @classmethod
    async def get_all_profiles(cls, session: AsyncSession) -> list[Profile_model]:
        """
        Возвращает все профили, существующие в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: список моделей профилей
        """

    @classmethod
    async def get_profile_by_user_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> Profile_model:
        """
        Возвращает профиль, соответствующий id пользователя в БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: модель конкретного профиля
        """

    @classmethod
    async def add_profile(
        cls, session: AsyncSession, id: int, profile_input: ProfileInput
    ) -> dict:
        """
        Создает профиль конкретного пользователя в БД
        :param profile_input: ProfileInput - объект, содержащий данные профиля пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: dict
        """

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
