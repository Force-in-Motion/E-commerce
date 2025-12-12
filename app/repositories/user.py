from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepo
from app.models import User as User_model, RefreshToken
from app.tools.exeptions import DatabaseError


class UserRepo(BaseRepo[User_model]):

    model = User_model

    @classmethod
    async def get_by_login(
        cls,
        login: EmailStr,
        session: AsyncSession,
    ) -> Optional[User_model]:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        try:
            stmt = select(cls.model).where(cls.model.login == login)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"Error when receiving {cls.model.__name__} by login") from e


    @classmethod
    async def get_refresh(
    cls,
    user_id: int,
    session: AsyncSession,
    ) -> Optional[RefreshToken]:
        """
        Возвращает refresh_token пользователя
        """
        try:
            stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().first()

        except SQLAlchemyError as e:
            raise DatabaseError("Error when receiving refresh") from e


    @classmethod
    async def add_refresh(
        cls,
        user_id: int,
        refresh: str,
        session: AsyncSession,
    ) -> RefreshToken:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        try:
            model = RefreshToken(user_id, refresh)

            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model

        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseError("Error when adding refresh") from e
