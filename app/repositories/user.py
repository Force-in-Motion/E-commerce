from typing import Optional

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepo
from app.models import User as User_model
from app.schemas.user import UserCreate
from app.tools.exeptions import DatabaseError
from app.utils.auth import AuthUtils


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
            raise DatabaseError(
                f"Error when receiving {cls.model.__name__} by login"
            ) from e
