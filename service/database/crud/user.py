from datetime import date, datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import User as User_model
from web.schemas import UserInput


class UserAdapter:

    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[User_model] | []:
        """
        Возвращает всех пользователей из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :return: list[User_model]
        """
        try:
            expression = select(User_model).order_by(User_model.id)
            response = await session.execute(expression)
            users = response.scalars().all()
            return list(users)

        except SQLAlchemyError:
            return []

    @classmethod
    async def get_user_by_id(
        cls,
        session: AsyncSession,
        id: int,
    ) -> User_model | None:
        """
        Возвращает пользователя по его id из БД
        :param session: Объект сессии, полученный в качестве аргумента
        :param id: id конкретного пользователя
        :return: User_model | None
        """
        try:
            return await session.get(User_model, id)

        except SQLAlchemyError:
            return None

    @classmethod
    async def get_added_users_by_date(
        cls,
        session: AsyncSession,
        input_date: date,
    ) -> list[User_model] | []:
        """
        Возвращает список всех пользователей, добавленных за указанный интервал времени
        :param session: Объект сессии, полученный в качестве аргумента
        :param input_date: полученный интервал времени
        :return: список всех пользователей, добавленных за указанный интервал времени
        """
        start_of_day = datetime.combine(input_date, datetime.min.time())
        end_of_day = datetime.combine(input_date, datetime.max.time())

        try:
            request = select(User_model).where(
                User_model.created_at.between(start_of_day, end_of_day)
            )
            response = await session.execute(request)
            users = response.scalars().all()
            return list[users]

        except SQLAlchemyError:
            await session.rollback()
            return []

    @classmethod
    async def add_user(
        cls,
        session: AsyncSession,
        user_input: UserInput,
    ) -> dict:
        """
        Добавляет пользователя в БД
        :param user_input: UserInput - объект, содержащий данные пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            user_model = User_model(**user_input.model_dump())
            session.add(user_model)
            await session.commit()
            return {"status": "ok", "detail": "User has been added"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error added User"}

    @classmethod
    async def update_user(
        cls,
        user_input: UserInput,
        user_model: User_model,
        session: AsyncSession,
        partial: bool = False,
    ) -> dict:
        """
        Обновляет данные пользователя в БД полностью или частично
        :param user_input: UserInput - объект, содержащий данные пользователя
        :param user_model: User_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :param partial: Флаг, передаваем значение True или False,
               значение передается в метод model_dump(exclude_unset=partial),
               параметр exclude_unset означает - "То, что не было передано, исключить",
               по умолчанию partial = False, то есть заменяются все данные объекта в БД, если partial = True,
               то заменятся только переданные данные объекта. То есть если переданы не все поля объекта UserInput,
               то заменить в базе только переданные, не переданные пропустить
        :return: dict
        """
        try:
            for key, value in user_input.model_dump(exclude_unset=partial).items():
                if value is not None:
                    setattr(user_model, key, value)

            await session.commit()
            return {"status": "ok", "detail": "User has been updated"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error updated User"}

    @classmethod
    async def del_user(
        cls,
        user_model: User_model,
        session: AsyncSession,
    ) -> dict:
        """
        Удаляет продукт из БД
        :param user_model: User_model - конкретный объект в БД, найденный по id
        :param session: Объект сессии, полученный в качестве аргумента
        :return: dict
        """
        try:
            await session.delete(user_model)
            await session.commit()
            return {"status": "ok", "detail": "User has been deleted"}

        except SQLAlchemyError:
            await session.rollback()
            return {"status": "False", "detail": "Error deleted User"}
