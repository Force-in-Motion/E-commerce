from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.service.base import BaseService
from app.models import User as User_model, RefreshToken
from app.repositories import UserRepo


class UserService(BaseService[UserRepo]):

    repo = UserRepo

    @classmethod
    async def get_user_by_login(
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
        return await cls.repo.get_by_login(login=login, session=session)

    @classmethod
    async def get_refresh_token(
        cls,
        user_id: int,
        session: AsyncSession,
    ) -> Optional[RefreshToken]:
        """
        Возвращает модель пользователя по его имени из БД
        :param name: Имя пользователя
        :param session: Объект сессии, полученный в качестве аргумента
        :return: Модель пользователя | None
        """
        return await cls.repo.get_refresh(user_id=user_id, session=session)

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
        return await cls.repo.add_refresh(
            user_id=user_id,
            refresh=refresh,
            session=session,
        )
